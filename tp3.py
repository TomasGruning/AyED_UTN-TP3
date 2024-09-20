# TP3 - Tomás Gruning, Lucía Godoy, Joaquin Raffaelli
import random
import pickle
import os
from datetime import datetime, timedelta
from pwinput import pwinput
from random import randint
from time import sleep

## En caso de querer mantener una sesion activa
## cambiar este valor
vto_horas = 72

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
 --------------------------------------
 | Gestionar usuarios                 |
 |                                    |
 | a. Desactivar usuario o moderador  |
 | b. Dar de alta moderador           |
 | c. Desactivar usuario              |
 | d. Volver                          |
 --------------------------------------
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
		self.id = None
		self.estado = None
		self.nombre = None
		self.email = None
		self.contraseña = None
		self.fecha_nacimiento = None
		self.biografia = None
		self.hobbies = None

class Moderador:
	def __init__(self):
		self.id = None
		self.estado = None
		self.email = None
		self.contraseña = None

class Administrador:
	def __init__(self):
		self.id = None
		self.email = None
		self.contraseña = None 

class Reporte:
	def __init__(self):
		self.id_reportante = None
		self.id_reportado = None
		self.id_moderador = None
		self.motivo = ''
		self.estado = None

class Cookie:
	def __init__(self):
		self.time = None
		self.tipo = 0
		self.id = None

# Inicializacion de la carpeta y las rutas de los archivos
if not os.path.exists('.data'):
	os.makedirs('.data')
afUsuarios = './.data/usuarios.dat'
afModeradores = './.data/moderadores.dat'
afAdmins = './.data/administradores.dat'
afLikes = './.data/likes.dat'
afReportes = './.data/reportes.dat'
afCookie = './.data/cookie.dat'

usuarios = [Usuario() for n in range(20)]
moderadores = [Moderador() for n in range(10)]
administradores = [Administrador() for n in range(10)]
likes = [[0]*20 for n in range(20)]
reportes = [Reporte() for n in range(60)]
cookie = Cookie()
cant_usuarios, cant_moderadores, cant_reportes = 0, 0, 0

