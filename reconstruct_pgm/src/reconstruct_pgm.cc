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

struct gaussian_pgm {
  // file input storage vectors
  vector<unsigned> inputSource, inputTarget, obsPoints; 
  vector<double> inputDist;
  vector<AnyType> obsPos;
  vector<bool> inputChangedFlag;

  // assume that there are no gaps in point numbering, possible improvement to handle it
  // find max value in source and target to find number of points
  unsigned numPoints = 0;
  // find number of records -> number of factors
  unsigned numRecords = 0;

  // define random varibles
  // for every point have x, y, z
  // e.g. to find point i_y: (i-1)*3 +1
  // after 3d data, add rvs for distances
  RVIds theVarsFull = {};
  RVIds theVarsObs = {};
  RVIds theVarsDists = {};

  // define factors
  vector< rcptr<Factor> > factors;
  vector< rcptr<Factor> > old_factors;

};

void readDataFile(string fileString, gaussian_pgm &gpgm);
void readObsFile(string fileString, gaussian_pgm &gpgm);
void initialiseVars(gaussian_pgm &gpgm);
void initialiseFactors(gaussian_pgm &gpgm);
void reconstructSigmaFactors(gaussian_pgm &gpgm);
void extractNewFactors(gaussian_pgm &gpgm);

unsigned getNumPoints(vector<unsigned> &inputSource, vector<unsigned> &inputTarget);
RVIds getVariableSubset(unsigned factorNum, const gaussian_pgm &gpgm);
vector<double> getStartingPos(unsigned pointNum);
double getDist(double x1, double y1, double z1, double x2, double y2, double z2);
rcptr<Factor> getObsFactor(unsigned factorNum, const gaussian_pgm &gpgm);
double getTotalMahanalobisDist(vector< rcptr<Factor> > &factors, vector< rcptr<Factor> > &old_factors);


int main(int, char *argv[]) {

  string dataString = "../../cube_gen/Data/dists.csv";
  string obsString = "../../cube_gen/Data/obs.csv";
  double tolerance = 0.1;

  gaussian_pgm pgm1;
  
  
  // fill input storage vectors from file
  readDataFile(dataString, pgm1);
  cout << "Opened data file" << endl;
  readObsFile(obsString, pgm1);
  cout << "Opened observations file" <<  endl;

  // assume that there are no gaps in point numbering, possible improvement to handle it
  // find max value in source and target to find number of points
  pgm1.numPoints = getNumPoints(pgm1.inputSource, pgm1.inputTarget);
  
  // find number of records -> number of factors
  pgm1.numRecords = pgm1.inputSource.size();

  cout << "Num points: " << pgm1.numPoints << endl;
  cout << "Num records: " << pgm1.numRecords << endl;
  
  // fill rv vectors
  initialiseVars(pgm1);

  // initialise factors with input data
  initialiseFactors(pgm1);

  //do {
  // reconstruct new factors with additional dimension for distance
  reconstructSigmaFactors(pgm1);
  
  // observe and reduce full joint, extract new factors using mean
  extractNewFactors(pgm1);

  //} while(getTotalMahanalobisDist(pgm1.factors, pgm1.old_factors) > tolerance);
  
  cout << "total diff dist: " << getTotalMahanalobisDist(pgm1.factors, pgm1.old_factors) << endl;

} // main

// function will modify storage vectors
void readDataFile(string fileString, gaussian_pgm &gpgm)
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
    gpgm.inputSource.push_back((unsigned)stod(row[1]));
    gpgm.inputTarget.push_back((unsigned)stod(row[2]));
    gpgm.inputDist.push_back(stod(row[3]));

    bool parsedBool = (row[4].compare("True") == 1) ? true : false;
    gpgm.inputChangedFlag.push_back(parsedBool);

  }
}

