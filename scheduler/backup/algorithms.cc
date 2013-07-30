
/*                                                                            */
/* File Name..........: ~/ucare/scheduler/algorithms.cc 
 * Author.............: Bjorn Barrefors
 * Institution........: University of Nebraska-Lincoln
 * ...................: Department of Computer Science and Engineering
 * Date Written.......: October 25, 2012
 * Date Last Modified.: Algorithm 2, 2013
 * Language...........: C++
 * Brief Description..: See algorithms.h for description of class and functions.
 */

#include "algorithms.h"

void Algorithms::WorstFit( ) {
  printf( "Worst Fit Algorithm\n" );
  for ( int i=( num_processors_ - 1 ); i>0; --i) {
    
  }
}

void Algorithms::Genetic( ) {
  printf( "Genetic Algorithm\n" );
  
  int generation_ = 1;
  double max_fit_ = 0;
  int conv_ = 1;
  
  while( (generation_ < max_gen_) && (conv_ < max_conv_) ) {
    /* Compute fitness values */
    /*
     * Equation 12.
     * Calculate Emax
     * Is core inactive? -> 0
     * Does it satisfy eq 11? -> power model
     * else high value
     */
    double fitness_value_;
    double e_max_;
    double e_chromo_;
    for ( int i=0; i<population_size_; ++i ) {
      e_max_ = population_->EMax( cluster_, i );
      e_chromo_ = population_->EChromo( i, task_set_, cluster_ );
      fitness_value_ = e_max_ - e_chromo_;
      population_->set_fitness_value( i, fitness_value_ );
    }
    
    population_->Sort();
    
    std::default_random_engine generator_;
    std::uniform_int_distribution<int> crossover_( max_elite_,population_size_ - 1 );
    std::uniform_int_distribution<int> mutation_( 0, num_tasks_ - 1 );
    
    for ( int i=0; i<max_crossover_; ++i ) {
      int cp1_ = max_elite_ + i;
      int cp2_ = crossover_( generator_ );
      int tp1_ = mutation_( generator_ );
      int tp2_ = mutation_( generator_ );
      
      // swap
      if ( tp1_ < tp2_ ) {
	for ( int j=tp1_; j<=tp2_; ++j ) {
	  population_->Swap( cp1_, cp2_, j );
	}
      }
      else {
	for ( int j=tp2_; j<=tp1_; ++j ) {
	  population_->Swap( cp1_, cp2_, j );
	}
      }
    }
    
    for ( int i=max_elite_; i<(max_elite_ + max_mutation_); ++i ) {
      int tp1_ = mutation_( generator_ );
      int tp2_ = mutation_( generator_ );
      if ( tp2_ < tp1_ ) {
	int tmp = tp1_;
	tp1_ = tp2_;
	tp2_ = tmp;
      }
      population_->Mutate( i, num_processors_, tp1_, tp2_ );
    }
    
    double max_fit_tmp_ = population_->MaxFit();
    if (max_fit_tmp_ == max_fit_) {
      ++conv_;
    }
    else {
      conv_ = 1;
      max_fit_ = max_fit_tmp_;
    }
    ++generation_;
  }
  //  population_->Print();
}

void Algorithms::GeneticInit( ) {
  printf( "Genetic Algorithm\n" );
  Genetic( );
}

void Algorithms::HybridWGA( ) {
  printf( "Hybrid Worst-Fit Genetic Algorithm\n" );
  WorstFit( );
  Genetic( );
}

void Algorithms::Print( ) {
  printf( "Print results or something\n" );
}