#FUNCIONES
def inicializacion(test=False):
	global usuarios, moderadores, administradores, likes, reportes, cookie 
	global cant_usuarios, cant_moderadores, cant_reportes
	
	# Carga de usuarios
	if os.path.exists(afUsuarios):
		alUsuarios = open(afUsuarios, "r+b")
		usuarios = pickle.load(alUsuarios)
	else:
		alUsuarios = open(afUsuarios, "w+b")

		for n in range(5): 
			usuarios[n].id = n
			usuarios[n].estado = 'ACTIVO'

		usuarios[0].nombre = 'Tomas'
		usuarios[0].email = 'estudiante1@ayed.com'
		usuarios[0].contraseña = '111222'
		usuarios[0].fecha_nacimiento = '2005-03-07'

		usuarios[1].nombre = 'Lucia'
		usuarios[1].email = 'estudiante2@ayed.com'
		usuarios[1].contraseña = '333444'
		usuarios[1].fecha_nacimiento = '2001-06-23'

		usuarios[2].nombre = 'Agustin'
		usuarios[2].email = 'estudiante3@ayed.com'
		usuarios[2].contraseña = '555666'
		usuarios[2].fecha_nacimiento = '2003-09-19'

		usuarios[3].nombre = 'Martina'
		usuarios[3].email = 'estudiante4@ayed.com'
		usuarios[3].contraseña = '777888'
		usuarios[3].fecha_nacimiento = '2004-12-09'

		usuarios[4].nombre = 'Joaquin'
		usuarios[4].email = 'estudiante5@ayed.com'
		usuarios[4].contraseña = '999101010'
		usuarios[4].fecha_nacimiento = '2005-01-27'
		
		pickle.dump(usuarios, alUsuarios)
	alUsuarios.close()

	for i in usuarios: 
		if i.id != None: cant_usuarios += 1

	# Carga de moderadores
	if os.path.exists(afModeradores):
		alModeradores = open(afModeradores, "r+b")
		moderadores = pickle.load(alModeradores)
	else:
		alModeradores = open(afModeradores, "w+b")
		
		for n in range(3): 
			moderadores[n].id = n
			moderadores[n].estado = 'ACTIVO'

		moderadores[0].email = 'moderador1@ayed.com'
		moderadores[0].contraseña = 'mod111222'

		moderadores[1].email = 'moderador2@ayed.com'
		moderadores[1].contraseña = 'mod333444'

		moderadores[2].email = 'moderador3@ayed.com'
		moderadores[2].contraseña = 'mod555666'
		pickle.dump(moderadores, alModeradores)
	alModeradores.close()

	for i in moderadores: 
		if i.id != None: cant_moderadores += 1

	# Carga de administradores
	if os.path.exists(afAdmins):
		alAdmins = open(afAdmins, "r+b")
		administradores = pickle.load(alAdmins)
	else:
		alAdmins = open(afAdmins, "w+b")
		
		administradores[0].id = 0
		administradores[0].estado = 'ACTIVO'
		administradores[0].email = 'administrador1@ayed.com'
		administradores[0].contraseña = 'admin111222'
		
		pickle.dump(administradores, alAdmins)
	alAdmins.close()
	
	# Carga de matriz de likes
	if os.path.exists(afLikes):
		alLikes = open(afLikes, "r+b")
		likes = pickle.load(alLikes)
	else:
		alLikes = open(afLikes, "w+b")

		for i in range(cant_usuarios):
			for e in range(cant_usuarios):
				if usuarios[i].estado == 'ACTIVO' and usuarios[e].estado == 'ACTIVO' and i != e:
					likes[i][e] = randint(0, 1)
					likes[e][i] = randint(0, 1)
				else:
					likes[i][e] = -1
					likes[e][i] = -1

		pickle.dump(likes, alLikes)
	alLikes.close()

	# Carga de reportes
	if os.path.exists(afReportes):
		alReportes = open(afReportes, "r+b")
		reportes = pickle.load(alReportes)
		for i in reportes:
			if i.estado != None: cant_reportes += 1
	
		alReportes.close()

	if test:
		for n in range(40):
			reportes[n].id_reportante = randint(0, cant_usuarios-1)
			reportes[n].id_reportado = randint(0, cant_usuarios-1)
			reportes[n].id_moderador = randint(0, cant_moderadores-1)
			reportes[n].motivo = ''
			reportes[n].estado = randint(0, 2)
			cant_reportes += 1

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

##INICIO
def verificar_tipo(email, contraseña):
	global opc_modo
	for i in range(cant_usuarios):
		if usuarios[i].email == email and usuarios[i].contraseña == contraseña and usuarios[i].estado == 'ACTIVO':
			opc_modo = 1
			return i
	for i in range(len(moderadores)):
		if moderadores[i].email == email and moderadores[i].contraseña == contraseña and moderadores[i].estado == 'ACTIVO':
			opc_modo = 2
			return i
	for i in range(len(administradores)):
		if administradores[i].email == email and administradores[i].contraseña == contraseña and administradores[i].estado == 'ACTIVO':
			opc_modo = 3
			return i

	return -1

def login():
	cont_intentos = 0
	
	limpiar()
	print(' Log in  |')
	print('----------\n')

	while cont_intentos < 3:
		email = input(' Ingrese su email: ')
		contraseña = pwinput(' Ingrese su contraseña: ')

		indice = verificar_tipo(email, contraseña)
		if indice == -1:
			mensaje_error('El email y/o contraseña son incorrectos')
		else:
			return indice
		cont_intentos += 1

	print('\n Maximo de intentos alcanzado')
	sleep(2)
	ptos_suspensivos()
	return indice

