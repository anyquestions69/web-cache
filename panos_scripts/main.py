from panos.firewall import Firewall

fw = Firewall("192.168.1.1", "admin", "admin")
print(fw.show_system_info())