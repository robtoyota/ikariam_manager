from pg import Pg
from API.cmd import Cmd
from API.util import Util


class API:
	def __init__(self, config_dict):
		# Load the config that was provided
		self.config = config_dict

	def __enter__(self):
		# Connect to the DB
		self.db = Pg(self.config)

		# Load the child libraries
		self.Cmd = Cmd(self.db)
		self.Util = Util()

		# Return yo'self
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		# Close the DB when done with this instance
		self.db.close()
