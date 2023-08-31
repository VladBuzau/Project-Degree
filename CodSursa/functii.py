import os
import grp
import json
#functia de inserare reguli
def insert_rule(path,verdict,tip_p,destinatar):
    while True:
        if(tip_p=="grup"):
            user="not"
            nume_grup=destinatar
        else:
            user=destinatar
        if os.path.isdir(path):#verifica daca este director

            with open("/etc/fapolicyd/rules.d/rules_by_user.rules","a") as fisier:
                if verdict=='0' and user !='all' and tip_p=='user':
                    fisier.write(f"deny perm=open uid={user} : dir={path}\n")
                
                elif verdict=='0' and user=='all' and tip_p=='user':
                    fisier.write(f"deny perm=open all : dir={path}\n") #scrie regula in fisier
                elif verdict=='1' and user!='all' and tip_p=='user':
                    fisier.write(f"allow perm=open uid={user} : dir={path}\n")
                elif verdict=='1' and user=='all' and tip_p=='user':
                    fisier.write(f"allow perm=open all : dir={path}\n")
                elif verdict=='0' and tip_p=='group':
                    fisier.write(f"deny perm=open gid={nume_grup} : dir={path}\n")
                if verdict=='1' and tip_p=='group':
                    fisier.write(f"allow perm=open gid={nume_grup} : dir={path}\n")
 
                        
            break
        if os.path.isfile(path) and os.access(path,os.X_OK):#verifica daca este executabil
            with open("/etc/fapolicyd/rules.d/rules_by_user.rules","a") as fisier:
                if verdict=='0' and user!='all' and tip_p=='user':
                    fisier.write(f"deny perm=execute uid={user} : path={path}\n")
                elif verdict=='0' and user=='all' and tip_p=='user':
                    fisier.write(f"deny perm=execute all : path={path}\n")
                elif verdict=='1' and user !='all' and tip_p=='user':
                    fisier.write(f"allow perm=execute uid={user} : path={path}\n")
                elif verdict=='1' and user=='all' and tip_p=="user":
                    fisier.write(f"allow perm=execute all : path={path}\n")
                elif verdict=='0' and tip_p=='group':
                    fisier.write(f"deny perm=execute gid={nume_grup} : path={path}\n")
                if verdict=='1' and tip_p=='group':
                    fisier.write(f"allow perm=execute gid={nume_grup} : path={path}\n")
 

            
            break

#functia  verifica ce tip de resetare primeste si sterge textul din fisierele respective
def reset_rules(tip):
    dir='/etc/fapolicyd/rules.d'
    if(tip=="all_rules"):
        for file in os.listdir(dir):
            path=dir+"/"+file
            with open(path,"w") as fisier:
                fisier.truncate()
        with open(dir+"/95-allow-open.rules","w") as f:
            f.write("perm=any uid=root all : all\n")

    elif(tip=="politic_rules"):
        with open(dir+"/allow_politic.rules","w") as fisier:
            fisier.truncate()
        
        with open(dir+"/deny_politic.rules","w") as fisier:
            fisier.truncate()
    elif(tip=="scan_rules"):
        with open(dir+"/deny_scan.rules","w") as fisier:
            fisier.truncate()
    elif (tip=="admin_rules"):
        with open(dir+"/rules_by_user","w") as fisier:
            fisier.truncate()
    
    os.system("systemctl stop fapolicyd")
    os.system("fagenrules --load")
    os.system("systemctl start fapolicyd")


    



       
def update_fapolicyd():
    os.system("systemctl stop fapolicyd")
    os.system("fagenrules --load")
    os.system("systemctl start fapolicyd")

def stop_fapolicyd():
    os.system("systemctl stop fapolicyd")

def start_fapolicyd():
    os.system("systemctl start fapolicyd")
    































