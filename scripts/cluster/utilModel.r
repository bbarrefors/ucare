sink("./33/utilModel.out")

data <- read.table("./33/utilData.dat", header = FALSE, sep = "\t", dec = ".", skip = 3)

util <- as.vector(data[[1]])
power <- as.vector(data[[2]])

u = util[1:5]
p = power[1:5]
u2 = u^2

model <- lm(p ~ u + u2)

print(model)