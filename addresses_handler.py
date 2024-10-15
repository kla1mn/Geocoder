import logging
import osmium

from parsed_object import ParsedObject
from osm_parser import insert_data

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')


class AddressesHandler(osmium.SimpleHandler):
    def __init__(self, db_name):
        super(AddressesHandler, self).__init__()
        self.db_name = db_name
        self.counter = 0

    def node(self, node):
        self.parse_node(node)

    def parse_node(self, node):
        if node and node.location.valid():
            parsed_obj = self.get_info_about_object(node, lon=node.location.lon, lat=node.location.lat)
            if parsed_obj is not None:
                self.add_address(parsed_obj)

    def way(self, way):
        if way:
            for node in way.nodes:
                self.parse_node(node)

    def relation(self, relation):
        if relation:
            parsed_obj = self.get_info_about_object(relation)
            if parsed_obj is not None:
                self.add_address(parsed_obj)

    @staticmethod
    def get_info_about_object(n, lon=None, lat=None) -> ParsedObject | None:
        try:
            city = n.tags.get('addr:city', None)
            postcode = n.tags.get('addr:postcode', None)
            street = n.tags.get('addr:street', None)
            house_number = n.tags.get('addr:housenumber', None)
            if city is not None and street is not None and house_number is not None:
                return ParsedObject(city, street, house_number, postcode, lon, lat)
            return None
        except Exception as e:
            logging.error(f"Error parsing object: {e}")
            return None

    def add_address(self, parsed_obj: ParsedObject):
        insert_data(parsed_obj, self.db_name)
        self.counter += 1
        if self.counter % 1000 == 0:
            logging.info(f"Processed {self.counter} addresses.")
