# TP3 - Tomás Gruning, Lucía Godoy, Joaquin Raffaelli, Baremboum Micaela, Rafael Ghione Nazabal
import random
import pickle
import io
import os
from datetime import datetime, timedelta
from pwinput import pwinput
from random import randint
from time import sleep

## En caso de no querer mantener una sesion activa
## cambiar este valor a 0
vto_horas = 48

#CONSTANTES 
menu = '''
 ------------------------------
 | 1. Gestionar mi perfil     |
 | 2. Gestionar candidatos    |
 | 3. Matcheos                |
 | 4. Reportes estadisticos   |
 | 0. Cerrar Sesion           |
 ------------------------------
'''
menu1 = '''
 ------------------------------------
 | Gestionar mi perfil              |
 |                                  |
 | a. Editar mis datos personales   |
 | b. Eliminar mi perfil            |
 | c. Volver                        |
 ------------------------------------
'''
menu2 = '''
 ------------------------------
 | Gestionar candidatos       |
 |                            |
 | a. Ver candidatos          |
 | b. Reportar un candidato   |
 | c. Volver                  |
 ------------------------------
'''

menu_mod = '''
 ------------------------------
 | 1. Gestionar usuarios      |
 | 2. Gestionar reportes      |
 | 3. Reportes estadisticos   |
 | 0. Cerrar Sesion           |
 ------------------------------
'''
menu_mod1 = '''
 ---------------------------
 | Gestionar usuarios      |
 |                         |
 | a. Desactivar usuario   |
 | b. Volver               |
 ---------------------------
'''
menu_mod2 = '''
 ------------------------
 | Gestionar reportes   |
 |                      |
 | a. Ver reportes      |
 | b. Volver            |
 ------------------------
'''

menu_admin1 = '''
 ------------------------------------
 | Gestionar usuarios               |
 |                                  |
 | a. Eliminar usuario o moderador  |
 | b. Dar de alta moderador         |
 | c. Desactivar usuario            |
 | d. Volver                        |
 ------------------------------------
'''

menu_inicio = '''
 ---------------
 | Bienvenido  |
 ---------------
   1. Log in
   2. Sign up

  Bonus
   3. Ruleta
   4. Edades
   5. Matcheos combinados

   0. Salir
'''

#DATOS
##CLASES
class Usuario:
	def __init__(self):
		self.id = -1
		self.estado = True
		self.nombre = ' '.ljust(32, ' ')
		self.email = ' '.ljust(32, ' ')
		self.contraseña = ' '.ljust(32, ' ')
		self.fecha_nacimiento = ' '.ljust(10, ' ')
		self.biografia = ' '.ljust(255, ' ')
		self.hobbies = ' '.ljust(255, ' ')

class Moderador:
	def __init__(self):
		self.id = -1
		self.estado = True
		self.email = ' '.ljust(32, ' ')
		self.contraseña = ' '.ljust(32, ' ')

class Administrador:
	def __init__(self):
		self.id = -1
		self.email = ' '.ljust(32, ' ')
		self.contraseña = ' '.ljust(32, ' ') 

class Reporte:
	def __init__(self):
		self.id_reportante = -1
		self.id_reportado = -1
		self.id_responsable = -1
		self.motivo = ' '.ljust(255, ' ')
		self.estado = 0
		self.rol = 0

class Like:
    def __init__(self):
        self.id_remitente = 0
        self.id_destinatario = 0

class Cookie:
	def __init__(self):
		self.time = None
		self.rol = 0
		self.id = None

# Inicializacion de la carpeta y las rutas de los archivos
if not os.path.exists('data'):
	os.makedirs('data')
afUsuarios = './data/usuarios.dat'
afModeradores = './data/moderadores.dat'
afAdmins = './data/administradores.dat'
afLikes = './data/likes.dat'
afReportes = './data/reportes.dat'
afCookie = './data/cookie.dat'

cookie = Cookie()
cant_usuarios, cant_moderadores, cant_reportes = 0, 0, 0

#FUNCIONES
def generar_likes(test):
	alLikes = open(afLikes, "w+b")
	if test:
		for _ in range((cant_usuarios-1) * (cant_usuarios-2)):
			repetido = True
			while repetido:
				like = Like()
				like.id_remitente, like.id_destinatario = 0, 0
				while like.id_remitente == like.id_destinatario:
					like.id_remitente = randint(0, cant_usuarios-1)
					like.id_destinatario = randint(0, cant_usuarios-1)
				
				repetido = False

				if os.path.getsize(afLikes) > 0:
					alLikes.seek(0, 0)
					while alLikes.tell() < os.path.getsize(afLikes) and not repetido:
						reg = pickle.load(alLikes)
						if (reg.id_remitente == like.id_remitente) and \
							(reg.id_destinatario == like.id_destinatario): repetido = True

			alLikes.seek(0, 2)
			pickle.dump(like, alLikes)
		alLikes.close()
