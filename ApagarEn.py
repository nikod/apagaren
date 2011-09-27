import dbus

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
		self.Accion(self.cb_activo(self.combobox),self.cb_activo(self.combobox1))
#		self.gtk_main_quit(*args)
	
	def gtk_main_quit (self, *args):
		gtk.main_quit()

	def cb_activo (self, combobox):
		model = combobox.get_model()
		activo = combobox.get_active()
		return model[activo][0]
		
	def Accion(self, seleccion1, seleccion2):
		if seleccion2 == "Apagar":
			Dbus_Apagar()
		elif seleccion2 == "Reiniciar":
			Dbus_Reiniciar()
		elif seleccion2 == "Suspender":
			Dbus_Suspender()
		elif seleccion2 == "Hibernar":
			Dbus_Hibernar()
	
	def Eboton(self, widget, data=None):
		seleccion = self.cb_activo(self.combobox1)
		self.Apagar.set_label(seleccion)

def Dbus_Apagar():
	bus = dbus.SystemBus()
	bus_object = bus.get_object("org.freedesktop.ConsoleKit", "/org/freedesktop/ConsoleKit/Manager")
	bus_object.Stop(dbus_interface="org.freedesktop.ConsoleKit.Manager")
	
def Dbus_Reiniciar():
	bus = dbus.SystemBus()
	bus_object = bus.get_object("org.freedesktop.ConsoleKit", "/org/freedesktop/ConsoleKit/Manager")
	bus_object.Restart(dbus_interface="org.freedesktop.ConsoleKit.Manager")

def Dbus_Suspender():
	bus = dbus.SystemBus()
	bus_object = bus.get_object("org.freedesktop.UPower", "/org/freedesktop/UPower")
	bus_object.Suspend(dbus_interface="org.freedesktop.UPower")

def Dbus_Hibernar():
	bus = dbus.SystemBus()
	bus_object = bus.get_object("org.freedesktop.UPower", "/org/freedesktop/UPower")
	bus_object.Hibernate(dbus_interface="org.freedesktop.UPower")


def Minutos_Segundos(tiempo):
	int(tiempo)
	tiempo = tiempo / 60
	return tiempo
	
def Horas_Segundos(tiempo):
	int(tiempo)
	tiempo = tiempo / ( 60 * 60 )
	return tiempo
	
def Mixto_Segundos(tiempo):
	tiempo = tiempo.split(':')
	return Hora_Segundos(tiempo[1]) + Minutos_Segundos(tiempo[2]) + init(tiempo[3])
	

if __name__ == "__main__":
	gui()
	gtk.main()
