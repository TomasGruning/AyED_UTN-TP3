# TP3 - Tomás Gruning, Lucía Godoy, Joaquin Raffaelli
import random
import pickle
from datetime import datetime
from pwinput import pwinput
from random import randint
from time import sleep
from os import system, name, path

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
menu_inicio_login = '''
  1. Usuario
  2. Moderador
'''

#DATOS
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
		self.email = None
		self.contraseña = None

##USUARIOS
afUsuarios = './usuarios.dat'
usuarios = [Usuario() for n in range(20)]

if path.exists(afUsuarios):
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

ultimo_usuario = 0
for i in usuarios: 
	if i.id != None: ultimo_usuario += 1

##MODERADORES
afModeradores = './moderadores.dat'
moderadores = [Moderador() for n in range(10)]

if path.exists(afModeradores):
	alModeradores = open(afModeradores, "r+b")
	moderadores = pickle.load(alModeradores)
else:
	alModeradores = open(afModeradores, "w+b")

	for n in range(3): moderadores[n].id = n
	moderadores[0].email = 'moderador1@ayed.com'
	moderadores[0].contraseña = 'mod111222'

	moderadores[1].email = 'moderador2@ayed.com'
	moderadores[1].contraseña = 'mod333444'

	moderadores[2].email = 'moderador3@ayed.com'
	moderadores[2].contraseña = 'mod555666'
	pickle.dump(moderadores, alModeradores)
alModeradores.close()

##EXTRAS
reportes_candidatos = [[-1]*3 for n in range(24)]
motivos_reportes = [None for n in range(24)]

likes = [[0]*ultimo_usuario for n in range(ultimo_usuario)]
for i in range(ultimo_usuario):
	for e in range(ultimo_usuario):
		if usuarios[i].estado == 'ACTIVO' and usuarios[e].estado == 'ACTIVO' and i != e:
			likes[i][e] = randint(0, 1)
			likes[e][i] = randint(0, 1)
		else:
			likes[i][e] = -1
			likes[e][i] = -1

#FUNCIONES
##ESTETICA
def limpiar():
	system('cls' if name == 'nt' else 'clear')
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
def verificar_tipo(email, contraseña, tipo):
	if tipo == 'usuario':
		for i in range(ultimo_usuario):
			if usuarios[i].email == email and usuarios[i].contraseña == contraseña and usuarios[i].estado == 'ACTIVO':
				return i
	elif tipo == 'moderador':
		for i in range(len(moderadores)):
			if moderadores[i].email == email and moderadores[i].contraseña == contraseña:
				return i
	return -1

def login(modo):
	indice = -1
	cont = 0
	
	limpiar()
	print(' Log in  |')
	print('----------\n')

	while cont < 3:
		email = input(' Ingrese su email: ')
		contraseña = pwinput(' Ingrese su contraseña: ')

		if modo == 1: 
			indice = verificar_tipo(email, contraseña, 'usuario')
		else: 
			indice = verificar_tipo(email, contraseña, 'moderador')

		if indice == -1:
			mensaje_error('El email y/o contraseña son incorrectos')
		else:
			return indice
		cont += 1

	print('\n Maximo de intentos alcanzado')
	sleep(2)
	ptos_suspensivos()
	return indice

def emailRep(email):
	for n in range(ultimo_usuario):
		if usuarios[n].email == email: return True
	i = 0
	while moderadores[i].email:
		if moderadores[i].email == email: return True
		i += 1
	return False
def signup():
	global ultimo_usuario
	limpiar()
	print(' Sign up  |')
	print('-----------\n')

	nombre = input(' Ingrese su nombre de usuario: ')
	while not nombre.isalpha():
		mensaje_error('El nombre no puede ser un numero')
		nombre = input(' Ingrese su nombre de usuario: ')

	email = input(' Ingrese su email: ')
	while emailRep(email):
		mensaje_error('El email ya se encuentra registrado')
		email = input(' Ingrese su email: ')
	else:
		contraseña = input(' Ingrese su contraseña: ')

		fecha_nacimiento = input(' Ingrese su fecha de nacimiento (YYYY-MM-DD): ')
		while not calcular_edad(fecha_nacimiento): 
			fecha_nacimiento = input(' Ingrese su fecha de nacimiento (YYYY-MM-DD): ')

		biografia = input(' Ingrese una biografia: ')
		hobbies = input(' Ingrese sus hobbies: ')

		usuarios[ultimo_usuario].id = ultimo_usuario
		usuarios[ultimo_usuario].estado = 'ACTIVO'
		usuarios[ultimo_usuario].nombre = nombre
		usuarios[ultimo_usuario].email = email
		usuarios[ultimo_usuario].contraseña = contraseña
		usuarios[ultimo_usuario].fecha_nacimiento = fecha_nacimiento
		usuarios[ultimo_usuario].biografia = biografia
		usuarios[ultimo_usuario].hobbies = hobbies
		ultimo_usuario += 1

		alUsuarios = open(afUsuarios, "w+b")
		pickle.dump(usuarios, alUsuarios)
		alUsuarios.close()

		print('\n Registrado')
		sleep(1)
		ptos_suspensivos()
		return i
	
