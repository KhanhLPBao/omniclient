#######   CONFIGURATION - EDIT DIRECTORY HERE   #######
sessiondir = "/mnt/share/source/debug/signal/session"
clientdir = '/mnt/share/source/debug/omniclient/node'
admindir = '/mnt/share/source/debug/admin'
req_progress = "/mnt/share/source/debug/omniclient/node"    #location of all processing jobs
scriptdir = "/mnt/share/source/omniclient/admin/bash/system"
serverIP = '192.168.1.51'       #IP of server contain fastq files
serverstoragedir = ''   #Storage directory of server
"""
Adjustable variables
    * proceed_without_MD5: Continue to proceed to lvl2 without MD5 results or MD5 check failed. Default is True
"""
proceed_without_MD5 = True
debug = False
#######################################################
import os, sys, json
from subprocess import run, check_output, CalledProcessError, DEVNULL, getoutput
#######################################################
client_input_dir = f'{clientdir}/input'
packagedir = os.path.dirname(os.path.abspath(__file__))
all_aug = sys.argv
sessionname = all_aug[1]
if "--debug" in all_aug:
    debug = True
    print(f'[sessioninit] Debug mode activated, please check log at {req_progress}/debug/{sessionname}.txt')
    with open(f'{req_progress}/debug/{sessionname}.txt','w') as debugfile:
        debugfile.write(f'DEBUGGING {sessionname}'+'\n')
        debugfile.close()

with open(f'{packagedir}/joblist.json') as _ref_joblist:
    joblist = json.load(_ref_joblist)
############ IMPORT SESSION FILES ################
session_source = f'{sessiondir}/{sessionname}/session'
with open(f'{session_source}.files') as listfile,\
    open(f'{session_source}.jobs') as listjobs:
    listfile = [_a.rstrip() for _a in listfile.readlines()]
    listjobs = [_b.rstrip() for _b in listjobs.readlines()]
def debug_output(log):
    if debug:
        with open(f'{req_progress}/debug/{sessionname}.txt','a') as debugfile:
            if isinstance(log, str):
                debugfile.write(log + '\n')
            elif isinstance(log, str):
                debugfile.write(' '.join(log) + '\n')
            debugfile.close()
def subcommand(cmd:list):
    try:
        results = check_output(cmd)#, stderror=DEVNULL)
        debug_output([f'Command {" ".join(cmd)} returned with result {results}'])
        return results
    except CalledProcessError as ex:
        return False
def md5check(md5ref,md5file):
    debug_output(['='*2,md5ref,'='*2,md5file,'='*2])
    try:         
        with open(md5ref) as _md5ref: #read refmd5
            ref_md5 = _md5ref.read().rstrip()    
        _down_md5 = ['md5sum', md5file,'| cut -d " " -f1']  
        down_md5 = getoutput(' '.join(_down_md5))
#            down_md5 = down_md5.rstrip().decode('utf-8')
        md5_compare = ref_md5 == down_md5 
        debug_output(['md5sum of downloaded/copied file is: ',down_md5])
        debug_output(['md5sum of reference file is: ',ref_md5])
        debug_output(['MD5 Comparison returned with result: ',md5_compare])
    except FileNotFoundError:
        debug_output('Not found MD5 file')
        md5_compare = False
    subcommand(['rm',md5ref])   
    return md5_compare
