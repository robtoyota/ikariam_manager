from prompt_toolkit import print_formatted_text as print
from prompt_toolkit import PromptSession, prompt

from pg import Pg
from config import Config
from Entities.user import User
from Entities.city import City
from Entities.resource import Resource


class Cmd:
	@staticmethod
	# Create the database and user ONLY (no other DDLs for tables or functions)
	def create_database(config: dict) -> dict:
		print("Enter your postgres server/root login (typically 'postgres'), to create the database.")
		print("The root user credentials are not saved.")

		while True:  # Repeat until successfully connected:
			# Get the connection details
			host = prompt('Postgres Hostname> ')
			port = prompt('Postgres Port> ')
			user = prompt('Postgres root user> ')
			password = prompt('Postgres root password> ', is_password=True)

			# Attempt to create the database and user
			if Pg.create_database(host, port, user, password):
				break  # If successful, exit the loop
			else:
				print("Please double check the information and try to connect again:")

		# Update the config with the new connection details
		config['POSTGRES']['host'] = host
		config['POSTGRES']['port'] = port
		config['POSTGRES']['dbname'] = 'ikariam_manager'
		config['POSTGRES']['user'] = 'ikariam_manager'
		config['POSTGRES']['password'] = 'KhY/z@zaTN~k{&5;!g3+dzj5VmWKJ[.%'

		# Write the new config to disk
		Config.write_config(config)

		# Return the new config
		return config

	@staticmethod
	# Install the DB DDLs for tables/functions/etc
	def install_database(db: Pg) -> bool:
		print("Installing tables...")
		Resource.install_tables(db)
		City.install_tables(db)
		User.install_tables(db)

		print("Installing base functions...")

		print("Installing indexes...")
		Resource.install_indexes(db)
		City.install_indexes(db)
		User.install_indexes(db)

		print("Installing views...")
		Resource.install_views(db)
		City.install_views(db)
		User.install_views(db)

		print("Installing functions...")
		Resource.install_pg_functions(db)
		City.install_pg_functions(db)
		User.install_pg_functions(db)

		print("Installing views...")
