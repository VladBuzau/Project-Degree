import os
import json
#aici se vor crea reguli pentru fiecare executabil sau director

def create_rules(paths,trusted,tip,destinatar):
    for path in paths:
        if os.path.isdir(path):#verifica daca este director
            if trusted==1 and tip=="user" and destinatar!="all":
                with open ("/etc/fapolicyd/rules.d/allow_politic.rules","a") as fisier_trust:
                    fisier_trust.write(f"allow perm=open uid={destinatar} : dir={path}\n");
            elif trusted==1 and tip=="group":
                with open ("/etc/fapolicyd/rules.d/allow_politic.rules","a") as fisier_trust:
                    fisier_trust.write(f"allow perm=open gid={destinatar} : dir={path}\n");
            elif trusted==0 and tip=="user" and destinatar!="all":
                with open ("/etc/fapolicyd/rules.d/deny_politic.rules","a") as fisier_untrust:
                    fisier_untrust.write(f"deny perm=open uid={destinatar} : dir={path}\n");
            elif trusted==0 and tip=="group":
                with open ("/etc/fapolicyd/rules.d/deny_politic.rules","a") as fisier_untrust:
                    fisier_untrust.write(f"deny perm=open gid={destinatar} : dir={path}\n");
            elif trusted==0 and tip=="user" and destinatar=="all":
                with open ("/etc/fapolicyd/rules.d/deny_politic.rules","a") as fisier_untrust:
                    fisier_untrust.write(f"deny perm=open all : dir={path}\n");
            elif trusted==1 and tip=="user" and destinatar=="all":
                with open ("/etc/fapolicyd/rules.d/allow_politic.rules","a") as fisier_untrust:
                    fisier_untrust.write(f"allow perm=open all : dir={path}\n");
          
          

        elif os.path.isfile(path) and os.access(path,os.X_OK):#verifica daca este executabil
            if trusted==1 and tip=="user" and destinatar!="all":
                with open ("/etc/fapolicyd/rules.d/allow_politic.rules","a") as fisier_trust:
                    fisier_trust.write(f"allow perm=execute uid={destinatar} : path={path}\n");
            elif trusted==1 and tip=="group":
                with open ("/etc/fapolicyd/rules.d/allow_politic.rules","a") as fisier_trust:
                    fisier_trust.write(f"allow perm=execute gid={destinatar} : path={path}\n");
            elif trusted==0 and tip=="user"and destinatar!="all":
                with open ("/etc/fapolicyd/rules.d/deny_politic.rules","a") as fisier_untrust:
                    fisier_untrust.write(f"deny perm=execute uid={destinatar} : path={path}\n");
            elif trusted==0 and tip=="group":
                with open ("/etc/fapolicyd/rules.d/deny_politic.rules","a") as fisier_untrust:
                    fisier_untrust.write(f"deny perm=execute gid={destinatar} : path={path}\n");
            elif trusted==1 and tip=="user" and destinatar=="all":
                with open ("/etc/fapolicyd/rules.d/allow_politic.rules","a") as fisier_trust:
                    fisier_trust.write(f"allow perm=execute all : path={path}\n");
            elif trusted==0 and tip=="user"and destinatar=="all":
                with open ("/etc/fapolicyd/rules.d/deny_politic.rules","a") as fisier_untrust:
                    fisier_untrust.write(f"deny perm=execute all : path={path}\n");
            

                      
#functia de procesare json unde se va apele functia create_rules de doua ori pentru fisierele citite# din json-ul primit ca parametru  
def process_json(file):
    path=f"json_files/politici/{file}"
    
    with open(path) as fisier:
        p_json=fisier.read()
    
    data=json.loads(p_json)
    
    apps=data["APPS"]
    whitelist=apps["whitelist"]
    blacklist=apps["blacklist"]
    tip=data["TARGET_TYPE"];
    destinatar=data["TARGET_NAME"];
    with open ("/etc/fapolicyd/rules.d/allow_politic.rules","w") as fisier_trust:
        fisier_trust.truncate()
    with open ("/etc/fapolicyd/rules.d/deny_politic.rules","w") as fisier_untrust:
        fisier_untrust.truncate()
    create_rules(blacklist,0,tip,destinatar)
    create_rules(whitelist,1,tip,destinatar)
    


