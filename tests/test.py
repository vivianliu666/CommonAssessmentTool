"""
Unit tests for the interpret_and_calculate function.
"""

import unittest
from app.clients.service.logic import interpret_and_calculate


class TestLogic(unittest.TestCase):
    """
    Unit test class for testing the logic in the interpret_and_calculate function.
    """

    def test_interpret_and_calculate(self):
        """
        Tests the interpret_and_calculate function with valid input data.
        Verifies the baseline and interventions are included and of correct types.
        """
        data = {
            "age": 23,
            "gender": 1,
            "work_experience": 1,
            "canada_workex": 1,
            "dep_num": 0,
            "canada_born": 1,
            "citizen_status": 2,
            "level_of_schooling": 2,
            "fluent_english": 3,
            "reading_english_scale": 2,
            "speaking_english_scale": 2,
            "writing_english_scale": 3,
            "numeracy_scale": 2,
            "computer_scale": 3,
            "transportation_bool": 2,
            "caregiver_bool": 1,
            "housing": 1,
            "income_source": 5,
            "felony_bool": 1,
            "attending_school": 0,
            "currently_employed": 1,
            "substance_use": 1,
            "time_unemployed": 1,
            "need_mental_health_support_bool": 1,
        }
        result = interpret_and_calculate(data)

        # Verify that the returned dictionary includes the expected keys
        self.assertIn("baseline", result, "Result should include a 'baseline' key")
        self.assertIn(
            "interventions", result, "Result should include an 'interventions' key"
        )

        # Additional checks can be made based on the contents of 'baseline' and 'interventions'
        self.assertIsInstance(result["baseline"], float, "Baseline should be a float")
        self.assertIsInstance(
            result["interventions"], list, "Interventions should be a list"
        )


if __name__ == "__main__":
    unittest.main()
