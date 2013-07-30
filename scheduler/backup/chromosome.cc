/*                                                                            */
/* File Name..........: ~/ucare/scheduler/chromosome.cc 
 * Author.............: Bjorn Barrefors
 * Institution........: University of Nebraska-Lincoln
 * ...................: Department of Computer Science and Engineering
 * Date Written.......: April 2, 2013
 * Date Last Modified.: April 2, 2013
 * Language...........: C++
 * Purpose............: Represents a set of genes.
 * Brief Description..: See chromosome.h for further description.
 */

#include "chromosome.h"

const double Chromosome::freq_[] = { 2.395000, 2.394000, 2.261000, 2.128000, 1.995000, 1.862000, 1.729000, 1.596000, 1.463000, 1.330000, 1.197000 };

void Chromosome::Mutate( int num_processors, int p1, int p2 ) {
  for ( int i=p1; i<=p2; ++i ) {
    genes_[i]->set_processor( ( rand( ) % num_processors + 1 ) );
  }
}

double Chromosome::EMax( Cluster *cluster ) {
  double e_max_ = 0;
  double power_;
  for ( int i=0; i<num_tasks_; ++i ) {
    power_ = cluster->Power( genes_[i]->processor( ), freq_[0] );
    e_max_ = e_max_ + power_;
  }
  
  return e_max_;
}

double Chromosome::EChromo( TaskSet *task_set, Cluster *cluster ) {
  double e_chromo_ = 0;
  double power_;
  for ( int i=0; i<num_tasks_; ++i ) {
    int j = 10;
    double utilization_ = task_set->utilization( i );
    while ( j >= 0 ) {
      double f = freq_[j] / freq_[0];
      if ( f >= utilization_ ) {
	if ( kMaxTemp_ >= cluster->MaxTemp( genes_[i]->processor( ), freq_[j] ) ) {
	  power_ = cluster->Power( genes_[i]->processor( ), freq_[j] );
	  e_chromo_ = e_chromo_ + power_;
	  j = -1;
	  genes_[i]->set_frequency( freq_[j] );
	}
	else {
	  j = 0;
	}
      }
      --j;
    }
    if ( j == -1 ) {
      power_ = kLargeInteger_ * freq_[0];
      e_chromo_ = e_chromo_ + power_;
    }
  }

  return e_chromo_;
}
