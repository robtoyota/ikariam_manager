import sys
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit import PromptSession

from config import Config
from API.api import API
from shell import Shell


class IkariamManager:
	def __init__(self, config_dict: dict):
		self.config = config_dict

		# Start up the API
		with API(self.config) as self.API:
			# Run the shell session
			self.shell = Shell(self.API)
			self.ps = PromptSession('> ')
			self.inp = ""  # User input
			exit_cmd = False

			# Begin the user input loop
			print("Welcome to Ikariam Manager. Type ? to list commands")
			while not exit_cmd:
				self.inp = self.ps.prompt()
				exit_cmd = self.shell.run_command(self.inp)


if __name__ == '__main__':
	# Defaults
	in_config_file = "config.json"

	# Use the user-supplied config file
	if len(sys.argv) > 1:
		in_config_file = sys.argv[1]

	# Load the config, to be passed on
	config = Config.load_config(in_config_file)

	IkariamManager(config)