def email_rep(email):
	for n in range(cant_usuarios):
		if usuarios[n].email == email: return True
	i = 0
	while moderadores[i].email:
		if moderadores[i].email == email: return True
		i += 1
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
	while email_rep(email):
		mensaje_error('El email ya se encuentra registrado')
		email = input(' Ingrese otro email: ')

	contraseña = input(' Ingrese su contraseña: ')

	fecha_nacimiento = input(' Ingrese su fecha de nacimiento (YYYY-MM-DD): ')
	while not calcular_edad(fecha_nacimiento): 
		fecha_nacimiento = input(' Ingrese su fecha de nacimiento (YYYY-MM-DD): ')

	biografia = input(' Ingrese una biografia: ')
	hobbies = input(' Ingrese sus hobbies: ')

	usuarios[cant_usuarios].id = cant_usuarios
	usuarios[cant_usuarios].estado = 'ACTIVO'
	usuarios[cant_usuarios].nombre = nombre
	usuarios[cant_usuarios].email = email
	usuarios[cant_usuarios].contraseña = contraseña
	usuarios[cant_usuarios].fecha_nacimiento = fecha_nacimiento
	usuarios[cant_usuarios].biografia = biografia
	usuarios[cant_usuarios].hobbies = hobbies
	cant_usuarios += 1

	# Actualiza la matriz de likes
	for n in range(cant_usuarios):
		if n == cant_usuarios-1:
			likes[n][n] = -1
		else:
			likes[n][cant_usuarios] = 0
			likes[cant_usuarios][n] = 0

	alLikes = open(afLikes, "w+b")
	pickle.dump(likes, alLikes)
	alLikes.close()
	#

	alUsuarios = open(afUsuarios, "w+b")
	pickle.dump(usuarios, alUsuarios)
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
		f' Nombre: {us.nombre}\n'
		f' Fecha de nacimiento: {us.fecha_nacimiento}\n'
		f' Edad: {calcular_edad(us.fecha_nacimiento)} años\n'
		f' Biografía: {us.biografia}\n'
		f' Hobbies: {us.hobbies}\n\n'
	)

def editar_datos(indice):
	limpiar()
	mostrar_usuario(moderadores[indice])
	
	fecha_nacimiento = input(' Ingrese su fecha de nacimiento (YYYY-MM-DD): ')
	while not calcular_edad(fecha_nacimiento): 
		fecha_nacimiento = input(' Ingrese su fecha de nacimiento (YYYY-MM-DD): ')

	biografia = input(' Ingrese su biografia: ')
	hobbies = input(' Ingrese sus hobbies: ')

	usuarios[indice].fecha_nacimiento = fecha_nacimiento
	usuarios[indice].biografia = biografia
	usuarios[indice].hobbies = hobbies

	alUsuarios = open(afUsuarios, "w+b")
	pickle.dump(usuarios, alUsuarios)
	alUsuarios.close()

def eliminar_perfil(indice, lista='us'):
	print('')
	cont = 0
	for i in range(cant_usuarios):
		if usuarios[i].estado == 'ACTIVO': cont += 1

	if (cant_usuarios > 4 and lista == 'us') or (cant_moderadores > 2 and lista == 'mod'):
		confirmar = None
		while confirmar != 'S' and confirmar != 'N':
			confirmar = input(' Esta seguro? [S/N]: ').upper()
			if confirmar == 'S':
				ptos_suspensivos(' Eliminando usuario')
				if lista == 'mod': 
					moderadores[indice].estado = 'INACTIVO'

					alModeradores = open(afUsuarios, "w+b")
					pickle.dump(moderadores, alModeradores)
					alModeradores.close()
				else: 
					usuarios[indice].estado = 'INACTIVO'

					alUsuarios = open(afUsuarios, "w+b")
					pickle.dump(usuarios, alUsuarios)
					alUsuarios.close()

				print(' Listo') 
				sleep(4)
				return True
			elif confirmar == 'N':
				ptos_suspensivos(' Cancelando')
				return False
			else: mensaje_error('La opcion no es valida')
	else:
		mensaje_error('No se pueden eliminar mas usuarios')
		sleep(1.5)
		ptos_suspensivos()

def ver_candidatos(indice):
	limpiar()
	for i in range(cant_usuarios):
		if i != indice and usuarios[i].estado == 'ACTIVO':
			mostrar_usuario(usuarios[i])

	while True:
		me_gusta = input('\n Ingrese el nombre de un estudiante: ').capitalize()

		for i in range(cant_usuarios):
			if usuarios[i].nombre == me_gusta and usuarios[indice].nombre != me_gusta:
				likes[indice][i] = 1
				alLikes = open(afLikes, "w+b")
				pickle.dump(likes, alLikes)
				alLikes.close()

				print('\n Usuario guardado como posible match')
				sleep(1.5)
				ptos_suspensivos()
				return 0
		mensaje_error('El nombre no coincide con ningun usuario')

