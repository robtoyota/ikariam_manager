from pg import Pg


class User:
	@staticmethod
	def install_tables(db: Pg) -> None:
		with db.cursor() as cur:
			cur.execute("""
				create table if not exists user
				(
					id int generated by default as identity,
					username text,
					server text,
					inserted_on timestamp,
					updated_on timestamp
				);
			""")

	@staticmethod
	def install_indexes(db: Pg) -> None:
		with db.cursor() as cur:
			cur.execute("""
				create index if not exists user_username on user(username);
			""")

	@staticmethod
	def install_pg_functions(db: Pg) -> None:
		with db.cursor() as cur:
			pass  # cur.execute()
