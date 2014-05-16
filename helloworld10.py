#!/opt/python3/bin/python3
import os
import sys
import socket
import warnings
import time
import re
import base64
import mimetypes #Magia que te deja guessear que tipo de contenido es


class mk_socket:
    
    def __init__(self, sid, host, port=21):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        self.sid = str(sid)
        self.open = True
    def cls(self):
        if self.open:
            self.s.close()
            self.open = False
    def relay(self, mes='', expect=False, filt=''):
        self.send(mes, True, filt)
        return self.recv(expect)

    def recv(self, expect=False):
        print ('RESPUESTA')
        
        try:
            rec = self.s.recv(1024)
        except socket.error:
            self.hold_state('Software caused connection abort')
            
        print (rec)

        

        if len(rec) > 3:
            
            if rec[3] == '-':
                return rec+self.recv()
        return rec        

    def send(self, mes='', CRLF=True, filt='',tipo='B'):
        if tipo == 'B':
            print ('ENVIADO')

        try:    
            if tipo == 'A' or tipo == 'B':
                self.s.send(bytes(mes + ('', '\r\n')[CRLF==True], 'UTF-8'))
            else:
                self.s.send(mes)
            # '\r\n' is a <CRLF> (endline), this tells the 
            # server that this is the end of the command
        except socket.error:
            self.hold_state('Connection reset')

        if CRLF: # avoid outputting the file transfers
            if filt:
                print (mes.replace(filt, '*'*len(filt)))
            else:
                print (mes)
    def login(self, user, passwd): #Esta para que el login fuera mas organizado, y la meti a esta clase porque python no es muy amigable con "referencias" D:
        self.relay('USER '+ user)
        sock_main.relay('PASS '+passwd, filt=passwd)
def testa(var):    
    dir = os.listdir(var)
    return dir
def moveinthedirectoryftp(listoffiles,currentdir,auxi='A'):  
    i= 1;
    print("0.- ..")
    for file in listoffiles:
       print(str(i) + ".- " + file)
       i+=1
    print(str((len(listoffiles)+1))+".- Salir")
    input_var = input("Write the number of your file plz: ")
    if input_var == '0':
        CDUP()
        return ''
    elif int(input_var) == (len(listoffiles)+1):
        print("Back to menu it is!")
        return ''
    else:
        currentdir=currentdir+listoffiles[int(input_var) - 1]
        s = listoffiles[int(input_var) - 1]
        if s.find(".") < 0:
            #currentdir += listoffiles[int(input_var) - 1]
            print ("This is a directory! " + s)
            sock_main.relay('CWD '+currentdir, 250)
        else:
            if auxi == 'A':
                recievefile(currentdir, listoffiles[int(input_var) - 1])
            elif auxi == 'B':
                changepermission(s)
            elif auxi == 'X':
                delete(s)
            elif auxi == 'Y':
                rename(s)
        return s
def moveinthedirectory(listoffiles,currentdir,auxi='A'):
    print(auxi)
    i= 1;
    print("0.- ...")
    for file in listoffiles:
       print(str(i) + ".- " + file)
       i+=1
    print(str((len(listoffiles)+1))+".- Salir")
    input_var = input("Write the number of your file plz: ")
    if input_var == '0':
        currentdir = gobackadirectory(currentdir)
        moveinthedirectory(testa(currentdir),currentdir,auxi)
    elif int(input_var) == (len(listoffiles)+1):
        print("Back to menu it is!")
    else:
        s = listoffiles[int(input_var) - 1]
        currentdir += '/'
        if s.find(".") < 0:
            currentdir=currentdir+listoffiles[int(input_var) - 1]
            os.chdir( currentdir )
            print ("This is a directory! " + s)
            moveinthedirectory(testa(currentdir),currentdir,auxi)
        else:
            if auxi == 'A':
                currentdir=currentdir+listoffiles[int(input_var) - 1]
                sendfile(currentdir, listoffiles[int(input_var) - 1])
            elif auxi == 'B':
                moveinthedirectory(testa(currentdir),currentdir,auxi)
def howmanytrips(nof):
    MODE('I')
    n = sock_main.relay("SIZE " + nof)
    n = n.decode()
    n = n.split(" ")
    return n[0]
def recievefile(pof, nof):    
    print ("This is a file! I should be able to recieve it")
    n = howmanytrips(nof)
    modo = asignarmodocorrecto(nof)
    MODE(modo)
    sock_pasv = pasiv()
    sock_main.relay("RETR " + nof)
    aux = "A"
    if modo == 'A':
        target = open (nof, 'w') ## a will append, w will over-write 
    else:
        target = open (nof, 'wb') ## a will append, w will over-write 
    #writing the entered content to the file we just created
    while aux != "":
        aux = sock_pasv.recv()
        if modo == 'A':
            aux = aux.decode()
            target.write(aux)
        else:
            target.write(aux)
            aux = str(aux)
            aux = aux[:-1]
            aux = aux[2:]
        
        
    target.close()
    sock_main.recv()
