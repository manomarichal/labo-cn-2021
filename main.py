from parser import Parser
parser = Parser()
parser.parse_file("test.txt")
print(parser.total_uptime)
print(parser.total_downtime)