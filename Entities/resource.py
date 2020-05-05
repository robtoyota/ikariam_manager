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
	def set_value(column: str, db: Pg, city_id: int, resource_type: str, amount: int) -> bool:
		# Validate the input
		if not (
			isinstance(city_id, int)
			and city_id > 0
			and resource_type in ['B', 'W', 'M', 'C', 'S']
			and isinstance(amount, int)
			and amount > 0
		):
			print("Error: Invalid values")
			return False
		
		# Whitelist the column to be updated
		if column not in ['amount', 'maximum', 'production', 'target_amount', 'target_maximum', 'target_minimum', 'usage']:
			print(f"Error: Invalid column: {column}")
			return False

		# Upsert the change
		with db.cursor() as cur:
			cur.execute(
				"""
					-- Get the ID of the resource
					with r as (
						select id
						from resource
						where city_id=%(city_id)s and resource_type=%(resource_type)s
					)
					-- Insert the value row if it does not already exist
					insert into resource_""" + column + """
						(resource_id, amount)
					select id, %(amount)s from r
					-- If it exists already, then update the value
					on conflict (resource_id)
					do update 
					set amount = excluded.amount
				""",
				{
					'city_id': city_id,
					'resource_type': resource_type,
					'amount': amount,
				}
			)

	@staticmethod
	def install_tables(db: Pg) -> None:
		with db.cursor() as cur:
			# Base resource table
			cur.execute("""
				create table if not exists resource
				(
					id int generated by default as identity,
					city_id int,
					resource_type varchar(1),  -- B/W/M/C/S
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
	def install_views(db: Pg) -> None:
		with db.cursor() as cur:
			# resource_detail
			cur.execute("""
				create or replace view resource_detail as
				select
					r.id as resource_id, c.user_id, usr.server, usr.username, r.city_id, c.city_name, r.resource_type
					, coalesce(amt.amount, 0) as amount
					, coalesce(mx.amount, 0) as maximum
					, coalesce(prd.amount, 0) as production
					, coalesce(tamt.amount, 0) as target_amount
					, coalesce(tmx.amount, 0) as target_maximum
					, coalesce(tmn.amount, 0) as target_minimum
					, coalesce(usg.amount, 0) as usage
					, (
						coalesce(amt.amount, 0)  
						+ (
							(coalesce(prd.amount, 0)-coalesce(usg.amount, 0))
							* floor(extract(epoch from now()-amt.updated_on) / (60*60))
						)
					)::int  as predicted_amount
				from
					resource r
					join city c
						on (c.id=r.city_id)
					join username usr
						on (usr.id=c.user_id)
					left join resource_amount amt
						on (amt.resource_id=r.id)
					left join resource_maximum mx
						on (mx.resource_id=r.id)
					left join resource_production prd
						on (prd.resource_id=r.id)
					left join resource_target_amount tamt
						on (tamt.resource_id=r.id)
					left join resource_target_maximum tmx
						on (tmx.resource_id=r.id)
					left join resource_target_minimum tmn
						on (tmn.resource_id=r.id)
					left join resource_usage usg
						on (usg.resource_id=r.id)
			""")

	@staticmethod
	def install_pg_functions(db: Pg) -> None:
		with db.cursor() as cur:
			pass  # cur.execute()
