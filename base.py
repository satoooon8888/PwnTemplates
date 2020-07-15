from pwn import *
import sys

process_name = ""
host = ""
port = 0
arch_bit = 64

if len(sys.argv) < 1:
	raise Exception("solve.py (local|remote|ssh)")

def get_stream(process_type):
	if process_type == "local":
		return process(process_name)
	elif process_type == "remote":
		return remote(host=host, port=port)
	elif process_type == "ssh":
		name = ""
		password = ""
		host = ""
		remote_process_name = ""
		server = ssh(host=host, user=name, password=password)
		return server.process(remote_process_name)
	raise Exception("Invalid process type.")

def pack(content):
	if arch_bit == 32:
		return p32(content)
	elif arch_bit == 64:
		return p64(content)
	else:
		raise Exception("No support this architecture.")

def solve(io):
	io.readline()


def main():
	io = get_stream(sys.argv[1])
	solve(io)
	io.interactive()

main()