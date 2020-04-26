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
