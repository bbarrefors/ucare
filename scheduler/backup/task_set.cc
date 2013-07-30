/*                                                                            */
/* File Name..........: ~/ucare/scheduler/task_set.cc 
 * Author.............: Bjorn Barrefors
 * Institution........: University of Nebraska-Lincoln
 * ...................: Department of Computer Science and Engineering
 * Date Written.......: October 25, 2012
 * Date Last Modified.: April 15, 2013
 * Language...........: C++
 * Brief Description..: See task_set.h for description of class and functions.
 */

#include "task_set.h"

const int TaskSet::kPeriods_[] = { 1, 2, 4, 8, 10, 20, 25, 40, 50, 100, 125 };

void TaskSet::Generate( ) {
  double mean_utilization_ = this->total_utilization( ) / this->num_tasks( );
  std::default_random_engine generator_;
  std::normal_distribution<double> utilization_distribution_( mean_utilization_, 0.03 );
  std::uniform_int_distribution<int> period_distribution_( 0,10 );
  double tot_util = 0;
  
  for ( int i=0; i<num_tasks( ); ++i ) {
    /* Task utilization always has to be in the (0,1] range */
    double task_utilization_ = utilization_distribution_( generator_ );
    while ( ! ( ( task_utilization_>0.0 ) && ( task_utilization_<=1.0 ) ) ) {
      task_utilization_ = utilization_distribution_( generator_ );
    }
    tasks_[i].set_task_utilization( task_utilization_ );
    tasks_[i].set_period( this->kPeriods_[period_distribution_( generator_ )] );
    tot_util = tot_util + task_utilization_;
    printf("Task util: %f, period: %d\n", tasks_[i].task_utilization(), tasks_[i].period());
  }
  printf("Total util: %f\n", tot_util);
}
