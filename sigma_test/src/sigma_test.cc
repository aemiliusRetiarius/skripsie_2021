/*
 * Author     :  (DSP Group, E&E Eng, US)
 * Created on :
 * Copyright  : University of Stellenbosch, all rights retained
 */

// standard headers
#include <iostream>  // cout, endl, flush, cin, cerr

#include "discretetable.hpp"
#include "prlite_zfstream.hpp"

using namespace std;
using namespace emdw;
using namespace prlite;

/**                            **/

#include "emdw.hpp"
#include "sqrtmvg.hpp"

int main(int, char *argv[]) {

  unsigned seedVal = emdw::randomEngine.getSeedVal();
  cout <<  seedVal << endl;
  emdw::randomEngine.setSeedVal(seedVal);

  enum{x1, x2, d};
  vector< rcptr<Factor> > scalarFactors;
  prlite::ColVector<double> mn1D(1);
  prlite::RowMatrix<double> cv1D(1,1);

  mn1D[0] = 0;
  cv1D(0,0) = 0.01;

  scalarFactors.push_back( uniqptr<SqrtMVG> ( new SqrtMVG({x1}, mn1D, cv1D) ) );

  mn1D[0] = 10;
  cv1D(0,0) = 0.01;

  scalarFactors.push_back( uniqptr<SqrtMVG> ( new SqrtMVG({x2}, mn1D, cv1D) ) );

  rcptr<Factor> priorFactor = absorb(scalarFactors)->normalize();

  prlite::ColMatrix<double> sigmaPoints;
  prlite::ColMatrix<double> sigmaDists;
  prlite::ColMatrix<double> distNoise(1,1);

  distNoise(0,0) = 0.1;

  rcptr<SqrtMVG>mvgFactor = std::dynamic_pointer_cast<SqrtMVG>(priorFactor);  // get the factor
  sigmaPoints = mvgFactor->getSigmaPoints();  
  sigmaDists.resize(1, sigmaPoints.cols());

  cout << sigmaPoints << endl;

  unsigned cols = (unsigned)sigmaPoints.cols();
  for(unsigned col = 0; col < cols; col++)
  {
    sigmaDists(0, col) = abs(sigmaPoints(0, col) - sigmaPoints(1, col));
  }

  mvgFactor = uniqptr<SqrtMVG>(
      SqrtMVG::constructFromSigmaPoints(
      {x1, x2}, sigmaPoints,
      {d},
      sigmaDists, distNoise) );

  cout << sigmaDists << endl;
  cout << "constucted from sigma points" << endl;

  rcptr<Factor> newFactor = mvgFactor->Factor::observeAndReduce({d}, {3.0})->normalize();
  rcptr<SqrtMVG> mvgQueryJoint = std::dynamic_pointer_cast<SqrtMVG>(newFactor);

  cout << mvgQueryJoint->getMean() << endl;
  cout << mvgQueryJoint->getCov() << endl;
  
  rcptr<Factor> query = newFactor->marginalize({x1})->normalize();
  rcptr<SqrtMVG> mvgQuery = std::dynamic_pointer_cast<SqrtMVG>(query);

  cout << "point 1:" << endl;
  cout << mvgQuery->getMean() << endl;
  cout << mvgQuery->getCov() << endl;
  
  cout << "success" << endl;

} // main