def inicializacion(test=False):
	global usuarios, moderadores, administradores, likes, reportes, cookie 
	global cant_usuarios, cant_moderadores, cant_reportes
	
	# Carga de usuarios
	if os.path.exists(afUsuarios):
		cant_usuarios = contar_registros(afUsuarios)
		
	else:
		alUsuarios = open(afUsuarios, "w+b")
		nombres = ['Martin', 'Juila', 'Luis', 'Rafael', 'Laura', 'Juan']

		for n in range(len(nombres)): 
			usuario = Usuario()
			usuario.id = n
			usuario.nombre = nombres[n].ljust(32, ' ')
			usuario.email = f'estudiante{n+1}@ayed.com'.ljust(32, ' ')
			usuario.contraseña = f'{n+1}{n+1}{n+1}{(n+1)*2}{(n+1)*2}{(n+1)*2}'.ljust(32, ' ')
			usuario.fecha_nacimiento = f'200{randint(0, 5)}-03-07'
		
			pickle.dump(usuario, alUsuarios)
			cant_usuarios += 1
		alUsuarios.close()

	# Carga de moderadores
	if os.path.exists(afModeradores):
		cant_moderadores = contar_registros(afModeradores)
	else:
		alModeradores = open(afModeradores, "w+b")

		for n in range(3): 
			moderador = Moderador()
			moderador.id = n
			moderador.estado = True
			moderador.email = f'moderador{n+1}@ayed.com'.ljust(32, ' ')
			moderador.contraseña = f'mod{n+1}{n+1}{n+1}{(n+1)*2}{(n+1)*2}{(n+1)*2}'.ljust(32, ' ')
		
			pickle.dump(moderador, alModeradores)
			cant_moderadores += 1
		alModeradores.close()

	# Carga de administradores
	if not os.path.exists(afAdmins):
		alAdmins = open(afAdmins, "w+b")
		
		administrador = Administrador()
		administrador.id = 0
		administrador.estado = True
		administrador.email = 'administrador1@ayed.com'.ljust(32, ' ')
		administrador.contraseña = 'admin111222'.ljust(32, ' ')
		
		pickle.dump(administrador, alAdmins)
		alAdmins.close()
	
	# Carga de likes 
	if not os.path.exists(afLikes): generar_likes(test)

	# Carga de reportes
	if os.path.exists(afReportes):
		cant_reportes = contar_registros(afReportes)
	else:
		alReportes = open(afReportes, "w+b")
		if test:
			for _ in range(20):
				reporte = Reporte()

				reporte.id_reportante, reporte.id_reportado = 0, 0
				while reporte.id_reportante == reporte.id_reportado:
					reporte.id_reportante = randint(0, cant_usuarios-1)
					reporte.id_reportado = randint(0, cant_usuarios-1)

				reporte.motivo = ' '.ljust(255, ' ')
				reporte.id_responsable = randint(0, cant_moderadores-1)
				reporte.estado = randint(0, 2)
				
				pickle.dump(reporte, alReportes)
				cant_reportes += 1
		alReportes.close()

	# Carga de ultima sesion
	if os.path.exists(afCookie):
		alCookie = open(afCookie, "r+b")
		cookie = pickle.load(alCookie)

		if datetime.now() >= cookie.time:
			os.remove(afCookie)
		
		alCookie.close()

##ESTETICA
def limpiar():
	os.system('cls' if os.name == 'nt' else 'clear')
def mensaje_error(mensaje: str):
	print('\x1b[1;31m'+' (*) ' + mensaje + '\033[0;m\n')
def mensaje_advertencia(mensaje: str):
	print('\x1b[1;33m'+' (*) ' + mensaje + '\033[0;m\n')
def ptos_suspensivos(mensaje=' Saliendo'):
	print(mensaje, end='', flush=True)
	for _ in range(3):
		sleep(1)
		print('.', end='', flush=True)
	sleep(2)

##LIKES
def agregar_like(id_remitente, id_destinatario):
	alLikes = open(afLikes, "r+b")
	like = Like()
	like.id_remitente = id_remitente
	like.id_destinatario = id_destinatario
	
	alLikes.seek(0,2)
	pickle.dump(like, alLikes)

	alLikes.close()

def verificar_like(id_remitente, id_destinatario):
	if os.path.exists(afLikes):
		alLikes = open(afLikes, "r+b")
		tam = os.path.getsize(afLikes)

		while alLikes.tell() < tam:
			reg = pickle.load(alLikes)
			if reg.id_remitente == id_remitente and reg.id_destinatario == id_destinatario:
				alLikes.close()
				return True
		alLikes.close()
	return False
def verificar_match(id_usuario1, id_usuario2):
	if os.path.exists(afLikes):
		alLikes = open(afLikes, "r+b")
		tam = os.path.getsize(afLikes)

		while alLikes.tell() < tam:
			reg = pickle.load(alLikes)
			if (reg.id_remitente == id_usuario1 and reg.id_destinatario == id_usuario2) or \
				(reg.id_remitente == id_usuario2 and reg.id_destinatario == id_usuario1):
				alLikes.close()
				return True
		alLikes.close()
	return False

