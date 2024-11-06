from typing import List
import pandas as pd
import json
import numpy as np
import pickle
from itertools import combinations_with_replacement
from itertools import product
from app.database import get_db

column_intervention = [
    'Life Stabilization',
    'General Employment Assistance Services',
    'Retention Services',
    'Specialized Services',
    'Employment-Related Financial Supports for Job Seekers and Employers', 
    'Employer Financial Supports',
    'Enhanced Referrals for Skills Development'
]

#loads the model into logic

import os

current_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(current_dir, 'model.pkl')
model = pickle.load(open(filename, "rb"))


def clean_input_data(data):
    #translate input into wahtever we trained the model on, numerical data in a specific order
    columns = ["age","gender","work_experience","canada_workex","dep_num",	"canada_born",	
               "citizen_status",	"level_of_schooling",	"fluent_english",	"reading_english_scale",	
               "speaking_english_scale",	"writing_english_scale",	"numeracy_scale",	"computer_scale",	
               "transportation_bool",	"caregiver_bool",	"housing",	"income_source",	"felony_bool",	"attending_school",	
               "currently_employed",	"substance_use",	"time_unemployed",	"need_mental_health_support_bool"]
    demographics = {
        'age': data['age'],
        'gender': data['gender'],
        'work_experience': data['work_experience'],
        'canada_workex': data['canada_workex'],
        'dep_num': data['dep_num'],
        'canada_born': data['canada_born'],
        'citizen_status': data['citizen_status'],
        'level_of_schooling': data['level_of_schooling'],
        'fluent_english': data['fluent_english'],
        'reading_english_scale': data['reading_english_scale'],
        'speaking_english_scale': data['speaking_english_scale'],
        'writing_english_scale': data['writing_english_scale'],
        'numeracy_scale': data['numeracy_scale'],
        'computer_scale': data['computer_scale'],
        'transportation_bool': data['transportation_bool'],
        'caregiver_bool': data['caregiver_bool'],
        'housing': data['housing'],
        'income_source': data['income_source'],
        'felony_bool': data['felony_bool'],
        'attending_school': data['attending_school'],
        'currently_employed': data['currently_employed'],
        'substance_use': data['substance_use'],
        'time_unemployed': data['time_unemployed'],
        'need_mental_health_support_bool': data['need_mental_health_support_bool']
    }
    output = []
    for column in columns:
        data = demographics.get(column, None) #default is None, and if you want to pass a value, can return any value
        if isinstance(data, str):
            data = convert_text(column, data)
        output.append(data)
    return output


def convert_text(column, data:str):
    # Convert text answers from front end into digits
    # TODO: ensure that categorical columns match the valid answers in FormNew.jsx (L131)
    categorical_cols_integers = [
        {
            "": 0,
            "true": 1,
            "false": 0,
            "no": 0,
            "yes": 1,
            "No": 0,
            "Yes": 1
        },
        {
            'Grade 0-8': 1,
            'Grade 9': 2,
            'Grade 10': 3,
            'Grade 11': 4,
            'Grade 12 or equivalent': 5,
            'OAC or Grade 13': 6,
            'Some college': 7,
            'Some university': 8,
            'Some apprenticeship': 9,
            'Certificate of Apprenticeship': 10,
            'Journeyperson': 11,
            'Certificate/Diploma': 12,
            'Bachelor’s degree': 13,
            'Post graduate': 14
        },
        {
            'Renting-private': 1,
            'Renting-subsidized': 2,
            'Boarding or lodging': 3,
            'Homeowner': 4,
            'Living with family/friend': 5,
            'Institution': 6,
            'Temporary second residence': 7,
            'Band-owned home': 8,
            'Homeless or transient': 9,
            'Emergency hostel': 10
        },
        {
            'No Source of Income': 1,
            'Employment Insurance': 2,
            'Workplace Safety and Insurance Board': 3,
            'Ontario Works applied or receiving': 4,
            'Ontario Disability Support Program applied or receiving': 5,
            'Dependent of someone receiving OW or ODSP': 6,
            'Crown Ward': 7,
            'Employment': 8,
            'Self-Employment': 9,
            'Other (specify)': 10
        }
    ]
    for category in categorical_cols_integers:
        print(f"data: {data}")
        print(f"column: {column}")
        if data in category:
            return category[data]

    if isinstance(data, str) and data.isnumeric():
        return int(data)

    return data

