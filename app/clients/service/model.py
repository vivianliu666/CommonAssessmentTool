"""
This module prepares a machine learning model using Random Forest
for client success rate prediction.
It defines functions to load data, train the model,
and save/load the model using pickle.
"""

import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor


def prepare_models():
    """
    Prepares and trains a Random Forest model using client success data.

    Returns:
        RandomForestRegressor: The trained Random Forest model.
    """
    # Load dataset and define the features and labels
    backend_code = pd.read_csv('data_commontool.csv')

    categorical_cols = [
        'age', 'gender', 'work_experience', 'canada_workex', 'dep_num',
        'canada_born', 'citizen_status', 'level_of_schooling',
        'fluent_english', 'reading_english_scale', 'speaking_english_scale',
        'writing_english_scale', 'numeracy_scale', 'computer_scale',
        'transportation_bool', 'caregiver_bool',
        'housing', 'income_source', 'felony_bool', 'attending_school',
        'currently_employed', 'substance_use', 'time_unemployed',
        'need_mental_health_support_bool', 'employment_assistance',
        'life_stabilization', 'retention_services', 'specialized_services',
        'employment_related_financial_supports', 'employer_financial_supports',
        'enhanced_referrals'
    ]

    x_categorical_baseline = backend_code[categorical_cols]
    y_baseline = backend_code['success_rate']

    x_train_baseline, _, y_train_baseline, _ = train_test_split(
        x_categorical_baseline, y_baseline, test_size=0.2, random_state=42
    )

    # Train the model
    rf_model_baseline = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model_baseline.fit(x_train_baseline, y_train_baseline)

    return rf_model_baseline


def main():
    """
    Main function to train and serialize the Random Forest model.

    Saves:
        model.pkl: Serialized Random Forest model.
    """
    print("Start model.")
    model = prepare_models()

    # Save and load the model using pickle
    with open("model.pkl", "wb") as file:
        pickle.dump(model, file)

    with open("model.pkl", "rb") as file:
        model = pickle.load(file)


if __name__ == "__main__":
    main()