def reportar_candidato(indice):
	global cant_reportes
	
	if cant_reportes == 60:
		print(' No se aceptan mas reportes\n')
		sleep(1)
		ptos_suspensivos()
	else:
		salir = False
		while not salir:
			elim = input(' Ingrese el nombre o ID del usuario: ')
			try:
				elim = int(elim)
				if elim != indice and elim < cant_usuarios and elim >= 0 and usuarios[elim].estado == 'ACTIVO': 
					print('\n ID:', usuarios[elim].id)
					mostrar_usuario(usuarios[elim])

					reportes[cant_reportes].id_reportante = int(indice)
					reportes[cant_reportes].id_reportado = int(elim)
					reportes[cant_reportes].estado = 0
					reportes[cant_reportes].motivo = input(' Ingrese el motivo del reporte: ')

					alReportes = open(afReportes, "w+b")
					pickle.dump(reportes, alReportes)
					alReportes.close()

					salir = True
					cant_reportes += 1
					print('\n Reporte guardado')
					sleep(1)
					ptos_suspensivos()

			except ValueError:
				for i in range(cant_usuarios):
					if elim.capitalize() != usuarios[indice].nombre and elim.capitalize() == usuarios[i].nombre and usuarios[i].estado == 'ACTIVO': 
						print('\n ID:', usuarios[i].id)
						mostrar_usuario(usuarios[i])
						
						reportes[cant_reportes].id_reportante = int(indice)
						reportes[cant_reportes].id_reportado = i
						reportes[cant_reportes].estado = 0
						reportes[cant_reportes].motivo = input(' Ingrese el motivo del reporte: ')

						alReportes = open(afReportes, "w+b")
						pickle.dump(reportes, alReportes)
						alReportes.close()

						salir = True
						cant_reportes += 1
						print('\n Reporte guardado')
						sleep(1)
						ptos_suspensivos()

			if not salir: mensaje_error('No se encontro el usuario o ID')

def reportes_est(indice, test=False):
	limpiar()
	cont, match, ida, vuelta = 0, 0, 0, 0

	if test:
		print('      ', end='', flush=True)
		for n in range(cant_usuarios): print(n, ' ', end='', flush=True)
		print('\n     ', end='', flush=True)
		for n in range(cant_usuarios): print(' - ', end='', flush=True)
		print('')

	for i in range(cant_usuarios):
		if test: print(f' {i} |', end='', flush=True)
		for e in range(cant_usuarios): 
			if test: 
				if likes[i][e] != -1: print(' ', likes[i][e], end='', flush=True)
				else: print(' ', '\x1b[1;31m'+'x'+'\033[0;m', end='', flush=True)

			if likes[i][e] != -1 and i == indice: cont += 1
		if test: print('')

	for i in range(cant_usuarios):
		if i != indice:
			if likes[indice][i] == 1 and likes[i][indice] == 1: match += 1
			elif likes[indice][i] == 1: ida += 1
			elif likes[i][indice] == 1: vuelta += 1

	print(
		f'\n\n* Matcheados sobre el % posible: %{int((match*100)/cont)}\n'
		f'* Likes dados y no recibidos: {ida}\n'
		f'* Likes recibidos y no respondidos: {vuelta}'
	)

##MODERADOR
def desactivar_usuario():
	salir = False
	while not salir:
		elim = input(' Ingrese el nombre o ID del usuario: ')
		try:
			elim = int(elim)
			if elim < cant_usuarios and elim >= 0 and usuarios[elim].estado == 'ACTIVO': 
				print('\n ID:', usuarios[elim].id)
				mostrar_usuario(usuarios[elim])

				eliminar_perfil(elim)
				salir = True
		except ValueError:
			for i in range(cant_usuarios):
				if elim.capitalize() == usuarios[i].nombre and usuarios[i].id == 'ACTIVO': 
					print('\n ID:', usuarios[elim].id)
					mostrar_usuario(usuarios[elim])

					eliminar_perfil(i)
					salir = True

		if not salir: mensaje_error('No se encontro el usuario o ID')

def reportesPendientes():
	for n in range(60):
		if reportes[n].estado == 0: return True
	return False
