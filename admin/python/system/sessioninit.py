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
#######################################################
import os, sys, json
#######################################################
client_input_dir = f'{clientdir}/input'
packagedir = os.path.dirname(os.path.abspath(__file__))
sessionname = sys.argv[1]
with open(f'{packagedir}/joblist.json') as _ref_joblist:
    joblist = json.load(_ref_joblist)


############ IMPORT SESSION FILES ################
session_source = f'{sessiondir}/{sessionname}/session'
with open(f'{session_source}.files') as listfile,\
    open(f'{session_source}.jobs') as listjobs:
    listfile = [_a.rstrip() for _a in listfile.readlines()]
    listjobs = [_b.rstrip() for _b in listjobs.readlines()]
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
    from subprocess import run, check_output, CalledProcessError, DEVNULL
    def subcommand(cmd:list):
        try:
            results = check_output(cmd)#, stderror=DEVNULL)
            print(f"Process completed with results: \n{results}")            
            return results

        except CalledProcessError as ex:
            return False
    def md5check(md5ref,md5file):
        md5_check = False
        md5_redownload = False
        try:
            with open(md5ref) as _md5ref: #read refmd5
                ref_md5 = _md5ref.read().rstrip()    
        except FileNotFoundError:
            return False    
        _ref_md5 = [
            'bash', f'{scriptdir}/ftp.sh',
            serverIP, 'guest',
            '123456', f'{file}.md5.txt',
            md5ref,
            ]
        ref_md5 = subcommand(_ref_md5)          
        _down_md5 = [
            'md5sum',
            f'{md5file}'
        ]  
        down_md5 = subcommand(_down_md5)
        down_md5 = down_md5.rstrip().decode('utf-8')
        md5_compare = ref_md5 == down_md5 
        if md5_compare:   #Check true
            return True
        else:
            return False
    _loop = 1
    try:
        os.mkdir(f'{req_progress}/input/L1/{sessionname}')
    except FileExistsError:
        pass
    fileanalyzed = {}
    for job, file in [_c.split('|') for _c in listfile]:
        filename = os.path.basename(file)
        filenamemd5 = f'{filename}.md5.txt' #MD5 of file, content can be changed later
        match job:
            case 'ftp': #Import through import folder on workstation or any storage device that has ftp server enabled
                mkdirresults = subcommand(['mkdir',f'{req_progress}/{sessionname}'])
                if mkdirresults == 0:
                    downloadresults = False
                    redownloaded = False
                    while downloadresults is False:
                        downloadlink = [
                                'curl', '-vk', f'sftp://{serverIP}{file}', '--user',f'guest:123456','-o',
                                f'{req_progress}/input/L1/{sessionname}/{filename}'
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
                                fileanalyzed[filename] = True
                    if downloadresults:
                        md5_redownloaded = False
                        md5 = False
                        while md5 is False:
                            md5 = md5check(
                                f'{filenamemd5}',
                                f'{req_progress}/input/L1/{sessionname}/{filenamemd5}',
                                )
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
                cp_results = False
                recopied = False
                while cp_results is False:
                    _cp_results = [
                        'mv','-f',
                        f'{req_progress}/input/L1/{sessionname}/{filename}'
                        ]
                    cp_results = subcommand(_cp_results)  
                    if cp_results is False:
                        cp_results = subcommand(_cp_results)  #Recopy files 
                        recopied = True
                    elif recopied:
                        cp_results = "Fail"
                        break
                    else:
                        md5_check = False
                        md5_redownload = False
                _cp_md5_results = ['mv','-f',
                        f'{req_progress}/input/L1/{sessionname}/{filenamemd5}'
                        ]
                while cp_results != "Fail" and md5_check is False:
                    cp_md5_ref = subcommand(_cp_md5_results)
                    md5_check = md5check(
                        f'{filenamemd5}',
                        f'{req_progress}/input/L1/{sessionname}/{filenamemd5}',
                        )
                    if md5_check is False and md5_redownload is False:
                        md5_redownload = True
                        subcommand(_cp_results)
                    elif md5_check is False and md5_redownload is True:
                        fileanalyzed[filename] = False
                        md5_check = 'Fail'
                        break
                if md5_check:
                    fileanalyzed[filename] = True
    with open(f'{req_progress}/input/L1/{sessionname}/status.txt','w') as _final_status:
        if proceed_without_MD5:
            filepassed = [x for x in fileanalyzed]
        else:
            filepassed = [x for x,y in fileanalyzed.items() if y is not False]
        if len(filepassed) == 0:    # No files downloaded or copied or pass MD5 if proceed_without_MD5 set to False
            _final_status.write('STOP')
        else:
            _final_status.write('DONE')

###################################################################################################################
###     LEVEL 2 JOBS: ESSENTIAL JOBS, REQUIRED FOR ALL LEVEL 3 JOBS      ###
def job_lvl2and3(job:list,level):
    #   1: Create pendind
    from subprocess import getstatusoutput
    for _task in job:
        writeresults = getstatusoutput(
            f'echo 0 > {req_progress}/input/L{level}/{_task}/{sessionname}.request'
            )
        match writeresults:
            case 0: #Job write success
                pass
            #Other case require different output

job_apply = {1:[],2:[],3:[]}
for _lvl,_refjoblib in joblist.items():
    _job_list = []
    _job_list = [
        _job \
            for _job in listjobs \
                if _job in _refjoblib
                ]
    job_apply[_lvl] = _job_list

#job_lvl1()
job_lvl2and3(job_apply['2'],'2')
job_lvl2and3(job_apply['3'],'3')