##ARCHIVOS
def contar_registros(AF):
	contador = 0
	AL = open(AF, "r+b")
	tam = os.path.getsize(AF)
	
	if tam == 0:
		return 0
	
	AL.seek(0)
	while AL.tell() < tam:
		reg = pickle.load(AL)
		contador += 1
				
	AL.close()
	return contador
def buscar_usuario(AF, indice):
	AL = open(AF, "r+b")
	tam = os.path.getsize(AF)

	if tam != 0:
		AL.seek(0)
		while AL.tell() < tam:
			pos = AL.tell()
			reg = pickle.load(AL)
			
			if reg.id == indice:
				AL.close()
				return pos
	else:
		AL.close()
		return -1

	AL.close()
	return -1	

def aux_verificar_tipo(AF: str, clase, email, contraseña):
	AL = open(AF, "r+b")
	tam = os.path.getsize(AF)

	if tam != 0:
		AL.seek(0)
		pos = 0

		while AL.tell() < tam:
			reg = pickle.load(AL)
			if isinstance(clase, Administrador):
				if reg.email == email and reg.contraseña == contraseña:
					AL.close()
					return reg.id
			elif reg.estado and reg.email == email and reg.contraseña == contraseña:
				AL.close()
				return reg.id
	else:
		AL.close()
		return -1

	AL.close()
	return -1

##INICIO
def verificar_tipo(email, contraseña):
	global opc_modo

	indice = aux_verificar_tipo(afUsuarios, Usuario(), email, contraseña)
	if indice != -1:
		opc_modo = 1
		return indice

	indice = aux_verificar_tipo(afModeradores, Moderador(), email, contraseña)
	if indice != -1:
		opc_modo = 2
		return indice

	indice = aux_verificar_tipo(afAdmins, Administrador(), email, contraseña)
	if indice != -1:
		opc_modo = 3
		return indice

	return -1

def login():
	cont_intentos = 0
	
	limpiar()
	print(' Log in  |')
	print('----------\n')

	while cont_intentos < 3:
		email = input(' Ingrese su email: ')
		contraseña = pwinput(' Ingrese su contraseña: ')

		indice = verificar_tipo(email.ljust(32, ' '), contraseña.ljust(32, ' '))
		if indice == -1:
			mensaje_error('El email y/o contraseña son incorrectos')
		else:
			return indice
		cont_intentos += 1

	print('\n Maximo de intentos alcanzado')
	sleep(2)
	ptos_suspensivos()
	return indice

def email_rep(AF, email):
	AL = open(AF, "r+b")
	tam = os.path.getsize(AF)
	email = email.ljust(32, ' ')

	if tam != 0:
		AL.seek(0)

		while AL.tell() < tam:
			reg = pickle.load(AL)
			if reg.email == email: 
				AL.close()
				return True
	else: 
		AL.close()
		return False

	AL.close()
	return False
def signup():
	global cant_usuarios

	limpiar()
	print(' Sign up  |')
	print('-----------\n')

	nombre = input(' Ingrese su nombre de usuario: ')
	while not nombre.isalpha():
		mensaje_error('El nombre no puede ser un numero')
		nombre = input(' Ingrese su nombre de usuario: ')

	email = input(' Ingrese su email: ')
	while email_rep(afUsuarios, email) or email_rep(afModeradores, email) or email_rep(afAdmins, email):
		mensaje_error('El email ya se encuentra registrado')
		email = input(' Ingrese otro email: ')

	contraseña = input(' Ingrese su contraseña: ')

	fecha_nacimiento = input(' Ingrese su fecha de nacimiento (YYYY-MM-DD): ')
	while not calcular_edad(fecha_nacimiento): 
		fecha_nacimiento = input(' Ingrese su fecha de nacimiento (YYYY-MM-DD): ')

	biografia = input(' Ingrese una biografia: ')
	hobbies = input(' Ingrese sus hobbies: ')

	us = Usuario()
	us.id = cant_usuarios
	us.estado = True
	us.nombre = nombre.capitalize().ljust(32, ' ')
	us.email = email.ljust(32, ' ')
	us.contraseña = contraseña.ljust(32, ' ')
	us.fecha_nacimiento = fecha_nacimiento.ljust(10, ' ')
	us.biografia = biografia.ljust(255, ' ')
	us.hobbies = hobbies.ljust(255, ' ')
	cant_usuarios += 1

	alUsuarios = open(afUsuarios, "r+b")
	alUsuarios.seek(0, 2)
	pickle.dump(us, alUsuarios)
	alUsuarios.close()

	print('\n Registrado')
	sleep(1)
	ptos_suspensivos(' Ingresando')
	return cant_usuarios-1

