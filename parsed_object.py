class ParsedObject:
    def __init__(self, city, street, house_number, postcode, lon, lat):
        self.city = city
        self.street = street
        self.house_number = house_number
        self.postcode = postcode
        self.lon = lon
        self.lat = lat

    def __str__(self):
        return (f"city: {self.city}, street: {self.street}, house_number: {self.house_number}, "
                f"postcode: {self.postcode}, lon: {self.lon}, lat: {self.lat}")