def ver_reportes(indice):
	if not reportesPendientes():
		limpiar()
		print(reportes[cant_reportes-1].id_reportado)
		print('\n No hay reportes ')
		input('\n\n Presione cualquier tecla')
	else:
		for i in range(cant_reportes):
			if (
				usuarios[reportes[i].id_reportante].estado == 'ACTIVO' and 
				usuarios[reportes[i].id_reportado].estado == 'ACTIVO' and 
				reportes[i].estado == 0
			):
				idReportante = reportes[i].id_reportante
				idReportado = reportes[i].id_reportado
				print(
					f'-----------------------------------------'
					f'\n ID reportante: {idReportante}\n'
					f' Nombre reportante: {usuarios[idReportante].nombre}\n'
					f'\n ID reportado: {idReportado}\n'
					f' Nombre reportado: {usuarios[idReportado].nombre}\n'
					f'\n Motivo: {reportes[i].motivo}\n'
					f'------------------------------------------'
					f'\n\n Que desea hacer: '
					f'\n  1. ignorar reporte'
					f'\n  2. bloquear usuario\n'
				)
				
				salir = False
				while not salir:
					try:	
						opcion = int(input(': '))

						if opcion == 1:
							reportes[i].motivo = 1
							reportes[i].id_moderador = indice

							print('\nReporte ignorado\n')
							sleep(2)
							salir = True
						elif opcion == 2:
							if eliminar_perfil(idReportado): 
								reportes[i].motivo = 2
								reportes[i].id_moderador = indice

							print('\n')
							salir = True
						else: mensaje_error('La opcion no existe')

					except ValueError:
						mensaje_error('Ingrese una numero entero')
						
		alReportes = open(afReportes, "w+b")
		pickle.dump(reportes, alReportes)
		alReportes.close()

		print(' No quedan mas reportes')
		sleep(2)
		ptos_suspensivos()

