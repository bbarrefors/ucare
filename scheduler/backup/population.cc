/*                                                                            */
/* File Name..........: ~/ucare/scheduler/population.cc 
 * Author.............: Bjorn Barrefors
 * Institution........: University of Nebraska-Lincoln
 * ...................: Department of Computer Science and Engineering
 * Date Written.......: April 2, 2013
 * Date Last Modified.: April 2, 2013
 * Language...........: C++
 * Purpose............: Represents a set of chromosomes.
 * Brief Description..: See population.h for further description.
 */

#include "population.h"

double Population::EMax( Cluster *cluster, int chromosome ) {
  return chromosomes_[chromosome]->EMax( cluster );
}

double Population::EChromo( int chromosome, TaskSet *task_set, Cluster *cluster ) {
  return chromosomes_[chromosome]->EChromo( task_set, cluster );
}

void Population::QuickSort( int left, int right ) {
  int i = left, j = right;
  double pivot = chromosomes_[(left + right) / 2]->fitness_value( );
  
  /* partition */
  while (i <= j) {
    while (chromosomes_[i]->fitness_value( ) > pivot)
      ++i;
    while (chromosomes_[j]->fitness_value( ) < pivot)
      --j;
    if (i <= j) {
      for (int k=0;k<num_tasks_;++k) {
	Swap(i, j, k);	
      }
      double tmp_fitness_ = chromosomes_[i]->fitness_value();
      set_fitness_value(i, chromosomes_[j]->fitness_value());
      set_fitness_value(j, tmp_fitness_);
      ++i;
      --j;
    }
  };
  
  /* recursion */
  if (left < j)
    QuickSort( left, j );
  if (i < right)
    QuickSort( i, right );
}
