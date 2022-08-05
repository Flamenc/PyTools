import subprocess
import sys

#if len(args) < 4 :
print(sys.argv[0]+" <USER> <PASSW> <DOMAIN> <IP> <EXT/NOEXT>")
 #   exit()
user=sys.argv[1]
passw=sys.argv[2]
domain=sys.argv[3]
server=sys.argv[4]
ext_op=sys.argv[5]
#if ext_op != "EXT" and ext_op != "NOEXT" :
#    print(sys.argv[0]+" <USER> <PASSW> <DOMAIN> <IP> <EXT/NOEXT>")

command="smbmap -u "+user+" -p "+passw+" -d "+domain+" -H "+server
com=command
outp=subprocess.check_output(com.split(" "))


ext_find=[".txt",".vbs",".vba",".vbe",".bat",".pdf"]

def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

def get_dir_name(dir_name):
    dir_d=""
    dir_root=dir_name.split(" ")
    cont=0
    while cont < len(dir_root):
        if "" !=dir_root[cont]:
            if cont != 0:
                dir_d=dir_d+" "+dir_root[cont]
            else:
                dir_d=dir_root[cont]

        cont=cont+1
    return dir_d


def decode_out(outp):
    for a in outp.decode("utf-8").split("\n"):
        #dir_root = a.split("\t")[1]
        lineinfo = a.split("\n")[0]
        #type
        print(lineinfo.split("\t")[1])
        #name
        print(lineinfo.split("\t")[-1])
        
        
def get_content_dir(outp2,pwd):
    for a in outp2.decode("utf-8").split("\n"):
        
        lineinfo = a.split("\n")[0]
        
        if len(lineinfo.split("\t")) > 1:
            
            type_l=lineinfo.split("\t")[1]
            
            name_l = lineinfo.split("\t")[-1]
            
            if ("dr-" in type_l or "dw-" in type_l )and name_l != "." and name_l != "..":
                comd_d=str(command).split(" ")
                comd_d.append("-r")
                
                comd_d.append(pwd+"/"+name_l)
                
                get_content_dir(subprocess.check_output(comd_d), pwd+"/"+name_l )
                
            elif "fr-" in type_l or "fw-" in type_l:
                len_file=int(get_dir_name(type_l).split(" ")[1])
                if ext_op == "EXT":
                    if any(ext in name_l for ext in ext_find):
                        print(pwd+"/"+name_l+"!-!"+sizeof_fmt(len_file)+"!-!"+str(len_file))
                else:
                    print(pwd+"/"+name_l+"!-!"+sizeof_fmt(len_file)+"!-!"+str(len_file))

                    
#print(outp)
for a in outp.decode("utf-8").split("\n"):
    if "READ" in a:
        dir_root = a.split("\t")[1]
        dir_root=get_dir_name(dir_root)
        outp2=subprocess.check_output(str(command+" -r "+dir_root).split(" "))
        get_content_dir(outp2,dir_root)
        
                      
