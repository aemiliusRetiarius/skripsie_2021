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
    fstream fout;
  
    // opens an existing csv file or creates a new file.
    fout.open("../gaussian_data.csv", ios::out | ios::app);
    fout << 0 << "," << 1 << "\n";

} // main