//function will modify storage vectors
void readObsFile(string fileString, gaussian_pgm &gpgm)
{
  // file pointer
  fstream fin;

  // file input handlers
  string line, word;

  // opens an existing csv file or creates a new file.
  fin.open(fileString, ios::in);
  
  // remove first line
  getline(fin, line);
  
  // get obs points
  getline(fin, line);
  stringstream s(line);
  while (getline(s, word, ',')) 
  {
    // parse and add point num to a vector
    gpgm.obsPoints.push_back((unsigned)stod(word));   
  }
  // remove next line
  getline(fin, line);

  // read remaining lines and add to obs pos
  while (getline(fin, line)) 
  {
  
    // used for breaking words
    stringstream s(line);
  
    // read every column data of a row and
    // store it in a string variable, 'word'
    while (getline(s, word, ',')) 
    {
  
      gpgm.obsPos.push_back(stod(word));
      
    }
  }
}

// function will modify theVarsFull, theVarsObs, theVarsDists
void initialiseVars(gaussian_pgm &gpgm)
{
  for(unsigned i = 0; i < 3*(gpgm.numPoints); i++)
  {
    gpgm.theVarsFull.push_back(i); // 3d rvs
  }
  for(unsigned i = 0; i < gpgm.numRecords; i++)
  {
    gpgm.theVarsFull.push_back(3*gpgm.numPoints + i); // dist rvs
    gpgm.theVarsDists.push_back(3*gpgm.numPoints + i);
  }
  for(unsigned obsPoint : gpgm.obsPoints)
  {
    gpgm.theVarsObs.push_back((obsPoint-1)*3); // obs rvs
    gpgm.theVarsObs.push_back((obsPoint-1)*3 + 1);
    gpgm.theVarsObs.push_back((obsPoint-1)*3 + 2);
  }
}

// function will modify factors
void initialiseFactors(gaussian_pgm &gpgm)
{
  // define initial gaussian parameters //mult gaussians*, larger cov, init grid
  prlite::ColVector<double> theMn(6);
  prlite::RowMatrix<double> theCv(6,6);
  theCv.assignToAll(0.0);

  for(unsigned i = 0; i < 6; i++)
  {
    theCv(i,i) = 30.0;
  }

  // create factors
  RVIds theVarsSubset = {};
  vector<double> sourcePos = {};
  vector<double> targetPos = {};
  //unsigned RVIndexBase = 0;
  for(unsigned i = 0; i < gpgm.numRecords; i++)
  {
    // get variable subset of record
    theVarsSubset = getVariableSubset(i, gpgm);
    // get starting positions of variables and fill mean
    sourcePos = getStartingPos(gpgm.inputSource[i]-1);
    targetPos = getStartingPos(gpgm.inputTarget[i]-1); 
    for(unsigned j = 0; j < 3; j++)
    {
      theMn[j] = sourcePos[j];
      theMn[3+j] = targetPos[j];
    }
    // construct gaussians and append to factor list
    rcptr<SqrtMVG> pdfSGPtr ( new SqrtMVG(theVarsSubset, theMn, theCv));
    rcptr<Factor> pdfPtr = pdfSGPtr;
    gpgm.factors.push_back(pdfPtr);
  }
  return;

}

// function will modify factors, old_factors
void reconstructSigmaFactors(gaussian_pgm &gpgm)
{
  cout << "starting reconstruction..." << endl;
  // step through factors and add sigmapoints
  unsigned index = 0; 
  gpgm.old_factors.clear();
  for(rcptr<Factor> factor : gpgm.factors)
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
    RVIds theVarsDist = {3*gpgm.numPoints + index};
    RVVals theDist = {gpgm.inputDist[index]};
    
    // reconstruct new gaussian
    rcptr<SqrtMVG> pdfSigmaSGPtr(SqrtMVG::constructFromSigmaPoints(theVarsSubset, sigmaPoints, theVarsDist, sigmaPointsDists, sigmaPointsNoise));
    rcptr<Factor> pdfSigmaPtr = pdfSigmaSGPtr;
    pdfSigmaPtr = pdfSigmaPtr->observeAndReduce(theVarsDist, theDist)->normalize();

    // redefine factor and push into old factors
    gpgm.old_factors.push_back(factor);
    factor = pdfSigmaPtr;

    // increment record index
    index++;
  }
}

