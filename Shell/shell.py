from prompt_toolkit import print_formatted_text as print
from prompt_toolkit import PromptSession

from API.api import API


class Shell:
	def __init__(self, api: API):
		# Set the object for making API calls
		self.api = api

		# Create the prompt session
		self.ps = PromptSession('> ')

	def run_command(self) -> bool:
		# Prompt for the input command from the user
		inp = self.ps.prompt()

		# Validate the input
		if len(inp.strip()) > 0:
			# Split the input into a cmd and its args
			cmd, args = self.parse_inp(inp)
		else:
			return False  # No command provided, but don't stop running the program

		# Run the command
		# TODO: Make this dynamic
		if cmd == "add_city":
			return self.do_upsert_city(args)

		return False  # Don't stop running the program

	def parse_inp(self, inp: str) -> list:
		inp = inp.strip().split(maxsplit=1)  # Split the cmd and the arg
		if len(inp) == 1:  # Was there only a cmd?
			inp.append('')  # Add a blank arg
		return inp

	def do_upsert_city(self, args: str) -> bool:
		# Parse the coordinates and (optionally) the name

		self.api.Cmd.upsert_city(args)
		return False  # Do not exit the program
