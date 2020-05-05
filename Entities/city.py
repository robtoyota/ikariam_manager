from pg import Pg


class City:
	def __init__(self, properties: dict):
		self.city_id = properties.get('city_id', 0)
		self.user_id = properties.get('user_id', 0)
		self.x = properties.get('x', 0)
		self.y = properties.get('y', 0)
		self.city_name = properties.get('city_name', "")
		self.list_order = properties.get('list_order', 0)
		self.resource_type = properties.get('resource_type', "")
		self.city_level = properties.get('city_level', 0)
		self.population = properties.get('population', 0)
		self.max_population = properties.get('max_population', 0)
		self.satisfaction = properties.get('satisfaction', 0)
		self.action_points_available = properties.get('action_points_available', 0)

	@staticmethod
	def add_city(db: Pg, x: int, y: int, city_name: str, user_id: int) -> int:
		# Insert the new user
		with db.cursor() as cur:
			cur.execute(
				"""
					insert into city (x, y, city_name, user_id, list_order) 
					values (
						%(x)s, %(y)s, %(city_name)s, %(user_id)s,
						(select coalesce(max(list_order), 0) + 1 from city where user_id=%(user_id)s)
					) 
					on conflict do nothing returning id
				""",
				{'x':x, 'y':y, 'city_name':city_name, 'user_id':user_id}
			)

			# If city was created:
			if cur.rowcount > 0:
				row = cur.fetchone()

				# Insert each of the resource types
				for r in ['B', 'W', 'M', 'C', 'S']:
					cur.execute(
						"insert into resource (city_id, resource_type) values (%s, %s) on conflict do nothing", 
						(row['id'], r)
					)
				# Return the ID of the new city row
				return row['id']
			# If no ID was returned
			else:
				# Does the city already exist? Try get the ID:
				cur.execute("select id from username where x=%s and y=%s and city_name=%s and user_id=%s", (x, y, city_name, user_id))
				row = cur.fetchone()
				if row['id'] > 0:  # Return the ID of the existing row
					return row['id']
				else:
					return -1  # Error

	@staticmethod
	def set_resource_type(db: Pg, city_id: int, resource_type: str) -> None:
		# Update the city_type
		with db.cursor() as cur:
			cur.execute("update city set resource_type=%s where id=%s", (resource_type, city_id))

	@staticmethod
	def move_city(db: Pg, city_id: int, x: int, y: int) -> None:
		# Update the coordinates
		with db.cursor() as cur:
			cur.execute("update city set x=%s, y=%s where id=%s", (x, y, city_id))

	@staticmethod
	def install_tables(db: Pg) -> None:
		with db.cursor() as cur:
			cur.execute("""
				create table if not exists city
				(
					id int generated by default as identity,
					user_id int not null,
					x int not null,
					y int not null,
					city_name text null,
					list_order int null,
					resource_type varchar(1),  -- W/M/C/S
					city_level int null,
					population int null,
					max_population int null,
					satisfaction int null,
					action_points_available int null,
					inserted_on timestamp default now(),
					updated_on timestamp default now(),
					unique(user_id, x, y, city_name)
				);
			""")

	@staticmethod
	def install_indexes(db: Pg) -> None:
		with db.cursor() as cur:
			cur.execute("""
				create index if not exists city_x on city(x);
				create index if not exists city_y on city(y);
				create index if not exists city_city_name on city(city_name);
				create index if not exists city_user_id on city(user_id);
			""")

	@staticmethod
	def install_views(db: Pg) -> None:
		with db.cursor() as cur:
			cur.execute("""
				create or replace view city_detail as
				with r as (
					select
						server, username, user_id, city_id,
						max(case when(resource_type='B') then predicted_amount else 0 end) as building_material, 
						max(case when(resource_type='W') then predicted_amount else 0 end) as wine, 
						max(case when(resource_type='M') then predicted_amount else 0 end) as marble, 
						max(case when(resource_type='C') then predicted_amount else 0 end) as crystal, 
						max(case when(resource_type='S') then predicted_amount else 0 end) as sulfur 
					from resource_detail
					group by
						server, username, user_id, city_id 
				)
				select
					c.id as city_id, c.user_id, c.x, c.y, c.city_name, r.server, r.username, c.resource_type,
					r.building_material, r.wine, r.marble, r.crystal, r.sulfur,
					c.city_level, c.population, c.max_population, c.satisfaction, c.action_points_available, c.list_order
				from
					city c
					join r
						on (c.id=r.city_id)
				order by c.user_id, c.list_order
			""")

	@staticmethod
	def install_pg_functions(db: Pg) -> None:
		with db.cursor() as cur:
			pass  # cur.execute()