##MENUS
def ingresar_menu(menu: str, opciones=[0, 1, 2, 3, 4], construccion=[]):
	limpiar()
	print(menu)
	
	while True:
		try:
			opcion = int(input(' Ingrese una opción: '))

			if opcion in construccion: mensaje_advertencia('En Construcción')
			elif opcion in opciones: return opcion
			else: mensaje_error('La opción no existe')

		except ValueError:
			mensaje_error('Ingrese una numero entero')

def ingresar_submenu(menu: str, opciones= ['a', 'b', 'c'], construccion=[]):
	limpiar()
	print(menu)
	
	while True:
		opcion = input(' Ingrese una opcion: ')

		if opcion in construccion: mensaje_advertencia('En Construcción')
		elif opcion in opciones: return opcion
		else: mensaje_error('La opcion no existe')
				
	return opcion

##USUARIO
def calcular_edad(fecha_nacimiento: str):
	try:
		fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
	except ValueError:
		mensaje_error('La fecha no tiene el formato indicado')
		return False
	
	fecha_actual = datetime.now().date()

	edad = fecha_actual.year - fecha_nacimiento.year - 1
	if fecha_actual.month > fecha_nacimiento.month and fecha_actual.day >= fecha_nacimiento.day:
		edad += 1

	if edad < 18 or edad > 100:
		mensaje_error(f'La fecha no es valida\n Edad: {edad} años')
		return False
	else:
		return edad
def mostrar_usuario(us: Usuario):
	print (
		f' Nombre: {us.nombre.strip()}\n'
		f' Fecha de nacimiento: {us.fecha_nacimiento}\n'
		f' Edad: {calcular_edad(us.fecha_nacimiento.strip())} años\n'
		f' Biografía: {us.biografia.strip()}\n'
		f' Hobbies: {us.hobbies.strip()}\n'
	)

def editar_datos(indice):
	pos = buscar_usuario(afUsuarios, indice)
	alUsuarios = open(afUsuarios, "r+b")

	us = Usuario()
	alUsuarios.seek(pos, 0)
	us = pickle.load(alUsuarios)

	limpiar()
	mostrar_usuario(us)
	
	fecha_nacimiento = input(' Ingrese su fecha de nacimiento (YYYY-MM-DD): ')
	while not calcular_edad(fecha_nacimiento): 
		fecha_nacimiento = input(' Ingrese su fecha de nacimiento (YYYY-MM-DD): ')

	biografia = input(' Ingrese su biografia: ')
	hobbies = input(' Ingrese sus hobbies: ')

	us.fecha_nacimiento = fecha_nacimiento.ljust(10, ' ')
	us.biografia = biografia.ljust(255, ' ')
	us.hobbies = hobbies.ljust(255, ' ')

	alUsuarios.seek(pos, 0)
	pickle.dump(us, alUsuarios)
	alUsuarios.flush()
	alUsuarios.close()

def eliminar_perfil(indice, lista='us'):
	print('')
	if lista == 'us': AF = afUsuarios
	else: AF = afModeradores

	AL = open(AF, "r+b")
	activos = 0
	while AL.tell() < os.path.getsize(AF):
		reg = pickle.load(AL)
		if reg.estado: activos += 1

	if (activos > 4 and lista == 'us') or (activos > 2 and lista == 'mod'):
		confirmar = None
		while confirmar != 'S' and confirmar != 'N':
			confirmar = input(' Esta seguro? [S/N]: ').upper()
			if confirmar == 'S':
				pos = buscar_usuario(AF, indice)
				AL.seek(pos, 0)
				reg = pickle.load(AL)
				reg.estado = False

				AL.seek(pos, 0)
				pickle.dump(reg, AL)
				AL.flush()
				AL.close()

				ptos_suspensivos(' Eliminando usuario')
				print(' Listo') 
				sleep(4)
				return True
			elif confirmar == 'N':
				AL.close()
				ptos_suspensivos(' Cancelando')
				return False
			else: mensaje_error('La opcion no es valida')
	else:
		AL.close()
		mensaje_error('No se pueden eliminar mas usuarios')
		sleep(1.5)
		ptos_suspensivos()

def ver_candidatos(indice):
	limpiar()
	us_registrado = Usuario()
	alUsuarios = open(afUsuarios, "r+b")
	alUsuarios.seek(0)

	while alUsuarios.tell() < os.path.getsize(afUsuarios):
		reg = pickle.load(alUsuarios)

		if reg.id == indice:
			us_registrado = reg
		elif reg.estado:
			mostrar_usuario(reg)

	encontrado = False
	while not encontrado:
		me_gusta = input(' Ingrese el nombre de un estudiante para dar like: ').capitalize()

		alUsuarios.seek(0, 0)
		while alUsuarios.tell() < os.path.getsize(afUsuarios) and not encontrado:
			reg = pickle.load(alUsuarios)
			if reg.nombre.strip() == me_gusta and us_registrado.nombre.strip() != me_gusta: 
				encontrado = True
				
				if verificar_like(indice, reg.id):
					print('\n Ya le dio like a este usuario')
				
				elif not reg.estado:
					mensaje_error('El usuario ya no está disponible')

				else:
					agregar_like(indice, reg.id)
					print('\n Usuario guardado como posible match')
				
				sleep(1.5)
				ptos_suspensivos()

		if not encontrado:
			mensaje_error('El nombre no coincide con ningún usuario')

	alUsuarios.close()
	
