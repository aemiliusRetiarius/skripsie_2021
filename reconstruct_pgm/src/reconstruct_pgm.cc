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
  vector<double> inputSource, inputTarget, inputDist;
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
    inputSource.push_back(stod(row[1]));
    inputTarget.push_back(stod(row[2]));
    inputDist.push_back(stod(row[3]));

    bool parsedBool = (row[4].compare("True") == 1) ? true : false;
    inputChangedFlag.push_back(parsedBool);
    


  }


} // main
