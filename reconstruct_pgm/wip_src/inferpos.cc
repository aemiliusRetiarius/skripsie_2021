/*
 * Author     :  (DSP Group, E&E Eng, US)
 * Created on :
 * Copyright  : University of Stellenbosch, all rights retained
 *
 * Purpose: Infers the positions in D-dim space of a number of points,
 *          where we know the distances between some pairs of those
 *          points.
 */

// standard headers
#include <iostream>  // cout, endl, flush, cin, cerr
#include <cctype>  // toupper
#include <string>  // string
#include <memory>
#include <set>
#include <map>
#include <algorithm>
#include <limits>
#include <random>
#include <iomanip>
#include <tuple>

// patrec headers
#include "prlite_zfstream.hpp"
#include "prlite_logging.hpp"  // initLogging
#include "prlite_testing.hpp"
#include "prlite_matrix.hpp"
#include "prlite_vector.hpp"
#include "gLinear/gLapackWrap.h"

// emdw headers
#include "emdw.hpp"
#include "sqrtmvg.hpp"

#include "iomaps.hpp"

using namespace std;
using namespace emdw;

typedef SqrtMVG SG;

int main(int, char *argv[]) {

  // NOTE: this activates logging and unit tests
  initLogging(argv[0]);
  prlite::TestCase::runAllTests();

  try {

    // ########################################
    // ### first load data from input files ###
    // ########################################

    string priorName, distName;
    cout << "Name the files with the prior_positions and measured_distances\n> ";
    cin >> priorName >> distName;

    // priorMap: value is a vector of the coordinates followed by
    // their stdevs
    // distMap: value is a pair containing the distance and its
    // stdev
    // see iomaps.hpp for full detail
    auto [dim, priorMap, distMap] = loadFromFile(priorName, distName);
    //saveToFile("pr.txt", "ds.txt", priorMap, distMap);

    // we use a nested iteration process. The outer one (below) resets
    // everything, but with using the newest available position estimates.
    // In particular we reset the variances to a predetermined value.
    for (unsigned outer = 0; outer < 5; outer++) {

      cout << "Working in a " << dim << "-dimensional space\n\n";
      for (auto el : priorMap) {  //priorMap< pnt, vector[coords, tols]>
        cout << setw(3) << el.first << " ";
        for (unsigned d = 0; d < 2*dim; d++) {
          cout << setw(12) << el.second[d] << " ";
        } // for d
        cout << endl;
      } // for el
      cout << endl;

      // for (auto el : distMap) { // distMap< pair<pnt1, pnt2>, pair<dist, tol> >
      //   cout << setw(3) << el.first.first << " "
      //        << setw(3) << el.first.second << " "
      //        << setw(12) <<el.second.first << " "
      //        << setw(12) << el.second.second
      //        << endl;
      // } // for el
      // cout << endl;


      // #######################################
      // ### define RV's and observed values ###
      // #######################################

      // Individual position RVs posRV< <pair{pnt,dim}>, id>
      // IMPORTANT: Later on we rely on ordering such that
      // posRV[{p,d}] < posRV[{p,d+1}] for all valid dims,
      // posRV[{p,dim-1}] < posRV[{p+1,0}] for all valid points.
      map< pair<unsigned,unsigned>, RVIdType> posRV;
      std::map<emdw::RVIdType, AnyType> obsv;
      RVIdType idCnt = 0;
      for (auto el : priorMap) {  // map< unsigned, vector<double> >
        RVIds posIds;
        for (unsigned d = 0; d < dim; d++) {
          if (el.second[d+dim] < 1E-20) { // we have an observed value here
            obsv[idCnt] = el.second[d];
          } // if
          posIds.push_back(idCnt);
          posRV[{el.first, d}] = idCnt++;
        } // for d
      } // for

      map< pair<unsigned,unsigned>, RVIdType> distRV; // distRV[{pnt1,pnt2}]
      map< pair<unsigned,unsigned>, RVIds> clusterRVs;  // all position RVs at a position posRVD< pnt,vector<ids> >
      for (auto el : distMap) { // map< pair<unsigned, unsigned>, pair<double,double> >
        unsigned p1 = el.first.first; unsigned p2 = el.first.second;
        // Collect all the position RV ids involved in a cluster.
        // IMPORTANT: We assume that clusterRVs[{p1,p2}][d] and
        // clusterRVs[{p1,p2}][d+dim] are on the same dimension
        // for points p1 and p2 respectively.
        for (unsigned d = 0; d < dim; d++) {clusterRVs[{p1,p2}].push_back(posRV[{p1,d}]);} // for
        for (unsigned d = 0; d < dim; d++) {clusterRVs[{p1,p2}].push_back(posRV[{p2,d}]);} // for
        // The distance RV
        obsv[idCnt] = el.second.first;
        distRV[{p1,p2}] = idCnt++;
      } // for

      // cout << "Position RVs:\n";
      // for (auto el : posRV) {
      //   cout << el.first.first << " " << el.first.second << ": " << el.second << endl;
      // } // for
      // cout << endl;

      // cout << "Distance RVs:\n";
      // for (auto el : distRV) {
      //   cout << el.first.first << " " << el.first.second << ": " << el.second << endl;
      // } // for
      // cout << endl;

      // repackage observed variables
      RVIds theVars;
      RVVals theirVals;
      for (auto el : obsv) {
        theVars.push_back(el.first);
        theirVals.push_back(el.second);
      } // for


      // cout << "Observed RVs:\n";
      // for (auto el : obsv) {
      //   cout << el.first << ": " << double(el.second) << endl;
      // } // for
      // cout << endl;

      // ##############################
      // ### Lets build the factors ###
      // ##############################

      // ************************************************************************
      // *** Now we build the various prior factors. Small stdev for observed ***
      // ************************************************************************

      rcptr<SqrtMVG> mvgFactor;
      map< unsigned, rcptr<Factor> > priorFactors;

      prlite::ColVector<double> mn1D(1);
      prlite::RowMatrix<double> cv1D(1,1);

      for (auto el : priorMap) {  // map< pntId, vector< D x coords D x tols> >

        // ++++++++++++++++++++++++++++++++++++++++++++++++++
        // +++ Build a 1d factor for each non-observed RV +++
        // ++++++++++++++++++++++++++++++++++++++++++++++++++

        vector< rcptr<Factor> > scalarFactors;
        for (unsigned d = 0; d < dim; d++) {
          if (el.second[d+dim] >  1E-20) { // only for non-observed RVs
            mn1D[0] = el.second[d];
            cv1D(0,0) = el.second[d+dim]*el.second[d+dim];
            scalarFactors.push_back(
              uniqptr<SqrtMVG> ( new SqrtMVG({posRV[{el.first,d}]}, mn1D, cv1D) ) );
          } // if
        } // for d

        // +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        // +++ Combine them into a multi-dim factor for each point +++
        // +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        if ( scalarFactors.size() ) {
          priorFactors[el.first] = absorb(scalarFactors)->normalize();
          mvgFactor = std::dynamic_pointer_cast<SqrtMVG>(priorFactors[el.first]);
          //cout << mvgFactor->getVars() << endl;
          // cout << mvgFactor->getMean() << endl;
          // cout << mvgFactor->getCov() << endl;
        } // if
        else {
          priorFactors[el.first] = nullptr; // fully observed point
        } // else

      } // for

      // *********************************************************************
      // *** Combine them into pairs of points with distances between them ***
      // *********************************************************************

      map< pair<unsigned,unsigned>, rcptr<Factor> > clusters;
      for (auto el : distMap) { // map< pair<pnt1, pnt2>, pair<dist, tol> >

        // +++++++++++++++++++++++++++++++++++++++
        // +++ The joint factor for two points +++
        // +++++++++++++++++++++++++++++++++++++++

        unsigned p1 = el.first.first;
        unsigned p2 = el.first.second;
        // need to first check if prior still exists after observing
        if (priorFactors[p1] == nullptr) {

          if (priorFactors[p2] == nullptr) {
            cerr << __FILE__ << __LINE__ << " unexpected distance between two fully observed points "
                 << p1 << " and " << p2 << endl;
            cerr << "Rather just remove this distance, it does not contribute anything!\n";
            exit(-1);
          } // if

          clusters[{p1,p2}] = priorFactors[p2];
        } // if
        else if (priorFactors[p2] == nullptr) {
          clusters[{p1,p2}] = priorFactors[p1];
        } // else if
        else {
          clusters[{p1,p2}] = priorFactors[p1]->absorb(priorFactors[p2])->normalize();
        } // else
        //cout << *clusters[{p1,p2}] << endl;
      } // for

      rcptr<Factor> bigJoint;

      // inner estimation loop. This one refines both position and stdev

      for (unsigned inner = 0; inner < 5; inner++) {
        vector< rcptr<Factor> > factors;
        prlite::ColMatrix<double> spD; // sigma points for the pairs of points
        prlite::ColMatrix<double> sp1; // corresponding distance sigma points
        prlite::ColMatrix<double> distR(1,1);

        rcptr<Factor> jointFactor;
        for (auto el : distMap) { // for all points with measured distances between them
          // distMap: map< pair<pnt1, pnt2>, pair<dist, tol> >

          unsigned p1 = el.first.first;
          unsigned p2 = el.first.second;
          RVIds theIds = clusterRVs[{p1,p2}];
          mvgFactor = std::dynamic_pointer_cast<SqrtMVG>(clusters[{p1,p2}]);  // get the factor
          spD = mvgFactor->getSigmaPoints();                                  // put its sigma points in the columns
          sp1.resize( 1,spD.cols() );                                         // corresponding distance

          for (int j = 0; j < spD.cols(); j++) { // for all sigma points of the current cluster

            // We need to find the distance between the two points according to each sigma point j. Some variables
            // might be observed, so we'll first have to rebuild a full dimensional version of each sigma point.

            vector<double> vals(dim*2); // this will hold the full coordinates of both points for a given sigma point
            unsigned offset = 0;
            for (unsigned d = 0; d < 2*dim; d++) {
              auto itr = obsv.find(theIds[d]);
              if ( itr != obsv.end() ) {
                vals[d] = double(itr->second); // for observed RVs, use its value directly
                offset++;
              } // if
              else { // otherwise use the coordinates from the sigma point value
                vals[d] = spD[d-offset][j];
              } // else
            } // for d
            //cout << "ids:  " << theIds << endl;
            //cout << "vals: " << vals << endl;

            // we now have both points fully specified, can now calculate the distance

            double sumDiff2 = 0;
            for (unsigned d = 0; d < dim; d++) {
              double diff = vals[d] - vals[d+dim];
              sumDiff2 += diff*diff;
            } // for d
            sp1(0,j) = sqrt(sumDiff2); // the distance between the two points

          } // for j (i.e. all sigma points)
          //cout << sp1 << endl; exit(-1);


          // +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
          // +++ joint for the two points including their distance +++
          // +++++++++++++++++++++++++++++++++++++++++++++++++++++++++

          distR(0,0) = distMap[{p1,p2}].second;
          // build the full factor including the distance
          mvgFactor = uniqptr<SqrtMVG>(
            SqrtMVG::constructFromSigmaPoints(
              clusters[{p1,p2}]->getVars(),spD,
                {distRV[{p1,p2}]},sp1,
              distR) );
          // and observe the distance value
          factors.push_back( mvgFactor->Factor::observeAndReduce(theVars,theirVals)->normalize() );
          mvgFactor = std::dynamic_pointer_cast<SqrtMVG>(factors[factors.size()-1]);
          //cout << mvgFactor->getVars() << endl << mvgFactor->getMean() << endl << mvgFactor->getCov() << endl;

          //if (p2 == 13) exit(-1);

        } // for all pairs of points with measured distances

        // ##########################################################
        // ### Get the joint for the whole lot and interrogate it ###
        // ##########################################################

        bigJoint = absorb(factors)->normalize();
        //cout << *bigJoint << endl;
        mvgFactor = std::dynamic_pointer_cast<SqrtMVG>(bigJoint);
        cout << "Outer: " << outer << " Inner: " << inner << " with dimension: " << bigJoint->noOfVars() << endl;
        cout << "Condition number of joint L is " << cond2( mvgFactor->getL() ) << endl;


        // lets find out what happened to each position
        prlite::ColVector<double> mn(dim);
        prlite::RowMatrix<double> cv(dim,dim);
        rcptr<Factor> query;
        for (auto& el : clusters) {

          // update each position in the system
          el.second = bigJoint->marginalize( el.second->getVars() )->normalize();

          //mvgFactor = std::dynamic_pointer_cast<SqrtMVG>(el.second);
          //mn = mvgFactor->getMean();
          //cv = mvgFactor->getCov();
          // cout << "mean\n";
          // for (int d = 0; d < mn.size(); d++) {
          //   cout << setw(12) << mn[d] << " ";
          // } // for
          // cout << "\nstdev\n";
          // for (int d = 0; d < mn.size(); d++) {
          //   cout << setw(12)<< sqrt(cv(d,d)) << " ";
          // } // for
          // cout << endl;
        } // for
        //cout << endl << endl;

      } // for inner

      // lets find out what happened to each position
      rcptr<Factor> query;
      for (auto& pnt : priorMap) { // lets update each position in the system
        vector<double> updated(2*dim); //priorMap< pntId, vector[coords, tols]>
        for (unsigned d = 0; d < dim; d++) {
          RVIdType rvId = posRV[{pnt.first, d}];
          auto itr = obsv.find(rvId);
          if ( itr == obsv.end() ) { // not observed, lets use query for it
            query = bigJoint->marginalize({rvId})->normalize();
            //cout << *query << endl;
            mvgFactor = std::dynamic_pointer_cast<SqrtMVG>(query);
            updated[d] = mvgFactor->getMean()[0];
            // to prevent numeric issues, limit stdev to bigger than 1/3 of original value
            updated[d+dim] = std::max( pnt.second[d+dim]/3.0,sqrt( mvgFactor->getCov()(0,0) ) );
          } // if
          else {
            updated[d] = double(itr->second);
            updated[d+dim] = 0;
          } // else

        } // for d
        pnt.second = updated;
        //cout << updated << endl;
      } // for pnt
      cout << endl << endl;

    } // for outer

    // priorMap is already updated. Lets now update distMap;
    for (auto& el : distMap) {

      // now calculate the distance
      double sumDiff2 = 0;
      for (unsigned d = 0; d < dim; d++) {
        double diff = priorMap[el.first.first][d] - priorMap[el.first.second][d];
        sumDiff2 += diff*diff;
      } // for d
      double dist = sqrt(sumDiff2);
      el.second.second = abs(el.second.first - dist);
      el.second.first = dist;
    } // for

    saveToFile("estpos.csv", "estdist.csv", priorMap, distMap);
  } // try

  catch (char msg[]) {
    cerr << msg << endl;
  } // catch

  catch (char const* msg) {
    cerr << msg << endl;
  } // catch

  catch (const string& msg) {
    cerr << msg << endl;
    throw;
  } // catch

  catch (const exception& e) {
    cerr << "Unhandled exception: " << e.what() << endl;
    throw e;
  } // catch

  catch(...) {
    cerr << "An unknown exception / error occurred\n";
    throw;
  } // catch

} // main
