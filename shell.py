class Shell:
	def __init__(self):
		pass

	@staticmethod
	def run_command(inp: str) -> bool:
		inp = Shell.parse_inp(inp)
		return False

	@staticmethod
	def parse_inp(inp: str) -> str:
		pass
