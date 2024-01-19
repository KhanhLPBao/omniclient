#!/usr/env/python3.10
import sys
import os
all_args = sys.argv
inputdir = ''       #Input directory inside docker container
outputdir = ''      #Output directory inside docker container
scriptdir = "omnipack/omniclient/client/inside"
queqefile = f'{scriptdir}/queqe.txt'
nofile = False
if os.path.isfile(queqefile):
    pass
else:
    with open(queqefile,'w') as _q:
        _q.write()

def import_queqe():
    with open(queqefile,'r') as _q:
        queqes = _q.read().split('\n')
        priority = [a for a in queqes if "prior" in a]
        normal = [a for a in queqes if "prior" not in a]
    return [priority,normal]

def write_queqe(queqelist):
    with open(queqefile,'w') as _q:
        _q.write('\n'.join(queqelist))

def add_queqe():
    
    with open(f'{scriptdir}/queqeworking.txt','w') as _w:    #Signal script is working
        _w.write("1")
    #####################
    priority, normal = import_queqe()
    sessionname = all_args[2]
    print(f'Begin add {sessionname} to queqe')
    if "prior" in sessionname:
        priority.append('prior ' + sessionname)
    else:
        normal.append('normal ' + sessionname)
    write_queqe(priority+normal)
    ####################
    with open(f'{scriptdir}/queqeworking.txt','w') as _w:    #Signal script is stopped
        _w.write("0")

def del_queqe():
    with open(f'{scriptdir}/queqeworking.txt','w') as _w:    #Signal script is working
        _w.write("1")
    ####################
    priority, normal = import_queqe()
    sessionname = all_args[2]
    if "prior" in sessionname:
        priority.remove(sessionname)
    else:
        normal.remove(sessionname)
    write_queqe(priority+normal)
    ####################
    with open(f'{scriptdir}/queqeworking.txt','w') as _w:    #Signal script is stopped
        _w.write("0")

def queqe_check():
    if nofile:
        print("")
    else:
        with open(f'{scriptdir}/queqeworking.txt','w') as _w:    #Signal script is working
            _w.write("1")
        ####################
        _queqe = import_queqe()
        sessionname = all_args[2]
        try:
            session_index = _queqe.index(sessionname)
            if session_index == 0:
                print("")
            else:
                print(_queqe[session_index-1])
        except:
            #   <Code for error output>
            pass
        ####################
        with open(f'{scriptdir}/queqeworking.txt','w') as _w:    #Signal script is stopped
            _w.write("0")    

command = all_args[1]
match command:
    case 'add':
        add_queqe()
    case 'delete':
        del_queqe()
    case 'check':
        queqe_check()