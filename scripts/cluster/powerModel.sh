#!/bin/sh

#                                                                              #
# File Name..........: ~/bjorn/collect_data/power_model.sh
# Author.............: Bjorn Barrefors
# Institution........: University of Nebraska-Lincoln
# ...................: Department of Computer Science and Engineering
# Date Written.......: October 2, 2012
# Date Last Modified.: March 24, 2013
# Language...........: Bash Shell Script
# Purpose............: Collect 8 datatpoints of temperature vs. dynamic power 
# ...................: consumption at UIUC's Green Server Farm.
# Brief Description..: Compile and run dummyProgram.cpp that loops infinitely. 
# ...................: Get values for temperature and power consumption.
# ...................: Send data to file power_data.dat.
# ...................: Kill dummy program.
# Improvements.......: Loop over all frequencies

date                                    # Print date and time to prompt
echo "Script starts"                    # Print start to prompt

# Initiate variables
# Create list of frequencies
# Print date and time of data to data file
date >> power_data.dat
echo "Tarek 31" >> power_data.dat
echo -e "Frequency\tTemp\tPower\tUtilization" >> power_data.dat

# Compile dummyProgram.cpp
g++ -o barrefors_dummy dummy_program.cc

timer=8

for freq in 1197000 1330000 1463000 1596000 1729000 1862000 1995000 2128000 2261000 2394000
do
#freq=2128000
# Set frequency
  python bjornAPI.py set_cpu_freq $freq

  timer=`expr $timer + 2`

  sleep 45s

  pidnum=0                                # To keep track of PID's
  count=0
  
    
  while [ $pidnum -lt 6 ]                 # 6 dummy programs
    do
    
    pidnum=`expr $pidnum + 1`               # Increase PID counter
    
    ./barrefors_dummy &                     # Run dummyProgram
    eval pid$pidnum="$!"                    # Get PID of dummyProgram
    
  done

  sleep 2s
  
  while [ $count -lt 12 ]
    do
    
    count=`expr $count + 1`

# Collect data: freq, temp, power
# Collecting from tarekc09 (now)
    freq_tmp=`python bjornAPI.py get_cpu_freq`
    temp_tmp=`python bjornAPI.py get_cpu_temp`
    util_tmp=`python bjornAPI.py get_cpu_util`

    sleep 26s
    power_tmp=`python bjornAPI.py get_self_power`
    
# Print data to data.dat
    echo -e "${freq_tmp}\t\t${temp_tmp}\t${power_tmp}\t${util_tmp}" >> power_data.dat
    
    

    sleep $timer

  done                                    # While loop done  
  while [ $pidnum -gt 0 ]                 # Kill all dummyProgram's
    do
    eval kill -9 '$'pid$pidnum              # kill dummyProgram
    pidnum=`expr $pidnum - 1`               # Decrease PID counter  
  done                                    # While loop done
  
done

echo "Script done"                      # Print to prompt

# Check to make sure all processes of dummyProgram was killed
ps -A | grep barrefors_dummy

rm barrefors_dummy                      # Clean up
exit 0                                  # Exit script
