import unittest

from parsed_object import ParsedObject


class TestParsedObject(unittest.TestCase):
    def setUp(self):
        self.city = "Test City"
        self.street = "Test Street"
        self.house_number = "123"
        self.postcode = "12345"
        self.lon = 12.34
        self.lat = 56.78
        self.parsed_object = ParsedObject(self.city, self.street, self.house_number, self.postcode, self.lon, self.lat)

    def test_initialization(self):
        self.assertEqual(self.parsed_object.city, self.city)
        self.assertEqual(self.parsed_object.street, self.street)
        self.assertEqual(self.parsed_object.house_number, self.house_number)
        self.assertEqual(self.parsed_object.postcode, self.postcode)
        self.assertEqual(self.parsed_object.lon, self.lon)
        self.assertEqual(self.parsed_object.lat, self.lat)

    def test_str_method(self):
        expected_str = (f"city: {self.city}, street: {self.street}, house_number: {self.house_number}, "
                        f"postcode: {self.postcode}, lon: {self.lon}, lat: {self.lat}")
        self.assertEqual(str(self.parsed_object), expected_str)


if __name__ == "__main__":
    unittest.main()