def reportar_candidato(indice):
	global cant_reportes
	
	if cant_reportes == 60:
		print(' No se aceptan mas reportes\n')
		sleep(1)
		ptos_suspensivos()
	else:
		alUsuarios = open(afUsuarios, "r+b")

		salir = False
		while not salir:
			elim = input(' Ingrese el nombre o ID del usuario: ')
			try:
				elim = int(elim)
				if elim in range(cant_usuarios):
					pos = buscar_usuario(afUsuarios, elim)
					alUsuarios.seek(pos, 0)
					reg = pickle.load(alUsuarios)

					if elim != indice and elim >= 0 and reg.estado: 
						print('\n ID:', reg.id)
						mostrar_usuario(reg)

						reporte = Reporte()
						reporte.id_reportante = indice
						reporte.id_reportado = elim
						reporte.motivo = input(' Ingrese el motivo del reporte: ').ljust(255, ' ')

						salir = True

			except ValueError:
				pos = buscar_usuario(afUsuarios, indice)
				alUsuarios.seek(pos, 0)
				us_registrado = pickle.load(alUsuarios)

				alUsuarios.seek(0)
				while alUsuarios.tell() < os.path.getsize(afUsuarios):
					reg = pickle.load(alUsuarios)
					if elim.capitalize() != us_registrado.nombre.strip() and elim.capitalize() == reg.nombre.strip() and reg.estado: 
						print('\n ID:', reg.id)
						mostrar_usuario(reg)
						
						reporte = Reporte()
						reporte.id_reportante = indice
						reporte.id_reportado = i
						reporte.motivo = input(' Ingrese el motivo del reporte: ').ljust(255, ' ')
						
						salir = True

			if not salir: mensaje_error('No se encontro el usuario o ID')
			else:
				alReportes = open(afReportes, "r+b")
				alReportes.seek(2)
				pickle.dump(reporte, alReportes)
				cant_reportes += 1

				alReportes.close()
				alUsuarios.close()

				print('\n Reporte guardado')
				sleep(1)
				ptos_suspensivos()

def reportes_est(indice, test=False):
	limpiar()
	total_candidatos, match, likes_dados, likes_recibidos = 0, 0, 0, 0

	if test:
		alLikes = open(afLikes, "r+b")
		print(' remitente | destinatario\n--------------------------')
		while alLikes.tell() < os.path.getsize(afLikes):
			reg = pickle.load(alLikes)
			if reg.id_remitente == indice or reg.id_destinatario == indice: 
				print(f'     {reg.id_remitente}     |      {reg.id_destinatario}')
		alLikes.close()
	
	if os.path.exists(afUsuarios): 
		alUsuarios = open(afUsuarios, "r+b")
		while alUsuarios.tell() < os.path.getsize(afUsuarios):
			reg = pickle.load(alUsuarios)

			if reg.id != indice and reg.estado: 
				total_candidatos += 1
				
				if verificar_match(indice, reg.id): match += 1
				if verificar_like(indice, reg.id):  likes_dados += 1
				if verificar_like(reg.id, indice): likes_recibidos += 1
		
		alUsuarios.close()

	if total_candidatos > 0:
		porcentaje_matcheados = (match * 100) / total_candidatos
	else:
		porcentaje_matcheados = 0

	print(
		f'\n\n* Matcheados sobre el % posible: %{porcentaje_matcheados}\n'
		f'* Likes dados y no recibidos: {likes_dados}\n'
		f'* Likes recibidos y no respondidos: {likes_recibidos}'
	)

##MODERADOR
def desactivar_usuario():
	salir = False
	while not salir:
		alUsuarios = open(afUsuarios, "r+b")
		tam = os.path.getsize(afUsuarios)

		elim = input(' Ingrese el nombre o ID del usuario: ')
		try:
			elim = int(elim)

			if elim in range(cant_usuarios):
				pos = buscar_usuario(afUsuarios, elim)
				alUsuarios.seek(pos, 0)
				us = pickle.load(alUsuarios)

				if us.estado:
					print('\n ID:', us.id)
					mostrar_usuario(us)

					eliminar_perfil(elim)
					salir = True
		except ValueError:
			while alUsuarios.tell() < tam:
				us = pickle.load(alUsuarios)
				
				if elim.capitalize() == us.nombre and us.id: 
					print('\n ID:', us.id)
					mostrar_usuario(us)

					eliminar_perfil(us.id)
					salir = True

		if not salir: mensaje_error('No se encontro el usuario o ID')
		alUsuarios.close()