##ADMINISTRADOR
def desactivar_usuario_moderador():
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
					while not salir:
						elim = input(' Ingrese el ID del moderador: ')
						try:
							elim = int(elim)
							if elim < cant_moderadores and elim >= 0 and moderadores[elim].estado == 'ACTIVO': 
								print(
									f'\n  ID: {moderadores[elim].id}'
									f'\n  Email: {moderadores[elim].email}\n'
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
	while email_rep(email):
		mensaje_error('El email ya se encuentra registrado')
		email = input(' Ingrese otro email: ')

	contraseña = input(' Ingrese la contraseña: ')

	moderadores[cant_moderadores].id = cant_moderadores
	moderadores[cant_moderadores].estado = 'ACTIVO'
	moderadores[cant_moderadores].email = email
	moderadores[cant_moderadores].contraseña = contraseña
	cant_moderadores += 1

	alModeradores = open(afModeradores, "w+b")
	pickle.dump(moderadores, alModeradores)
	alModeradores.close()

	print('\n Registrado')
	sleep(1)
	ptos_suspensivos()

def mayor_contador(arr):
	indice = 0
	for i in range(1, len(arr)):
		if arr[i] > arr[i-1]: indice = i
	return indice
# Sin testear
def reportes_est_admin(test=False):
	reportes_ignorados, reportes_aceptados = 0, 0
	acciones_reportes = [[0]*cant_moderadores for n in range(2)]
	acciones_total_reportes = [0 for n in range(cant_moderadores)]

	limpiar()
	if cant_reportes > 0:
		for i in range(cant_reportes):
			if reportes[i].estado == 1: 
				reportes_ignorados += 1
				acciones_reportes[0][reportes[i].id_moderador] += 1

			if reportes[i].estado == 2: 
				reportes_aceptados += 1
				acciones_reportes[1][reportes[i].id_moderador] += 1
		
		for i in range(cant_moderadores):
			acciones_total_reportes[i] = acciones_reportes[0][i] + acciones_reportes[1][i]

		if test:
			print(acciones_reportes[0])
			print(acciones_reportes[1])
			print(acciones_total_reportes)
		print(
			f'\n* Cantidad de reportes: {cant_reportes}\n'
			f'* % de reportes ignorados: %{int((reportes_ignorados*100)/cant_reportes)}\n'
			f'* % de reportes aceptados: %{int((reportes_aceptados*100)/cant_reportes)}\n\n'
			f'* Moderador con mas reportes ignorados: {moderadores[mayor_contador(acciones_reportes[0])].email}\n'
			f'* Moderador con mas reportes aceptados: {moderadores[mayor_contador(acciones_reportes[1])].email}\n'
			f'* Moderador con mas reportes procesados: {moderadores[mayor_contador(acciones_total_reportes)].email}'
		)
	else: print('\n No hay reportes')

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
	input('\n\nPresione cualquier tecla ')
	
def matcheos_comb_bonus():
	cont = 0
	for i in range(cant_usuarios):
		if usuarios[i].estado == 'ACTIVO': cont += 1
	
	limpiar()
	matcheos = cont * (cont - 1)
	print('\n Cantidad de usuarios:', cont - 1)
	print(' Matcheos posibles:', matcheos, '\n')

	input('\n\nPresione cualquier tecla ')

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
					if eliminar_perfil(indice): salir = True
			case 2:
				sub_opcion = ingresar_submenu(menu2)
				if sub_opcion == 'a': ver_candidatos(indice)
				elif sub_opcion == 'b': reportar_candidato(indice)    
			case 4:
				reportes_est(indice, True)
				input('\n\n Presione cualquier tecla')

def pagina_moderador(indice):
	salir = False
	while not salir:
		opcion = ingresar_menu(menu_mod, [0, 1, 2])

		if opcion == 0:
			cerrar_sesion()
			salir = True
		elif opcion == 1:
			sub_opcion = ingresar_submenu(menu_mod1, ['a', 'b'])
			if sub_opcion == 'a': desactivar_usuario() 	
		elif opcion == 2:
			sub_opcion = ingresar_submenu(menu_mod2, ['a', 'b'])
			if sub_opcion == 'a': ver_reportes(indice)

def pagina_admin():
	salir = False
	while not salir:
		opcion = ingresar_menu(menu_mod, [0, 1, 3], [2])

		if opcion == 0:
			cerrar_sesion()
			salir = True
		elif opcion == 1:
			sub_opcion = ingresar_submenu(menu_admin1, ['b', 'c', 'd'], ['a'])
			if sub_opcion == 'b': alta_moderador()
			elif sub_opcion == 'c': desactivar_usuario_moderador()
		elif opcion == 3:
			reportes_est_admin(True)
			input('\n\n Presione cualquier tecla')

def crear_cookie(id, tipo):
	global cookie
	cookie.id = id
	cookie.tipo = tipo
	cookie.time = datetime.now() + timedelta(hours=vto_horas)

opcion = None
while opcion != 0:
	limpiar()
	print(menu_inicio)
	inicializacion(True)

	if cookie.id != None:
		indice = cookie.id
		opc_modo = cookie.tipo

		if opc_modo == 1:
			pagina_usuario(indice)
		elif opc_modo == 2:  
			pagina_moderador(indice)
		elif opc_modo == 3:  
			pagina_admin()
	else:
		try:
			opcion = int(input(' Ingrese una opción: '))
			if opcion > 5 or opcion < 0: mensaje_error('La opción no es válida')
			elif opcion == 1: 
				opc_modo = 0
				indice = login()
				if indice != -1:
					crear_cookie(indice, opc_modo)
					alCookie = open(afCookie, "w+b")
					pickle.dump(cookie, alCookie)
					alCookie.close()

					if opc_modo == 1:
						pagina_usuario(indice)
					elif opc_modo == 2:  
						pagina_moderador(indice)
					elif opc_modo == 3:  
						pagina_admin()
					else: mensaje_error('Ingrese una opcion valida')
			elif opcion == 2:
				if cant_usuarios == 20: mensaje_error('No hay espacio en la base de datos')
				else: pagina_usuario(signup())
			elif opcion == 3:
				ruleta_bonus()
			elif opcion == 4:
				edades_bonus()
			elif opcion == 5:
				matcheos_comb_bonus()

			if opcion > 0 and opcion < 6:
				limpiar()
				print(menu_inicio)
		
		except ValueError:
			mensaje_error('Ingrese un numero entero')
print('')