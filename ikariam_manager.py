import sys
from prompt_toolkit import print_formatted_text as print

from config import Config
from pg import Pg
from Shell.shell import Shell
from Shell.cmd import Cmd


class IkariamManager:
	def __init__(self, config_dict: dict):
		self.config = config_dict

		# Start up the API
		with Pg(self.config) as self.db:
			# Run the shell session
			self.shell = Shell(self.config, self.db)
			exit_cmd = False

			# Begin the user input loop
			print("Welcome to Ikariam Manager. Type ? to list commands")
			while not exit_cmd:
				exit_cmd = self.shell.run_command()


if __name__ == '__main__':
	# Defaults
	in_config_file = "config.json"

	# Use the user-supplied config file
	if len(sys.argv) > 1:
		in_config_file = sys.argv[1]

	# Load the config, to be passed on
	config = Config.load_config(in_config_file)

	# Install the DB if necessary
	if not config['POSTGRES']['dbname']:
		config = Cmd.create_database(config)

	IkariamManager(config)
