from prompt_toolkit import print_formatted_text as print
from prompt_toolkit import PromptSession, prompt

from pg import Pg
from config import Config
from city import City
from resource import Resource

class Cmd:
	@staticmethod
	def install_database(config: dict) -> bool:
		print("Enter your postgres server/root login (typically 'postgres'), to create the database.")
		print("The root user credentials are not saved.")

		while True:  # Repeat until successfully connected:
			# Get the connection details
			host = prompt('Postgres Hostname> ')
			port = prompt('Postgres Port> ')
			user = prompt('Postgres root user> ')
			password = prompt('Postgres root password> ', is_password=True)

			# Attempt to create the database and user
			if Pg.install_database(host, port, user, password):
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
