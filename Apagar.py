import dbus
bus = dbus.SystemBus()
bus_object = bus.get_object("org.freedesktop.ConsoleKit", "/org/freedesktop/ConsoleKit/Manager")
bus_object.Stop(dbus_interface="org.freedesktop.ConsoleKit.Manager")