def reportesPendientes():
	alReportes = open(afReportes, "r+b")

	while alReportes.tell() < os.path.getsize(afReportes):
		reg = pickle.load(alReportes)
		if reg.estado == 0: return True
	return False
def ver_reportes(indice, rol):
	limpiar()
	if not reportesPendientes():
		print('\n No hay reportes \n')
		ptos_suspensivos()
	else:
		alReportes = open(afReportes, "r+b")
		alReportes.seek(0)
		
		while alReportes.tell() < os.path.getsize(afReportes):
			reg = pickle.load(alReportes)

			alUsuarios = open(afUsuarios, "r+b")
			pos = buscar_usuario(afUsuarios, reg.id_reportante)
			alUsuarios.seek(pos, 0)
			us_reportante = pickle.load(alUsuarios)

			pos = buscar_usuario(afUsuarios, reg.id_reportado)
			alUsuarios.seek(pos, 0)
			us_reportado = pickle.load(alUsuarios)
			alUsuarios.close()

			if (
				us_reportante.estado and 
				us_reportado.estado and 
				reg.estado == 0
			):
				print(
					f'-----------------------------------------'
					f'\n ID reportante: {reg.id_reportante}\n'
					f' Nombre reportante: {us_reportante.nombre.strip()}\n'
					f'\n ID reportado: {reg.id_reportado}\n'
					f' Nombre reportado: {us_reportado.nombre.strip()}\n'
					f'\n Motivo: {reg.motivo.strip()}\n'
					f'------------------------------------------'
					f'\n\n Que desea hacer: '
					f'\n  1. ignorar reporte'
					f'\n  2. bloquear usuario\n'
				)
				
				salir = False
				while not salir:
					try:
						opcion = int(input(': '))

						if opcion != 1 and opcion != 2: mensaje_error('La opcion no existe')
						else:
							if opcion == 1:
								reg.estado = 1
								print('\nReporte ignorado\n')
								sleep(1)
							elif opcion == 2:
								if eliminar_perfil(us_reportado.id): reg.estado = 2
								else: reg.estado = 1

							reg.rol = rol
							pickle.dump(reg, alReportes)
							print('\n')
							salir = True

					except ValueError:
						mensaje_error('Ingrese una numero entero')

		print(' No quedan mas reportes')
		alReportes.close()
		sleep(2)
		ptos_suspensivos()

##ADMINISTRADOR
# Pendiente para consulta
def eliminar_usuario_moderador():
	salir = False
	while not salir:
		limpiar()
		print(
			f'\n Que desea desactivar: '
			f'\n  1. Usuario'
			f'\n  2. Moderador\n'
		)

		salir = False
		while not salir:
			try:
				opc = int(input(': '))
				print('')

				if opc == 1:
					limpiar()
					desactivar_usuario()
				elif opc == 2:
					limpiar()
					alModeradores = open(afModeradores, "r+b")
					tam = os.path.getsize(afModeradores)

					while not salir:
						elim = input(' Ingrese el ID del moderador: ')
						try:
							elim = int(elim)
							if elim < cant_moderadores and elim >= 0:
								alModeradores.seek(buscar_usuario(afModeradores, elim), 0)
								reg = pickle.load(alModeradores)

								if reg.estado: 
									print(
										f'\n  ID: {reg.id}'
										f'\n  Email: {reg.email}\n'
									)

									eliminar_perfil(elim, 'mod')
									salir = True
							
							if not salir: mensaje_error('No se encontro el ID del moderador')
						except ValueError:
							mensaje_error('Ingrese un numero')
				else: mensaje_error('La opcion no existe')

			except ValueError:
				mensaje_error('Ingrese un numero')

def alta_moderador():
	global cant_moderadores

	limpiar()
	print(' Nuevo moderador  |')
	print('-------------------\n')

	email = input(' Ingrese el email: ')
	while email_rep(afUsuarios, email) or email_rep(afModeradores, email) or email_rep(afAdmins, email):
		mensaje_error('El email ya se encuentra registrado')
		email = input(' Ingrese otro email: ')

	contraseña = input(' Ingrese la contraseña: ')

	moderador = Moderador()
	moderador.id = cant_moderadores
	moderador.email = email
	moderador.contraseña = contraseña
	cant_moderadores += 1

	alModeradores = open(afModeradores, "r+b")
	alModeradores.seek(0, 2)
	pickle.dump(moderador, alModeradores)
	alModeradores.close()

	print('\n Registrado')
	sleep(1)
	ptos_suspensivos()

def mayor_contador(arr):
	indice = 0
	for i in range(1, len(arr)):
		if arr[i] > arr[i-1]: indice = i
	return indice
