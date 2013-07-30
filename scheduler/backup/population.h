#ifndef SCHEDULER_POPULATION_H_
#define SCHEDULER_POPULATION_H_

/*                                                                            */
/* File Name..........: ~/ucare/scheduler/population.h 
 * Author.............: Bjorn Barrefors
 * Institution........: University of Nebraska-Lincoln
 * ...................: Department of Computer Science and Engineering
 * Date Written.......: March 7, 2013
 * Date Last Modified.: April 15, 2013
 * Language...........: C++
 * Purpose............: Represents a set of chromosomes.
 * Brief Description..: Each population has a finite number of chromosomes
 *                      Each chromosome has a finite number of genes
 */

#include "chromosome.h"
#include "task_set.h"
#include "cluster.h"

#include <vector>

class Population {
 public:
  Population( int population_size, int num_tasks ) {
    population_size_ = population_size;
    num_tasks_ = num_tasks;
    printf("Testing");
    for ( int i=0; i < population_size_; ++i ) {
      Chromosome *tmp_chrom = new Chromosome();
      chromosomes_.push_back( tmp_chrom );
      chromosomes_[i]->Init( num_tasks_ );
    }
  }

  ~Population( ) {
    std::vector<Chromosome*>().swap(chromosomes_);
  }

  void Mutate( int chromosome, int num_processors, int p1, int p2 ) {
    chromosomes_[chromosome]->Mutate( num_processors, p1, p2 );
  }
  
  double EMax( Cluster *cluster_, int chromosome );

  double EChromo( int chromosome, TaskSet *task_set, Cluster *cluster );

  void Sort( ) {
    QuickSort( 0, num_tasks_ - 1 );
  }
  
  void QuickSort( int left, int right );
  
  double MaxFit( ) {
    return chromosomes_[0]->fitness_value( );
  }

  int get_processor( int chromosome, int gene ) {
    return chromosomes_[chromosome]->get_processor( gene );
  }
  
  void set_processor( int chromosome, int gene, int processor ) {
    chromosomes_[chromosome]->set_processor( gene, processor );
  }

  double get_frequency( int chromosome, int gene ) {
    return chromosomes_[chromosome]->get_frequency( gene );
  }
  
  void set_frequency( int chromosome, int gene, double frequency ) {
    chromosomes_[chromosome]->set_frequency( gene, frequency );
  }
  
  void set_fitness_value( int chromosome, double fitness_value ) {
    chromosomes_[chromosome]->set_fitness_value( fitness_value );
  }

  void Swap( int c1, int c2, int gene ) {
    double tmp_freq_ = get_frequency( c1, gene );
    int tmp_processor_ = get_processor( c1, gene );
    set_processor( c1, gene, get_processor( c2, gene ) );
    set_frequency( c1, gene, get_frequency( c2, gene ) );
    set_processor( c2, gene, tmp_processor_ );
    set_frequency( c2, gene, tmp_freq_ );
  }

  void Print( ) {
    chromosomes_[0]->Print();
  }
  
 private:
  std::vector<Chromosome*> chromosomes_;
  int num_tasks_;
  int population_size_;
};

#endif  /* SCHEDULER_POPULATION_H_ */