#creates 128 possible combinations in order to run every possibility through model
def create_matrix(row):
    data = [row.copy() for _ in range(128)] 
    perms = intervention_permutations(7)
    data = np.array(data)
    perms = np.array(perms)
    matrix = np.concatenate((data,perms), axis = 1) 
    return np.array(matrix)
#create matrix of permutations of 1 and 0 of num length
def intervention_permutations(num):
    perms = list(product([0,1],repeat=num))
    return np.array(perms)

def get_baseline_row(row):
    print(type(row))
    base_interventions = np.array([0]*7) # no interventions
    row = np.array(row)
    print(row)
    print(type(row))
    line = np.concatenate((row,base_interventions))
    return line

def intervention_row_to_names(row):
    names = []
    for i, value in enumerate(row):
        if value == 1: 
            names.append(column_intervention[i])
    return names

def process_results(baseline, results):
    ##Example:
    """
    {
        baseline_probability: 80 #baseline percentage point with no interventions
        results: [
            (85, [A,B,C]) #new percentange with intervention combinations and list of intervention names
            (89, [B,C])
            (91, [D,E])
        ]
    }
    """
    result_list= []
    for row in results:
        percent = row[-1] 
        names = intervention_row_to_names(row)
        result_list.append((percent,names))

    output = {
        "baseline": baseline[-1], #if it's an array, want the value inside of the array
        "interventions": result_list,
    }
    return output

def interpret_and_calculate(data):
    raw_data = clean_input_data(data)
    baseline_row = get_baseline_row(raw_data)
    baseline_row = baseline_row.reshape(1, -1)
    print("BASELINE ROW IS",baseline_row)
    intervention_rows = create_matrix(raw_data)
    baseline_prediction = model.predict(baseline_row)
    intervention_predictions = model.predict(intervention_rows)
    intervention_predictions = intervention_predictions.reshape(-1, 1) #want shape to be a vertical column, not a row
    result_matrix = np.concatenate((intervention_rows,intervention_predictions), axis = 1) ##CHANGED AXIS
    
    # sort this matrix based on prediction
    # print("RESULT SAMPLE::", result_matrix[:5])
    result_order = result_matrix[:,-1].argsort() #take all rows and only last column, gives back list of indexes sorted
    result_matrix = result_matrix[result_order] #indexing the matrix by the order

    # slice matrix to only top N results
    result_matrix = result_matrix[-3:,-8:] #-8 for interventions and prediction, want top 3, 3 combinations of intervention
    # post process results if needed ie make list of names for each row
    results = process_results(baseline_prediction,result_matrix)
    # build output dict
    print(f"RESULTS: {results}")
    return results

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

    # Define the SQL INSERT statement
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

    # Prepare the values from the client_data dictionary
    values = (
        client_data['age'], client_data['gender'], client_data['work_experience'], client_data['canada_workex'],
        client_data['dep_num'], client_data['canada_born'], client_data['citizen_status'], client_data['level_of_schooling'],
        client_data['fluent_english'], client_data['reading_english_scale'], client_data['speaking_english_scale'],
        client_data['writing_english_scale'], client_data['numeracy_scale'], client_data['computer_scale'],
        client_data['transportation_bool'], client_data['caregiver_bool'], client_data['housing'], client_data['income_source'],
        client_data['felony_bool'], client_data['attending_school'], client_data['currently_employed'],
        client_data['substance_use'], client_data['time_unemployed'], client_data['need_mental_health_support_bool'],
        client_data['employment_assistance'], client_data['life_stabilization'], client_data['retention_services'],
        client_data['specialized_services'], client_data['employment_related_financial_supports'],
        client_data['employer_financial_supports'], client_data['enhanced_referrals'], client_data['success_rate']
    )

    # Execute the query and commit the transaction
    try:
        cursor.execute(query, values)
        db.commit()
        cursor.close()
        return client_data  # Returning the inserted data
    except Exception as e:
        print(f"Error inserting client data: {e}")
        db.rollback()
        cursor.close()
        return None

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

