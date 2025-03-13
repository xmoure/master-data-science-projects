# Script for D1 (get a subset of the original data and determine the number of missing values)

dd <- read.csv("Google-Playstore.csv", stringsAsFactors = FALSE)

# Number of records/observations/entries and number of variables
dim(dd)

data <- dd[dd$Rating!=0.0 | is.na(dd$Rating),]
data <- data[c(1:20000),]
summary(data)

# List of all variables available in the original dataset
str(data)
variables = attributes(data)$names
variables

total_missing = 0 # Number of missing values in the whole data matrix
summary(data)

for (var in names(data)) {
  # print(typeof(data[[var]]))
  if (typeof(data[[var]]) == "character") missing = sum(data[var] == "")
  else missing = sum(is.na(data[var]))
  total_missing = total_missing + missing
  missing_percentage = 100*missing/nrow(data)
  cat(var, ": ", missing, " missings or ", missing_percentage, "%\n", sep="")
}

# Percentage of missing values in the whole data matrix
total_data = nrow(data) * ncol(data)
total_missing_percentage = (total_missing/total_data) * 100
total_missing_percentage
total_data
total_missing

# Write this data to a new CSV file
write.csv(data, file.path(getwd(), "Playstore-reduced.csv"), row.names = FALSE)
