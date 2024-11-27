"""
Helper functions for testing the client service logic.

This module provides utility functions and sample data
to support unit tests for the client management system.
"""


def get_sample_client_data():
    """
    Provides sample client data for testing purposes.

    Returns:
        dict: Sample client data.
    """
    return {
        'age': 23, 'gender': 1, 'work_experience': 1, 'canada_workex': 1, 'dep_num': 0,
        'canada_born': 1, 'citizen_status': 2, 'level_of_schooling': 2, 'fluent_english': 3,
        'reading_english_scale': 2, 'speaking_english_scale': 2, 'writing_english_scale': 3,
        'numeracy_scale': 2, 'computer_scale': 3, 'transportation_bool': 2, 'caregiver_bool': 1,
        'housing': 1, 'income_source': 5, 'felony_bool': 1, 'attending_school': 0,
        'currently_employed': 1, 'substance_use': 1, 'time_unemployed': 1,
        'need_mental_health_support_bool': 1
    }
