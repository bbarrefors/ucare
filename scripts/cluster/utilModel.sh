#!/bin/sh

#                                                                              #
# File Name..........: ~/scripts/thermal_model.sh
# Author.............: Bjorn Barrefors
# Institution........: University of Nebraska-Lincoln
# ...................: Department of Computer Science and Engineering
# Date Written.......: January 28, 2013
# Date Last Modified.: January 28, 2013
# Language...........: Bash Shell Script
# Purpose............: Collect 8 datatpoints of temp vs power vs intake temp
# ...................: consumption at UIUC's Green Server Farm.
# Brief Description..: Compile and run dummyProgram.cpp that loops infinitely. 
# ...................: Get values for temperature and power consumption.
# ...................: Send data to file thermal_data.dat.
# ...................: Kill dummy program.
# Improvements.......: 

date                                    # Print date and time to prompt
echo "Script starts"                    # Print start to prompt

# Initiate variables
# Create list of frequencies
# Print date and time of data to data file
date > utilData.dat
echo "Tarek 33" >> utilData.dat
# Print headers for data to data file
echo -e "Util\tPower" >> utilData.dat

# Set frequency
freq=1197000
python bjornAPI.py set_cpu_freq $freq

pidnum=0                                # To keep track of PID's

# Compile dummyProgram.cpp
g++ -o barrefors_dummy dummy_program.cc

util_tmp=`python bjornAPI.py get_cpu_util`
power_tmp=`python bjornAPI.py get_self_power`
echo -e "${util_tmp}\t${power_tmp}" >> utilData.dat
echo -e "${util_tmp}\t${power_tmp}"

while [ $pidnum -lt 4 ]                 # 4 dummy programs
do
    
    pidnum=`expr $pidnum + 1`               # Increase PID counter
    
    ./barrefors_dummy &                     # Run dummyProgram
    eval pid$pidnum="$!"                    # Get PID of dummyProgram

    sleep 45s
    
    util_tmp=`python bjornAPI.py get_cpu_util`
    power_tmp=`python bjornAPI.py get_self_power`
    echo -e "${util_tmp}\t${power_tmp}" >> utilData.dat
    echo -e "${util_tmp}\t${power_tmp}"    
done

while [ $pidnum -gt 0 ]                 # Kill all dummyProgram's
do
    
    eval kill -9 '$'pid$pidnum              # kill dummyProgram
    pidnum=`expr $pidnum - 1`               # Decrease PID counter
    
done                                    # While loop done

echo "Script done"                      # Print to prompt

# Check to make sure all processes of dummyProgram was killed
ps -A | grep barrefors_dummy

rm barrefors_dummy                      # Clean up
exit 0                                  # Exit script
