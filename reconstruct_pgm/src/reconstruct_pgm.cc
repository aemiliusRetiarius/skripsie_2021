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


struct gaussian_pgm 
{
    
    double lambda = 0;
    unsigned iter = 0;
    
    map< unsigned, unsigned> dimMap; // map <point_num, dim>
    map< unsigned, vector<double> > posMap; // map <point_num, vector<x_pos, y_pos, ...>>
    map< unsigned, vector<double> > posTolMap; // map <point_num, vector<x_tol, y_tol, ...>>
    map< unsigned, vector<double> > posMap_old; // map <point_num, vector<x_pos, y_pos, ...>> used for convergence

    map< pair<unsigned, unsigned>, double> distMap; // map <pair<point_num1, point_num2>, dist>
    map< pair<unsigned, unsigned>, double> distTolMap; // map <pair<point_num1, point_num2>, dist_tol>

    map< unsigned, RVIds> posRVsMap; // map <point_num, RVIds>
    map< pair<unsigned,unsigned>, RVIds> clusterRVsMap; // map <pair<point_num1, point_num2>, RVIds>
    map< RVIdType, double > obsPosMap; // map <obs_pos_rv, obs_value>
    map< pair<unsigned,unsigned>, RVIdType> distRVsMap; // map <pair<point_num1, point_num2>, RVId>

    vector< rcptr<Factor> > clusters; // combined factor that corresponds to single dist record
    rcptr<Factor> joint_factor; // full joint factor
};

void readPosFile(const string fileString, gaussian_pgm &gpgm, const char delimiter=',', const bool discardLineFlag=true, const bool discardIndexFlag=true);
void readDistFile(const string fileString, gaussian_pgm &gpgm, const char delimiter=',', const bool discardLineFlag=true, const bool discardIndexFlag=true);
void initRVs(gaussian_pgm &gpgm);
void initClusters(gaussian_pgm &gpgm);

int main(int, char *argv[])
{
    //string dataString = "../../cube_gen/Data/dists.csv";
    string posDdataString = "../Data/initpos10.csv";
    string distDataString = "../Data/dists1.csv";
    //string resultString = "../result.csv";
    double lambda = 0.0;
    double tolerance = 0.1;
    unsigned iter = 0;

    gaussian_pgm pgm1;

    readPosFile(posDdataString, pgm1, ' ', false, false);
    readDistFile(distDataString, pgm1, ' ', false, false);
    initRVs(pgm1);
    for(auto point : pgm1.clusterRVsMap)
    {
        //cout << point.second << endl;
    }

}

void readPosFile(const string fileString, gaussian_pgm &gpgm, const char delimiter, const bool discardLineFlag, const bool discardIndexFlag)
{
    // file pointer
    fstream fin;
    // file input handlers
    vector<string> row;
    string line, word;

    // opens an existing csv file or creates a new file.
    fin.open(fileString, ios::in);
    // remove first line with col names if flag set
    if(discardLineFlag) {getline(fin, line);}

    unsigned dim, point_num;
    // while there is a next line, read
    while(getline(fin, line))
    {
        row.clear();
        stringstream s(line);
        // break line using delimiter
        while (getline(s, word, delimiter)) 
        {
            // add data to row vector
            row.push_back(word);
        }

        // remove first col with index if flag set
        if(discardIndexFlag) {row.erase(row.begin());}
        // get dim of record and check format
        dim = (row.size()-1)/2;
        PRLITE_ASSERT(dim*2+1 == row.size(), "Badly formatted line in " << fileString);
        
        // fill pgm dim, pos and tol maps
        point_num = (unsigned)stod(row[0]);
        gpgm.dimMap[point_num] = dim;
        for(unsigned i = 0; i < dim; i++)
        {
            (gpgm.posMap[point_num]).push_back(stod(row[i+1]));
            (gpgm.posTolMap[point_num]).push_back(stod(row[i+1+dim]));
        } 

    }

    fin.close();
    return;
}

void readDistFile(const string fileString, gaussian_pgm &gpgm, const char delimiter, const bool discardLineFlag, const bool discardIndexFlag)
{
    // file pointer
    fstream fin;
    // file input handlers
    vector<string> row;
    string line, word;

    // opens an existing csv file or creates a new file.
    fin.open(fileString, ios::in);
    // remove first line with col names if flag set
    if(discardLineFlag) {getline(fin, line);}
    unsigned p1, p2;
    // while there is a next line, read
    while(getline(fin, line))
    {
        row.clear();
        stringstream s(line);
        // break line using delimiter
        while (getline(s, word, delimiter)) 
        {
            // add data to row vector
            row.push_back(word);
        }

        // remove first col with index if flag set
        if(discardIndexFlag) {row.erase(row.begin());}
        // check format for record
        PRLITE_ASSERT(row.size() == 4, "Badly formatted line in " << fileString);
        
        // fill pgm dist and distTol maps
        p1 = (unsigned)stod(row[0]);
        p2 = (unsigned)stod(row[1]);
        gpgm.distMap[ {p1,p2} ] = (unsigned)stod(row[2]);
        gpgm.distTolMap[ {p1,p2} ] = (unsigned)stod(row[3]);
    }

    fin.close();
    return;
}

void initRVs(gaussian_pgm &gpgm)
{
    // step through position map and add RV for every axis to mirrored map
    unsigned RVIndex = 0;
    for(auto point : gpgm.posMap)
    {
        for(unsigned i = 0; i < gpgm.dimMap[point.first]; i++)
        {
            // add incremented RV to RV vector of point
            (gpgm.posRVsMap[point.first]).push_back(RVIndex);

            // check tol to see if observed, if obs add to observed position map
            if(gpgm.posTolMap[point.first][i] < 1E-20)
            {
                gpgm.obsPosMap[RVIndex] = point.second[i];
            }
            RVIndex++;
        }
    }

    for(auto record : gpgm.distMap)
    {   
        unsigned p1 = record.first.first;
        unsigned p2 = record.first.second;
        // Add dist RV to map
        gpgm.distRVsMap[{p1,p2}] = RVIndex;
        // Add pos RVs of point 1 to cluster RVs map
        for(unsigned i = 0; i < gpgm.dimMap[p1]; i++)
        {
            gpgm.clusterRVsMap[{p1,p2}].push_back(gpgm.posRVsMap[p1][i]);
        }
        // Add pos RVs of point 2 to cluster RVs map
        for(unsigned i = 0; i < gpgm.dimMap[p1]; i++)
        {
            gpgm.clusterRVsMap[{p1,p2}].push_back(gpgm.posRVsMap[p2][i]);
        }

        RVIndex++;
    }

    return;

}

void initClusters(gaussian_pgm &gpgm)
{

}