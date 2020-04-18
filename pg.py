import psycopg2
import psycopg2.extras


class Pg:
	# connect to postgres
	def __init__(self, config: dict):
		self.connection = psycopg2.connect(
			host=config['POSTGRES']['host'],
			port=config['POSTGRES']['port'],
			dbname=config['POSTGRES']['dbname'],
			user=config['POSTGRES']['user'],
			password=config['POSTGRES']['password'],
			cursor_factory=psycopg2.extras.DictCursor,  # Return dicts instead of tuples
		)

		# Enable autocommit by default.
		# Some thoughts: Both the database design and the Python code is crafted to not require rollbacks.  Whenever
		# 	multiple statements in a transaction are require, they should be occurring within a database proc.
		# 	This also helps to enforce the practice of keeping the number of DB calls to a minimum by placing multiple
		# 	queries only within DB procs or functions.
		self.connection.autocommit = True

	def __enter__(self):
		return self.connection

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.close()

	def close(self):
		self.connection.close()
	
	@staticmethod
	def create_database(host: str, port: str, user: str, password: str) -> bool:
		# Connect to the DB
		try:
			with psycopg2.connect(host=host, port=port, user=user, password=password, dbname='postgres') as db:
				db.autocommit = True
				with db.cursor() as cur:
					# Create the user
					cur.execute("""
						create role ikariam_manager
						with
							encrypted password 'KhY/z@zaTN~k{&5;!g3+dzj5VmWKJ[.%'
							login;
					""")

					# Create the DB
					cur.execute("""
						create database ikariam_manager
						with
							owner = ikariam_manager
							encoding = 'UTF8'
							connection limit = -1;
					""")

					return True
		except psycopg2.OperationalError:  # Could not connect
			return False
