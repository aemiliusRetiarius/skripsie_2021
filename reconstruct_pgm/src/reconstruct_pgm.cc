/*
 * Author     :  (DSP Group, E&E Eng, US)
 * Created on :
 * Copyright  : University of Stellenbosch, all rights retained
 */

// standard headers
#include <iostream>  // cout, endl, flush, cin, cerr
#include <string>  // string, stod
#include <cmath>   // sqrt


#include "discretetable.hpp"
#include "prlite_zfstream.hpp"

using namespace std;
using namespace emdw;

/**                            **/

#include "emdw.hpp"
#include "sqrtmvg.hpp"

void readDataFile(string fileString, vector<unsigned> &inputSource, vector<unsigned> &inputTarget, vector<double> &inputDist, vector<bool> inputChangedFlag);
void initialiseVars(RVIds &theVarsFull, RVIds &theVarsDists, unsigned numPoints, unsigned numRecords);
void initialiseFactors(vector< rcptr<Factor> > &factors, vector<unsigned> &inputSource, vector<unsigned> &inputTarget, unsigned numRecords);
void reconstructSigmaFactors(vector< rcptr<Factor> > &factors, vector< rcptr<Factor> > &old_factors, unsigned numPoints, vector<double> &inputDist);
void extractNewFactors(vector< rcptr<Factor> > &factors, RVIds &theVarsDists, vector<double> inputDist, vector<unsigned> &inputSource, vector<unsigned> &inputTarget);

unsigned getNumPoints(vector<unsigned> &inputSource, vector<unsigned> &inputTarget);
RVIds getVariableSubset(unsigned pointNum, const vector<unsigned> &inputSource, const vector<unsigned> &inputTarget);
double getDist(double x1, double y1, double z1, double x2, double y2, double z2);
double getTotalMahanalobisDist(vector< rcptr<Factor> > &factors, vector< rcptr<Factor> > &old_factors);

int main(int, char *argv[]) {

  string fileString = "../../cube_gen/Data/dists.csv";
  double tolerance = 0.1;

  // file input storage vectors
  vector<unsigned> inputSource, inputTarget; 
  vector<double> inputDist;
  vector<bool> inputChangedFlag;
  
  // fill input storage vectors from file
  readDataFile(fileString, inputSource, inputTarget, inputDist, inputChangedFlag);

  // assume that there are no gaps in point numbering, possible improvement to handle it
  // find max value in source and target to find number of points
  unsigned numPoints = getNumPoints(inputSource, inputTarget);
  
  // find number of records -> number of factors
  unsigned numRecords = inputSource.size();

  cout << "Num points: " << numPoints << endl;
  cout << "Num records: " << numRecords << endl;

  // define random varibles
  // for every point have x, y, z
  // e.g. to find point i_y: (i-1)*3 +1
  // after 3d data, add rvs for distances
  RVIds theVarsFull = {};
  RVIds theVarsDists = {};
  
  // fill rv vectors
  initialiseVars(theVarsFull, theVarsDists, numPoints, numRecords);

  vector< rcptr<Factor> > factors;
  vector< rcptr<Factor> > old_factors;

  // initialise factors with input data
  initialiseFactors(factors, inputSource, inputTarget, numRecords);

  do {
  // reconstruct new factors with additional dimension for distance
  reconstructSigmaFactors(factors, old_factors, numPoints, inputDist);
  
  // observe and reduce full joint, extract new factors using mean
  extractNewFactors(factors, theVarsDists, inputDist, inputSource, inputTarget);

  } while(getTotalMahanalobisDist(factors, old_factors) > tolerance);
  
  cout << "total diff dist: " << getTotalMahanalobisDist(factors, old_factors) << endl;

  //cout << inputDist << endl;
  //cout << theVarsDists << endl;
  //cout << jointFactorSGPtr->getMean() << endl;
  //cout << *factors[2] << endl;

} // main

