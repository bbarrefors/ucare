#ifndef SCHEDULER_Task_H_
#define SCHEDULER_Task_H_

/*                                                                            */
/* File Name..........: ~/ucare/scheduler/task.h 
 * Author.............: Bjorn Barrefors
 * Institution........: University of Nebraska-Lincoln
 * ...................: Department of Computer Science and Engineering
 * Date Written.......: October 23, 2012
 * Date Last Modified.: April 15, 2013
 * Language...........: C++
 * Purpose............: Represents a periodic real-time task.
 * Brief Description..: The periodic real-time task has a periodicity and
 * ...................: worst-case execution time.
 */

class Task {
 public:
  Task( ) { }

  ~Task( ) { }

  void set_period( int period ) {
    period_ = period;
    worst_execution_time_ = task_utilization_ * period;
  }
  
  void set_task_utilization( double task_utilization ) {
    task_utilization_ = task_utilization;
  }
  
  void set_worst_execution_time( double worst_execution_time ) {
    worst_execution_time_ = worst_execution_time;
  }

  int period( ) const { return period_; }

  double task_utilization( ) const { return task_utilization_; }
  
  double worst_execution_time( ) const { return worst_execution_time_; }
  
 private:
  int period_;
  double task_utilization_;
  double worst_execution_time_;  /* On core with performance coefficient 1 */
};

#endif  /* SCHEDULER_Task_H_ */
