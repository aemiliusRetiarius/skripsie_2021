#include "iomaps.hpp"

#include <iomanip>
#include <fstream>
#include <random>

#include "prlite_testing.hpp"
#include "emdw.hpp"

using namespace std;

/**
 * @brief Loads two files specifying the space to be mapped. The first
 *        records a prior distribution for where each sample might be
 *        placed. The second records pairs of points and the measured
 *        distances between the points in each pair.
 *
 * @param priorName Name of file containing the prior
 *        positions. Format: Each row consists of 2*D+1 numbers:
 *        unsigned_pntId D times double_dCoord D times double_dTol,
 *        all separated with just white space. pntId is a number
 *        uniquely identifying each point. The D various coord values
 *        are the perturbed prior coordinates (in D-dim space)
 *        designating the approximate location of the sample. The D
 *        tol values are the stdevs indicating how close the true
 *        position is to the reported prior position. A tol==0 value
 *        indicates a known/observed coordinate.
 *
 * @param distName Name of file containing the interpoint
 *        distances. Format: Each row consists of 4 numbers:
 *        unsigned_pnt1 unsigned_pnt2 double_dist double_tol, all
 *        separated by white space. The two pnt values identifies the
 *        two points concerned. dist is the measured distance between
 *        them, and tol is a standard deviation indicating the
 *        accuracy of the distance measurement.
 *
 * @return A tuple of 3 values. The first is the dimension of the
 *         space, the second is a map of the prior positions and the
 *         third is a map containing the distances between selected
 *         points.
 */
tuple<unsigned, map< unsigned, vector<double> >, map< pair<unsigned, unsigned>, pair<double,double> > >
loadFromFile(const string& priorName, const string& distName) {

  ifstream priorFile(priorName);

  // lets first figure out the dim
  string theLine;
  getline(priorFile, theLine);
  PRLITE_ASSERT(priorFile, "empty file " << priorName);
  unsigned dim;
  stringstream ss1(theLine);
  unsigned cnt = 0;
  double val;
  while (ss1) {
    ss1 >> val;
    if (!ss1) break;
    cnt++;
  } // while
  dim = (cnt-1)/2;
  PRLITE_ASSERT(dim*2+1 == cnt, "Badly formatted first line in " << priorName);
  //cout << "Dim is " << dim << endl;
  // reset to beginning
  priorFile.clear();
  priorFile.seekg(0, ios::beg);

  map< unsigned, vector<double> > priorMap;
  vector<double> readVec(dim*2);
  unsigned id;
  while (priorFile) { // get and check the file format

    priorFile >> id;
    if (!priorFile) break;

    for (unsigned n = 0; n < 2*dim; n++) {
      priorFile >> readVec[n];
    } // for
    //if (id == 59) continue;  // skip point 59
    priorMap[id] = readVec;
  } // while
  priorFile.close();

  ifstream distFile(distName);  // idx1 idx2 dist tol
  theLine.clear();
  getline(distFile, theLine);
  PRLITE_ASSERT(distFile, "empty file " << distName);
  stringstream ss2(theLine);
  cnt = 0;
  while (ss2)  {
    ss2 >> val;
    if (!ss2) break;
    cnt++;
  } // while
  PRLITE_ASSERT(cnt == 4, "Badly formatted first line in " << distName);
  // reset to beginning
  distFile.clear();
  distFile.seekg(0, ios::beg);

  ofstream diagnosticsFile("diagnostics.txt");
  map<unsigned,unsigned> distCounts;
  for (auto el : priorMap) { distCounts[el.first] = 0; } // for

  map< pair<unsigned, unsigned>, pair<double,double> >  distMap;
  unsigned p1, p2; double d, tol;
  while (distFile) { // get and check the file format

    distFile >> p1 >> p2 >> d >> tol;
    if (!distFile) break;
    //if (p1 == 59 or p2 == 59) continue;  // skip point 59

    distCounts[p1]++; distCounts[p2]++;
    auto findPnt = priorMap.find(p1);
    if ( findPnt == priorMap.end() ) {
      diagnosticsFile << "Point " << p1 << " has no prior!\n";
    } // if
    findPnt = priorMap.find(p2);
    if ( findPnt == priorMap.end() ) {
      diagnosticsFile << "Point " << p2 << " has no prior!\n";
    } // if

    p1 < p2 ? distMap[{p1,p2}] = {d,tol} : distMap[{p2,p1}] = {d,tol};
  } // while
  distFile.close();

  for (auto el : distCounts) {
    diagnosticsFile << el.first << " linked_to: " << el.second << endl;
  } // for
  diagnosticsFile.close();

  return {dim, priorMap, distMap};
} // loadFromFile

void
saveToFile(const string& priorName,
           const string& distName,
           const map< unsigned, vector<double> >& priorMap,
           const map< pair<unsigned, unsigned>, pair<double,double> >& distMap,
           bool perturbPrior,
           bool perturbDist) {

  ofstream priorFile(priorName);
  unsigned dim = priorMap.begin()->second.size() /2;
  cout << "dim is: " << dim << endl;
  for (auto el : priorMap) {

    priorFile << setw(3) << el.first << " ";

    // when writing out the position file we hide the true positions
    // with some gaussian noise.
    vector<double> perturbed(2*dim);
    for (unsigned d = 0; d < dim; d++) {
      double mn = el.second[d];
      double stdev = el.second[d+dim] > 0.0 ? max(0.05,el.second[d+dim]) : 0.0; //el.second[d+dim];
      if  (perturbPrior) {
        normal_distribution<> gen(mn, stdev); // mn, stddev
        perturbed[d] = gen( emdw::randomEngine() );
      } // if
      else {perturbed[d] = mn;} // else
      perturbed[d+dim] = stdev;
    } // for

    for (auto val : perturbed) {
      priorFile << setw(12) << val << " ";
    } // for val
    priorFile << endl;
  } // for el
  priorFile.close();

  ofstream distFile(distName);
  for (auto el : distMap) {
    double dist = el.second.first;
    if (perturbDist) {
      normal_distribution<> gen(dist, el.second.second); // mn, stddev
        dist = gen( emdw::randomEngine() );
    } // if

    distFile << setw(3) << el.first.first << " "
             << setw(3) << el.first.second << " "
             << setw(12) << dist << " "
             << setw(12) << el.second.second
             << endl;
  } // for el
  distFile.close();

} // saveToFile