// function will modify storage vectors
void readDataFile(string fileString, vector<unsigned> &inputSource, vector<unsigned> &inputTarget, vector<double> &inputDist, vector<bool> inputChangedFlag)
{
  // file pointer
  fstream fin;

  // file input handlers
  vector<string> row;
  string line, word;

  // opens an existing csv file or creates a new file.
  fin.open(fileString, ios::in);
  
  // remove first line with col names
  getline(fin, line);
  

  while (getline(fin, line)) 
  {
  
    row.clear();
  
    // read an entire row and
    // store it in a string variable 'line'
    //getline(fin, line);
  
    // used for breaking words
    stringstream s(line);
  
    // read every column data of a row and
    // store it in a string variable, 'word'
    while (getline(s, word, ',')) 
    {
  
      // add all the column data
      // of a row to a vector
      row.push_back(word);
      
    }

    // parse and add input file variables
    inputSource.push_back((unsigned)stod(row[1]));
    inputTarget.push_back((unsigned)stod(row[2]));
    inputDist.push_back(stod(row[3]));

    bool parsedBool = (row[4].compare("True") == 1) ? true : false;
    inputChangedFlag.push_back(parsedBool);

  }
}

// function will modify theVarsFull, theVarsDists
void initialiseVars(RVIds &theVarsFull, RVIds &theVarsDists, unsigned numPoints, unsigned numRecords)
{
  for(unsigned i = 0; i < 3*(numPoints); i++)
  {
    theVarsFull.push_back(i); // 3d rvs
  }
  for(unsigned i = 0; i < numRecords; i++)
  {
    theVarsFull.push_back(3*numPoints + i); // dist rvs
    theVarsDists.push_back(3*numPoints + i);
  }
}

// function will modify factors
void initialiseFactors(vector< rcptr<Factor> > &factors, vector<unsigned> &inputSource, vector<unsigned> &inputTarget, unsigned numRecords)
{
  // define initial gaussian parameters //mult gaussians*, larger cov, init grid
  prlite::ColVector<double> theMn(6);
  prlite::RowMatrix<double> theCv(6,6);
  theCv.assignToAll(0.0);

  for(unsigned i = 0; i < 6; i++)
  {
    theMn[i] = 0.0;
    theCv(i,i) = 20.0;
  }

  // create factors
  RVIds theVarsSubset = {};
  //unsigned RVIndexBase = 0;
  for(unsigned i = 0; i < numRecords; i++)
  {
    // get variable subset of record
    theVarsSubset = getVariableSubset(i, inputSource, inputTarget);

    // construct gaussians and append to factor list
    rcptr<SqrtMVG> pdfSGPtr ( new SqrtMVG(theVarsSubset, theMn, theCv));
    rcptr<Factor> pdfPtr = pdfSGPtr;
    factors.push_back(pdfPtr);
  }
  return;

}

// function will modify factors, old_factors
void reconstructSigmaFactors(vector< rcptr<Factor> > &factors, vector< rcptr<Factor> > &old_factors, unsigned numPoints, vector<double> &inputDist)
{
  cout << "starting reconstruction..." << endl;
  // step through factors and add sigmapoints
  unsigned index = 0; 
  old_factors.clear();
  for(rcptr<Factor> factor : factors)
  {
    // 6 x 13 matrix of sigma points
    prlite::ColMatrix<double> sigmaPoints = dynamic_pointer_cast<SqrtMVG>(factor)->getSigmaPoints();

    // get variables factor is defined for
    RVIds theVarsSubset = dynamic_pointer_cast<SqrtMVG>(factor)->getVars();

    // define dist row
    prlite::ColMatrix<double> sigmaPointsDists(1, 13);
    prlite::ColMatrix<double> sigmaPointsNoise(1, 13);
    sigmaPointsNoise.assignToAll(0.0); // neccesary?

    // calc dist row
    for(unsigned i = 0; i < 13; i++)
    {
      sigmaPointsDists(0, i) = getDist(sigmaPoints(0,i), sigmaPoints(1,i), sigmaPoints(2,i), sigmaPoints(3,i), sigmaPoints(4,i), sigmaPoints(5,i));
    }

    
    // define dist rv
    RVIds theVarsDist = {3*numPoints + index};
    RVVals theDist = {inputDist[index]};
    
    // reconstruct new gaussian
    rcptr<SqrtMVG> pdfSigmaSGPtr(SqrtMVG::constructFromSigmaPoints(theVarsSubset, sigmaPoints, theVarsDist, sigmaPointsDists, sigmaPointsNoise));
    rcptr<Factor> pdfSigmaPtr = pdfSigmaSGPtr;
    pdfSigmaPtr = pdfSigmaPtr->observeAndReduce(theVarsDist, theDist)->normalize();

    // redefine factor and push into old factors
    old_factors.push_back(factor);
    factor = pdfSigmaPtr;

    // increment record index
    index++;
  }
}

