import os
import grp
import json
#functie de selectat executabile cu comanda find
def select_all_exe_files(file_name,dir):
    command=f"find {dir} -type f -executable"
    os.system(f"{command}>>{file_name}")
#functie de citit liniile dintr-un fisier si le returneaza intr-o lista
def read_exe_from_file(file_name):
    executabili=[]
    with open(file_name,"r") as f:
        for line in f:
            line=line.rstrip("\n")
            executabili.append(line)
    return executabili
#functie de interogare pachet cu comanda rpm
def request_package(exe):
    command=f"rpm -qf {exe}"
    result=os.popen(command).read()
    if"not owned by any package"  in result:
        return  True
    return False

#constructia listei cu executabile untrust
def select_exec_unsafe(executabili):
    exec_untrust=[]
    for i in executabili:
        if request_package(i):
            exec_untrust.append(i)
    return exec_untrust
#functie de scriere intr-un fisier
def write_list_to_file(_list,file_name):
    with open(file_name,"w") as file_exe:
        for i in _list:
            file_exe.write(i+"\n")
#functie de stergere text din fisier
def remove_txt_from_file(file):
    with open (file,"w") as f:
        f.truncate()
#functie de scanare care apeleaza metodele de mai sus
def scanare(dir,file_exe,file_untrust):
    remove_txt_from_file(file_exe)
    remove_txt_from_file(file_untrust)
    executabili=[]
    select_all_exe_files(file_exe,dir)
    executabili=read_exe_from_file(file_exe)
    exec_untrust=select_exec_unsafe(executabili)
    write_list_to_file(exec_untrust,file_untrust)


#functie de scris regula in fapolicyd
def write_to_fapolicyd(rule,file):
    lista_reguli=read_exe_from_file(file)
    lista_reguli.append(rule)
    all=list(set(lista_reguli))
    write_list_to_file(all,file)
    
#functi de creare reguli pentru toti utilizatorii pentru fisierele untrust provenite din scanare
def create_rules_for_all_non_root_users(file):
    exec_untrust=read_exe_from_file(file)
    list_rules=[]
    for i in exec_untrust:
        print(f"\n {i}  Press  1=True  |   0=False")
        
        while True:
            verdict=input()
            if verdict=='0' or verdict=='1':
                break

        if verdict=='1':
            list_rules.append(f"deny perm=any all : path={i}")

    return list_rules

