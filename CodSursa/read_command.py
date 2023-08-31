#!/usr/bin/env python3
import dbus
from scan_files import scanare
from json_files import load_json
import functii
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
DBusGMainLoop(set_as_default=True)
with open("config_file.txt",'r')as file:#citire date de cofiguratie
    configs=[linie.strip() for linie in file.readlines()]

interface=configs[0]
service=configs[1]
object_address=configs[2]
#crearea de functii care citesc semnalele de pe interfata
def read_scan(dir,file1,file2):
    scanare.scanare(dir,file1,file2)
def read_json(file):
    load_json.process_json(file)
def reset_f(tip):
    functii.reset_rules(tip)
def insert_one_rule(path,verdict,tip_politica,destinatar):
    print("a fost inserata o regula")
    functii.insert_rule(path,verdict,tip_politica,destinatar)
def write_rule_to_fapolicyd(file):
    scanare.write_to_fapolicyd(file,"/etc/fapolicyd/rules.d/deny_scan.rules")
def start():
    functii.start_fapolicyd()
def stop():
    functii.stop_fapolicyd()
def update():
    functii.update_fapolicyd()
session_bus=dbus.SessionBus()
object=session_bus.get_object(service,object_address)
interface=dbus.Interface(object,interface)
#conectarea semnalelor la functiile de mai sus
interface.connect_to_signal('scan_semnal',read_scan)
interface.connect_to_signal('sendJson_semnal',read_json)
interface.connect_to_signal('reset_semnal',reset_f)
interface.connect_to_signal('insert_rule_semnal',insert_one_rule)
interface.connect_to_signal('send_scan_rule_semnal',write_rule_to_fapolicyd)
interface.connect_to_signal('start_fapolicyd_semnal',start)
interface.connect_to_signal('stop_fapolicyd_semnal',stop)
interface.connect_to_signal('update_fapolicyd_semnal',update)
loop=GLib.MainLoop()
loop.run()
