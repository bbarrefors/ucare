#ifndef SCHEDULER_GENE_H_
#define SCHEDULER_GENE_H_

/*                                                                            */
/* File Name..........: ~/ucare/scheduler/gene.h 
 * Author.............: Bjorn Barrefors
 * Institution........: University of Nebraska-Lincoln
 * ...................: Department of Computer Science and Engineering
 * Date Written.......: April 2, 2013
 * Date Last Modified.: April 15, 2013
 * Language...........: C++
 * Purpose............: Represents one gene in a set of chromosomes.
 * Brief Description..: Each population has a finite number of chromosomes
 *                      Each chromosome has a finite number of genes
 */

class Gene {
 public:
  Gene( ) { }

  ~Gene( ) { }

  void set_processor( int processor ) {
    processor_ = processor;
  }

  void set_frequency( double frequency ) {
    frequency_ = frequency;
  }
  
  int processor( ) const { return processor_; }

  double frequency( ) const { return frequency_; }
  
 private:
  int processor_;
  double frequency_;
};

#endif  /* SCHEDULER_GENE_H_ */
