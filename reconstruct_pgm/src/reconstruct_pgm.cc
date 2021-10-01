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
  rcptr<Factor> joint_factor;

  unsigned dim = 6;
  double lambda = 0;
  vector<prlite::RowMatrix<double>> old_covs;
  
};

void readDataFile(string fileString, gaussian_pgm &gpgm);
void readObsFile(string fileString, gaussian_pgm &gpgm);
void initialiseVars(gaussian_pgm &gpgm);
void initialiseFactors(gaussian_pgm &gpgm);
void reconstructSigmaFactors(gaussian_pgm &gpgm);
void extractNewFactors(gaussian_pgm &gpgm);
void writeResultFile(string fileString, const gaussian_pgm &gpgm);

unsigned getNumPoints(vector<unsigned> &inputSource, vector<unsigned> &inputTarget);
RVIds getVariableSubset(unsigned factorNum, const gaussian_pgm &gpgm);
vector<double> getStartingPos(unsigned pointNum);
rcptr<Factor> dampenCovMat(const rcptr<Factor> newFactor, const rcptr<Factor> oldFactor, const gaussian_pgm &gpgm);
prlite::RowMatrix<double> scalarProduct(prlite::RowMatrix<double> mat, double scalar, unsigned dim);
rcptr<Factor> getObsFactor(unsigned factorNum, const gaussian_pgm &gpgm);
rcptr<Factor> getPointFactor(unsigned pointNum, const gaussian_pgm &gpgm);
double getDist(double x1, double y1, double z1, double x2, double y2, double z2);
double getTotalMahanalobisDist(vector< rcptr<Factor> > &factors, vector< rcptr<Factor> > &old_factors);


int main(int, char *argv[]) {

  string dataString = "../../cube_gen/Data/dists_full.csv";
  string obsString = "../../cube_gen/Data/obs.csv";
  string resultString = "../result.csv";
  double lambda = 0.95;
  double tolerance = 0.1;
  unsigned iter = 0;

  gaussian_pgm pgm1;
  
  
  // fill input storage vectors from file
  readDataFile(dataString, pgm1);
  cout << "Opened data file" << endl;
  readObsFile(obsString, pgm1);
  cout << "Opened observations file" <<  endl;

  // insert lambda value
  pgm1.lambda = lambda;
  
  // assume that there are no gaps in point numbering, possible improvement to handle it
  // find max value in source and target to find number of points
  pgm1.numPoints = getNumPoints(pgm1.inputSource, pgm1.inputTarget);

  // find number of records -> number of factors
  pgm1.numRecords = pgm1.inputSource.size();

  cout << "Num points: " << pgm1.numPoints << endl;
  cout << "Num records: " << pgm1.numRecords << endl;
  
  // fill rv vectors
  initialiseVars(pgm1);

  cout << "RV's initialized" << endl;

  // initialise factors with input data
  initialiseFactors(pgm1);
  cout << "Factors initialized" << endl;

  rcptr<SqrtMVG> testSGPtr; 
  do {

  cout << "loop iter " << iter+1 << endl;
  // reconstruct new factors with additional dimension for distance
  reconstructSigmaFactors(pgm1);
  
  // observe and reduce full joint, extract new factors using mean
  extractNewFactors(pgm1);

  testSGPtr = dynamic_pointer_cast<SqrtMVG>(getPointFactor(1, pgm1));
  //cout << "point 1 mean: " << testSGPtr->getMean() << "cov: " << testSGPtr->getCov() << endl;
  testSGPtr = dynamic_pointer_cast<SqrtMVG>(getPointFactor(58, pgm1));
  //cout << "point 58 mean: " << testSGPtr->getMean() << "cov: " << testSGPtr->getCov() << endl;
  cout << "total mahanalobis dist: " << getTotalMahanalobisDist(pgm1.factors, pgm1.old_factors) << endl;
  iter ++;
  } while (iter <30);
  //} while(getTotalMahanalobisDist(pgm1.factors, pgm1.old_factors) > tolerance);
  
  writeResultFile(resultString, pgm1);

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
  prlite::ColVector<double> theMn(gpgm.dim);
  prlite::RowMatrix<double> theCv(gpgm.dim,gpgm.dim);
  theCv.assignToAll(0.0);
  
  for(unsigned i = 0; i < gpgm.dim; i++)
  {
    theCv(i,i) = 200.0;
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
    for(unsigned j = 0; j < gpgm.dim/2; j++)
    {
      theMn[j] = sourcePos[j];
      theMn[gpgm.dim/2+j] = targetPos[j];
    }
    // construct gaussians and append to factor list
    rcptr<SqrtMVG> pdfSGPtr ( new SqrtMVG(theVarsSubset, theMn, theCv));
    rcptr<Factor> pdfPtr = pdfSGPtr;
    gpgm.factors.push_back(pdfPtr);
  }
  //cout << *gpgm.factors[60] << endl;
  return;

}

