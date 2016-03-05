#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# main.py
# Copyright (C) 2016 Aurelio Gallardo Rodr??guez <inf2bacseritium@gmail.com>
# 
# resistencias is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# resistencias is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, GdkPixbuf, Gdk
import os, sys, math

#Comment the first line and uncomment the second before installing
#or making the tarball (alternatively, use project variables)
UI_FILE = "src/resistencias.ui"
# UI_FILE = "/usr/local/share/resistencias/ui/resistencias.ui"

# =========
# Funciones
# =========

# ===============
# Clase principal 
# ===============
class GUI:

	# --> Listado de los colores de las bandas 
	# índice, color de la banda (descripción), código color fondo, código color texto
	listaColores = [ # --> lista que representa a los colores principales.
		[0,"Negro",'#000000','#FFFFFF'],
		[1,"Marrón",'#8C662E','#000000'],
		[2,"Rojo",'#FF0000','#000000'],
		[3,"Naranja",'#FE9A2E','#000000'],
		[4,"Amarillo",'#EBEB5F','#000000'],
		[5,"Verde",'#00FF00','#000000'],
		[6,"Azul",'#0000FF','#FFFFFF'],
		[7,"Violeta",'#BF00FF','#FFFFFF'],
		[8,"Gris",'#848484','#000000'],
		[9,"Blanco",'#FFFFFF','#000000'], 
	]

	listaTolerancias = [ # --> lista que representa a los colores de las tolerancias principales.
		[0,"Oro",'#ffd700','#000000'],
		[1,"Plata",'#6b8096','#000000'],
	]

	R = 0.0 # --> Resultado del cálculo
	Tol = 0.0 # --> Tolerancia
	columnas = [0,0,0,0] # --> Guarda los datos de cada columna.

	factor = 0 # -> Corresponde a Ohmios
	unidades = ["","K","M"] # -> Multiplicadores

	colorMarcado = "LightSteelBlue" # -> Color que indica el valor seleccionado

	listaComercial = [10,12,15,18,22,27,33,39,47,51,56,68,75,82,91] # -> Valores comerciales
		#-> Hasta el 22 tiene Mega, después no

	# -> listado de los valores comerciales entre 10 y 22M
	valoresComerciales =[]
	for i in range(0,7): # -> -1 para las que son entre 1 y 10.
		for k in listaComercial:
			if i<=5 or (i==6 and k<=22):
				valoresComerciales.append(k * 10 ** i)

	# ================
	# Método principal 
	# ================

	def __init__(self):

		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)

		window = self.builder.get_object('miVentana')

		lblResultado = self.builder.get_object('labelResultado')

		cmb1 = self.builder.get_object('listadoUnidades') # --> Objeto combo
		listado1 = self.builder.get_object('liststore1') # --> Objeto listado
		cmb1.set_model(listado1)  # --> Establece que para ese combo el modelo es el del listado dado
		render=Gtk.CellRendererText() # --> Objeto que se dibuja sobre otro.
		cmb1.pack_start(render, True) 
		cmb1.add_attribute(render, 'text', 0) # --> columna 
		#supuestamente con esta  linea se activa el evento change
		# cmb1.set_active(0)

		self.txtValor = self.builder.get_object('txtValor') # --> Objeto texto
		self.lblR1 = self.builder.get_object('labelResultado1') # --> Se imprime el resultado al cmabiar la entrada
		self.lblRenSerie = self.builder.get_object('labelResultadoSerie') # --> Etiqueta de resultados en serie
		self.lblRenParalelo = self.builder.get_object('labelResultadoParalelo') # --> Etiqueta de resultados en paralelo
		self.lblR1.set_text("- - - ")
		self.lblRenSerie.set_text("- - - ")
		self.lblRenParalelo.set_text("- - - ") # -> valores iniciales de las etiquetas

		# print self.valoresComerciales				
		
		# ========================================
		# Añado los botones a cada caja de botones
		# ========================================
		caja=[] # --> lista vacía
		for i in range(0,3): # --> por cada caja (parámetro i)
			caja.append(self.builder.get_object('cBotones'+str(i+1))) # --> Obtengo la zona dibujada		
			for elementos in self.listaColores:
				print elementos[0], " - ", elementos[1], " - ", elementos[2]," - ", elementos[3]
				# boton = Gtk.Button() --> No uso botones por no poder cambiarle el color
				# boton.set_label(i)--> No uso botones por no poder cambiarle el color
				etiqueta = Gtk.Label()	# etiqueta.set_text(i) --> ya se pone en markup
				etiqueta.set_markup('<span foreground="'+elementos[3]+'">'+elementos[1]+'</span>')
					# Ver PANGO MARKUP Language http://www.pygtk.org/pygtk2reference/pango-markup-language.html
				botonCon = Gtk.EventBox() # --> utilizo "cajas de eventos"
				botonCon.connect('button-press-event', self.fclick, elementos[0],i,elementos[2],lblResultado)
				botonCon.add(etiqueta)		
				botonCon.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(elementos[2]))
				# botonCon.add(boton) --> No uso botones por no poder cambiarle el color
				caja[i].add(botonCon)

		# ========================================
		# Añado los botones a la caja de Tolerancias
		# ========================================
		caja.append(self.builder.get_object('cBotones4'))
		for elementos in self.listaTolerancias:
			print elementos[0], " - ", elementos[1], " - ", elementos[2]," - ", elementos[3]
			etiqueta = Gtk.Label()	# etiqueta.set_text(i) --> ya se pone en markup
			etiqueta.set_markup('<span foreground="'+elementos[3]+'">'+elementos[1]+'</span>')
			# Ver PANGO MARKUP Language http://www.pygtk.org/pygtk2reference/pango-markup-language.html
			botonCon = Gtk.EventBox() # --> utilizo "cajas de eventos"
			botonCon.connect('button-press-event', self.fclick, elementos[0],3,elementos[2],lblResultado)
			botonCon.add(etiqueta)		
			botonCon.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(elementos[2]))
			# botonCon.add(boton) --> No uso botones por no poder cambiarle el color
			caja[3].add(botonCon)

		# =================
		# Valores iniciales
		# =================
		# colorea del color de marcado (selección) a los EventBox Marrón - Negro -Negro -Oro
		# Corresponde al valor inicial 10 Ohmios
		self.cambiarColor(self.builder.get_object('cBotones1').get_children()[1],self.colorMarcado)
		self.cambiarColor(self.builder.get_object('cBotones2').get_children()[0],self.colorMarcado)
		self.cambiarColor(self.builder.get_object('cBotones3').get_children()[0],self.colorMarcado)
		self.cambiarColor(self.builder.get_object('cBotones4').get_children()[0],self.colorMarcado)
		self.columnas = [1,0,0,0]
		self.calcularResultado(lblResultado) # --> Muestra el resultado.
		
		# ===============
		# Mostrar ventana
		# ===============
		window.show_all()

	# ===============
	# Métodos	
	# ===============	
	
	# No lo borro porque son la muestra de manejo de checkboxes y radiobuttons
	'''def on_toogled_muestra(self, widget):
		print widget.get_active()

	def dos_res(self, widget):
		valor = self.txtValor.get_text()
		valor = valor.replace(",",".") #-> Si escriben coma, se reemplaza con punto
		valor = self.multiplo(valor) # -> Cálculo con las letras
		# --> Si elijo resistencias en serie
		if widget.get_active() and widget.get_label()=="Serie" and float(valor)>=100:
			print "Activado Serie"
		# --> Si elijo resistencias en paralelo
		if widget.get_active() and widget.get_label()=="Paralelo" and float(valor)>1:
			print "Activado Paralelo"'''
			
	
	# METODO 1: Al cambiar el valor de la entrada numérica txtValor
	# Escribe un valor en la caja de texto y calcula resistencias
	def on_change_valor(self, widget):
		# pre: el texto del GtkEntry. Debe ser un valor numérico mayor que 0, aunque se acepte como texto.
		# pre: Admite las letras al final k y m (tb. en mayúsculas) como múltiplos válidos
		# post: devuelve las cadenas de las correspondientes etiquetas: resultado, enSerie y enParalelo
		texto_widget = widget.get_text() 
		imprimir = self.muestraColores(texto_widget)
		self.lblR1.set_label(imprimir)
		self.lblRenSerie.set_label(self.enSerie(texto_widget))
		self.lblRenParalelo.set_label(self.enParalelo(texto_widget))
	
	# METODO 2:Al cambiar el valor del combo
	def on_listadoUnidades_changed(self, widget):
		modelo = widget.get_model() # --> Obtiene el modelo de datos
		activo = widget.get_active() # --> Obtiene el que se activa
		obtenido = modelo[activo][1] # --> así se escoge el de la columna ....[n]
		# http://pitonpy.blogspot.com.es/search/?q=combobox
		self.factor=obtenido # --> Obtiene el factor de la lista
		# self.calcularResultado(lblResultado)
		self.calcularResultado(self.builder.get_object('labelResultado')) # -> ¿Única manera de obtener el objeto?
		# print self.factor
	
	# METODO 3:Al hacer click, cambia de color una casilla y calcula el resultado R
	def fclick(self, widget, *data):
		# pre: widget --> un elemento GTKEVENTOBOX pulsado ¿y/o data[0]?
		# pre: data[1]: índice del elemento pulsado 0,1,2...,9
		# pre: data[2]: columna afectada. Banda 1, 2, Multiplicador o Tolerancia
		# pre: data[3]: código de color
		# pre: data[4]: widget donde se escribe el resultado lblResultado
		# post: en la columna seleccionada, debe quedarse marcada el nuevo valor escogido y debe presentarse
		# post: en la etiqueta, el valor de resistencia correspondiente
		# print widget
		col = data[2] # --> columna de la que se trata
		dato = data[1] # --> dato a calcular
		# widgetLabel = data[4] # -->  Objeto o widget a modificar
		self.resetColores(widget, col) # --> Reinicializa los colores de una banda "limpiar colores"
		self.cambiarColor(widget,self.colorMarcado) # --> en el widget, marca con el color de marcado 
		# En las pruebas, pintaba de rosa. widget.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("pink"))
		self.columnas[col] = dato # --> modifico la variable columnas con el nuevo dato
		self.calcularResultado(data[4]) # --> Envía el resultado a presentar a otro lugar. Pasa el widget lblResultado

	# METODO 4: Marca con un color el widget GTKEVENTBOX clicado
	def cambiarColor(self, widgetMarcado, strColor):
		# pre: widget que se ha pulsado
		# pre: strColor: se le pasa un color determinado
		# post: el widget marcado debe haber cambiado el color 
		widgetMarcado.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(strColor)) # --> el color de cada uno
		
	# METODO 5: Realiza el cálculo de las bandas clicads y lo presenta en el label
	def calcularResultado(self, widgetLabel):
		# pre: widgetLabel --> en qué objeto label presentará el resultado
		# pre: variables GLOBALES resultado R, tolerancia TOL
		# post: cambia el valor en la etiqueta correspondiente
		# invariantes: R es siempre el valor nominal de las resistencias marcadas por sus bandas, Tol
		# la tolerancia.
		self.R = (self.columnas[0]*10+self.columnas[1])*10 ** self.columnas[2]
		self.Tol = 0.05*(self.columnas[3]+1)*self.R
		dividiendo = 10 ** (self.factor*3) # --> factores de miles
		uni = self.unidades[self.factor]
		presentarEtiqueta = "Resultado: " + str(float(self.R)/float(dividiendo)) + chr(32) + unichr(177) 
		presentarEtiqueta += chr(32) + str(self.Tol/dividiendo) + chr(32) + uni + unichr(937) + "\n"
		presentarEtiqueta += "["+str((self.R-self.Tol)/dividiendo)+chr(32) +uni +unichr(937)+" , "+str((self.R+self.Tol)/dividiendo)+chr(32) +uni+unichr(937)+"]"
		widgetLabel.set_label(presentarEtiqueta)
		widgetLabel.set_justify(2) # --> 2 es centrar
		
	# METODO 6: Reinicializa los colores de cada una de las tres columnas principales.	
	def resetColores(self,wid,columna):
		# pre: acepta un widget GTKEVENTBOX clicado
		# pre: acepta el valor de una de las columnas
		# post: coloca los colores iniciales de la banda entera donde se ha clicado. Desmarca lo marcado.
		padre = wid.get_parent() # --> obtiene el contenedor
		hijos = padre.get_children() # --> lista de los hijos
		for cada in hijos: # --> por cada hijo
			indice = hijos.index(cada) # --> obtiene el índice
			if columna<=2: # --> Siestoy en las columnas 0, 1 ó 2
				colorReset = self.listaColores[indice] # --> lista correspondiente a cada Banda
			elif columna == 3: # --> Estoy en la columna de tolerancia
				colorReset = self.listaTolerancias[indice] # --> la lista correspondiente a las Tolerancias
			cada.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(colorReset[2])) # --> el color de cada uno
		
	# METODO 7: Cierra la ventana
	def on_window_destroy(self, window):
		Gtk.main_quit()

	# ==================
	# Métodos no señales
	# ==================

	# MÉTODO 8: Valor como resultado de dos resistencias en serie comerciales
	def enSerie(self,valor):
		# pre: valor escrito en la caja de texto, en formato string
		# post: string con el resultado de dos resistencias en serie
		valor = valor.replace(",",".") #-> Si escriben coma, se reemplaza con punto
		valor = self.multiplo(valor) # --> Si se escribe K ó M, se añaden los ceros correspondientes
		try: 
			# -> Calcula los límites comerciales 
			min = 2*self.valoresComerciales[0] # --> mínima suma posible 
			max = 2.0 * self.valoresComerciales[-1] # -> máxima suma posible
			if float(valor)<min or float(valor)>max: # --> Si está fuera de ese rango, no puedo calcularlo
				return "Lo siento, no puedo calcularla como dos resistencias comerciales en serie"
			# -> Encuentra la lista de subvalores en los que buscar.
			# ========= Bucle que delimita la lista a unos valores en los que es posible la suma =======
			for n in sorted(self.valoresComerciales,reverse = True):
				tope = n
				if float(valor)>float(tope):
					break
			indice = self.valoresComerciales.index(tope)
			sublista = self.valoresComerciales[:indice+1] # --> Sublista donde es posible la suma
			# ==========================================================================================
			# -> Algoritmo de suma: calcula valor1 y valor2, como los que tienen menor diferencia respecto al valor
			# -> Introducido en la caja de texto
			valor1 = 0.0
			valor2 = 0.0
			for i in sublista:
				for j in sublista:
					if abs(float(valor)-(valor1+valor2))>abs(float(valor)-(i+j)):
						valor1 = i
						valor2 = j
			#-> valores devueltos
			devolver = self.muestraColores(str(valor1))
			devolver += " y " 
			devolver += self.muestraColores(str(valor2))
			return devolver

		except Exception, ex:
			print "Se ha producido otro tipo de error: " + str(ex)
			return "No se ha podido calcular resistencias en serie"
			
	# MÉTODO 9: Valor como resultado de dos resistencias en paralelo comerciales
	def enParalelo(self,valor):
		# pre: valor escrito en la caja de texto, en formato string
		# post: string con el resultado de dos resistencias en paralelo		
		valor = valor.replace(",",".") #-> Si escriben coma, se reemplaza con punto
		valor = self.multiplo(valor) # --> Si se escribe K ó M, se añaden los ceros correspondientes
		# ========= Los valores comerciales se transforman en sus inversos ==================
		# Así es posible casi usar el algoritmo "serie", pero para 1/R
		valoresComercialesInverso = []		
		for k in self.valoresComerciales:
			valoresComercialesInverso.append(1/float(k))
		# print sorted(valoresComercialesInverso)
		# ===================================================================================
		try: 
			valorInverso = 1.0/float(valor) # --> Inverso del valor que he introducido en la caja de texto
			max = 2.0 * valoresComercialesInverso[0] # --> máxima suma posible 
			min = 2.0 * valoresComercialesInverso[-1] # --> mínima suma posible
			# print min, max, valorInverso
			if valorInverso < min or valorInverso > max: # --> Si está fuera de ese rango, no puedo calcularlo
				return "Lo siento, no puedo calcularla como dos resistencias comerciales en paralelo"
			# ========= Bucle que delimita la lista a unos valores en los que es posible la suma =======
			# IMPORTANTE: lista ordenada, de menor a mayor
			for n in sorted(valoresComercialesInverso):
				# print n
				tope = n
				if tope>valorInverso: # --> si el elemento tope es mayor que el que busco, para
					break
			indice = sorted(valoresComercialesInverso).index(tope)
			sublista = sorted(valoresComercialesInverso)[:indice]
			# ===========================================================================================
			# print tope, valorInverso, indice
			# print sublista
			# ==========================================================================================
			# -> Algoritmo de suma: calcula valor1 y valor2, como los que tienen menor diferencia respecto al valorInverso
			valor1 = 0.0
			valor2 = 0.0
			for i in sublista:
				for j in sublista:
					if abs(valorInverso-(valor1+valor2))>abs(valorInverso-(i+j)):
						valor1 = i
						valor2 = j
			#-> valores devueltos
			# ===========================================================================================
			# return str(valorInverso) + " " + str(int(1/valor1)) + " "+  str(int(1/valor2))
			devolver = self.muestraColores(str(int(1/valor1)))
			devolver += " y " 
			devolver += self.muestraColores(str(int(1/valor2)))
			return devolver
			
		except Exception, ex:
			print "Se ha producido otro tipo de error: " + str(ex)
			return "No se ha podido calcular resistencias en paralelo"


	# MÉTODO 10: Calcula el multiplo 
	def multiplo(self, valor):
		# pre: valor, string escrito en la caja de texto
		# post: traduce la K por tres ceros y la M por seis ceros.
		try: 
			ultimo = valor[-1].upper()
			# --> print ultimo
			if ultimo == "K":
				valor = str(float(valor[:-1])*1000)
			elif ultimo == "M":
				valor = str(float(valor[:-1])* 10 ** 6)
			return valor

		except Exception, ex:
			print "Se ha producido otro tipo de error: " + str(ex)
			return "0" # --> devuelve cero en caso que la cadena no sea válida

	# MÉTODO 11: escribe un múltiplo
	def escribeMultiplo(self, valor):
		# pre: acepta un valor (string) 
		# post: devuelve el valor formateado en múltiplos según los miles (K) y los millones (M)
		# post: presenta más elegantemente resultados en los label serie y paralelo
		try:
			if float(valor)>=10 ** 3 and float(valor)<10 ** 6:
				valor = str(float(valor)/1000) + "K"
			elif float(valor)>=10**6:
				valor = str(float(valor)/10**6) + "M"
			return valor
			
		except Exception, ex:
			print "Error en escribeMultiplo",str(ex)
		
			
	# Método 12: Función que retorna una cadena con los colores ajustados a una resistencia.
	def muestraColores(self,valor):
		# pre: valor introducido en la caja de texto
		# post: una cadena que indica la resistencia correspondiente en colores y en valor
		valor = valor.replace(",",".") #-> Si escriben coma, se reemplaza con punto
		colorBanda=["","",""] # --> Listado con los resultados de los colores
		try:
			# --> Añadido de factores
			valor = self.multiplo(valor) # -> comprueba lo de la letra K y M
			# --> Cálculo de las bandas.
			if float(valor)>=0 and float(valor)<=9:
				colorBanda[0]=self.listaColores[0][1] # --> SIN DECENAS, 0
				colorBanda[1]=self.listaColores[int(float(valor))][1] # --> Factor de las unidades
				colorBanda[2]=self.listaColores[0][1] # --> Sin facto de multiplicación, cero
				num = str(self.listaColores[int(float(valor))][0]) # --> Construye como número
			elif float(valor)>9 and float(valor)<=99:
				colorBanda[0]  = self.listaColores[int(float(valor)/10.0)][1] # --> primer valor, decenas
				colorBanda[1]  = self.listaColores[int(float(valor)%10.0)][1] # --> segundo valor, unidades
				colorBanda[2]  = self.listaColores[0][1] # --> tercer valor 0
				# --> Construye como número
				num = str(self.listaColores[int(float(valor)/10.0)][0]) + str(self.listaColores[int(float(valor)%10.0)][0])
			elif float(valor)>99:
				digitos3mas = 10 ** (len(str(int(round(float(valor)))))-2)
					# -> Redondeo, paso a cadena y calculo el número de dígitos
				valor = str(digitos3mas*round(float(valor)/digitos3mas))
					# -> print digitos3mas, valor, float(valor[2:])
					# Nuevo valor según las bandas que son posibles.
				numceros =  int(math.ceil(math.log10(float(digitos3mas))))
					# --> A la potencia de 10 se le hace el logaritmo B10 para obtener número de ceros
				colorBanda[0]  = self.listaColores[int(valor[0])][1] # --> decenas
				colorBanda[1]  = self.listaColores[int(valor[1])][1] # --> unidades
				colorBanda[2]  = self.listaColores[numceros][1] # --> valor según el número de ceros
				# --> Construye como número
				num = str(self.listaColores[int(valor[0])][0]) + str(self.listaColores[int(valor[1])][0]) + "0" * numceros

			# Presenta el resultado
			resultado =  colorBanda[0]  +" - " + colorBanda[1] + " - "+colorBanda[2]
			resultado += " ("+ self.escribeMultiplo(num) +unichr(937).encode('utf-8') +")" 
			return resultado

		except ValueError:
			return "Debes escribir un número mayor que cero."
		
		except Exception, ex:
			print "Se ha producido otro tipo de error: " + str(ex)

		
# ===============
# PROGRAMA MAIN
# ===============	
		
def main():
	app = GUI()
	Gtk.main()
		
if __name__ == "__main__":
	sys.exit(main())

