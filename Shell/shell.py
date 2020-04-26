from prompt_toolkit import print_formatted_text as print, HTML
from prompt_toolkit import PromptSession

from Shell.util import Util
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
		self.ps = PromptSession()

		# Set the session variables
		self.user_id = 1  # ID from the user table
		self.city_id = 0  # ID from the city table

	def run_command(self) -> bool:
		# Prompt for the input command from the user
		inp = self.ps.prompt('> ')

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
					Util.success(f"Current user has been set to {args[0]}: {args[1]}")
			else:
				Util.error("Server and Username are required")

		# Add cities
		elif cmd == "city":
			Util.message(HTML("Paste the name in the format <b>[xx:yy] CityName</b>. Enter a blank line to stop entering cities."))
			# Request each city, one by one
			while True:
				city_inp = self.ps.prompt('Add City> ')  # Get the input
				city_inp = city_inp.strip()

				# Check if the user entered a blank input, to break the loop
				if not city_inp:
					break

				# Parse the input for the city to extract the coordinates and name
				city = Util.parse_city_square_brackets(city_inp)
				if "error" in city:
					Util.error(city['error'])
					continue

				# Insert the city
				city_id = City.add_city(db=self.db, x=city['x'], y=city['y'], city_name=city['city_name'], user_id=self.user_id)
				if city_id > 0:
					Util.success("City has been added.")
				else:
					Util.error("There was an error adding the city")
					continue


	def do_set(self, inp: str) -> None:
		# Determine what needs to be set:
		cmd, args = self.split_cmd_arg(inp)

		# Set the resource amounts
		if cmd == "resource":
			Util.message("Paste your resources for each city, or press [Enter] to skip")
			# Loop through each city and get its values
			for city in User.city_list(self.db, self.user_id):
				# Get the list of resources as input
				resources = self.ps.prompt(f"{city['city_name']} resources> ")

				# Parse the input into each resource
				amounts = Util.parse_resource_amount_listing(resources)

				# Make sure all resources are accounted for
				if len(amounts) != 5:
					Util.error("Missing resource values. Skipping to the next city.")
					continue

				# Loop through each resource type, and set each value
				for r in ['B', 'W', 'M', 'C', 'S']:
					Resource.set_amount(self.db, city['id'], r, amounts[r])

			Util.success("All resources have been updated.")

		elif cmd == "city":
			pass
