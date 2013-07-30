/*                                                                            */
/* File Name..........: ~/ucare/scheduler/driver.cc 
 * Author.............: Bjorn Barrefors
 * Institution........: University of Nebraska-Lincoln
 * ...................: Department of Computer Science and Engineering
 * Date Written.......: October 25, 2012
 * Date Last Modified.: November 12, 2012
 * Language...........: C++
 * Brief Description..: the main driver for testing schedulers.
 */

#include "algorithms.h"

int main( int argc, char *argv[] ) {
  int num_tasks_[4] = { 100, 150, 200, 300 };
  double total_utilization_[3] = { 20, 35, 45 };
  int population_size_[2] = { 2000, 10000 };
  
  for ( int i = 0; i<4; ++i ) {
    for ( int j = 0; j<3; ++j ) {
      for ( int k = 0; k<2; ++k ) {
	printf( "Task set %d / %f / %d\n", num_tasks_[i], total_utilization_[j], population_size_[k] );
	Algorithms *algorithm_ = new Algorithms( total_utilization_[j], num_tasks_[i], population_size_[k] );
	algorithm_->Genetic( );
	delete algorithm_;
	printf( "Next population size\n" );
      }
      printf( "Next total utilization\n" );
    }
    printf( "Next task set\n" );
  }
  printf( "Done\n" );
  return 0;
}
