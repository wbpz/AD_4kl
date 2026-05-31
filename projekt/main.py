from enum import Enum
import sys
import server, client

class Mode(Enum):
	CLIENT = 1
	SERVER = 2


def parse_args() -> Mode:
	mode = Mode.CLIENT
	for i in range(1, len(sys.argv)):
		match sys.argv[i]:
				case "server": mode = Mode.SERVER
	return mode

def main():
	mode = parse_args()
	print(mode)
	match mode:
		case Mode.CLIENT:
			client.Client().run()
		case Mode.SERVER:
			server.main()


if __name__ == "__main__":
	main()
