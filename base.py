from pwn import *
from time import sleep
import sys

process_name = ""
host = ""
port = 0

# libc = ELF("./libc.so.6")


def get_stream(process_type):
	if process_type == "local":
		return process(process_name)
	elif process_type == "remote":
		return remote(host=host, port=port)
	elif process_type == "ssh":
		remote_user = ""
		remote_password = ""
		server = ssh(host=host, user=remote_user, password=remote_password)
		return server.process(remote_process_name)
	raise Exception("Invalid process type.")


def init():
	if "libc" in globals():
		libc.address = 0
	context.os = 'linux'
	context.arch = 'amd64'
	context.terminal = ["~/bin/wterminal"]


def solve(io):
	io.readline()


def main():
	init()
	if len(sys.argv) <= 1:
		raise Exception("solve.py (local|remote|ssh)")

	io = get_stream(sys.argv[1])

	if len(sys.argv) > 2 and sys.argv[2] == "debug":
		gdb_command = [
			"b *main",
			"c"
		]
		gdb.attach(io, "\n".join(gdb_command))

	solve(io)
	io.interactive()

def force(io):
	while 1:
		try:
			main()
		except Exception as e:
			if sys.argv[1] != "local":
				sleep(1)
			print(e)
			continue

main()