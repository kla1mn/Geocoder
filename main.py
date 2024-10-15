import aiohttp
import logging

import config
import osm_parser
from aiohttp import web

DB_NAME = "addresses.db"
TOKEN = config.TOKEN

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')


def create_app() -> web.Application:
    """Creates and configures the web application."""
    app = web.Application()
    app.router.add_get('/search_by_address', search_by_address)
    app.router.add_get('/search_by_coordinates', search_by_coordinates)
    return app


async def search_by_address(request: web.Request) -> web.Response:
    """Handles the request to search for an address by city, street, and house number."""
    try:
        city, street, house_number = await _validate_address_params(request)
        if not all([city, street, house_number]):
            return web.json_response({'error': 'Please provide city, street, and house number'}, status=400)

        result: tuple[str, str, str, str, float, float, str] \
            = osm_parser.find_address_by_city_street_house(city, street, house_number, DB_NAME, "addresses")

        if result:
            response = await _create_json_address_response(result)

            lon, lat = result[4], result[5]
            if lon is None or lat is None:
                response['organizations'] = 'Organizations cannot be returned: no coordinates available'
            else:
                organizations = await _get_organizations_by_coordinates(lon, lat)
                response['organizations'] = organizations if organizations else 'No organizations found'

            return web.json_response(response, status=200)

        return web.json_response({'message': 'Address not found'}, status=404)
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return web.json_response({'error': str(e)}, status=500)


async def search_by_coordinates(request: web.Request) -> web.Response:
    """Handles the request to search for an address by coordinates."""
    try:
        lon, lat = await _validate_coordinate_params(request)
        if lon is None or lat is None:
            return web.json_response({'error': 'Please provide both longitude and latitude'}, status=400)

        organizations = await _get_organizations_by_coordinates(lon, lat)

        result: tuple[str, str, str, str, float, float, str]\
            = osm_parser.find_address_by_coordinates(lon, lat, DB_NAME, "addresses")

        if result:
            response = await _create_json_address_response(result)
            response['organizations'] = organizations if organizations else 'No organizations found'
            return web.json_response(response, status=200)

        return web.json_response({'message': 'Address not found'}, status=404)
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return web.json_response({'error': str(e)}, status=500)


async def _validate_address_params(request: web.Request) -> tuple[str | None, str | None, str | None]:
    """Validates and extracts address parameters from the request."""
    city = request.query.get('city')
    street = request.query.get('street')
    house_number = request.query.get('house_number')
    return city, street, house_number


async def _validate_coordinate_params(request: web.Request) -> tuple[float | None, float | None]:
    """Validates and extracts coordinate parameters from the request."""
    lon = request.query.get('lon')
    lat = request.query.get('lat')
    return float(lon) if lon else None, float(lat) if lat else None


async def _create_json_address_response(result: tuple[str, str, str, str, float, float, str]) \
        -> dict[str, str | float | list[dict[str, str]]]:
    """Creates a JSON response from the address data."""
    return {
        'country': "Россия",
        'city': result[0],
        'street': result[1],
        'house_number': result[2],
        'postcode': result[3],
        'lon': result[4],
        'lat': result[5],
    }


async def _get_organizations_by_coordinates(lon: float, lat: float) -> list[dict[str, str]] | None:
    """Returns a list of all organizations by coordinates."""
    url = f"https://catalog.api.2gis.com/3.0/items"
    params = {
        'point': f'{lon},{lat}',
        'radius': 500,
        'type': 'branch,building',
        'key': TOKEN,
        'fields': 'items.name'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data: dict = await response.json()
                organizations = [{'name': item.get('name')} for item in data.get('result', {}).get('items', [])]
                logging.info(f'Organizations: {organizations}')
                return organizations
            else:
                logging.error(f"Error {response.status}: {response.text()}")
                return None


if __name__ == '__main__':
    web.run_app(create_app(), host='127.0.0.1', port=8080)
