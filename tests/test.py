"""
Unit tests for the `interpret_and_calculate` function in the logic module.
"""
import unittest
from app.clients.service.logic import interpret_and_calculate
from tests.helper import get_sample_client_data


class TestLogic(unittest.TestCase):
    """
    Test cases for the `interpret_and_calculate` function.
    """
    def test_interpret_and_calculate(self):
        """
        Test the `interpret_and_calculate` function for expected output structure.
        """
        data = get_sample_client_data()
        result = interpret_and_calculate(data)

        # Verify that the returned dictionary includes the expected keys
        self.assertIn('baseline', result, "Result should include a 'baseline' key")
        self.assertIn('interventions', result, "Result should include an 'interventions' key")

        # Additional checks can be made based on the contents of 'baseline' and 'interventions'
        self.assertIsInstance(result['baseline'], float, "Baseline should be a float")
        self.assertIsInstance(result['interventions'], list, "Interventions should be a list")


if __name__ == '__main__':
    unittest.main()
