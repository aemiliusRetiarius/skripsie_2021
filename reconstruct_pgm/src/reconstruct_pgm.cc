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

/**                            **/

#include "emdw.hpp"
#include "sqrtmvg.hpp"

int main(int, char *argv[]) {

  // file pointer
  fstream fin;

  vector<string> row;
  string line, word;
  
  // opens an existing csv file or creates a new file.
  fin.open("../../cube_gen/Data/dists.csv", ios::in);
  cout << "opened file" <<endl;
  
  //remove first line with col names
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
      cout << word << endl;
      
    }


  }


} // main
