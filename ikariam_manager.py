from prompt_toolkit import print_formatted_text as print
from prompt_toolkit import PromptSession
from api import API
from shell import Shell


class IkariamManager:
	def __init__(self):
		# Start up the API
		self.API = API()

		# Run the shell session
		self.ps = PromptSession('> ')
		self.inp = ""  # User input
		exit_cmd = False
		print("Welcome to Ikariam Manager. Type ? to list commands")
		while not exit_cmd:
			self.inp = self.ps.prompt()
			exit_cmd = Shell.run_command(self.inp)


if __name__ == '__main__':
	IkariamManager()