// function will modify factors
void extractNewFactors(gaussian_pgm &gpgm)
{
  // observe and reduce joint of reconsructed gaussians
  rcptr<Factor> jointFactorPtr = absorb(gpgm.factors);
  jointFactorPtr = jointFactorPtr->observeAndReduce(gpgm.theVarsObs, gpgm.obsPos)->normalize(); //obsv individual
  rcptr<SqrtMVG> jointFactorSGPtr = dynamic_pointer_cast<SqrtMVG>(jointFactorPtr);
  
  //gpgm.factors.clear(); // watch for aliasing issues with jointFactorPtr
  // step through factors to extract new gaussians by marginalizing joint gaussians
  unsigned index = 0;
  RVIds theVarsSubset = {};
  rcptr<Factor> obsFactor, unobsFactor;
  for(rcptr<Factor> factor : gpgm.factors)
  {
    theVarsSubset = getVariableSubset(index, gpgm);
    if(find(gpgm.theVarsObs.begin(), gpgm.theVarsObs.end(), theVarsSubset[0]) != gpgm.theVarsObs.end())
    {
      // get known gaussian
      // pass index
      // get unobserved half of factor
      theVarsSubset = {theVarsSubset[3], theVarsSubset[4], theVarsSubset[5]};
      unobsFactor = jointFactorPtr->marginalize(theVarsSubset)->normalize();
      factor = obsFactor->absorb(unobsFactor)->normalize();

    }
    else if(find(gpgm.theVarsObs.begin(), gpgm.theVarsObs.end(), theVarsSubset[3]) != gpgm.theVarsObs.end())
    {

    }
    else
    {
      //cout << "old factor: " << *factor << endl;
      factor = jointFactorPtr->marginalize(theVarsSubset)->normalize();
      //cout << "new factor: " << *factor << endl;
    }
    index++;
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

RVIds getVariableSubset(unsigned factorNum, const gaussian_pgm &gpgm)
{
  RVIds theVarsSubset = {};

  unsigned RVIndexBase = 3*(gpgm.inputSource[factorNum] - 1);
  theVarsSubset.push_back(RVIndexBase);
  theVarsSubset.push_back(RVIndexBase+1);
  theVarsSubset.push_back(RVIndexBase+2);

  RVIndexBase = 3*(gpgm.inputTarget[factorNum] - 1);
  theVarsSubset.push_back(RVIndexBase);
  theVarsSubset.push_back(RVIndexBase+1);
  theVarsSubset.push_back(RVIndexBase+2);

  return theVarsSubset;
}

vector<double> getStartingPos(unsigned pointNum)
{
  // vector contains starting {x, y, z}
  vector<double> pos = {};
  pos.push_back((double)(pointNum % 10)*10);
  pos.push_back((double)(pointNum / 10)*10);
  pos.push_back((double) 0); //init grid om x-y plane

  return pos;
}

rcptr<Factor> getObsFactor(unsigned factorNum, const gaussian_pgm &gpgm)
{
  // find observed half of full factor and return it
  unsigned obsNum, obsIndex = 0;
  for(unsigned obsPoint : gpgm.obsPoints)
  {
    if((obsPoint == gpgm.inputSource[factorNum])||(obsPoint == gpgm.inputTarget[factorNum]))
    {
      //if current observed point num is in requested factor, break
      break;
    }
    obsIndex++;
  }

  // define gaussian parameters 
  prlite::ColVector<double> theMn(3);
  prlite::RowMatrix<double> theCv(3,3);
  RVIds theVarsSubset = {};

  theCv.assignToAll(0.0);
  for(unsigned i = 0; i < 3; i++)
  {
    theCv(i,i) = 0.1;
    theMn[i] = (double)(gpgm.obsPos[obsIndex*3 + i]);
    theVarsSubset.push_back((gpgm.obsPoints[obsIndex]-1)*3 + i);
  }

  rcptr<SqrtMVG> obsSGPtr ( new SqrtMVG(theVarsSubset, theMn, theCv));
  rcptr<Factor> obsPtr = obsSGPtr; 
  return obsPtr->normalize();
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