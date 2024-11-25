"""
This module trains a Random Forest model to predict success rates
based on client data and saves the model as a pickle file.
"""

import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor


def prepare_models():
  """
  Prepares the dataset, trains a Random Forest model,
  and returns the trained model.
  """
  client_data = pd.read_csv('data_commontool.csv')

  # Define categorical columns and interventions
  categorical_cols = [
    'age', 'gender', 'work_experience', 'canada_workex', 'dep_num', 'canada_born',
    'citizen_status', 'level_of_schooling', 'fluent_english', 'reading_english_scale',
    'speaking_english_scale', 'writing_english_scale', 'numeracy_scale', 'computer_scale',
    'transportation_bool', 'caregiver_bool', 'housing', 'income_source', 'felony_bool',
    'attending_school', 'currently_employed', 'substance_use', 'time_unemployed',
    'need_mental_health_support_bool'
  ]
  interventions = [
    'employment_assistance', 'life_stabilization', 'retention_services',
    'specialized_services', 'employment_related_financial_supports',
    'employer_financial_supports', 'enhanced_referrals'
  ]
  categorical_cols.extend(interventions)

  # Prepare features and labels
  x_features = client_data[categorical_cols]
  y_labels = client_data['success_rate']

  # Split data
  x_train, x_test, y_train, y_test = train_test_split(
    x_features, y_labels, test_size=0.2, random_state=42
  )

  # Train Random Forest model
  rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
  rf_model.fit(x_train, y_train)

  return rf_model


def main():
  """
  Main function to train and save the model.
  """
  model = prepare_models()

  # Save model
  with open("model.pkl", "wb") as file:
    pickle.dump(model, file)

  # Test loading the model
  with open("model.pkl", "rb") as file:
    model = pickle.load(file)
  print("Model loaded successfully.")


if __name__ == "__main__":
  main()
