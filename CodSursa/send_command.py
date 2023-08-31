#!/usr/bin/env python3
import dbus
import json
import sys
import os
import functii
from scan_files import scanare
if __name__=="__main__":
    args=sys.argv[1:]

    #se citeste textul din help si se salveaza in text
    with open("help.txt","r") as f:
        text=f.read()
    #se concteaza la obiectul dbus cu datele citite din cconfiguratii
    with open("config_file.txt",'r')as file:
        configs=[linie.strip() for linie in file.readlines()]

    interface=configs[0]
    service=configs[1]
    object_address=configs[2]
    session_bus=dbus.SessionBus()
    object=session_bus.get_object(service,object_address)
    interface= dbus.Interface(object,interface)
    #verifica argumentele primite pentru a decide ce comanda se executa
    if( args[0]=="scan_system"): 
        if os.path.isdir(args[1]):
            if(len(sys.argv)<4):
                interface.emit_semnal_scan(args[1],"./scan_files/all_exe.txt","./scan_files/exe_untrust.txt")
            else:
                
                interface.emit_semnal_scan(args[1],args[2],args[3])
        
    elif(args[0]=="insert_rule" and len(sys.argv)==6):
        if((args[2]=='0' or args[2]=='1' ) and (args[3]=='user' or args[3]=='group')):
            interface.emit_semnal_insert_rule(args[1],args[2],args[3],args[4])
            interface.emit_semnal_update_fapolicyd()
        else:
            print("comanda eronata")
            print(txt)
            
    elif( args[0]=="reset_system" and len(sys.argv)==3):
        if( args[1]=="all_rules"or args[1]=="scan_rules" or args[1]=="politic_rules" or args[1]=="admin_rules"): 
            interface.emit_semnal_reset(args[1])
        else:
            print("comanda eronata")
            print(txt)
    elif args[0]=="send_policy" and len(sys.argv)==3:
        politici=[]
        for filename in os.listdir("./json_files/politici"):
            politici.append(filename)
        if args[1] in politici:
            interface.emit_semnal_sendJson(args[1])
            interface.emit_semnal_update_fapolicyd()
        else:
            print("Ati introdus o politica care nu exista in folderul de politici")
            print("\nSelectati una din cele de mai jos:")
            print(politici)
    elif args[0]=="create_scan_rules":
        if(len(sys.argv)<=3):
            list=scanare.create_rules_for_all_non_root_users("./scan_files/exe_untrust.txt")

            for i in list:
                interface.emit_semnal_send_scan_rule(i)
            interface.emit_semnal_update_fapolicyd()
        else:
            list=scanare.create_rules_for_all_non_root_users(args[1])
            for i in list:
                interface.emit_semnal_send_scan_rule(i)
            interface.emit_semnal_update_fapolicyd()
    elif  args[0]=="start_fapolicyd":
        interface.emit_semnal_start_fapolicyd()
    elif args[0]=="stop_fapolicyd":
        interface.emit_semnal_stop_fapolicyd()
    elif args[0]=="update_fapolicyd":
        interface.emit_semnal_update_fapolicyd()
    else:
        print(text)
