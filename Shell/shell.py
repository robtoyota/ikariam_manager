from prompt_toolkit import print_formatted_text as print
from prompt_toolkit import PromptSession

from pg import Pg
from Shell.cmd import Cmd
from Entities.user import User
from Entities.city import City
from Entities.resource import Resource


class Shell:
	def __init__(self, config: dict, db: Pg):
		# Save the passed variables
		self.config = config
		self.db = db

		# Create the prompt session
		self.ps = PromptSession('> ')

		# Set the session variables
		self.user_id = 1  # ID from the user table
		self.city_id = 0  # ID from the city table

	def run_command(self) -> bool:
		# Prompt for the input command from the user
		inp = self.ps.prompt()

		# Validate the input
		if len(inp.strip()) > 0:
			# Split the input into a cmd and its args
			cmd, args = self.split_cmd_arg(inp)
		else:
			return False  # No command provided, but don't stop running the program

		# Run the command
		cmd_response = None  # Default value
		# TODO: Make this dynamic
		if cmd == "exit":
			cmd_response = True
		elif cmd == "install":
			self.do_install_database()
		elif cmd == "add":
			self.do_add(args)
		elif cmd == "set":
			self.do_set(args)

		if not cmd_response:
			return False  # Don't stop running the program
		else:
			return True  # Exit the program

	def split_cmd_arg(self, inp: str) -> list:
		# Accepts a string and separates the first word from the rest of the text
		inp = inp.strip().split(maxsplit=1)  # Split the cmd and the arg
		if len(inp) == 1:  # Was there only a cmd?
			inp.append('')  # Add a blank arg
		return inp

	def split_args(self, args: str) -> list:
		# Accepts a list of args, and returns a list of its items
		arg_split = args.strip().split()
		return arg_split

	def error(self, msg: str) -> None:
		print(f"==Error: {msg}")

	def warning(self, msg: str) -> None:
		print(f"==Warning: {msg}")

	def success(self, msg: str) -> None:
		print(f"{msg}")

	def message(self, msg: str) -> None:
		print(f"{msg}")

	def do_install_database(self) -> None:
		# Install the database tables/functions/etc
		Cmd.install_database(self.db)

	def do_add(self, inp: str) -> None:
		# Determine what needs to be added:
		cmd, inp_args = self.split_cmd_arg(inp)

		# Add users
		if cmd == "user":
			# add user [server] [username]
			# Get the username and server from the input
			args = self.split_args(inp_args)
			if len(args) == 2:  # Make sure both values are set:
				response = User.add_user(db=self.db, server=args[1], username=args[0])
				if response > 0:
					self.user_id = response
					self.success(f"Current user has been set to {args[0]}: {args[1]}")
			else:
				self.error("Server and Username are required")
		# Add cities
		if cmd == "city":
			pass

	def do_set(self, inp: str) -> None:
		# Determine what needs to be set:
		cmd, args = self.split_cmd_arg(inp)

		if cmd == "resource":
			pass
		if cmd == "city":
			pass