def sendfile(fsource, fname):    
    print ("This is a file! I should be able to send it")
    MODE(asignarmodocorrecto(fname))
    sock_pasv = pasiv()
    sock_main.relay('STOR '+fname)
    f = open(fname, 'rb')
    size = os.stat(fname)[6]
    opened = 1
    pos = 0
    buff=1024
    
    while opened == 1:
        f.seek(pos)
        pos += buff
        if pos >= size:
            piece = f.read(-1)
            opened = 0
        else:
            piece = f.read(buff) 
        try:
            sock_pasv.send(piece.decode(), False, ' ', 'A')
        except:
            #piece = base64.b64decode(piece)
            #piece = str(piece)
            #piece = piece[:-1]
            #piece = piece[2:]
            tipo = 'I'
            sock_pasv.send(piece, False, ' ','I')
            #print(piece)
    tipo = 'A'
    sock_pasv.cls()
    sock_main.recv(226)
def login(MainSocket, user, passwd):    
    print ("This is a file! I should be able to send it")
def pasiv():
    msg = sock_main.relay('PASV')
    msg = msg.decode("utf-8")
    m = re.search(' \(([0-9]+,[0-9]+,[0-9]+,[0-9]+),([0-9]+),([0-9]+)', msg)
    hostpasivo = m.group(1).replace(",", ".")
    print ("hostpasivo: " + hostpasivo)
    print ("Puerto Pasivo: " + m.group(2))
    print ("Puerto Pasivo: " + m.group(3))
    a = int(m.group(2))
    b = int(m.group(3))
    portpasivo = a*256+b
    print ("Puerto Pasivo: " + str(portpasivo))
    print ("Conexion Pasiva")
    sock_pasv = mk_socket(2, hostpasivo, portpasivo)
    return sock_pasv
def changepermission(pof):
    print("This is a file I should be able to change it's permissions!")
    input_var = input("Write the permission for example 744:")
    sock_main.relay('SITE CHMOD '+input_var + ' ' + pof)
def rename(pof):#De hecho es delete!
    print("This is a file I should be able to KILL IT! (Using fire if possible)")
    sock_main.relay('DELE '+ pof)
def delete(pof):#De hecho es rename!
    print("RENAMING!")
    input_var = input("Write the new name of the file! : ")
    sock_main.relay('RNFR '+ pof)
    sock_main.relay('RNTO '+ input_var)
def listdirectory():
    sock_pasv = pasiv()
    msg2 = sock_main.relay('NLST')
    listado= sock_pasv.recv()  
    listado = str(listado)
    listado = listado[:-5]
    listado = listado[2:]
    list = listado.split("\\r\\n")
    print (list)
    sock_main.recv(226)
    sock_pasv.cls()
    return list
def gobackadirectory(currentdir):
    os.chdir( currentdir )
    print(os.getcwd())
    os.chdir( '..' )
    print(os.getcwd())
    return os.getcwd()
def MODE(m):
    sock_main.relay('TYPE '+m)
def FTPCurrentDirectory():
    var = sock_main.relay('PWD')
    var = str(var)
    var = var.split('"')
    if var[1] == '/':
        return var[1]
    else:
        return var[1]+'/'
def CDUP():#Change Directory UP
    sock_main.relay('CDUP')
def asignarmodocorrecto(filename):
    mime = mimetypes.guess_type(filename)
    print (mime)
    if mime[0] == None:
        return('A')
    if mime[0].find("image") != -1:
        return('I')
    if mime[0].find("audio") != -1:
        return('I')
    return('A')
def openfile(self, name):
    f = open(name, 'rb')
    size = os.stat(name)[6]
    pos = 0
    buff=1024
    f.seek(self.pos)
    pos += buff
    if self.pos >= self.size:
        piece = f.read(-1)
        f.close()
    else:
        piece = f.read(buff)

        

currentdir = os.getcwd()
os.chdir( currentdir ) 
currentdirftp = '/'                 
FTP_PORT = input("Puerto al cual conectarse: ") 
host=  input("host: ")
user= input("user: ")
passwd= input("passwd: ")
sock_main = mk_socket(1, host,int(FTP_PORT))
sock_main.recv()
sock_main.login(user, passwd)
ans=True
print(FTPCurrentDirectory())
while ans:
    print ("""
    1.-Send a file
    2.-Recieve a file or Navigate thru the FTP
    3.-Change Permissions
    4.-Listar directorio del FTP
    5.-Navegar Directorio Local
    6.-Rename
    7.-Delete
    8.-Goodbye
    """)
    ans=input("What would you like to do? ") 
    if ans=="1": 
        moveinthedirectory(testa(os.getcwd()),os.getcwd())
    elif ans=="2":
        moveinthedirectoryftp(listdirectory(),FTPCurrentDirectory())
    elif ans=="3":
        moveinthedirectoryftp(listdirectory(),FTPCurrentDirectory(),'B') 
    elif ans=="4":
        listdirectory()
    elif ans=="5":
        moveinthedirectory(testa(os.getcwd()),os.getcwd(),'B')
    elif ans=="6":
        moveinthedirectoryftp(listdirectory(),FTPCurrentDirectory(),'X') 
    elif ans=="7":
        moveinthedirectoryftp(listdirectory(),FTPCurrentDirectory(),'Y')
    elif ans=="8":
        print("\n Goodbye")        
        ans=False
    elif ans !="":
        print("\n Not Valid Choice Try again")   
