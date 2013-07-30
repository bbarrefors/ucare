scheduler: driver.o algorithms.o population.o chromosome.o gene.o cluster.o processor.o task_set.o task.o
	g++ -std=c++0x -g driver.o algorithms.o population.o chromosome.o gene.o cluster.o processor.o task_set.o task.o -o scheduler

driver.o: driver.cc algorithms.h
	g++ -std=c++0x -c -g driver.cc

algorithms.o: algorithms.cc algorithms.h task_set.h cluster.h population.h
	g++ -std=c++0x -c -g algorithms.cc

population.o: population.cc population.h chromosome.h task_set.h cluster.h
	g++ -std=c++0x -c -g population.cc

chromosome.o: chromosome.cc chromosome.h gene.h cluster.h task_set.h
	g++ -std=c++0x -c -g chromosome.cc

gene.o: gene.cc gene.h
	g++ -std=c++0x -c -g gene.cc

cluster.o: cluster.cc cluster.h processor.h
	g++ -std=c++0x -c -g cluster.cc

processor.o: processor.cc processor.h
	g++ -std=c++0x -c -g processor.cc

task_set.o: task_set.cc task_set.h task.h
	g++ -std=c++0x -c -g task_set.cc

task.o: task.cc task.h
	g++ -std=c++0x -c -g task.cc