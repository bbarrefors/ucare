#ifndef SCHEDULER_CHROMOSOME_H_
#define SCHEDULER_CHROMOSOME_H_

/*                                                                            */
/* File Name..........: ~/ucare/scheduler/chromosome.h 
 * Author.............: Bjorn Barrefors
 * Institution........: University of Nebraska-Lincoln
 * ...................: Department of Computer Science and Engineering
 * Date Written.......: April 2, 2013
 * Date Last Modified.: April 15, 2013
 * Language...........: C++
 * Purpose............: Represents a set of genes.
 * Brief Description..: Each population has a finite number of chromosomes
 *                      Each chromosome has a finite number of genes
 */

#include "gene.h"
#include "cluster.h"
#include "task_set.h"

#include <random>
#include <vector>

class Chromosome {
 public:
  Chromosome( ) { }
  
  ~Chromosome( ) {
    std::vector<Gene*>().swap(genes_);
  }

  void Init( int num_tasks ) {
    num_tasks_ = num_tasks;
    fitness_value_ = 0;
    for ( int i=0; i<num_tasks_; ++i ) {
      Gene *tmp_gene = new Gene();
      genes_.push_back( tmp_gene );
      int processor = (rand() % 8) +1;
      genes_[i]->set_processor( processor );
    }
  }
  
  double EChromo( TaskSet *task_set, Cluster *cluster );
  
  double EMax( Cluster *cluster );

  void Mutate( int num_processors, int p1, int p2 );
  
  void set_fitness_value( double fitness_value  ) {
    fitness_value_ = fitness_value;
  }

  double fitness_value( ) const { return fitness_value_; }

  void set_processor( int gene, int processor ) {
    genes_[gene]->set_processor( processor );
  }

  void set_frequency( int gene, int frequency ) {
    genes_[gene]->set_frequency( frequency );
  }

  int get_processor( int gene ) {
    return genes_[gene]->processor( );
  }

  double get_frequency( int gene ) {
    return genes_[gene]->frequency( );
  }

  void Print( ) {
    for (int i=0; i<num_tasks_;++i) {
      printf("Task %d: proc: %d, freq: %f\n", i,  genes_[i]->processor(), genes_[i]->frequency());
    }
  }
  
 private:
  std::vector<Gene*> genes_;
  static const double freq_[];
  static const int kMaxTemp_ = 75;
  static const int kLargeInteger_ = 10000;
  int num_tasks_;
  double fitness_value_;
};

#endif  /* SCHEDULER_CHROMOSOME_H_ */
