# R translation of train_model_dbt_style.py using tidymodels + orbital

# Load required libraries
library(tidymodels)
library(orbital)
library(dplyr)

# Load and prepare data
data(iris)
iris <- iris %>% mutate(species = as.character(Species)) %>% select(-Species)

# Define the base recipe
rec <- recipe(species ~ ., data = iris) %>%
  step_log(all_numeric_predictors()) %>%
  step_normalize(all_numeric_predictors()) %>%
  step_dummy(all_nominal_predictors()) %>%
  step_interact(terms = ~ all_numeric_predictors():all_numeric_predictors()) %>%
  step_bin2factor(all_numeric_predictors(), bins = 5)

# Prepare recipe and apply transformations
prep_rec <- prep(rec)
transformed_data <- bake(prep_rec, new_data = NULL)

# Train model
set.seed(123)
split <- initial_split(transformed_data, prop = 0.7)
train_data <- training(split)
test_data <- testing(split)

rf_model <- rand_forest(mtry = 2, trees = 100, mode = "classification") %>%
  set_engine("ranger")

wf <- workflow() %>%
  add_model(rf_model) %>%
  add_recipe(rec)

fitted_model <- fit(wf, data = train_data)

# Evaluate model
predictions <- predict(fitted_model, test_data) %>% bind_cols(test_data)
metrics <- metrics(predictions, truth = species, estimate = .pred_class)

print(metrics)

# Translate recipe to SQL
sql_code <- orbital::recipe_to_sql(prep_rec, dialect = "postgresql")
cat(sql_code)
