/*
 * Author     :  (DSP Group, E&E Eng, US)
 * Created on :
 * Copyright  : University of Stellenbosch, all rights retained
 */

// standard headers
#include <iostream>  // cout, endl, flush, cin, cerr
#include <string>  // string, stod
#include <cmath>   // sqrt, abs


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
    double prev_change = 0;
    unsigned iter = 0;
    
    map< unsigned, unsigned> dimMap; // map <point_num, dim>
    map< unsigned, vector<double> > posMap; // map <point_num, vector<x_pos, y_pos, ...>>
    map< unsigned, vector<double> > posTolMap; // map <point_num, vector<x_tol, y_tol, ...>>
    map< unsigned, vector<double> > posMap_old; // map <point_num, vector<x_pos, y_pos, ...>> used for convergence

    map< pair<unsigned, unsigned>, double> distMap; // map <pair<point_num1, point_num2>, dist>
    map< pair<unsigned, unsigned>, double> distTolMap; // map <pair<point_num1, point_num2>, dist_tol>

    map< unsigned, RVIds> posRVsMap; // map <point_num, RVIds>
    map< pair<unsigned,unsigned>, RVIds> clusterRVsMap; // map <pair<point_num1, point_num2>, RVIds>
    map< RVIdType, double > obsMap; // map <obs_pos_rv, obs_value>
    RVIds obsVars; // repackaged observed vars
    RVVals obsVals; // repackaged observed vals
    map< pair<unsigned,unsigned>, RVIdType> distRVsMap; // map <pair<point_num1, point_num2>, RVId>

    map< pair<unsigned,unsigned>, rcptr<Factor> > clusters; // combined factor that corresponds to single dist record
    rcptr<Factor> joint_factor; // full joint factor
};

void readPosFile(const string fileString, gaussian_pgm &gpgm, const char delimiter=',', const bool discardLineFlag=true, const bool discardIndexFlag=true);
void readDistFile(const string fileString, gaussian_pgm &gpgm, const char delimiter=',', const bool discardLineFlag=true, const bool discardIndexFlag=true);

void initRVs(gaussian_pgm &gpgm);
void repackageObs(gaussian_pgm &gpgm);
void initClusters(gaussian_pgm &gpgm);
void reconstructFromSigmaPoints(gaussian_pgm &gpgm);
void updateClusters(gaussian_pgm &gpgm);
void updatePositions(gaussian_pgm &gpgm);

double getDist(const pair<vector<double>, vector<double>> pointsPair);
double getPosChange(gaussian_pgm &gpgm);

template<typename TK, typename TV> std::vector<TK> extract_keys(std::map<TK, TV> const& input_map);
template<typename TK, typename TV> std::vector<TV> extract_values(std::map<TK, TV> const& input_map);