// function will modify factors, old_factors
void reconstructSigmaFactors(gaussian_pgm &gpgm)
{
  cout << "starting reconstruction..." << endl;
  // step through factors and add sigmapoints
  unsigned index = 0; 
  gpgm.old_factors.clear();
  vector< rcptr<Factor> > new_factors;

  for(rcptr<Factor> factor : gpgm.factors)
  {
    // 6 x 13 matrix of sigma points
    prlite::ColMatrix<double> sigmaPoints = dynamic_pointer_cast<SqrtMVG>(factor)->getSigmaPoints();

    // get variables factor is defined for
    RVIds theVarsSubset = dynamic_pointer_cast<SqrtMVG>(factor)->getVars();

    // define dist row
    prlite::ColMatrix<double> sigmaPointsDists(1, gpgm.dim*2+1);
    prlite::ColMatrix<double> sigmaPointsNoise(1, gpgm.dim*2+1);
    sigmaPointsNoise.assignToAll(0.0); // neccesary?

    // calc dist row
    for(unsigned i = 0; i < gpgm.dim*2+1; i++)
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
    rcptr<Factor> dampenedPdfSigmaPtr = dampenCovMat(pdfSigmaPtr, factor, gpgm)->normalize();
    new_factors.push_back(dampenedPdfSigmaPtr);
    // increment record index
    index++;
  }
  gpgm.factors = new_factors;
  
}

// function will modify factors
void extractNewFactors(gaussian_pgm &gpgm)
{ 
  cout << "extracting factors..." << endl;
  // observe and reduce joint of reconstructed gaussians
  gpgm.joint_factor = absorb(gpgm.factors);
  rcptr<Factor>red_joint_factor = gpgm.joint_factor->observeAndReduce(gpgm.theVarsObs, gpgm.obsPos)->normalize(); //obsv individual
  // step through factors to extract new gaussians by marginalizing joint gaussians
  unsigned index = 0;
  RVIds theVarsSubset = {};
  rcptr<Factor> obsFactor, unobsFactor;
  vector< rcptr<Factor> > new_factors;

  for(rcptr<Factor> factor : gpgm.factors)
  {
    theVarsSubset = getVariableSubset(index, gpgm);
    if(index%500 == 0){cout << "index: " << index << endl;}
    
    if((find(gpgm.theVarsObs.begin(), gpgm.theVarsObs.end(), theVarsSubset[0]) != gpgm.theVarsObs.end())&&(find(gpgm.theVarsObs.begin(), gpgm.theVarsObs.end(), theVarsSubset[3]) != gpgm.theVarsObs.end()))
    {
      obsFactor = getObsFactor(index, gpgm)->normalize();  
      new_factors.push_back(obsFactor);

    }
    else if(find(gpgm.theVarsObs.begin(), gpgm.theVarsObs.end(), theVarsSubset[0]) != gpgm.theVarsObs.end())
    {
      
      // get known gaussian
      obsFactor = getObsFactor(index, gpgm);

      // get unobserved half of factor
      theVarsSubset = {theVarsSubset[3], theVarsSubset[4], theVarsSubset[5]};
      
      unobsFactor = red_joint_factor->marginalize(theVarsSubset)->normalize();

      // mult halves to get new factor
      rcptr<Factor> dampenedPdfPtr = dampenCovMat(obsFactor->absorb(unobsFactor)->normalize(), factor, gpgm)->normalize();
      
      new_factors.push_back(dampenedPdfPtr);

    }
    else if(find(gpgm.theVarsObs.begin(), gpgm.theVarsObs.end(), theVarsSubset[3]) != gpgm.theVarsObs.end())
    {

      // get known gaussian
      obsFactor = getObsFactor(index, gpgm);
      // get unobserved half of factor
      theVarsSubset = {theVarsSubset[0], theVarsSubset[1], theVarsSubset[2]};
      unobsFactor = red_joint_factor->marginalize(theVarsSubset)->normalize();
      // mult halves to get new factor
      rcptr<Factor> dampenedPdfPtr = dampenCovMat(obsFactor->absorb(unobsFactor)->normalize(), factor, gpgm)->normalize();
      new_factors.push_back(dampenedPdfPtr);
    }
    else
    {
      //if(index == 50) {cout << "old factor[50]: " << (dynamic_pointer_cast<SqrtMVG>(factor))->getMean() << endl;}
      //if(index == 50) {cout  << "pre margin:"<<(dynamic_pointer_cast<SqrtMVG>(factor))->getCov() << endl;}
      rcptr<Factor> dampenedPdfPtr = dampenCovMat(red_joint_factor->marginalize(theVarsSubset)->normalize(), factor, gpgm)->normalize();
      new_factors.push_back(dampenedPdfPtr);
      //if(index == 50) {cout << "new factor[50]: " << (dynamic_pointer_cast<SqrtMVG>(factor))->getMean() << endl;}
      //if(index == 50) {cout  << "post margin:"<<(dynamic_pointer_cast<SqrtMVG>(factor))->getCov() << endl;}

    }
    index++;
  }
  
  gpgm.factors = new_factors;
}