###################################################################################################################
#  Jobs level explained                                                                                           #
#   Lvl 1 >>> Lvl 2 >>> Lvl 3 >> Sublvl                                                                           #
#   Lvl 1 is file import, need to be done before moved to Lvl 2. Any files that cannot be imported to Lvl 2 input #
#  folders will be discarded and labeled "Not exists"                                                             #
#   Lvl 2 jobs must follow the progress if the request has 2 or more jobs on this level. Failed any jobs on Lvl 2 #
# will resulted in total failure of any job at lvl 3                                                              #
#   Lvl 3 jobs can be done parallelly, each jobs has no relations to another at the same level, require all Lvl 2 #
# jobs to be completed. Failure in each jobs will be reported separately                                          #
#   Sub level beyond 3 will be run inside snakemake script and error will be reported inside job results if any   #
###################################################################################################################
###     LEVEL 1 JOBS: IMPORT FILES      ###
def job_lvl1():
    debug_output(f'Job Level 1 of session {sessionname} begin!')
    _loop = 1
    try:
        os.mkdir(f'{req_progress}/input/{sessionname}')
    except FileExistsError:
        pass
    fileanalyzed = {}
    for job, file in [_c.split('|') for _c in listfile]:
        filename = os.path.basename(file)
        filenamemd5 = f'{filename}.md5.txt' #MD5 of file, content can be changed later
        match job:
            case 'ftp': #Import through import folder on workstation or any storage device that has ftp server enabled
                debug_output(f'Request to download files from ftp/sftp server detected. Download link is sftp://{serverIP}{file}')
                mkdirresults = subcommand(['mkdir',f'{req_progress}/{sessionname}'])
                if mkdirresults == 0:
                    downloadresults = False
                    redownloaded = False
                    while downloadresults is False:
                        downloadlink = [
                                'curl', '-k', f'sftp://{serverIP}{file}', '--user',f'guest:123456','-o',
                                f'{req_progress}/input/{sessionname}/{filename}'
                                ]
                        downloadresults = subcommand(downloadlink)
                        match downloadresults:
                            case False: #   Second download failed
                                if redownloaded:
                                    downloadresults = 'Fail'
                                    break
                                else:   # First download failed
                                    redownloaded = True
                            case Other:
                                pass
                    if downloadresults:
                        debug_output('Begin MD5 comparison of ',file)
                        md5_redownloaded = False
                        md5 = False
                        while md5 is False:
                            md5 = md5check(
                                f'{filenamemd5}',
                                f'{req_progress}/input/{sessionname}/{filename}')
                            if md5_redownloaded and md5 is False:
                                md5 = 'Failed'
                                fileanalyzed[filename] = False
                                break
                        if md5:
                            fileanalyzed[filename] = True

                        else:
                            fileanalyzed[filename] = False
                else:
                    # <Specific command to notice failed download
                    pass
            case Other:                   #Import through specific folder
                debug_output(f'Request to copy files from specific folder detected, original file link is: {file}')
                filemd5 = f'{file}.md5.txt' #MD5 of file, content can be changed later
                cp_results = False
                recopied = False
                while cp_results is False:
                    _cp_results = [
                        'cp','-f',
                        file,
                        f'{req_progress}/input/{sessionname}/'
                        ]
                    cp_results = subcommand(_cp_results)  
                    if cp_results is False:
                        debug_output('First copy failed, begin recopy')
                        cp_results = subcommand(_cp_results)  #Recopy files 
                        recopied = True
                    elif recopied:
                        cp_results = "Fail"
                        debug_output(f'Second copy failed, terminate analysis of {file}')
                        break
                    else:
                        cp_results = True
                        md5_check = False
                        md5_redownload = False
                _cp_md5_results = ['cp','-f',
                        filemd5,
                        f'{req_progress}/input/{sessionname}/'
                        ]
                if cp_results:
                    debug_output(['Copy completed! Begin MD5 comparison of ',file])
                while cp_results is True and md5_check is False:
                    debug_output('Begin loop')
                    cp_md5_ref = subcommand(_cp_md5_results)
                    md5_check = md5check(
                        filemd5,
                        f'{req_progress}/input/{sessionname}/{filename}'
                        )
                    debug_output(['md5_check: ',md5_check])
                    if md5_check is False and md5_redownload is False:
                        debug_output('MD5 check not matched, redownloading files')
                        cp2_results = subcommand(_cp_results)
                        md5_redownload = True
                        debug_output(['Recopy results:',cp2_results])
                    elif md5_check is False and md5_redownload is True:
                        debug_output('MD5 checking second time not matched. End the MD5 session check with False result')
                        fileanalyzed[filename] = False
                        md5_check = False
                        break
                if md5_check:
                    fileanalyzed[filename] = True
                
    with open(f'{req_progress}/input/{sessionname}/status.txt','w') as _final_status:
        if proceed_without_MD5:
            debug_output('Allow proceed to level 2 and 3 without MD5 check matched or conducted, treat results with caution')
            filepassed = [x for x in fileanalyzed]
        else:
            debug('Disallow files to proceeded to level 2 and 3 without MD5 check')
            filepassed = [x for x,y in fileanalyzed.items() if y is not False]
        if len(filepassed) == 0:    # No files downloaded or copied or pass MD5 if proceed_without_MD5 set to False
            debug_output(f'NO FILES FROM SESSION {sessionname} PASSED THROUGH LVL 1. TERMINATE SESSION!!!')
            _final_status.write('STOP')
        else:
            debug_output(f'{len(filepassed)} files passed through Level 1 process. Session {sessionname} is allowed to proceed to Level 2 and 3')
            _final_status.write('DONE')

    with open(f'{sessiondir}/{sessionname}/session.json') as _input_sstatus:
        totalsessionstatus = json.load(_input_sstatus)
        ssfile = totalsessionstatus["session files"]
        newssfile = [f'{file}-{fileanalyzed[file]}' if file in fileanalyzed else f'{file}-FAILED' for file in ssfile]
        totalsessionstatus['session files'] = newssfile
    with open(f'{sessiondir}/{sessionname}/session.json','w') as _output_sstatus:
        json.dump(totalsessionstatus,_output_sstatus,indent=1)
    debug_output(fileanalyzed)
    debug_output('Function lvl1job completed')    
###################################################################################################################
###     LEVEL 2 JOBS: ESSENTIAL JOBS, REQUIRED FOR ALL LEVEL 3 JOBS      ###
def job_lvl2and3(job:list,level):
    debug_output(f'Job Level {level} of session {sessionname} begin!')
    try:
        with open(f'{req_progress}/input/{sessionname}/status.txt') as _lvl1_status:
            lvl1_status = _lvl1_status.read()
    except FileNotFoundError:
        debug_output('ERROR! LVL1 JOBS NOT RUN YET')
        exit(1)
    if lvl1_status == "DONE":
        #   1: Create pending
        from subprocess import getstatusoutput
        output = f'{req_progress}/output/L{level}/{sessionname}'
        try:
            os.mkdir(output)
        except FileExistsError:
            pass
        except:
            #Command for other errors
            pass
        match level:
            case '2':
                writeresults = subcommand(['echo', '0', '>',f'{output}/{sessionname}.status'])
                if writeresults is False: 
                    #Command for false execution
                    pass
            case '3':
                for _task in job:
                    writeresults = subcommand(['echo', '0', '>',f'{output}/{_task}/{sessionname}.status'])
                if writeresults is False: 
                    #Command for false execution
                    pass
    else:
        #Sending signal to output fail logs and terminate session immediately
        pass


job_apply = {1:[],2:[],3:[]}
for _lvl,_refjoblib in joblist.items():
    _job_list = []
    _job_list = [
        _job \
            for _job in listjobs \
                if _job in _refjoblib
                ]
    job_apply[_lvl] = _job_list

job_lvl1()
job_lvl2and3(job_apply['2'],'2')
job_lvl2and3(job_apply['3'],'3')