def reportes_est_admin(test=False):
	reportes_ignorados, reportes_aceptados, cant_reportes_mods = 0, 0, 0
	acciones_reportes = [[0]*cant_moderadores for n in range(2)]
	acciones_total_reportes = [0 for n in range(cant_moderadores)]

	alReportes = open(afReportes, "r+b")
	while alReportes.tell() < os.path.getsize(afReportes):
		reg = pickle.load(alReportes)
		if reg.rol != 'admin': cant_reportes_mods += 1

	limpiar()
	if cant_reportes > 0:
		alReportes.seek(0, 0)
		while alReportes.tell() < os.path.getsize(afReportes):
			reg = pickle.load(alReportes)

			if reg.rol != 'admin':
				if reg.estado == 1: 
					reportes_ignorados += 1
					acciones_reportes[0][reg.id_responsable] += 1

				elif reg.estado == 2: 
					reportes_aceptados += 1
					acciones_reportes[1][reg.id_responsable] += 1
		alReportes.close()
		
		for i in range(cant_moderadores):
			acciones_total_reportes[i] = acciones_reportes[0][i] + acciones_reportes[1][i]
		
		posMRI = buscar_usuario(afModeradores, mayor_contador(acciones_reportes[0]))
		posMRA = buscar_usuario(afModeradores, mayor_contador(acciones_reportes[1]))
		posMRP = buscar_usuario(afModeradores, mayor_contador(acciones_total_reportes))

		alModeradores = open(afModeradores, "r+b")
		alModeradores.seek(posMRI, 0)
		moderadorMRI = pickle.load(alModeradores).email

		alModeradores.seek(posMRA, 0)	
		moderadorMRA = pickle.load(alModeradores).email
		
		alModeradores.seek(posMRP, 0)
		moderadorMRP = pickle.load(alModeradores).email
		alModeradores.close()

		if test:
			print(acciones_reportes[0])
			print(acciones_reportes[1])
			print(acciones_total_reportes)
		print(
			f'\n* Cantidad de reportes: {cant_reportes}\n'
			f'* % de reportes ignorados por moderadores: %{int((reportes_ignorados*100)/cant_reportes_mods)}\n'
			f'* % de reportes aceptados por moderadores: %{int((reportes_aceptados*100)/cant_reportes_mods)}\n\n'
			f'* Moderador con mas reportes ignorados: {moderadorMRI}\n'
			f'* Moderador con mas reportes aceptados: {moderadorMRA}\n'
			f'* Moderador con mas reportes procesados: {moderadorMRP}'
		)
	else: 
		print('\n No hay reportes')
		ptos_suspensivos()

##BONUS 
def ingresar_probabilidad():
	limpiar()
	while True:
		try:
			prob1 = int(input('Ingrese la probabilidad de matcheo de la Persona A: '))

			if prob1 > 0 and prob1 < 99:
				break
			elif prob1 == 99 or prob1 == 100:
				mensaje_error('Ingrese un porcentaje valido con respecto a los otros')
			else:
				mensaje_error('Ingrese un porcentaje valido')

		except ValueError:
			mensaje_error('Ingrese un numero entero')
	while True:
		try:
			prob2 = int(input('Ingrese la probabilidad de matcheo de la Persona B: '))

			if prob2 > 0 and prob2 < 100-prob1:
				break
			elif prob2 >= 100-prob1 and prob2 <= 100:
				mensaje_error('Ingrese un porcentaje valido con respecto a los otros')
			else:
				mensaje_error('Ingrese un porcentaje valido')

		except ValueError:
			mensaje_error('Ingrese un numero entero')
	while True:
		try:
			prob3 = int(input('Ingrese la probabilidad de matcheo de la Persona C: '))

			if prob3 == 100-prob1-prob2:
				break
			elif prob3 >= 0 and prob3 <= 100:
				mensaje_error('Ingrese un porcentaje valido con respecto a los otros')
			else:
				mensaje_error('Ingrese un porcentaje valido')

		except ValueError:
			mensaje_error('Ingrese un numero entero')

	return prob1, prob2, prob3
def ruleta_bonus():
	prob1, prob2, prob3 = ingresar_probabilidad()
	rango_persona1 = range(1, prob1 + 1)
	rango_persona2 = range(prob1 + 1, prob1 + prob2 + 1)
	rango_persona3 = range(prob1 + prob2 + 1, 101)

	ptos_suspensivos('\nEl ganador es')

	ganador = randint(1, 100)
	if ganador in rango_persona1:
		print('  La persona A!!\n')
	elif ganador in rango_persona2:
		print('  La persona B!!\n')
	else:
		print('  La persona C!!\n')
	sleep(5)

def insertion_sort(arr):
	for i in range(1, len(arr)):
		key = arr[i]
		j = i - 1
		
		while j >= 0 and key < arr[j]:
			arr[j + 1] = arr[j]
			j -= 1
		arr[j + 1] = key
