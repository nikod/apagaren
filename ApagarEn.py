import dbus
from time import sleep
from threading import Thread
import pynotify

try:
	import gtk
except:
	print "Se requiere PyGYK"
	import sys
	sys.exit(1)

class gui:
	def __init__(self):
		
		filename = "apagaren.glade"
		self.builder = gtk.Builder()
		self.builder.add_from_file(filename)
		self.builder.connect_signals(self)
		
		glade = [	
				"Ventana", "fixed", "ETiempo", "Tiempo",
				"Unidad", "combobox", "combobox1", "Apagar", "Cancelar"
				]
		
		for glade in glade:
			setattr(self, glade, self.builder.get_object(glade))
		
		self.boton = gtk.timeout_add (0, self.Eboton, self)
		self.Ventana.show_all()
		
	def Apagar(self, *args):
		Thread(target=self.Accion, 
			args=(self.cb_activo(self.combobox),
				self.cb_activo(self.combobox1),
				self.ETiempo.get_text())).start()
		self.Ventana.hide()
	
	def gtk_main_quit (self, *args):
		gtk.main_quit()

	def cb_activo (self, combobox):
		model = combobox.get_model()
		activo = combobox.get_active()
		return model[activo][0]
		
	def Accion(self, seleccion1, seleccion2, tiempo):
		gtk.gdk.threads_enter()
		espera = int(Convertidor(tiempo, seleccion1))
		if seleccion2 == "Apagar":
			Thread(target=Dbus_Apagar, args=(espera,)).start()
		elif seleccion2 == "Reiniciar":
			Thread(target=Dbus_Reinciar, args=(espera,)).start()
		elif seleccion2 == "Suspender":
			Thread(target=Dbus_Suspender, args=(espera,)).start()
		elif seleccion2 == "Hibernar":
			Thread(target=Dbus_Hibernar, args=(espera,)).start()
		gtk.gdk.threads_leave()

	
	def Eboton(self, widget, data=None):
		seleccion = self.cb_activo(self.combobox1)
		self.Apagar.set_label(seleccion)

def Dbus_Apagar(espera):
	notificacion(espera)
	bus = dbus.SystemBus()
	bus_object = bus.get_object("org.freedesktop.ConsoleKit", "/org/freedesktop/ConsoleKit/Manager")
	bus_object.Stop(dbus_interface="org.freedesktop.ConsoleKit.Manager")
	
def Dbus_Reiniciar(espera):
	notificacion(espera)
	bus = dbus.SystemBus()
	bus_object = bus.get_object("org.freedesktop.ConsoleKit", "/org/freedesktop/ConsoleKit/Manager")
	bus_object.Restart(dbus_interface="org.freedesktop.ConsoleKit.Manager")

def Dbus_Suspender(espera):
	notificacion(espera)
	bus = dbus.SystemBus()
	bus_object = bus.get_object("org.freedesktop.UPower", "/org/freedesktop/UPower")
	bus_object.Suspend(dbus_interface="org.freedesktop.UPower")

def Dbus_Hibernar(espera):
	notificacion(espera)
	bus = dbus.SystemBus()
	bus_object = bus.get_object("org.freedesktop.UPower", "/org/freedesktop/UPower")
	bus_object.Hibernate(dbus_interface="org.freedesktop.UPower")

class notificacion:
	def __init__(self, tiempo):
		pynotify.init("ApagarEn")
		self.obtener_capacidades()
		self.tiempo = tiempo
		self.enviar_notificacion(tiempo)
		
	def obtener_capacidades(self):
		self.capacidades = {};
		capacidades = pynotify.get_server_caps()
		for i in capacidades:
			self.capacidades[i] = True
	
	def enviar_notificacion(self,tiempo):
		if (self.capacidades['x-canonical-private-synchronous']):
			for i in range(tiempo + 1):
				sleep(1)
				j = i*100/tiempo
				if i == 0:
					n = pynotify.Notification("ApagarEn", "", "/home/niko/GIT/apagaren/Icono.png")
				else:
					n.update("ApagarEn", "", "/home/niko/GIT/apagaren/Icono.png")
				n.set_hint_int32("value", j)
				n.set_hint_string("x-canonical-private-synchronous", "")
				n.show()
		
class Convertidor:
	def __init__(self, tiempo, seleccion):
		self.tiempo = tiempo
		self.seleccion = seleccion
		
	def __int__(self):
		if self.seleccion == "Segundos":
			return int(self.tiempo)
		elif self.seleccion == "Minutos":
			return self.Minutos_Segundos(self.tiempo)
		elif self.seleccion == "Horas":
			return self.Horas_Segundos(self.tiempo)
		elif self.seleccion == "Mixto":
			return self.Mixto_Segundos(self.tiempo)
	
	def Minutos_Segundos(self, tiempo):
		tiempo = int(tiempo)
		tiempo = tiempo*60
		return tiempo

	def Horas_Segundos(self, tiempo):
		tiempo = int(tiempo)
		tiempo = tiempo*(3600)
		return tiempo

	def Mixto_Segundos(self, tiempo):
		tiempo = tiempo.split(':')
		return self.Horas_Segundos(tiempo[0]) + self.Minutos_Segundos(tiempo[1]) + int(tiempo[2])

if __name__ == "__main__":
	gtk.gdk.threads_init()	
	gui()
	gtk.main()
