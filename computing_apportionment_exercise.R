# This R script produces same priority values as published
# Multiple ways from multiple statistical programming languages can reach to the same results. 
# This is an informal exercise/test of codes. 
# Source: https://www2.census.gov/programs-surveys/decennial/2020/data/apportionment/2020PriorityValues.xlsx
library(readxl)
library(dplyr)
table_path = "redacted"
state_pop <- read_excel(path = table_path,
                        sheet = 1,
                        skip = 3,
                        n_max = 51)
state_pop <- state_pop |>
  rename(state = 1, 
         pop = 2, 
         apportionment = 3, 
         change = 4)
total_pop <- tail(state_pop, n = 1) # last row as total
state_pop <- state_pop |>
  filter(row_number() <= n() - 1) # exclude the last row for state population data frame
# confirm total population match
sum(state_pop$pop) == total_pop$pop
# send state-level population to a vector
pop <- state_pop$pop
# name the vector
names(pop) <- state_pop$state
options(scipen = 999)
options(digits=20)
n <- seq(2, 60, by = 1)
state_priority_value_l <- vector(mode = "list", length = dim(state_pop)[1])

# priority value
for (i in 1:dim(state_pop)[1]) {
  state_priority_value_l[[i]]  <- pop[i] / sqrt(n * (n - 1))
}
names(state_priority_value_l) <- state_pop$state

state_priority_values <- unlist(state_priority_value_l)

df_state_priority <- data.frame(state = names(state_priority_values),
                                priority_value = unlist(state_priority_value_l),
                                row.names = NULL) |>
  arrange(desc(priority_value))

# parse number, adding 1 to include the guaranteed 1 seat of each state
df_state_priority$seat <- readr::parse_number(df_state_priority$state) + 1
# remove 0-9 from state
df_state_priority$state <- gsub(pattern = "[0-9]+",replacement = "", df_state_priority$state)
# only keep a reasonable number to include the assignment of the available 385 seats, with a few extra rows
df_state_priority <- df_state_priority |>
  filter(row_number() <= 395) |>
  mutate(house = row_number() + 50) # add house seat enumeration