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
#amb <- as.vector(data[[5]])    

#f <- frequency[1:2]
T1 <- temperature[1]
P1 <- power[1]
T2 <- temperature[2]
P2 <- power[2]

R = (T1 - T2)/(P1 - P2)

print(R)

Ta <- T2 - R*P2

print(Ta)

#P <- 73

#T <- Ta + R*P
#print(T)
#T <- 37.75
#print(T)