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

    unsigned D = 1;

    RVIds theVars = {0};
    prlite::ColVector<double> theMn(D);
    prlite::RowMatrix<double> theCv(D,D);  // for legacy reasons we use Matrix and not prlite::ColMatrix;
    theCv.assignToAll(0.0);

    theMn[0] = 0.0;
    theCv(0,0) = 1.0;

    rcptr<SqrtMVG> pdf1SGPtr ( new SqrtMVG(theVars, theMn, theCv));
    rcptr<Factor> pdf1Ptr = pdf1SGPtr;
    
    theMn[0] = 1.0;
    theCv(0,0) = 2.0;
    rcptr<SqrtMVG> pdf2SGPtr ( new SqrtMVG(theVars, theMn, theCv));
    rcptr<Factor> pdf2Ptr = pdf2SGPtr;

    cout << pdf1SGPtr->getMean() <<  " " << pdf1SGPtr-> getCov() << endl;
    cout << pdf2SGPtr->getMean() <<  " " << pdf2SGPtr-> getCov() << endl;
    
    rcptr<Factor> jointPtr = pdf1Ptr->absorb(pdf2Ptr);
    jointPtr->inplaceNormalize();
    rcptr<SqrtMVG> jointSGPtr = dynamic_pointer_cast<SqrtMVG>(jointPtr);

    cout << jointSGPtr->getMean() <<  " " << jointSGPtr-> getCov() << endl;



} // main
