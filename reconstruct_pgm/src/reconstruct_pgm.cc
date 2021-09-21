/*
 * Author     :  (DSP Group, E&E Eng, US)
 * Created on :
 * Copyright  : University of Stellenbosch, all rights retained
 */

// standard headers
#include <iostream>  // cout, endl, flush, cin, cerr
#include <string>  // string, stod

#include "discretetable.hpp"
#include "prlite_zfstream.hpp"

using namespace std;
using namespace emdw;

/**                            **/

#include "emdw.hpp"
#include "sqrtmvg.hpp"

int main(int, char *argv[]) {

  // file pointer
  fstream fin;

  // file input handlers
  vector<string> row;
  string line, word;

  // file input storage vectors
  vector<unsigned> inputSource, inputTarget, sortedSource, sortedTarget; 
  vector<double> inputDist;
  vector<bool> inputChangedFlag;
  
  // opens an existing csv file or creates a new file.
  fin.open("../../cube_gen/Data/dists.csv", ios::in);
  cout << "opened file" <<endl;
  
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

  // assume that there are no gaps in point numbering, possible improvement to handle it
  // find max value in source and target to find number of points

  sortedSource = inputSource;
  sortedTarget = inputTarget;
  sort(sortedSource.begin(), sortedSource.end());
  sort(sortedTarget.begin(), sortedTarget.end());

  unsigned numPoints = max(sortedSource.back(), sortedTarget.back());
  cout << "Num points: " << numPoints << endl;

  // find number of records -> number of factors
  unsigned numRecords = inputSource.size();
  cout << "Num records: " << numRecords << endl;

  // define random varibles
  // for every point have x, y, z
  // e.g. to find point i_y: (i-1)*3 +1
  RVIds theVarsFull = {};
  for(unsigned i = 0; i < 3*(numPoints); i++)
  {
    theVarsFull.push_back(i);
  }

  vector< rcptr<Factor> > factors;

  // create factors
  RVIds theVarsSubset = {};
  unsigned RVIndexBase = 0;
  for(unsigned i = 0; i < numRecords; i++)
  {
    theVarsSubset.clear();

    // add source x,y,z rvs to subset
    RVIndexBase = 3*(inputSource[i] - 1);
    theVarsSubset.push_back(RVIndexBase);
    theVarsSubset.push_back(RVIndexBase+1);
    theVarsSubset.push_back(RVIndexBase);

    // add target x,y,z rvs to subset
    RVIndexBase = 3*(inputSource[i] - 1);
    theVarsSubset.push_back(RVIndexBase);
    theVarsSubset.push_back(RVIndexBase+1);
    theVarsSubset.push_back(RVIndexBase);



  }

  


} // main