##MENUS
def ingresar_menu(menu: str, opciones=[0, 1, 2, 4]):
	limpiar()
	print(menu)
	
	while True:
		try:
			opcion = int(input(' Ingrese una opción: '))

			if opcion in opciones: return opcion
			elif opcion == 3: mensaje_advertencia('En Construcción')
			else: mensaje_error('La opción no existe')

		except ValueError:
			mensaje_error('Ingrese una numero entero')

def ingresar_submenu(menu: str, opciones= ['a', 'b', 'c']):
	limpiar()
	print(menu)
	
	while True:
		opcion = input(' Ingrese una opcion: ')

		if opcion in opciones: return opcion
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

def eliminar_perfil(indice):
	print('')
	cont = 0
	for i in range(ultimo_usuario):
		if usuarios[i].estado == 'ACTIVO': cont += 1

	if cont > 4:
		confirmar = None
		while confirmar != 'S' and confirmar != 'N':
			confirmar = input(' Esta seguro? [S/N]: ').upper()
			if confirmar == 'S':
				ptos_suspensivos(' Eliminando usuario')
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
	for i in range(ultimo_usuario):
		if i != indice and usuarios[i].estado == 'ACTIVO':
			mostrar_usuario(usuarios[i])

	while True:
		me_gusta = input('\n Ingrese el nombre de un estudiante: ').capitalize()

		for i in range(ultimo_usuario):
			if usuarios[i].nombre == me_gusta and usuarios[indice].nombre != me_gusta:
				likes[indice][i] = 1
				print('\n Usuario guardado como posible match')
				sleep(1.5)
				ptos_suspensivos()
				return 0
		mensaje_error('El nombre no coincide con ningun usuario')

def ultimo_reporte():
	cont = 0
	for i in range(len(motivos_reportes)):
		if motivos_reportes[i]: cont += 1
	
	if cont < len(motivos_reportes):
		return cont
	else:
		return -1
def reportar_candidato(indice):
	espacioDisponible = ultimo_reporte()

	if espacioDisponible == -1:
		print(' No se aceptan mas reportes\n')
		sleep(1)
		ptos_suspensivos()
	else:
		salir = False
		while not salir:
			elim = input(' Ingrese el nombre o ID del usuario: ')
			try:
				elim = int(elim)
				if elim != indice and elim < ultimo_usuario and elim >= 0 and usuarios[elim].estado == 'ACTIVO': 
					print('\n ID:', usuarios[elim].id)
					mostrar_usuario(usuarios[elim])

					motivos_reportes[espacioDisponible] = input(' Ingrese el motivo del reporte: ')
					reportes_candidatos[espacioDisponible][0] = int(indice)
					reportes_candidatos[espacioDisponible][1] = int(elim)
					reportes_candidatos[espacioDisponible][2] = 0
					salir = True
					print('\n Reporte guardado')
					sleep(1)
					ptos_suspensivos()

			except ValueError:
				for i in range(ultimo_usuario):
					if elim.capitalize() != usuarios[indice].nombre and elim.capitalize() == usuarios[i].nombre and usuarios[i].estado == 'ACTIVO': 
						print('\n ID:', usuarios[elim].id)
						mostrar_usuario(usuarios[elim])
						
						motivos_reportes[espacioDisponible] = input('\n Ingrese el motivo del reporte: ')
						reportes_candidatos[espacioDisponible][0] = int(indice)
						reportes_candidatos[espacioDisponible][1] = i
						reportes_candidatos[espacioDisponible][2] = 0
						salir = True
						print('\n Reporte guardado')
						sleep(1)
						ptos_suspensivos()

			if not salir: mensaje_error('No se encontro el usuario o ID')

def reportes_est(indice, test=False):
	limpiar()
	cont, match, ida, vuelta = 0, 0, 0, 0
	for i in range(ultimo_usuario):
		for e in range(ultimo_usuario): 
			if test: 
				if likes[i][e] != -1: print(likes[i][e], ' ', end='', flush=True)
				else: print('\x1b[1;31m'+'x'+'\033[0;m', ' ', end='', flush=True)

			if likes[i][e] != -1 and i == indice: cont += 1
		if test: print('')

	for i in range(ultimo_usuario):
		if i != indice:
			if likes[indice][i] == 1 and likes[i][indice] == 1: match += 1
			elif likes[indice][i] == 1: ida += 1
			elif likes[i][indice] == 1: vuelta += 1

	print(
		f'\nMatcheados sobre el % posible: {int((match*100)/cont)}%\n'
		f'Likes dados y no recibidos: {ida}\n'
		f'Likes recibidos y no respondidos: {vuelta}'
	)

