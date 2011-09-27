import dbus
from time import sleep
from threading import Thread

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
			Thread(target=Dbus_Apagar, args=(espera,)).start()
		elif seleccion2 == "Suspender":
			Thread(target=Dbus_Apagar, args=(espera,)).start()
		elif seleccion2 == "Hibernar":
			Thread(target=Dbus_Apagar, args=(espera,)).start()
		gtk.gdk.threads_leave()

	
	def Eboton(self, widget, data=None):
		seleccion = self.cb_activo(self.combobox1)
		self.Apagar.set_label(seleccion)

def Dbus_Apagar(espera):
	sleep(espera)
	bus = dbus.SystemBus()
	bus_object = bus.get_object("org.freedesktop.ConsoleKit", "/org/freedesktop/ConsoleKit/Manager")
	bus_object.Stop(dbus_interface="org.freedesktop.ConsoleKit.Manager")
	
def Dbus_Reiniciar(espera):
	sleep(espera)
	bus = dbus.SystemBus()
	bus_object = bus.get_object("org.freedesktop.ConsoleKit", "/org/freedesktop/ConsoleKit/Manager")
	bus_object.Restart(dbus_interface="org.freedesktop.ConsoleKit.Manager")

def Dbus_Suspender(espera):
	sleep(espera)
	bus = dbus.SystemBus()
	bus_object = bus.get_object("org.freedesktop.UPower", "/org/freedesktop/UPower")
	bus_object.Suspend(dbus_interface="org.freedesktop.UPower")

def Dbus_Hibernar(espera):
	sleep(espera)
	bus = dbus.SystemBus()
	bus_object = bus.get_object("org.freedesktop.UPower", "/org/freedesktop/UPower")
	bus_object.Hibernate(dbus_interface="org.freedesktop.UPower")

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
