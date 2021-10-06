#ifndef IOMAPS_HPP
#define IOMAPS_HPP

#include <tuple>
#include <map>
#include <vector>
//#include <pair>
#include <string>

/**
 * @brief Loads two files specifying the space to be mapped. The first
 *        records a prior distribution for where each sample might be
 *        placed. The second records pairs of points and the measured
 *        distances between the points in each pair.
 *
 * @param priorName Name of file containing the prior positions.
 *
 *            File format: Each row consists of 2*D+1 numbers:
 *            unsigned_pntId
 *            D times double_dCoord
 *            D times double_dTol,
 *            all separated with just white space.
 *
 *            pntId is a number uniquely identifying each point. The D
 *            various coord values are the perturbed prior coordinates
 *            (in D-dim space) designating the approximate location of
 *            the sample.
 *
 *            The D tol values are the stdevs indicating how close the
 *            true position is to the reported prior position. A
 *            tol==0 value indicates a known/observed coordinate.
 *
 * @param distName Name of file containing the interpoint distances.
 *
 *           File format: Each row consists of 4 numbers:
 *           unsigned_pnt1,
 *           unsigned_pnt2
 *           double_dist
 *           double_tol, all separated with just
 *           white space.
 *
 *           The two pnt values identifies the two points
 *           concerned.
 *
 *           dist is the measured distance between them, and
 *
 *           tol is a standard deviation indicating the accuracy of
 *           the distance measurement.
 *
 * @param priorMap Key is the number of the point, value is a 2*dim
 *        vector containing dim*coordinates and then stdev of each
 *        coordinate.
 *
 * @param distMap Key is a pair with the two points involved, value is
 *        a pair with the distance and a stdev on that distance.
 *
 * @param perturbPrior If true the prior positions will be perturbed
 *        with gaussian noise matching the stdev specified in
 *        priorMap.
 *
 * @param perturbDist If true the distances will be perturbed with
 *        gaussian noise matching the stdev specified in distMap.
 */
void
saveToFile(const std::string& priorName,
           const std::string& distName,
           const std::map< unsigned, std::vector<double> >& priorMap,
           const std::map< std::pair<unsigned, unsigned>, std::pair<double,double> >& distMap,
           bool perturbPrior = false,
           bool perturbDist = false);

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
std::tuple<unsigned, std::map< unsigned, std::vector<double> >, std::map< std::pair<unsigned, unsigned>, std::pair<double,double> > >
loadFromFile(const std::string& priorName,
             const std::string& distName);



#endif
