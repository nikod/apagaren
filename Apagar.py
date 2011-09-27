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
		
	def Apagar(self):
		bus = dbus.SystemBus()
		bus_object = bus.get_object("org.freedesktop.ConsoleKit", "/org/freedesktop/ConsoleKit/Manager")
		bus_object.Stop(dbus_interface="org.freedesktop.ConsoleKit.Manager")
	
	def gtk_main_quit (self, *args):
		gtk.main_quit()

if __name__ == "__main__":
		gui()
		gtk.main()
