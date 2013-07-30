/*                                                                            */
/* File Name..........: ~/ucare/scheduler/cluster.cc 
 * Author.............: Bjorn Barrefors
 * Institution........: University of Nebraska-Lincoln
 * ...................: Department of Computer Science and Engineering
 * Date Written.......: November 13, 2012
 * Date Last Modified.: November 13, 2012
 * Language...........: C++
 * Brief Description..: See cluster.h for description.
 */

#include "cluster.h"

static const double kTAmb_ = 19.0;
const double Cluster::a1_[] = { -0.0045, 0.0089, 0.0706, 0.0044, 0.0022, 0.005, 0.01, 0.009 };
const double Cluster::a2_[] = { 5.2247, 12.2247, -10.6878, 11.8318, 7.7355, 10, 8, 2 };
const double Cluster::a3_[] = { 0.1755, -0.5667, 0.4917, 0.1674, 0.1922, 0.2, 0.5, 0.3 };
const double Cluster::a4_[] = { 0.3443, 0.6636, -6.5898, -0.5238, -0.3371, 0.2, -0.1, -0.5 };
const double Cluster::a5_[] = { -8.9638, -2.5894, 37.6126, -23.6464, -12.6605, -10, -5, -12 };
const double Cluster::a6_[] = { 53.7163, 38.7100, 155.3745, 28.0051, 63.7239, 50, 45, 60 };
const double Cluster::performance_coefficient_[] = { 1, 1, 1, 1, 1, 1, 1, 1 };
const double Cluster::r_[] = { 0.3685, 0.36, 0.37, 0.36, 0.37, 0.36, 0.37, 0.36 };
const double Cluster::utilization_[] = { 4, 4, 4, 4, 4, 4, 4, 4 };

double Cluster::MaxTemp( int processor_num, double frequency ) {
  /* Equation for MAX temperature
   * T_max = -(R*a3*f + R*a4 - 1) +/- sqrt( ( R*a3*f + R*a4 - 1 ) - 4*R*a1*( a2*f^2 + a5*f + a6 + T_amb ) ) / ( 2*R*a1 )
   */
  int i = processor_num;
  double f = frequency;
  // Sign before sqrt not sure if + or - yet
  double max_temp_ = ((a1_[i]*f-a4_[i]-1/r_[i])/(2*a1_[i]) + sqrt((a3_[i]*f-a4_[i]-1/r_[i])/(2*a1_[i]) - (a2_[i]*f*f + kTamb_/r_[i] - a5_[i]*f + a6_[i])));
  return max_temp_;
}

double Cluster::Power ( int processor_num, double frequency ) {
  /* Equation for power consumption
   * P = a1*T^2 + a2*f^2 + a3*fT + a4*T + a5*f + a6
   */
  double T = MaxTemp( processor_num, frequency );
  double f = frequency;
  int i = processor_num;
  double power_ = a1_[i]*pow( T, 2 ) + a2_[i]*pow( f, 2 ) + a3_[i]*f*T + a4_[i]*T + a5_[i]*f + a6_[i];
  return power_;
}
