class rdengine:
    def __init__(self):
        self.ran_elements = {
            'lower':'abcdefghijklmnopqrstuvwxyz',
            'UPPER':'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'number':'0123456789',
            'symbol':'-*~:+^.[]<>?=#'
        }
    def libcall(self):
        return self.ran_elements
    def randomstring(self,char_num:int,extra):
        from random import choice as rdstr
        from random import seed
        if extra is None:
            totalstr = ''.join(_b for _a,_b in self.ran_elements.items())
        elif 'seed:' in extra:
            seed(extra.replace('seed:',''))
            totalstr = ''.join(_b for _a,_b in self.ran_elements.items())
        else:
            totalstr = ''.join([self.ran_elements[x] for x in extra])
        output = ''.join(rdstr(totalstr) for _ in range(char_num))
        return output
    def rdtitle(self):
        from random import randint as rdint
        output = self.randomstring(rdint(10,22),['lower','UPPER','number'])
        return output
class encode:
    def __init__(self,seed):
        if seed is None:
            self.seed = self.seed_generator()
        elif seed == 0:
            pass
        else:
            self.seed = seed
    def rdindex(self,x,y):
        from random import randint
        return randint(x,y)
    def seed_generator(self):
        import random
        self.ran_elements = rdengine().libcall()
        self.allrdchar = ''.join([icon for _temp,icon in self.ran_elements.items()])
        seed_length = self.rdindex(10,25)
        seed_str =  ''.join(random.choice(self.allrdchar) for _ in range(seed_length))
        return seed_str
    def encode_matrix(self):
        import random
        ran_elements = rdengine().libcall()
        ran_elements['source_endline'] = '|'
        ran_elements['source_space'] = ' '
        ran_source = ('').join([_a for __a,_a in ran_elements.items()])
        already_exists = []
        matrix = {
            f'{_d}{_e}':0 for (_n,_b) in ran_elements.items() \
                for (_n,_c) in ran_elements.items() \
                for _d in _b for _e in _c
        }
        random.seed(self.seed)
        encoded_length = 4 #length of digest str
        for match in matrix:
            while matrix[match] == 0:
                represent = ''.join(random.choice(ran_source) for _ in range(encoded_length))
                if represent not in already_exists:
                    matrix[match] = represent
                    already_exists.append(represent)
        return matrix
    def encode_seq(self,seq):
        seq += '|'
        matrix = self.encode_matrix()
        seqlength = len(seq)
        output = ''
        for x in range(seqlength):
            if seq[x] == '|':   #End of line
                pass
            else:
                combination = seq[x:x+2]
#                try:
                encodeseq = matrix[combination]
#                except KeyError:
#                    encodeseq = '##ERROR##'
#                finally:
                output += encodeseq
        return output
class decode:
    def __init__(self, block):
        import os
        self.rd = rdengine()
        self.block = block
        self.seqdir = '/mnt/share/source/debug/omniclient/seq'
        match block:
            case 0:
                print('Zero block detected, you can use decode function separately for now')

            case other:
                self.sessionname = os.path.basename(self.block).split('.')[0]
                self.sessiondir = '/mnt/share/source/debug/omniclient/interface_request'    #Directory to session storage file
                self.rd = rdengine()
                self.servercomm = '/mnt/share/source/debug/omniclient/interface_request' #directory of server communication folder