##MODERADOR
def desactivar_usuario():
	salir = False
	while not salir:
		elim = input(' Ingrese el nombre o ID del usuario: ')
		try:
			elim = int(elim)
			if elim < ultimo_usuario and elim >= 0 and usuarios[elim].estado == 'ACTIVO': 
				print('\n ID:', usuarios[elim].id)
				mostrar_usuario(usuarios[elim])

				return eliminar_perfil(elim)
				salir = True
		except ValueError:
			for i in range(ultimo_usuario):
				if elim.capitalize() == usuarios[i].nombre and usuarios[i].id == 'ACTIVO': 
					print('\n ID:', usuarios[elim].id)
					mostrar_usuario(usuarios[elim])

					return eliminar_perfil(i)
					salir = True

		if not salir: mensaje_error('No se encontro el usuario o ID')

def ver_reportes():
	espacioDisponible = ultimo_reporte()
	if espacioDisponible == 0 or espacioDisponible == -1:
		limpiar()
		print('\n No hay reportes')
		input('\n\n Presione cualquier tecla')
	else:
		limpiar()
		for i in range(espacioDisponible):
			if (
				usuarios[reportes_candidatos[i][0]].estado == 'ACTIVO' and 
				usuarios[reportes_candidatos[i][1]].estado == 'ACTIVO' and 
				reportes_candidatos[i][2] == 0
			):
				idReportante = reportes_candidatos[i][0]
				idReportado = reportes_candidatos[i][1]
				print(
					f'-----------------------------------------'
					f'\n ID reportante: {idReportante}\n'
					f' Nombre reportante: {usuarios[idReportante].nombre}\n'
					f'\n ID reportado: {idReportado}\n'
					f' Nombre reportado: {usuarios[idReportado].nombre}\n'
					f'\n Motivo: {motivos_reportes[i]}\n'
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
							reportes_candidatos[i][2] = 1
							print('\nReporte ignorado\n')
							sleep(2)
							salir = True
						elif opcion == 2:
							if eliminar_perfil(idReportado): reportes_candidatos[i][2] = 2
							print('\n')
							salir = True
						else: mensaje_error('La opcion no existe')

					except ValueError:
						mensaje_error('Ingrese una numero entero')

		print(' No quedan mas reportes')
		sleep(2)
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
	input('\n\nPresione cualquier tecla ')
	
def matcheos_comb_bonus():
	cont = 0
	for i in range(ultimo_usuario):
		if usuarios[i].estado == 'ACTIVO': cont += 1
	
	limpiar()
	matcheos = cont * (cont - 1)
	print('\n Cantidad de usuarios:', cont - 1)
	print(' Matcheos posibles:', matcheos, '\n')

	input('\n\nPresione cualquier tecla ')

# M A I N
# opcion, opc_modo:  Integer
# sub_opcion:        Char

def pagina_usuario(indice):
	while indice != -1:
		opcion = ingresar_menu(menu)

		match opcion:
			case 0:
				ptos_suspensivos('\n Cerrando sesion')
				return 0
			case 1:
				sub_opcion = ingresar_submenu(menu1)
				if sub_opcion == 'a': editar_datos(indice)
				elif sub_opcion == 'b': 
					if eliminar_perfil(indice): return 0
			case 2:
				sub_opcion = ingresar_submenu(menu2)
				if sub_opcion == 'a': ver_candidatos(indice)
				elif sub_opcion == 'b': reportar_candidato(indice)    
			case 4:
				reportes_est(indice, True)
				input('\n\n Presione cualquier tecla')

def pagina_moderador():
	while True:
		opcion = ingresar_menu(menu_mod, [0, 1, 2])
		if opcion == 0:
			ptos_suspensivos(' Cerrando sesion')
			break
		if opcion == 1:
			sub_opcion = ingresar_submenu(menu_mod1, ['a', 'b'])
			if sub_opcion == 'a': desactivar_usuario() 	
		elif opcion == 2:
			sub_opcion = ingresar_submenu(menu_mod2, ['a', 'b'])
			if sub_opcion == 'a': ver_reportes()


limpiar()
print(menu_inicio)
opcion = None
while opcion != 0:
	try:
		opcion = int(input(' Ingrese una opción: '))
		if opcion > 5 or opcion < 0: mensaje_error('La opción no es válida')
		elif opcion == 1: 
			limpiar()
			print(menu_inicio_login)
			
			opc_modo = 0
			while opc_modo != 1 and opc_modo != 2:
				try:
					opc_modo = int(input(' Quiere iniciar como?: '))
					if opc_modo == 1:
						pagina_usuario(login(opc_modo))
					elif opc_modo == 2: 
						if login(opc_modo) != -1: pagina_moderador()
					else: mensaje_error('Ingrese una opcion valida')

				except ValueError:
					mensaje_error('Ingrese un numero entero')
		elif opcion == 2:
			if ultimo_usuario == 20: mensaje_error('No hay espacio en la base de datos')
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