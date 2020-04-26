from pg import Pg


class User:
	@staticmethod
	def list_cities(db: Pg, user_id: int) -> list:
		# Query the list of cities
		with db.cursor() as cur:
			cur.execute(
				"select id, x, y, city_name, resource_type from city where user_id=%s order by list_order",
				(user_id, )
			)

			# Build the list of cities

	@staticmethod
	def add_user(db: Pg, username: str, server: str) -> int:
		# Insert the new user
		with db.cursor() as cur:
			cur.execute(
				"insert into username (username, server) values (%s, %s) on conflict do nothing returning id",
				(username, server)
			)

			# Get the ID of the user
			if cur.rowcount > 0:
				row = cur.fetchone()
				return row['id']
			else:  # If no ID was returned
				# Does the user already exist? Try get the ID:
				cur.execute("select id from username where username=%s and server=%s", (username, server))
				row = cur.fetchone()
				if row['id'] > 0:
					return row['id']
				else:
					return -1

	@staticmethod
	def install_tables(db: Pg) -> None:
		with db.cursor() as cur:
			cur.execute("""
				create table if not exists username
				(
					id int generated by default as identity,
					username text not null,
					server text not null,
					inserted_on timestamp default now(),
					updated_on timestamp default now(),
					unique(username, server)
				);
			""")

	@staticmethod
	def install_indexes(db: Pg) -> None:
		with db.cursor() as cur:
			pass

	@staticmethod
	def install_pg_functions(db: Pg) -> None:
		with db.cursor() as cur:
			pass  # cur.execute()
