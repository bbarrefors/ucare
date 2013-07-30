#ifndef SCHEDULER_TASK_SET_H_
#define SCHEDULER_TASK_SET_H_

/*                                                                            */
/* File Name..........: ~/ucare/scheduler/task_set.h 
 * Author.............: Bjorn Barrefors
 * Institution........: University of Nebraska-Lincoln
 * ...................: Department of Computer Science and Engineering
 * Date Written.......: October 23, 2012
 * Date Last Modified.: April 15, 2013
 * Language...........: C++
 * Purpose............: Represents a set of periodic real-time tasks.
 * Brief Description..: Has a finite number of tasks and a total utilization.
 */

#include "task.h"

#include <random>

class TaskSet {
 public:
  TaskSet( double total_utilization, int num_tasks ) {
    total_utilization_ = total_utilization;
    num_tasks_ = num_tasks;
    tasks_ = new Task[num_tasks_];
  }
  
  ~TaskSet( ) {
    delete []tasks_;
  }
  
  void Generate( );
  
  void set_utilization( int task_num, double utilization ) {
    tasks_[task_num].set_task_utilization( utilization );
  }
  int hyper_period( ) const { return kHyperPeriod_; }
  
  int num_tasks( ) const { return num_tasks_; }
  
  double total_utilization( ) const { return total_utilization_; }
  
  double utilization( int task_num ) const { return tasks_[task_num].task_utilization( ); }
  
 private:
  static const int kHyperPeriod_ = 1000;
  static const int kPeriods_[];
  Task *tasks_;
  int num_tasks_;
  double total_utilization_;
};

#endif  /* SCHEDULER_TASK_SET_H_ */
