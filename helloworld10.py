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
	dir = os.listdir(path=var)
	return dir
def moveinthedirectoryftp(listoffiles,currentdir):  
	i= 1;
	for file in listoffiles:
	   print(str(i) + ".- " + file)
	   i+=1
	input_var = input("Write the number of your file plz: ")	
	currentdir=currentdir+listoffiles[int(input_var) - 1]
	s = listoffiles[int(input_var) - 1]
	if s.find(".") < 0:
		#currentdir += listoffiles[int(input_var) - 1]
		print ("This is a directory! " + s)
		sock_main.relay('CWD '+currentdir, 250)
	else:
		recievefile(currentdir, listoffiles[int(input_var) - 1])
	return s
def moveinthedirectory(listoffiles,currentdir):  
	i= 1;
	print("0.- ...")
	for file in listoffiles:
	   print(str(i) + ".- " + file)
	   i+=1
	input_var = input("Write the number of your file plz: ")
	if input_var == '0':
		currentdir = gobackadirectory(currentdir)
		moveinthedirectory(testa(currentdir),currentdir)
	else:
		currentdir=currentdir+listoffiles[int(input_var) - 1]
		s = listoffiles[int(input_var) - 1]
		if s.find(".") < 0:
			currentdir += '/'
			os.chdir( currentdir )
			print ("This is a directory! " + s)
			moveinthedirectory(testa(currentdir),currentdir)
		else:
			sendfile(currentdir, listoffiles[int(input_var) - 1])
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
asignarmodocorrecto("file.mp3")
currentdir = 'C:/'
os.chdir( currentdir ) 
currentdirftp = '/' 				
FTP_PORT = 21
host='192.100.230.21' 
user='userftp'
passwd='r3d3sf1s1c@s'
sock_main = mk_socket(1, host)
sock_main.recv()  
sock_main.login(user, passwd)
#moveinthedirectory(testa(currentdir),currentdir)
currentdirftp += moveinthedirectoryftp(listdirectory(),currentdirftp)
listdirectory()

#sock_main.relay('MLSD')
#sock_pasv.recv()  

#print (msg)
#newip, newport = self.handle.parse_pasv(msg)
# make passive connection
#self.sock_pasv = mk_socket(2, newip, newport)