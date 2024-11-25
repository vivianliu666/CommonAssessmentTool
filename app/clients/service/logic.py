"""
This module contains logic for processing client data, model predictions,
and database interactions for a client management system.
"""

import os
import pickle
from itertools import product
import numpy as np
from app.database import get_db

# Define column names for interventions
column_intervention = [
    'Life Stabilization',
    'General Employment Assistance Services',
    'Retention Services',
    'Specialized Services',
    'Employment-Related Financial Supports for Job Seekers and Employers',
    'Employer Financial Supports',
    'Enhanced Referrals for Skills Development'
]

# Load the pre-trained model
current_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(current_dir, 'model.pkl')
with open(filename, "rb") as file:
    model = pickle.load(file)


def clean_input_data(data):
    """
    Cleans and transforms input data into a format suitable for the trained model.

    Args:
        data (dict): Input data from the client.

    Returns:
        list: Transformed data ready for prediction.
    """
    columns = [
        "age", "gender", "work_experience", "canada_workex", "dep_num",
        "canada_born", "citizen_status", "level_of_schooling", "fluent_english",
        "reading_english_scale", "speaking_english_scale", "writing_english_scale",
        "numeracy_scale", "computer_scale", "transportation_bool",
        "caregiver_bool", "housing", "income_source", "felony_bool",
        "attending_school", "currently_employed", "substance_use",
        "time_unemployed", "need_mental_health_support_bool"
    ]
    output = []
    for column in columns:
        value = data.get(column, None)
        if isinstance(value, str):
            value = convert_text(column, value)
        output.append(value)
    return output


def convert_text(column, data: str):
    """
    Converts text inputs into numerical values based on predefined mappings.

    Args:
        column (str): Column name for context.
        data (str): Text data to convert.

    Returns:
        int: Converted numerical value.
    """
    # Predefined mappings for categorical data
    mappings = {
        "": 0, "true": 1, "false": 0, "no": 0, "yes": 1,
        'Grade 0-8': 1, 'Grade 9': 2, 'Grade 10': 3, 'Grade 11': 4,
        'Grade 12 or equivalent': 5, 'OAC or Grade 13': 6, 'Some college': 7,
        'Some university': 8, 'Some apprenticeship': 9,
        'Certificate of Apprenticeship': 10, 'Journeyperson': 11,
        'Certificate/Diploma': 12, 'Bachelor’s degree': 13, 'Post graduate': 14,
        'Renting-private': 1, 'Renting-subsidized': 2, 'Boarding or lodging': 3,
        'Homeowner': 4, 'Living with family/friend': 5, 'Institution': 6,
        'Temporary second residence': 7, 'Band-owned home': 8,
        'Homeless or transient': 9, 'Emergency hostel': 10,
        'No Source of Income': 1, 'Employment Insurance': 2,
        'Workplace Safety and Insurance Board': 3, 'Ontario Works applied or receiving': 4,
        'Ontario Disability Support Program applied or receiving': 5,
        'Dependent of someone receiving OW or ODSP': 6, 'Crown Ward': 7,
        'Employment': 8, 'Self-Employment': 9, 'Other (specify)': 10
    }
    return mappings.get(data, int(data) if data.isdigit() else 0)


def create_matrix(row):
    """
    Generates a matrix of possible intervention combinations.

    Args:
        row (list): Baseline data row.

    Returns:
        np.array: Matrix with intervention combinations.
    """
    base_data = [row.copy() for _ in range(128)]
    interventions = list(product([0, 1], repeat=7))
    return np.concatenate((base_data, interventions), axis=1)


def process_results(baseline, results):
    """
    Processes prediction results into a human-readable format.

    Args:
        baseline (float): Baseline prediction.
        results (np.array): Array of intervention results.

    Returns:
        dict: Processed results including baseline and top interventions.
    """
    processed_results = []
    for row in results:
        percent = row[-1]
        intervention_names = [column_intervention[i] for i, val in enumerate(row[:-1]) if val == 1]
        processed_results.append((percent, intervention_names))

    return {
        "baseline": baseline[-1],
        "interventions": processed_results
    }


def interpret_and_calculate(data):
    """
    Prepares input data, makes predictions, and processes results.

    Args:
        data (dict): Input data.

    Returns:
        dict: Processed prediction results.
    """
    raw_data = clean_input_data(data)
    baseline_row = np.array(raw_data + [0] * 7).reshape(1, -1)
    intervention_matrix = create_matrix(raw_data)

    baseline_prediction = model.predict(baseline_row)
    intervention_predictions = model.predict(intervention_matrix).reshape(-1, 1)

    result_matrix = np.concatenate((intervention_matrix, intervention_predictions), axis=1)
    top_results = result_matrix[result_matrix[:, -1].argsort()][-3:, -8:]

    return process_results(baseline_prediction, top_results)
