from prompt_toolkit import print_formatted_text as print
from prompt_toolkit import PromptSession

from API.api import API


class Shell:
	def __init__(self, api: API, ps: PromptSession):
		self.api = api
		self.ps = ps

	def run_command(self, inp: str) -> bool:
		# Parse the input
		if len(inp.strip()) > 0:
			cmd, args = self.parse_inp(inp)
		else:
			return False  # No command provided, but don't stop running the program

		# Run the commands
		cmd = inp[0]
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
