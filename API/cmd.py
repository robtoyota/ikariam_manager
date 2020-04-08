from city import City
from resource import Resource


class Cmd:
	def __init__(self, db):
		self.db = db  # DB connection instance

	def upsert_city(self, city: City):
		pass

	def set_resource_amount(self, resource: Resource):
		pass

	def set_resource_production(self, resource: Resource):
		pass
