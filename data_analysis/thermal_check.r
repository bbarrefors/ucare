#                                                                              #
# File Name..........: ~/UCARE/data_analylis/xx/thermal_check.r
# Author.............: Bjorn Barrefors
# Institution........: University of Nebraska-Lincoln 
# ...................: Department of Computer Science and Engineering
# Date Written.......: January 16, 2013
# Date Last Modified.: March 9, 2013
# Language...........: R
# Purpose............: Find a temperature model.
# Brief Description..: Collect data from thermal_data.dat.
# ...................: Find thermal resistivity.
# Improvements.......: 

sink("thermal.out")

# Read data from thermal_data.dat
data <- read.table("./thermal_data.dat", header = FALSE, sep = "\t", dec = ".", skip = 3)

# Put data as a linear model
# Extract data from table
temperature <- as.vector(data[[3]])        # T is temperature, column 3
power <- as.vector(data[[4]])    

T <- temperature[1:2]
P <- power[1:2]*0.1

# Model
R <- (T[1] - T[2]) / (P[1] - P[2])

# Print result
print(R)
