#
# File Name..........: ~/UCARE/data_analylis/08/power_check.r
# Author.............: Bjorn Barrefors
# Institution........: University of Nebraska-Lincoln 
# ...................: Department of Computer Science and Engineering
# Date Written.......: October 7, 2012
# Date Last Modified.: March 9, 2013
# Language...........: R
# Purpose............: Check data against power model for correctness.
# Brief Description..: Collect data from data.dat.
# ...................: Do linear regression on power model
# Improvements.......: 

# Print to out_check
sink("power.out")

# Read data from power_data.dat
data <- read.table("./power_data.dat", header = FALSE, sep = "\t", dec = ".", skip = 3)

# Put data as a linear model
# Extract data from table
frequency <- as.vector(data[[1]])          # f is frequency, column 2
temperature <- as.vector(data[[3]])        # T is temperature, column 1
power_consumption <- as.vector(data[[4]])  # p is power consumption, column 3

frequency <- frequency/1000             # Make f a measurement in GHz

f <- frequency[1:24]
T <- temperature[1:24]
P <- power_consumption[1:24]
P <- (P / 10)				# convert power from 0.1W to 1W
f2 <- f*f
T2 <- T*T

model <- lm(P ~ T2 + f2 + f*T + T + f)

print(model)
sum <- summary(model)
print(sum)