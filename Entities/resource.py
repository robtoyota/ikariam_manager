from pg import Pg


class Resource:
	def __init__(self, properties: dict):
		self.city_id = properties.get('city_id', 0)
		self.resource_type = properties.get('resource_type', "")
		self.amount = properties.get('amount', 0)
		self.production = properties.get('production', 0)
		self.usage = properties.get('usage', 0)
		self.maximum = properties.get('maximum', 0)
		self.target_minimum = properties.get('target_minimum', 0)
		self.target_maximum = properties.get('target_maximum', 0)
		self.target_amount = properties.get('target_amount', 0)

	@staticmethod
	def set_amount(db: Pg, resource_id: int, amount: int) -> bool:
		with db.cursor() as cur:
			pass

	@staticmethod
	def install_tables(db: Pg) -> None:
		with db.cursor() as cur:
			# Base resource table
			cur.execute("""
				create table if not exists resource
				(
					id int generated by default as identity,
					city_id int,
					resource_type varchar(1),  -- L/M/W/C/S
					inserted_on timestamp default now(),
					unique(city_id, resource_type)
				);
			""")

			# Resource amounts in each city
			cur.execute("""
				create table if not exists resource_amount
				(
					id int generated by default as identity,
					resource_id int not null unique,
					amount int not null,
					updated_on timestamp default now()
				);
			""")

			# Resource production in each city
			cur.execute("""
				create table if not exists resource_production
				(
					id int generated by default as identity,
					resource_id int not null unique,
					amount int not null,
					updated_on timestamp default now()
				);
			""")

			# Resource usage in each city
			cur.execute("""
				create table if not exists resource_usage
				(
					id int generated by default as identity,
					resource_id int not null unique,
					amount int not null,
					updated_on timestamp default now()
				);
			""")

			# Resource maximums in each city
			cur.execute("""
				create table if not exists resource_maximum
				(
					id int generated by default as identity,
					resource_id int not null unique,
					amount int not null,
					updated_on timestamp default now()
				);
			""")

			# Resource target maximums in each city
			cur.execute("""
				create table if not exists resource_target_maximum
				(
					id int generated by default as identity,
					resource_id int not null unique,
					amount int not null,
					updated_on timestamp default now()
				);
			""")

			# Resource target minimums in each city
			cur.execute("""
				create table if not exists resource_target_minimum
				(
					id int generated by default as identity,
					resource_id int not null unique,
					amount int not null,
					updated_on timestamp default now()
				);
			""")

			# Resource target amount in each city
			cur.execute("""
				create table if not exists resource_target_amount
				(
					id int generated by default as identity,
					resource_id int not null unique,
					amount int not null,
					updated_on timestamp default now()
				);
			""")



	@staticmethod
	def install_indexes(db: Pg) -> None:
		with db.cursor() as cur:
			# Base resource table
			cur.execute("""
				create index if not exists resouce_city_id on resource(city_id);

				create index if not exists resource_amount_resource_id on resource_amount(resource_id);
				create index if not exists resource_production_resource_id on resource_production(resource_id);
				create index if not exists resource_usage_resource_id on resource_usage(resource_id);
				create index if not exists resource_maximum_resource_id on resource_maximum(resource_id);
				create index if not exists resource_target_maximum_resource_id on resource_target_maximum(resource_id);
				create index if not exists resource_target_minimum_resource_id on resource_target_minimum(resource_id);
				create index if not exists resource_target_amount_resource_id on resource_target_amount(resource_id);
			""")

	@staticmethod
	def install_pg_functions(db: Pg) -> None:
		with db.cursor() as cur:
			pass  # cur.execute()
