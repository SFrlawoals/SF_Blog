from pwn import*
p = process('./user_admin')

def choice(sel):
    p.sendlineafter('Enter your choice: ',str(sel))

def create(age,name):
    choice(0)
    p.sendlineafter('Enter age of user: ',str(age))
    p.sendlineafter('Enter username: ',name)

def edit(age,name):
    choice(1)
    p.sendlineafter('Enter age of user: ',str(age))
    p.sendlineafter('Enter username: ',name)

def delete():
    choice(2)

def send(message):
    choice(3)
    p.sendlineafter('Enter message to be sent:\n',message)
    
create(10,'A'*0x10)
create(20,'B'*0x8)
#delete()

p.interactive()
