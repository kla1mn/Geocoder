import unittest

from osm_parser import (find_address_by_city_street_house, find_address_by_coordinates, insert_data,
                        _address_exists, create_table)
from parsed_object import ParsedObject


class TestDatabaseFunctions(unittest.TestCase):
    def setUp(self):
        """Creating an in-memory database before each test."""
        self.db_name = "memory"
        self.table_name = "test"
        create_table(self.db_name, self.table_name)

    def test_insert_and_find_address_by_city_street_house(self):
        """Test for inserting data and its subsequent location at the address."""
        parsed_obj = ParsedObject(city='Test City', street='Test Street', house_number='123',
                                  postcode='12345', lon=50.1234, lat=10.5678)

        insert_data(parsed_obj, self.db_name, self.table_name)

        result = find_address_by_city_street_house('Test City', 'Test Street', '123',
                                                   self.db_name, self.table_name)
        self.assert_result(result)

    def test_address_exists(self):
        """Test to check the existence of an address in the database."""
        parsed_obj = ParsedObject(city='Test City', street='Test Street', house_number='123',
                                  postcode='12345', lon=50.1234, lat=10.5678)

        insert_data(parsed_obj, self.db_name, self.table_name)

        exists = _address_exists(parsed_obj, self.db_name, self.table_name)
        self.assertTrue(exists)

    def test_find_address_by_coordinates(self):
        """Test for finding an address using coordinates."""
        parsed_obj = ParsedObject(city='Test City', street='Test Street', house_number='123',
                                  postcode='12345', lon=50.1234, lat=10.5678)

        insert_data(parsed_obj, self.db_name, self.table_name)

        result = find_address_by_coordinates(50.1234, 10.5678, self.db_name, self.table_name)
        self.assert_result(result)

    def test_address_not_found(self):
        """Test for the fact that the address was not found."""
        result = find_address_by_city_street_house('Nonexistent City', 'Nonexistent Street',
                                                   '999', self.db_name, self.table_name)
        self.assertIsNone(result)

        result_coords = find_address_by_coordinates(99.9999, 99.9999, self.db_name, self.table_name)
        self.assertIsNone(result_coords)

    def assert_result(self, result):
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 'Test City')
        self.assertEqual(result[1], 'Test Street')
        self.assertEqual(result[2], '123')
        self.assertEqual(result[3], '12345')
        self.assertEqual(result[4], 50.1234)
        self.assertEqual(result[5], 10.5678)


if __name__ == '__main__':
    unittest.main()
