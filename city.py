class City:
	@staticmethod
	def install_tables(db) -> None:
		with db.cursor() as cur:
			pass # cur.execute()

	@staticmethod
	def install_indexes(db) -> None:
		with db.cursor() as cur:
			pass # cur.execute()

	@staticmethod
	def install_pg_functions(db) -> None:
		with db.cursor() as cur:
			pass # cur.execute()
