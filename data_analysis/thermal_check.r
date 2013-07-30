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

sink("thermal_checkxx.out")

# Read data from thermal_data.dat
data <- read.table("./thermal_dataxx.dat", header = FALSE, sep = "\t", dec = ".", skip = 3)

a1 <- -0.004537
a2 <- 5.224674
a3 <- 0.175453
a4 <- 0.344344
a5 <- -8.963781
a6 <- 53.716303

# Put data as a linear model
# Extract data from table
frequency <- as.vector(data[[1]])          # f is frequency, column 1
temperature <- as.vector(data[[3]])        # T is temperature, column 3
amb_temperature <- as.vector(data[[5]])    # T_amb is ambient temperature, column 4

frequency <- frequency/1000000             # Make f a measurement in GHz

f <- frequency[1:10]
T <- temperature[1:10]
T_amb <- amb_temperature[1:10]

P <- a1*T^2 + a2*f^2 + a3*f*T + a4*T + a5*F + a6

# Model
R <- (T - T_amb) / P
average <- mean(R)

# Print result
print(R)
print(average)