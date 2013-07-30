#ifndef SCHEDULER_PROCESSOR_H_
#define SCHEDULER_PROCESSOR_H_

/*                                                                            */
/* File Name..........: ~/ucare/scheduler/processor.h 
 * Author.............: Bjorn Barrefors
 * Institution........: University of Nebraska-Lincoln
 * ...................: Department of Computer Science and Engineering
 * Date Written.......: April 15, 2013
 * Date Last Modified.: April 15, 2013
 * Language...........: C++
 * Purpose............: Represents a multicore processor.
 * Brief Description..: Have 4 cores.
 */

class Processor {
 public:
  Processor( ) { }

  ~Processor( ) { }

  void set_performance_coefficient( double performance_coefficient ) {
    performance_coefficient_ = performance_coefficient;
  }

  void set_a1( double a1 ) {
    a1_ = a1;
  }
  
  void set_a2( double a2 ) {
    a2_ = a2;
  }

  void set_a3( double a3 ) {
    a3_ = a3;
  }

  void set_a4( double a4 ) {
    a4_ = a4;
  }
  
  void set_a5( double a5 ) {
    a5_ = a5;
  }
  
  void set_a6( double a6 ) {
    a6_ = a6;
  }

  void set_r( double r ) {
    r_ = r;
  }
    
  void set_utilization( double utilization ) {
    utilization_ = utilization;
  }

  double a1( ) const { return a1_; }

  double a2( ) const { return a2_; }
  
  double a3( ) const { return a3_; }
  
  double a4( ) const { return a4_; }
  
  double a5( ) const { return a5_; }
  
  double a6( ) const { return a6_; }

  double performance_coefficient( ) const { return performance_coefficient_; }
  
  double r( ) const { return r_; }
  
  double utilization( ) const { return utilization_; }
  
 private:
  double a1_;
  double a2_;
  double a3_;
  double a4_;
  double a5_;
  double a6_;
  double performance_coefficient_;
  double r_;
  double utilization_;
};

#endif  /* SCHEDULER_PROCESSOR_H_ */