// function will modify factors
void extractNewFactors(vector< rcptr<Factor> > &factors, RVIds &theVarsDists, vector<double> inputDist, vector<unsigned> &inputSource, vector<unsigned> &inputTarget)
{
  // observe and reduce joint of reconsructed gaussians
  unsigned numRecords = factors.size();
  rcptr<Factor> jointFactorPtr = absorb(factors);
  //obsv known points

  //jointFactorPtr = jointFactorPtr->observeAndReduce(theVarsDists, inputDist); //obsv individual
  rcptr<SqrtMVG> jointFactorSGPtr = dynamic_pointer_cast<SqrtMVG>(jointFactorPtr);

  factors.clear(); // watch for aliasing issues with jointFactorPtr
  
  // extract mean from joint
  prlite::ColVector<double> jointMean = jointFactorSGPtr->getMean(); //marginalize for points to 6d, test cov with 3

  // define new gaussian parameters
  prlite::ColVector<double> theMn(6);
  prlite::RowMatrix<double> theCv(6,6);
  theCv.assignToAll(0.0);

  for(unsigned i = 0; i < 6; i++)
  {
    theCv(i,i) = 1.0;
  }

  // create factors
  RVIds theVarsSubset = {};
  for(unsigned i = 0; i < numRecords; i++)
  {
    // get variable subset of record
    theVarsSubset = getVariableSubset(i, inputSource, inputTarget);

    // get mean from joint mean and variable subset
    for(unsigned j = 0; j < 6; j++)
    {
      theMn[j] = jointMean[theVarsSubset[j]];
    }

    // construct gaussians and append to factor list
    rcptr<SqrtMVG> pdfSGPtr ( new SqrtMVG(theVarsSubset, theMn, theCv));
    rcptr<Factor> pdfPtr = pdfSGPtr;
    factors.push_back(pdfPtr);
  }

  

}

unsigned getNumPoints(vector<unsigned> &inputSource, vector<unsigned> &inputTarget)
{
  vector<unsigned> sortedSource, sortedTarget;

  sortedSource = inputSource;
  sortedTarget = inputTarget;
  sort(sortedSource.begin(), sortedSource.end());
  sort(sortedTarget.begin(), sortedTarget.end());

  return max(sortedSource.back(), sortedTarget.back());
}

RVIds getVariableSubset(unsigned factorNum, const vector<unsigned> &inputSource, const vector<unsigned> &inputTarget)
{
  RVIds theVarsSubset = {};

  unsigned RVIndexBase = 3*(inputSource[factorNum] - 1);
  theVarsSubset.push_back(RVIndexBase);
  theVarsSubset.push_back(RVIndexBase+1);
  theVarsSubset.push_back(RVIndexBase+2);

  RVIndexBase = 3*(inputTarget[factorNum] - 1);
  theVarsSubset.push_back(RVIndexBase);
  theVarsSubset.push_back(RVIndexBase+1);
  theVarsSubset.push_back(RVIndexBase+2);

  return theVarsSubset;
}

double getDist(double x1, double y1, double z1, double x2, double y2, double z2)
{
  return sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2) + (z1-z2)*(z1-z2));
}

double getTotalMahanalobisDist(vector< rcptr<Factor> > &factors, vector< rcptr<Factor> > &old_factors) //check if mahanalobis only check means, use Kuback liebler
{
  double dist = 0;
  for(unsigned i = 0; i < factors.size(); i++)
  {
    rcptr<SqrtMVG> factorSGPtr = dynamic_pointer_cast<SqrtMVG>(factors[i]);
    rcptr<SqrtMVG> old_factorSGPtr = dynamic_pointer_cast<SqrtMVG>(old_factors[i]);
    dist = dist + factorSGPtr->distance(&(*old_factors[i])); // pointer black magic
  }

  return dist;
}