void writeResultFile(string fileString, const gaussian_pgm &gpgm)
{

  fstream fout;
  // opens an existing csv file or creates a new file.
  fout.open(fileString, ios::out | ios::trunc);
  fout << ",x,y,z" <<"\n";
  
  rcptr<SqrtMVG> pointFactorSGPtr;
  string pointRecord = "";
  prlite::ColVector<double> theMn(3);
  for(unsigned i = 0; i < gpgm.numPoints; i++)
  {
    pointFactorSGPtr = dynamic_pointer_cast<SqrtMVG>(getPointFactor(i+1, gpgm));
    theMn = pointFactorSGPtr->getMean();
    pointRecord = pointRecord + to_string(i)+","+to_string(theMn[0])+","+to_string(theMn[1])+","+to_string(theMn[2])+"\n";
  }
  
  fout << pointRecord;
  fout.close();
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

/**
vector<double> getStartingPos(unsigned pointNum)
{
  // vector contains starting {x, y, z}
  vector<double> pos = {};
  pos.push_back((double)((pointNum % 20)%5)*20);
  pos.push_back((double)((pointNum % 20)/4)*20);
  pos.push_back((double) (pointNum / 20)*20); //init grid om x-y plane

  return pos;
}
**/

rcptr<Factor> dampenCovMat(const rcptr<Factor> newFactor, const rcptr<Factor> oldFactor, const gaussian_pgm &gpgm)
{
  rcptr<SqrtMVG> newFactorSG = dynamic_pointer_cast<SqrtMVG>(newFactor);
  rcptr<SqrtMVG> oldFactorSG = dynamic_pointer_cast<SqrtMVG>(oldFactor);
  prlite::RowMatrix<double> dampedCov = scalarProduct(oldFactorSG->getCov(), gpgm.lambda, gpgm.dim) + scalarProduct(newFactorSG->getCov(), (1-gpgm.lambda), gpgm.dim);
  rcptr<SqrtMVG> pdfSGPtr ( new SqrtMVG(newFactorSG->getVars(), newFactorSG->getMean(), dampedCov));
  rcptr<Factor> pdfPtr = pdfSGPtr;
  return pdfPtr;
}

prlite::RowMatrix<double> scalarProduct(const prlite::RowMatrix<double> mat, double scalar, unsigned dim)
{
  
  prlite::RowMatrix<double> resMat(dim, dim);

  for(unsigned row = 0; row < dim; row++)
  {
    for(unsigned col = 0; col < dim; col++)
    {
      resMat(row,col) = scalar * mat(row,col);
    }
  }

  return resMat;
}

rcptr<Factor> getObsFactor(unsigned factorNum, const gaussian_pgm &gpgm)
{
  // find observed half of full factor and return it
  vector<unsigned> obsIndices = {};
  unsigned index = 0;
  for(unsigned obsPoint : gpgm.obsPoints)
  {
    if((obsPoint == gpgm.inputSource[factorNum])||(obsPoint == gpgm.inputTarget[factorNum]))
    {
      //if current observed point num is in requested factor, push into obsIndex
      obsIndices.push_back(index);
    }
    index++;
  }

  vector<rcptr<Factor>> obsPdfs;
  for(unsigned obsIndex : obsIndices)
  {
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
    obsPdfs.push_back(obsPtr);
    
  }
  return absorb(obsPdfs);
}

rcptr<Factor> getPointFactor(unsigned pointNum, const gaussian_pgm &gpgm)
{
  // get x,y and z rvs of req point
  RVIds theVarsSubset = {};
  theVarsSubset.push_back(3*(pointNum-1));
  theVarsSubset.push_back(3*(pointNum-1) +1);
  theVarsSubset.push_back(3*(pointNum-1) +2);

  // observe and reduce joint of reconsructed gaussians
  rcptr<Factor> jointFactorPtr;
  jointFactorPtr = gpgm.joint_factor->marginalize(theVarsSubset)->normalize();

  return jointFactorPtr;
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