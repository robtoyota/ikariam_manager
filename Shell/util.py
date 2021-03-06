from prompt_toolkit import print_formatted_text as print
import re


class Util:
	# Output message methods
	@staticmethod
	def error(msg: str) -> None:
		print(f"==Error: ", msg)

	@staticmethod
	def warning(msg: str) -> None:
		print(f"==Warning: ", msg)

	@staticmethod
	def success(msg: str) -> None:
		print(msg)

	@staticmethod
	def message(msg: str) -> None:
		print(msg)

	# Parsing methods
	@staticmethod
	def parse_city_square_brackets(coords_name: str) -> dict:
		# Input is a string with the format: [xx:yy] CityName
		# Output is a dict(x:xx, y:yy, name:CityName)
		
		coords_name = coords_name.strip()
		try:
			city = re.search('^\[(\d{2}):(\d{2})\] (.+)$', coords_name)
			x = city.group(1)
			y = city.group(2)
			city_name = city.group(3)
		except (IndexError, AttributeError):
			return {'error': "City format was incorrect"}

		return {'x': x, 'y': y, 'city_name': city_name}
	
	@staticmethod
	def resource_name(resource_type: str) -> str:
		# Convert a resource type short form into the full name
		# Example: input = 'M', output = 'Marble'
		names = {
			'B': 'Building Material',
			'W': 'Wine',
			'M': 'Marble',
			'C': 'Crystal',
			'S': 'Sulfur',
		}
		
		# Return the name of the resource
		try:
			return names[resource_type]
		except KeyError:
			return ''

	@staticmethod
	def parse_resource_amount(amount: str) -> int:
		# Sanitize the resource value
		# Example: "10,000" becomes 10000, or "1,500K" becomes 1500000
		
		amount = amount.strip().replace(',', '')
		if not amount:  # Skip blank amounts
			return None

		# Handle cases of more than 1 million resources
		multiplier = 1  # Default to not multiply
		if amount[-1] == "k":  # Does the number end in "K"?
			amount = amount[:-1]  # Strip off the "K"
			multiplier = 1000

		# Validate the value
		try:
			amount = int(amount)
			amount *= multiplier  # Handle "K" suffix for 1+ million
		except (ValueError, TypeError):
			amount = None
		
		return amount
	
	@staticmethod
	def parse_resource_amount_listing(resources: str) -> dict:
		# Accepts 5 lines of numbers, and returns a dict of each resource's value
		
		# Prep the vars
		r_name = ['B', 'W', 'M', 'C', 'S']
		i = 0
		output = {}

		# Loop through each line and push it into 
		for amount in resources.split("\n"):
			# Set the current resource's amount
			output[r_name[i]] = Util.parse_resource_amount(amount)
			i += 1

		# Return the dict of each resource's amounts
		return output
