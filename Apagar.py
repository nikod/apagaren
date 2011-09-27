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
				"Unidad", "combobox", "Apagar", "Cancelar"
				]
		
		for glade in glade:
			setattr(self, glade, self.builder.get_object(glade))
		
		self.Ventana.show_all()
		
	def Apagar(self, *args):
		Dbus_Apagar()
		gtk_main_quit(*args)
	
	def gtk_main_quit (self, *args):
		gtk.main_quit()

	def cb_activo (self, combobox):
		model = self.combobox.get_model()
		activo = self.combobox.get_active()
		return model[active][0]
      		 
def Dbus_Apagar():
	bus = dbus.SystemBus()
	bus_object = bus.get_object("org.freedesktop.ConsoleKit", "/org/freedesktop/ConsoleKit/Manager")
	bus_object.Stop(dbus_interface="org.freedesktop.ConsoleKit.Manager")

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