int main(int, char *argv[])
{
    //string dataString = "../../cube_gen/Data/dists.csv";
    string posDdataString = "../Data/initpos10.csv";
    //string distDataString = "../Data/dists1.csv";
    string distDataString = "../Data/dists_inter_5_noise_1%.csv";
    //string resultString = "../result.csv";
    double lambda = 0.999;
    double tolerance = 10;
    unsigned iter = 25;

    gaussian_pgm pgm1;

    pgm1.lambda = lambda;
    readPosFile(posDdataString, pgm1, ' ', false, false);
    //readDistFile(distDataString, pgm1, ' ', false, false);
    readDistFile(distDataString, pgm1, ',');
    initRVs(pgm1);
    
    do{
    cout << "iter: "<< pgm1.iter << endl;
    pgm1.prev_change = getPosChange(pgm1);
    initClusters(pgm1);
    reconstructFromSigmaPoints(pgm1);
    updateClusters(pgm1);
    updatePositions(pgm1);
    cout << "change: " << getPosChange(pgm1) << endl;
    cout << "change dif: " << abs(pgm1.prev_change - getPosChange(pgm1)) << endl;
    pgm1.iter++;
    } while((abs(pgm1.prev_change - getPosChange(pgm1)) > tolerance)&&(pgm1.iter < iter));

    for(auto point : pgm1.posMap)
    {   
        //rcptr<SqrtMVG> mvgFactor = dynamic_pointer_cast<SqrtMVG>(cluster.second);
        //cout << mvgFactor->getMean() << endl;
        cout << point.second << endl;
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
    gpgm.posMap_old = gpgm.posMap;

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

// TODO: check implicit observation of lower dimensional points eg. if 2d point is given in 3d set, third dim is observed to be 0
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
                gpgm.obsMap[RVIndex] = point.second[i];
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
        // Add distance observation to map
        gpgm.obsMap[RVIndex] = record.second;
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

    repackageObs(gpgm);
    return;

}

void repackageObs(gaussian_pgm &gpgm)
{
    gpgm.obsVars.clear();
    gpgm.obsVals.clear();
    for (auto el : gpgm.obsMap) 
    {
        gpgm.obsVars.push_back(el.first);
        gpgm.obsVals.push_back(el.second);
    } // for

    return;
}

void initClusters(gaussian_pgm &gpgm)
{
    // step through points and create vector of factors for each point
    map< unsigned, rcptr<Factor> > priorFactors;

    for(auto point : gpgm.posMap)
    {
        // create 1D factor if unobserved
        vector< rcptr<Factor> > scalarFactors;
        prlite::ColVector<double> mn1D(1);
        prlite::RowMatrix<double> cv1D(1,1);
        unsigned point_num = point.first;

        for(unsigned i = 0; i < gpgm.dimMap[point_num]; i++)
        {   
            // check if observed
            if(gpgm.posTolMap[point_num][i] > 1E-20)
            {
                mn1D[0] = point.second[i];
                cv1D(0,0) = gpgm.posTolMap[point_num][i];
                scalarFactors.push_back( uniqptr<SqrtMVG> ( new SqrtMVG({gpgm.posRVsMap[point_num][i]}, mn1D, cv1D) ) );        
            }
        }
        // check if scalarFactors empty and collapse if not
        if(scalarFactors.size() > 0)
        {
            priorFactors[point_num] = absorb(scalarFactors)->normalize();
        }
        else
        {   
            // factor is observed, assign nullptr
            priorFactors[point_num] = nullptr;
        }
    }

    // step through cluster prototypes and build clusters
    for(auto cluster : gpgm.clusterRVsMap)
    {
        unsigned p1 = cluster.first.first;
        unsigned p2 = cluster.first.second;

        if(priorFactors[p1] == nullptr)
        {
            if (priorFactors[p2] == nullptr) 
            {
            cerr << __FILE__ << __LINE__ << " unexpected distance between two fully observed points "
                 << p1 << " and " << p2 << endl;
            cerr << "Rather just remove this distance, it does not contribute anything!\n";
            exit(-1);
            } // if
            gpgm.clusters[{p1,p2}] = priorFactors[p2];
        }
        else if(priorFactors[p2] == nullptr)
        {
            gpgm.clusters[{p1,p2}] = priorFactors[p1];
        }
        else
        {
            gpgm.clusters[{p1,p2}] = priorFactors[p1]->absorb(priorFactors[p2])->normalize();
        }
    }

    return;
}

void reconstructFromSigmaPoints(gaussian_pgm &gpgm)
{
    prlite::ColMatrix<double> sigmaPoints;
    prlite::ColMatrix<double> sigmaDists;
    prlite::ColMatrix<double> distNoise(1,1);
    vector<rcptr<Factor>> factors; // TODO:add result factors to jointfactor in struct one by one in loop below?

    for(auto cluster : gpgm.clusters)
    {
        unsigned p1 = cluster.first.first;
        unsigned p2 = cluster.first.second;

        RVIds clusterRVs = gpgm.clusterRVsMap[{p1,p2}];
        
        rcptr<SqrtMVG>mvgFactor = std::dynamic_pointer_cast<SqrtMVG>(cluster.second);  // get the factor
        sigmaPoints = mvgFactor->getSigmaPoints();  
        sigmaDists.resize(1, sigmaPoints.cols());

        // step through cols and add dist to sigmadists
        for(unsigned col = 0; col < (unsigned)sigmaPoints.cols(); col++)
        {
            pair<vector<double>, vector<double>>  sigmaPosValuesPair;

            unsigned RVIndex = 0;
            unsigned unobsCount = 0;
            // step through first point dimensions
            for(unsigned i = 0; i < gpgm.dimMap[p1]; i++)
            {
                auto itr = gpgm.obsMap.find(clusterRVs[RVIndex]);
                if(itr != gpgm.obsMap.end())
                {
                    // RV observed, use observed value
                    sigmaPosValuesPair.first.push_back(double(itr->second)); // for observed RVs, use its value directly
                }
                else
                {
                    // RV unobserved, use sigmapoint value
                    sigmaPosValuesPair.first.push_back(sigmaPoints(unobsCount,col));
                    unobsCount++;
                }
                RVIndex++;
            }
            // step through second point dimensions
            for(unsigned i = 0; i < gpgm.dimMap[p2]; i++)
            {
                auto itr = gpgm.obsMap.find(clusterRVs[RVIndex]);
                if(itr != gpgm.obsMap.end())
                {
                    // RV observed, use observed value
                    sigmaPosValuesPair.second.push_back(double(itr->second)); // for observed RVs, use its value directly
                }
                else
                {
                    // RV unobserved, use sigmapoint value
                    sigmaPosValuesPair.second.push_back(sigmaPoints(unobsCount,col));
                    unobsCount++;
                }
                RVIndex++;
            }
            // get distance from sigma and oberved points
            sigmaDists(0, col) = getDist(sigmaPosValuesPair);
        } // end sigmapoints for

        distNoise(0,0) = gpgm.distTolMap[{p1,p2}];
        mvgFactor = uniqptr<SqrtMVG>(
                    SqrtMVG::constructFromSigmaPoints(
                        cluster.second->getVars(), sigmaPoints,
                        {gpgm.distRVsMap[{p1,p2}]},
                        sigmaDists, distNoise) );
        // and observe the distance value
        factors.push_back( mvgFactor->Factor::observeAndReduce(gpgm.obsVars, gpgm.obsVals)->normalize() );

    }

    gpgm.joint_factor = absorb(factors)->normalize();
    return;
}

void updateClusters(gaussian_pgm &gpgm)
{
    for(auto& cluster : gpgm.clusters)
    {
        cluster.second = gpgm.joint_factor->marginalize(cluster.second->getVars())->normalize();
    }
    return;
}

// TODO: change to lambda damping
void updatePositions(gaussian_pgm &gpgm)
{
    rcptr<Factor> query;
    rcptr<SqrtMVG> mvgQuery;
    for(auto& point : gpgm.posMap)
    {   
        // step through point dimensions
        for(unsigned i = 0; i < gpgm.dimMap[point.first]; i++)
        {
            // find RV of current dim of point
            RVIdType posRV = gpgm.posRVsMap[point.first][i];
            // check if observed
            auto itr = gpgm.obsMap.find(posRV);
            if(itr != gpgm.obsMap.end())
            {   
                // point dim observed, use observed value
                // update old_pos of dim
                gpgm.posMap_old[point.first][i] = point.second[i];
                // update pos of dim
                point.second[i] = double(itr->second);
                // update tol of dim
                gpgm.posTolMap[point.first][i] = 0;
            }
            else
            {
                // point dim unobserved, query joint
                query = gpgm.joint_factor->marginalize({posRV})->normalize();
                mvgQuery = std::dynamic_pointer_cast<SqrtMVG>(query);
                // update old_pos of dim
                gpgm.posMap_old[point.first][i] = point.second[i];
                // update pos of dim
                point.second[i] = mvgQuery->getMean()[0];
                // update tol of dim
                gpgm.posTolMap[point.first][i] = std::max( gpgm.posTolMap[point.first][i]*gpgm.lambda, sqrt( mvgQuery->getCov()(0,0) ) );
            }
        }
    }

    return;
}
// get distance between two points of arbitrary dimension
double getDist(const pair<vector<double>, vector<double>> pointsPair)
{
    
    // get max dimension
    unsigned maxDim = max(pointsPair.first.size(), pointsPair.second.size());
    
    // step through max dimensions
    double square_sum = 0;
    double val1, val2, dif;
    for(unsigned i = 0; i < maxDim; i++)
    {
        val1 = 0;
        val2 = 0;
        // if current dim defined for point, use value (will be 0 otherwise)
        if(i < pointsPair.first.size()) val1 = pointsPair.first[i];
        if(i < pointsPair.second.size()) val2 = pointsPair.second[i];
        // calc difference
        dif = val1 - val2;
        // add square to running sum
        square_sum = square_sum + dif*dif;
    }

    return sqrt(square_sum);
}

double getPosChange(gaussian_pgm &gpgm)
{
    double totalChange = 0;
    double dif = 0;
    for(auto point : gpgm.posMap)
    {
        for(unsigned i = 0; i < gpgm.dimMap[point.first]; i++)
        {
            dif = abs(point.second[i] - gpgm.posMap_old[point.first][i]);
            totalChange = totalChange + dif;
        }
    }
    return totalChange;
}

// TODO: check if used
// source: https://www.lonecpluspluscoder.com/2015/08/13/an-elegant-way-to-extract-keys-from-a-c-map/
template<typename TK, typename TV> std::vector<TK> extract_keys(std::map<TK, TV> const& input_map) 
{
  std::vector<TK> retval;
  for (auto const& element : input_map) {
    retval.push_back(element.first);
  }
  return retval;
}

template<typename TK, typename TV> std::vector<TV> extract_values(std::map<TK, TV> const& input_map) 
{
  std::vector<TV> retval;
  for (auto const& element : input_map) {
    retval.push_back(element.second);
  }
  return retval;
}