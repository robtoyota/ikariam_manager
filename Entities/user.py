class User:
	@staticmethod
	def install_tables(db) -> None:
		with db.cursor() as cur:
			cur.execute("""
				create table if not exists user
				(
					id int generated by default as identity,
					username text,
					server text,
					inserted_on,
					updated_on
				);
			""")

	@staticmethod
	def install_indexes(db) -> None:
		with db.cursor() as cur:
			cur.execute("""
				create index if not exists user_username on user(username);
			""")

	@staticmethod
	def install_pg_functions(db) -> None:
		with db.cursor() as cur:
			pass  # cur.execute()
