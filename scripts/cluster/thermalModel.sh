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
date >> thermal_data.dat
echo "Tarek 33" >> thermal_data.dat
# Print headers for data to data file
echo -e "Frequency\tTemp\tPower\tIn_Temp" >> thermal_data.dat

#freq_list=(2394000 2261000 2128000 1995000 1862000 1729000 1596000 1463000 1330000 1197000)

#for $freq in $freq_list
#do
freq=2394000

# Set frequency
python bjornAPI.py set_cpu_freq $freq

pidnum=0                                # To keep track of PID's
count=0

# Compile dummyProgram.cpp
g++ -o barrefors_dummy dummy_program.cc

while [ $pidnum -lt 4 ]                 # 5 dummy programs
do

pidnum=`expr $pidnum + 1`               # Increase PID counter

./barrefors_dummy &                     # Run dummyProgram
eval pid$pidnum="$!"                    # Get PID of dummyProgram

done

sleep 30s

while [ $count -lt 8 ]
do

#count=`expr $count + 1`

# Collect data: freq, temp, power
# Collecting from tarekc08 (now)
freq_tmp=$freq
temp_tmp=`python bjornAPI.py get_cpu_temp`
in_tmp=`python bjornAPI.py get_crac_in_temp`
sleep 25s
power_tmp=`python bjornAPI.py get_self_power`

# Print data to data.dat
echo -e "${freq_tmp}\t\t${temp_tmp}\t${power_tmp}\t${in_tmp}" >> thermal_data.dat

echo -e "${freq_tmp}\t\t${temp_tmp}\t${power_tmp}\t${in_tmp}"

sleep 20s                               # Do nothing for XX s

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
