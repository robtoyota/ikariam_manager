from prompt_toolkit import print_formatted_text as print


class Util:
	@staticmethod
	def error(self, msg: str) -> None:
		print(f"==Error: {msg}")

	@staticmethod
	def warning(self, msg: str) -> None:
		print(f"==Warning: {msg}")

	@staticmethod
	def success(self, msg: str) -> None:
		print(f"{msg}")

	@staticmethod
	def message(self, msg: str) -> None:
		print(f"{msg}")
