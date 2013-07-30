#ifndef SCHEDULER_CLUSTER_H_
#define SCHEDULER_CLUSTER_H_

/*                                                                            */
/* File Name..........: ~/ucare/scheduler/cluster.h 
 * Author.............: Bjorn Barrefors
 * Institution........: University of Nebraska-Lincoln
 * ...................: Department of Computer Science and Engineering
 * Date Written.......: November 13, 2012
 * Date Last Modified.: April 2, 2013
 * Language...........: C++
 * Purpose............: Represents a set of heterogeneous multiprocessors.
 * Brief Description..: Have 4 cores each. Based on performancecoeffincent alpha.
 */

#include "processor.h"

#include <math.h>

class Cluster {
 public:
  Cluster( ) {
    processors_ = new Processor[num_processors_];
    for( int i=0; i<num_processors_; ++i ) {
      processors_[i].set_a1( a1_[i] );
      processors_[i].set_a2( a2_[i] );
      processors_[i].set_a3( a3_[i] );
      processors_[i].set_a4( a4_[i] );
      processors_[i].set_a5( a5_[i] );
      processors_[i].set_a6( a6_[i] );
      processors_[i].set_performance_coefficient( performance_coefficient_[i] );
      processors_[i].set_r( r_[i] );
      processors_[i].set_utilization( utilization_[i] );
    }
  }

  ~Cluster( ) {
    delete []processors_;
  }

  double MaxTemp( int processor_num, double frequency );

  double Power( int processor_num, double frequency );
  
 private:
  /* Arrays of power model values
   * 1 = c8
   * 2 = c9
   * 3 = c10
   * 4 = c12
   * 5 = c13
   * 6 = c14
   * 7 = c15
   * 8 = c16
   * 9 = c17
   * 10 = c18
   * 11 = c19
   */
  Processor *processors_;
  static const int num_processors_ = 8;
  static const double a1_[];
  static const double a2_[];
  static const double a3_[];
  static const double a4_[];
  static const double a5_[];
  static const double a6_[];
  static const double performance_coefficient_[];
  static const double r_[];
  static const double utilization_[];
};

#endif  /* SCHEDULER_CLUSTER_H_ */
