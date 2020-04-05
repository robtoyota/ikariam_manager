from pg import Pg
from city import City
from resource import Resource


class API:
	def __init__(self, config_dict):
		# Load the config that was provided
		self.config = config_dict

	def __enter__(self):
		# Connect to the DB
		self.db = Pg(self.config)
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		# Close the DB when done with this instance
		self.db.close()

	def upsert_city(self, city: City):
		pass

	def set_resource_amount(self, resource: Resource):
		pass

	def set_resource_production(self, resource: Resource):
		pass