#                print('codeengine-decode-init: session name is: ', self.sessionname)
    def codeblockextract(self,encodedseq):
        from time import sleep
        for x in range(len(encodedseq)):
            seed = encodedseq[x:x+5]
            buffer = rdengine().randomstring(15,f'seed:{seed}')
            if buffer in encodedseq:
                encodedhash = encodedseq.replace(buffer,'\n').split('\n')[-1]
                break
        seed = ''
        for idx,char in enumerate(encodedhash):
            seed += char
            confirmstr = self.bufferstr(seed)
            totalcharextract = idx + 16

            if encodedhash[:totalcharextract] == confirmstr:
                print('='*8 + 'MATCHED!' + '='*8)
                print('Matrix seed is: ',seed)
                codeseq = encodedhash.replace(confirmstr,'')
                codeblock = [codeseq[x:x+4] for x in range(0,len(codeseq),4)]
                break
        return {'seed':seed,'block':codeblock}
    def confirm_client_confirm_response(self,filename):
        from time import sleep
        import os
        confirmtime = 0
        confirmtimemax = 60     #Wait at least 1 min to the confirmation of interface
        while os.path.isfile(f'{self.servercomm}/{filename}.response') is True and os.path.isfile(f'{self.servercomm}/{filename}.request') is False:
            if confirmtime <= confirmtimemax:
                confirmtime += 1
                sleep(1)
            else:
                confirmtime = 'TIMEDOUT'
                break
        if confirmtime == 'TIMEOUT':
            return confirmtime
        else:
            return 0
    def confirm_client(self):    #Decode information received from Omniinterface and response
        from system.blockengine import requestblock,responseblock
        import os
        import datetime

        rpblock = responseblock()
        interfacematrix = 'No'
        if os.path.isfile(f'{self.sessiondir}/{self.sessionname}.seq'):
            nowtime = int(datetime.datetime.now().timestamp())
            created_time = int(blockengine.requestblock(f'{self.sessiondir}/{self.sessionname}.seq').block_export()[0])
            last_mod_sec = int(blockengine.requestblock(f'{self.sessiondir}/{self.sessionname}.seq').block_export()[1])
            total_time = int(blockengine.requestblock(f'{self.sessiondir}/{self.sessionname}.seq').block_export()[2])
            if nowtime - last_mod_sec < 901 and total_time < 3600:
                os.remove(self.block)
                # < Modified last_mod_sec > #
                interfacematrix = requestblock(f'{self.sessiondir}/{self.sessionname}.seq').block_export()[3]   
                rpblock.codeblock_export(self.sessionname, 'PROCEED', f'{datetime.datetime.now().ctime()}','','')
            else:       #Token expired, force interface to restart
                return 2
            
        else:
            rqblock = requestblock(self.block)     
            os.remove(self.block)   
            interfaceencodedseq = rqblock.block_export()[1][0]
            codedseqblock = [(block[0],block[1]) for block in interfaceencodedseq.split()]
            interfaceinitseq = ''
            for pos, _temp in codedseqblock:
                interfaceinitseq += f'{codedseqblock[int(pos)][1]}'
            seqlength = len(interfaceinitseq)
            blocktitle = str(seqlength)[0] + self.rd.rdtitle() + str(seqlength)[1]
            rpblock.codeblock_export(self.sessionname, blocktitle, interfaceinitseq,'','')
        confirmwait = self.confirm_client_confirm_response(self.sessionname)

        if type(confirmwait) is int:  #Proceed
            try:
                os.remove(self.block)
            except FileNotFoundError:
                pass
            if interfacematrix == 'No':
                created_time = int(datetime.datetime.now().timestamp())
                encode_engine = encode(None)
                interfacematrix = '\t'.join(['\t'.join(map(str,[_val for x,_val in encode_engine.encode_matrix().items()]))])
            rpblock.sequenceblock_export(
                    self.sessionname,
                    f'Sequences for {self.sessionname}',
                    created_time,
                    int(datetime.datetime.now().timestamp()),
                    interfacematrix
                    )
            return 0
        else:
            return confirmwait
            os.remove(self.block)
            exit(1)
    def decode(self,seed,codeblock):
        matrix = {e:c for c,e in encode(seed).encode_matrix().items()}
        combi_list = []
        for pos, component in enumerate(codeblock):
            try:
                val = matrix[component]
            except KeyError:
                val = f'<NOMATCH at pos {pos}>'
            except Exception as ex:
                print(str(ex))
                exit(1)
            finally:
                combi_list.append(val)
                val = ''    #Wipe data
        print(combi_list)
        out = ''
        max = len(combi_list)
        for x in range(0,max):
            combi0 = combi_list[x]
            match x:
                case 0: #Begin character
                    out += combi0[0]
                case other:
                    if combi0[1] == '|':
                        out += combi0[0]
                        break
                    else:
                        combi1 = combi_list[x+1]
                        if combi0[1] == combi1[0]:
                            out += combi0[0]
                        else:
                            out += f'<MISSMATCH at pos {x}'
        return out
    def matrix_reconstruct(self,matrixstr):
        import random
        if len(matrixstr)%4 > 0:
            matrix_value = ''
            return 'ERROR'
        else:
            matrix_value = [matrixstr[x:x+4] for x in range(0,len(matrixstr),4)]
        ran_elements = rdengine().libcall()
        ran_elements['source_endline'] = '|'
        ran_elements['source_space'] = ' '
        ran_source = ('').join([_a for __a,_a in ran_elements.items()])
        already_exists = []
        matrix_combination = [
            f'{_d}{_e}' for (_n,_b) in ran_elements.items() \
                for (_n,_c) in ran_elements.items() \
                for _d in _b for _e in _c
        ]
        len_comp = len(matrix_combination) == len(matrix_value)
        if len_comp:
            matrix = {matrix_value[i]:matrix_combination[i] for i in range(len(matrix_combination))}
            return matrix
        else:
            return 'ERROR'
