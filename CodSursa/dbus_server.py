#!/usr/bin/env python3
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
from scan_files import scanare
from json_files import load_json
import functii
DBusGMainLoop(set_as_default=True)
with open("/root/test/licenta/config_file.txt",'r')as file:# citire date de configurare
    configs=[linie.strip() for linie in file.readlines()]

interface=configs[0]
service=configs[1]
object_address=configs[2]
class MyDbusObject(dbus.service.Object):
#definirea de metode si semnale respective fiecarei functionalitati
    @dbus.service.method(interface,signature='s')
    def emit_semnal_sendJson(self,file):
        self.sendJson_semnal(file)
    @dbus.service.signal(interface,signature='s')
    def sendJson_semnal(self,file):
        pass
    
    @dbus.service.method(interface,signature='sss')
    def emit_semnal_scan(self,dir,file1,file2):
        self.scan_semnal(dir,file1,file2)
    @dbus.service.signal(interface,signature='sss')
    def scan_semnal(self,dir,file1,file2):
        pass
    
    @dbus.service.method(interface,signature='s')
    def emit_semnal_reset(self,tip):
        self.reset_semnal(tip)
    @dbus.service.signal(interface,signature='s')
    def reset_semnal(self,tip):
        pass

    @dbus.service.method(interface,signature='ssss')
    def emit_semnal_insert_rule(self,path,verdict,tip_politica,destinatar):
        self.insert_rule_semnal(path,verdict,tip_politica,destinatar)
    @dbus.service.signal(interface,signature='ssss')
    def insert_rule_semnal(self,path,verdict,tip_politica,destinatar):
        pass

    @dbus.service.method(interface,signature='s')
    def emit_semnal_send_scan_rule(self,file):
        self.send_scan_rule_semnal(file)
    @dbus.service.signal(interface,signature='s')
    def send_scan_rule_semnal(self,file):
        pass
 
    @dbus.service.method(interface,signature='')
    def emit_semnal_start_fapolicyd(self):
        self.start_fapolicyd_semnal()
    @dbus.service.signal(interface,signature='')
    def start_fapolicyd_semnal(self):
        pass
    @dbus.service.method(interface,signature='')
    def emit_semnal_stop_fapolicyd(self):
        self.stop_fapolicyd_semnal()
    @dbus.service.signal(interface,signature='')
    def stop_fapolicyd_semnal(self):
        pass
    @dbus.service.method(interface,signature='')
    def emit_semnal_update_fapolicyd(self):
        self.update_fapolicyd_semnal()
    @dbus.service.signal(interface,signature='')
    def update_fapolicyd_semnal(self):
        pass
   

#crerea unui obiect de tipul MyDbusObject
session_bus=dbus.SessionBus()
name=dbus.service.BusName(service,bus=session_bus)
object=MyDbusObject(session_bus,object_address)
loop=GLib.MainLoop()
loop.run()