def edades_bonus():
	limpiar()
	edades = [21, 18, 20, 19, 23, 24]

	print('\n Reporte de edades:', edades)
	insertion_sort(edades)
	print(' Arreglo ordenado: ', edades)
	
	huecos = [None] * 6
	index = 0
	for i in range(len(edades) - 1):
		if edades[i + 1] - edades[i] > 1:
			for j in range(edades[i] + 1, edades[i + 1]):
				huecos[index] = j
				index += 1
	
	if index: print('\n Los huecos son:', huecos[:index])
	else: print('\n No hay huecos')
	input('\n\nPresione ENTER  ')
	
def matcheos_comb_bonus():
	cont = 0
	alUsuarios = open(afUsuarios, "r+b")
	while afUsuarios.tell() < os.path.getsize(afUsuarios):
		reg = pickle.load(alUsuarios)
		if reg.estado: cont += 1
	alUsuarios.close()
	
	limpiar()
	matcheos = cont * (cont - 1)
	print('\n Cantidad de usuarios:', cont - 1)
	print(' Matcheos posibles:', matcheos, '\n')

	input('\n\nPresione ENTER  ')

# M A I N
# opcion, opc_modo:  Integer
# sub_opcion:        Char
def cerrar_sesion():
	global cookie
	cookie = Cookie()

	if os.path.exists(afCookie):
		os.remove(afCookie)
	
	ptos_suspensivos('\n Cerrando sesion')

def pagina_usuario(indice):
	salir = False
	while not salir:
		opcion = ingresar_menu(menu, construccion=[3])

		match opcion:
			case 0:
				cerrar_sesion()
				salir = True
			case 1:
				sub_opcion = ingresar_submenu(menu1)
				if sub_opcion == 'a': editar_datos(indice)
				elif sub_opcion == 'b': 
					if eliminar_perfil(indice): 
						cerrar_sesion()
						salir = True
			case 2:
				sub_opcion = ingresar_submenu(menu2)
				if sub_opcion == 'a': ver_candidatos(indice)
				elif sub_opcion == 'b': reportar_candidato(indice)    
			case 4:
				reportes_est(indice, True)
				input('\n\n Presione ENTER ')

def pagina_moderador(indice):
	salir = False
	while not salir:
		opcion = ingresar_menu(menu_mod, [0, 1, 2], [3])

		if opcion == 0:
			cerrar_sesion()
			salir = True
		elif opcion == 1:
			sub_opcion = ingresar_submenu(menu_mod1, ['a', 'b'])
			if sub_opcion == 'a': desactivar_usuario() 	
		elif opcion == 2:
			sub_opcion = ingresar_submenu(menu_mod2, ['a', 'b'])
			if sub_opcion == 'a': ver_reportes(indice, 1)

def pagina_admin(indice):
	salir = False
	while not salir:
		opcion = ingresar_menu(menu_mod, [0, 1, 2, 3])

		if opcion == 0:
			cerrar_sesion()
			salir = True
		elif opcion == 1:
			sub_opcion = ingresar_submenu(menu_admin1, ['b', 'c', 'd'], ['a'])
			if sub_opcion == 'a': eliminar_usuario_moderador()
			elif sub_opcion == 'b': alta_moderador()
			elif sub_opcion == 'c': desactivar_usuario()
		elif opcion == 2:
			sub_opcion = ingresar_submenu(menu_mod2, ['a', 'b'])
			if sub_opcion == 'a': ver_reportes(indice, 2)
		elif opcion == 3:
			reportes_est_admin(True)
			input('\n\n Presione ENTER ')

def crear_cookie(id, rol):
	global cookie
	cookie.id = id
	cookie.rol = rol
	cookie.time = datetime.now() + timedelta(hours=vto_horas)


inicializacion(True)

opcion = None
while opcion != 0:
	if cookie.id != None:
		indice = cookie.id
		opc_modo = cookie.rol

		if opc_modo == 1:
			pagina_usuario(indice)
		elif opc_modo == 2:  
			pagina_moderador(indice)
		elif opc_modo == 3:  
			pagina_admin(indice)
	else:
		limpiar()
		print(menu_inicio)
		
		try:
			opcion = int(input('\n Ingrese una opción: '))
			if opcion > 5 or opcion < 0: mensaje_error('La opción no es válida')
			elif opcion == 1: 
				opc_modo = 0
				indice = login()
				if indice != -1:
					if opc_modo > 0 and opc_modo < 4:
						crear_cookie(indice, opc_modo)
						alCookie = open(afCookie, "w+b")
						pickle.dump(cookie, alCookie)
						alCookie.close()

						if opc_modo == 1:
							pagina_usuario(indice)
						elif opc_modo == 2:
							pagina_moderador(indice)
						elif opc_modo == 3:
							pagina_admin(indice)
					else: mensaje_error('Ingrese una opcion valida')
			elif opcion == 2:
				pagina_usuario(signup())

			if opcion > 0 and opcion < 6:
				limpiar()
				print(menu_inicio)
		
		except ValueError:
			mensaje_error('Ingrese un numero entero')
print('')