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

    unsigned D = 2;

    enum{x,y};
    //RVIds theVars = {x,y};
    RVIds theVars = {};
    theVars.push_back(x);
    theVars.push_back(y);

    vector< rcptr<Factor> > factors;

    prlite::ColVector<double> theMn(D);
    prlite::RowMatrix<double> theCv(D,D);  // for legacy reasons we use Matrix and not prlite::ColMatrix;
    theCv.assignToAll(0.0);

    theMn[0] = 0.0;
    theMn[1] = 0.0;
    theCv(0,0) = 1.0;
    theCv(1,1) = 1.0;

    rcptr<SqrtMVG> pdf1SGPtr ( new SqrtMVG(theVars, theMn, theCv));
    rcptr<Factor> pdf1Ptr = pdf1SGPtr;
    factors.push_back(pdf1Ptr);
    
    theMn[0] = 1.0;
    theMn[1] = 1.0;
    theCv(0,0) = 1.0;
    theCv(1,1) = 1.0;

    rcptr<SqrtMVG> pdf2SGPtr ( new SqrtMVG(theVars, theMn, theCv));
    rcptr<Factor> pdf2Ptr = pdf2SGPtr;
    factors.push_back(pdf1Ptr);

    //can use getMean()[0] to isolate returned values

    cout << pdf1SGPtr->getMean() <<  " " << pdf1SGPtr-> getCov() << endl;
    cout << pdf2SGPtr->getMean() <<  " " << pdf2SGPtr-> getCov() << endl;
    
    rcptr<Factor> jointPtr = pdf1Ptr->absorb(pdf2Ptr);
    jointPtr->inplaceNormalize();
    rcptr<SqrtMVG> jointSGPtr = dynamic_pointer_cast<SqrtMVG>(jointPtr);

    cout << jointSGPtr->getMean() <<  " " << jointSGPtr-> getCov() << endl;

    //////////////collapsing factors
    rcptr<Factor> jointFactorPtr = absorb(factors);
    rcptr<SqrtMVG> jointFactorSGPtr = dynamic_pointer_cast<SqrtMVG>(jointFactorPtr);
    cout << jointFactorSGPtr->getMean() <<  " " << jointFactorSGPtr-> getCov() << endl;

    // file pointer
    fstream fout;
  
    // opens an existing csv file or creates a new file.
    fout.open("../gaussian_data.csv", ios::out | ios::app);
    fout << 0 << "," << 1 << "\n";


} // main
