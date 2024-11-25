"""
This module provides logic for client data processing and intervention analysis.
It includes functions for cleaning input data, creating matrices for model prediction,
and interacting with the database for CRUD operations on client data.
"""

import os
import pickle
from itertools import product
import numpy as np
from app.database import get_db

# Column names for interventions
column_intervention = [
    'Life Stabilization', 'General Employment Assistance Services', 'Retention Services',
    'Specialized Services', 'Employment-Related Financial Supports for Job Seekers and Employers',
    'Employer Financial Supports', 'Enhanced Referrals for Skills Development'
]

# Load the model
current_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(current_dir, 'model.pkl')

with open(filename, "rb") as file:
    model = pickle.load(file)


def clean_input_data(data):
    """
    Cleans and transforms input data into numerical format for model inference.

    Args:
        data (dict): Raw input data.

    Returns:
        list: Transformed numerical data.
    """
    columns = [
        "age", "gender", "work_experience", "canada_workex", "dep_num", "canada_born",
        "citizen_status", "level_of_schooling", "fluent_english", "reading_english_scale",
        "speaking_english_scale", "writing_english_scale", "numeracy_scale", "computer_scale",
        "transportation_bool", "caregiver_bool", "housing", "income_source", "felony_bool",
        "attending_school", "currently_employed", "substance_use", "time_unemployed",
        "need_mental_health_support_bool"
    ]
    cleaned_data = [
        convert_text(data.get(column, None))
        for column in columns
    ]
    return cleaned_data


def convert_text(data):
    """
    Converts text input from the frontend into numerical values.

    Args:
        data (str): Input text data.

    Returns:
        int or None: Converted numerical value or None if not applicable.
    """
    categorical_mapping = {
        "": 0, "true": 1, "false": 0, "no": 0, "yes": 1, "No": 0, "Yes": 1
    }
    if isinstance(data, str):
        if data.isnumeric():
            return int(data)
        return categorical_mapping.get(data, None)
    return data


def create_matrix(row):
    """
    Creates a matrix of all possible intervention combinations.

    Args:
        row (list): Baseline input data.

    Returns:
        np.ndarray: Matrix containing all combinations of interventions.
    """
    data = np.array([row.copy() for _ in range(128)])
    permutations = np.array(list(product([0, 1], repeat=7)))
    matrix = np.concatenate((data, permutations), axis=1)
    return matrix


def get_baseline_row(row):
    """
    Creates a baseline row without interventions.

    Args:
        row (list): Input data.

    Returns:
        np.ndarray: Baseline row with no interventions.
    """
    base_interventions = np.zeros(7, dtype=int)
    baseline_row = np.concatenate((np.array(row), base_interventions))
    return baseline_row


def intervention_row_to_names(row):
    """
    Maps intervention binary indicators to their names.

    Args:
        row (list): Binary intervention indicators.

    Returns:
        list: List of intervention names.
    """
    return [column_intervention[i] for i, value in enumerate(row) if value == 1]


def process_results(baseline, results):
    """
    Processes baseline and intervention results.

    Args:
        baseline (float): Baseline prediction value.
        results (np.ndarray): Matrix of intervention predictions.

    Returns:
        dict: Dictionary containing baseline and intervention results.
    """
    processed_results = [
        (row[-1], intervention_row_to_names(row[:-1]))
        for row in results
    ]
    return {
        "baseline": baseline[-1],
        "interventions": processed_results,
    }


def interpret_and_calculate(data):
    """
    Cleans input data, generates predictions, and processes results.

    Args:
        data (dict): Raw input data.

    Returns:
        dict: Dictionary containing baseline and top interventions.
    """
    raw_data = clean_input_data(data)
    baseline_row = get_baseline_row(raw_data).reshape(1, -1)
    intervention_rows = create_matrix(raw_data)

    baseline_prediction = model.predict(baseline_row)
    intervention_predictions = model.predict(intervention_rows).reshape(-1, 1)

    result_matrix = np.concatenate((intervention_rows, intervention_predictions), axis=1)
    sorted_indices = result_matrix[:, -1].argsort()
    result_matrix = result_matrix[sorted_indices][-3:, -8:]

    return process_results(baseline_prediction, result_matrix)


def create_client_data(client_data: dict):
    """
    Insert a new client record into the database.

    Args:
        client_data (dict): A dictionary containing the client data to be inserted.

    Returns:
        dict: The inserted client data if successful; None otherwise.
    """
    db = next(get_db())
    cursor = db.cursor()

    query = """
    INSERT INTO clients (age, gender, work_experience, canada_workex, dep_num, canada_born, citizen_status, 
                         level_of_schooling, fluent_english, reading_english_scale, speaking_english_scale, 
                         writing_english_scale, numeracy_scale, computer_scale, transportation_bool, caregiver_bool, 
                         housing, income_source, felony_bool, attending_school, currently_employed, 
                         substance_use, time_unemployed, need_mental_health_support_bool, employment_assistance, 
                         life_stabilization, retention_services, specialized_services, employment_related_financial_supports, 
                         employer_financial_supports, enhanced_referrals, success_rate)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = tuple(client_data.values())

    try:
        cursor.execute(query, values)
        db.commit()
        return client_data
    except Exception as e:
        print(f"Error inserting client data: {e}")
        db.rollback()
        return None
    finally:
        cursor.close()


def get_client_data(age: int, gender: int, work_experience: int):
    db = next(get_db())
    cursor = db.cursor()
    query = "SELECT * FROM clients WHERE age = %s AND gender = %s AND work_experience = %s"
    values = (age, gender, work_experience)
    cursor.execute(query, values)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return dict(zip(cursor.column_names, result))
    return None

def update_client_data(client_update: dict):
    db = next(get_db())
    cursor = db.cursor()
    query = "UPDATE clients SET ... WHERE age = %s AND gender = %s AND work_experience = %s"
    values = (client_update['age'], client_update['gender'], client_update['work_experience'])
    cursor.execute(query, values)
    db.commit()
    cursor.close()
    updated_client = get_client_data(client_update['age'], client_update['gender'], client_update['work_experience'])
    return updated_client

def delete_client_data(age: int, gender: int, work_experience: int):
    db = next(get_db())
    cursor = db.cursor()
    query = "DELETE FROM clients WHERE age = %s AND gender = %s AND work_experience = %s"
    values = (age, gender, work_experience)
    cursor.execute(query, values)
    db.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    return affected_rows > 0

if __name__ == "__main__":
    print("running")
    data = {
        "age": "23",
        "gender": "1",
        "work_experience": "1",
        "canada_workex": "1",
        "dep_num": "0",
        "canada_born": "1",
        "citizen_status": "2",
        "level_of_schooling": "2",
        "fluent_english": "3",
        "reading_english_scale": "2",
        "speaking_english_scale": "2",
        "writing_english_scale": "3",
        "numeracy_scale": "2",
        "computer_scale": "3",
        "transportation_bool": "2",
        "caregiver_bool": "1",
        "housing": "1",
        "income_source": "5",
        "felony_bool": "1",
        "attending_school": "0",
        "currently_employed": "1",
        "substance_use": "1",
        "time_unemployed": "1",
        "need_mental_health_support_bool": "1"
    }
    # print(data)
    results = interpret_and_calculate(data)
    print(results)

