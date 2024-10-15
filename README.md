# Geocoder

**Geocoder** is a console program that takes a city, street, and house number as input and outputs the full address with latitude and longitude. The program uses the osmium library and aiohttp. Geocoder uses SQLite database

### Requirements
- Python 3.12.0
- osmium 3.7.0
- aiohttp==3.10.10


### Usage
Run GeoCoder.py then send GET requests through Postman\
Examples:\
```http://127.0.0.1:8080/search_by_address?city=Екатеринбург&street=улица Вайнера&house_number=10``` \
or \
```http://127.0.0.1:8080/search_by_coordinates?lon=60.5938165&lat=56.836297```

Replace with the actual values you want to search for.

The program will send response with the full address with latitude and longitude.