class account:
    def __init__(self,account,state):
        self.accountdir = ''
        self.encode = encode
        self.account = account
        self.state = state
    def salt_generate(self):
        salt_str = self.encode(None).seed_generator()[:5]
        salt_seed = self.encode(None).seed_generator()
        buffer_seed = self.encode(None).seed_generator()
        buffer = self.bufferstr(None)
        salt_e = self.encode(salt_seed).encode_seq(salt_str)
        salt_combine = [
            buffer + self.bufferstr(salt_seed) + salt_e,
            salt_str
            ]
        return salt_combine
    def bufferstr(self,seed):
        if seed is None:
            rdstr1 = rdengine().randomstring(self.encode(0).rdindex(4,15),None)
            rdseed2 = self.encode(seed).seed_generator()[:5]
            rdstr2 = rdengine().randomstring(15,f'seed:{rdseed2}')
#            print('Buffer seed is: ',rdseed2)
            return rdstr1+rdseed2+rdstr2
        else:
            rdstr1 = rdengine().randomstring(15,f'seed:{seed}')  
            return seed+rdstr1
#        print('Buffer string is: ',rdstr1,rdseed2,rdstr2)
        
    def config(self,extra):
        from random import randint
        match self.state:
            case 0: #Sign up
                accountconfig = 'first:1 approved:0'
                buffer1 = self.bufferstr(None)
                buffer2 = rdengine().randomstring(randint(10,30),None)
                confseed = self.encode(None).seed_generator()
                confseedconfirmation = self.bufferstr(confseed)
                confencode = self.encode(confseed).encode_seq(str(accountconfig))
                self.configout = f'{buffer1}{confseedconfirmation}{confencode}'
    def accountextract(self):
        with open(f'{self.accountdir}/{self.account}.account') as acc:
            return [r.rstrip() for r in acc.readlines()]
    def passwd(self,extra):
        from hashlib import blake2b
        match self.state:
            case 0: #Sign up
                passwd = '123456'
                self.salt_str = self.salt_generate()[1]
                pwdseed = self.encode(None).seed_generator()
                pwdseedconfirmation = self.bufferstr(pwdseed)
#                print(f'Seed is: {pwdseed}')
#                print('Confirmation sequence is:',pwdseedconfirmation)
                s = bytes(self.salt_str,'utf-8')
                h = blake2b(salt = s)
                h.update(bytes(passwd,'utf-8'))
                passwd_h = h.hexdigest()
#                print('Hash of password is: ',passwd_h)
                passwd_e = self.encode(pwdseed).encode_seq(passwd_h)
                buffer = self.bufferstr(None)
                self.pwdout = f'{buffer}{pwdseedconfirmation}{passwd_e}'
#                print(f'seed for password is: ',pwdseed)

    def signup(self):
        self.config(0)
        self.passwd(0)
        return [
            self.saltextract()[0],
            self.pwdout,
            self.configout
        ]
    def login(self,loginfile):
        import os
    def saltextract(self):
        return self.salt_generate()

#        if os.path.isfile(f'{self.accountdir}/{account}.account'):



if __name__ == '__main__':
    print('YOU CANNOT RUN THIS FILE!!!!')
    exit(1)