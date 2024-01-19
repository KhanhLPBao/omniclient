#!/usr/env python3.10.13
import json
import sys
from system.blockengine import requestblock, responseblock,account
from system.codeengine import decode
import os
request = sys.argv[1] or None
loginrequest = sys.argv[2].split('|') or None
#loginrequest:
#[token]|[ID]|[pass - in encoded form]
################
packagedir = os.path.dirname(os.path.abspath(__file__))
packagedir = packagedir.replace('/account','')
sys.path.append(packagedir)

admindir = '/mnt/share/source/debug/admin'
account_storage = f'{admindir}/account'
responsedir = ''

class reg:
    def __init__(self,regfile):

        self.block_component = requestblock(regfile).blockexport()
#        self.responseblock = responseblock
        match self.block_component[1].split(':')[0]:
            case 'account':
                suggest_account = self.block_component[1].split(':')[1]
                accountfile = f'{account_storage}/{suggest_account}.account'
                if os.path.isdir(accountfile):
                    temp_config = requestblock(accountfile).block_export()
                    accountconfig = decode(0).codeblockextract(temp_config)['block']
                    if '--signup:1' in accountconfig:
                        signupblock = self.block_component[-1]
                        signup_encoded = decode(0).codeblockextract(signupblock)
                        signupform = decode(0).decode(signup_encoded['seed'],signup_encoded['block'])
                        account = f'{account_storage}/{signupform}.account'
                        if os.path.isdir(account):
                            reject('Account already exists!').export()
                        else:
                            acc_info = account(signupform).signup()
                            with open(account,'w') as createaccount:
                                createaccount.write('\n'.join(map(str,acc_info)))
            case 'adminkey':
                keyid = self.block_component[1].split(':')[1]
                keyseq = self.block_component[1].split(':')[2]
                keyhash = self.block_component[1].split(':')[3]
class login:
    def __init__(self,loginfile):
        loginblock_component = requestblock(loginfile).blockexport()
        self.accountblock, self.pwdblock = loginblock_component[1],loginblock_component[2]
        #_s,ecryptsalt,ecryptpwd,ecryptconfig = block_component
        rqacc,self.accpwd = self.decryptacc(self.accountblock)
        comparepwd = None
        if os.path.isdir(f'{account_storage}/{rqacc}.account'):
            comparepwd = self.compare_pwd()
        else:
            reject('2').export()
        if comparepwd is True:
            pass
            """
            Some code to confirm with omniclient that the account passed the test
            """
        else:
            reject('1').export()
    def decryptacc(self,acc_info):
        def decrypt_component(encryptedstr):
            decode_block = decode(0).codeblockextract(encryptedstr)
            return decode(0).decode(decode_block[0],decode_block[1])
        if type(acc_info) is list:
            return [decrypt_component(line) for line in acc_info]
        else:
            return decrypt_component(acc_info)
    def compare_pwd(self):
        """
        ==================+======================+
        In account file:  | In login file:       |
        #1: Salt          | #1: Account (encoded)|
        #2: PWD           | #2: Pass (encoded)   |
        #3: config        |                      |
        ==================+======================+
        """
        from hashlib import blake2b        
        libacc = account(rqacc).accountextract()
        libsalt,libpwd,libconfig = self.decryptacc(libacc)
        h = black2b(salt = libsalt)
        h.update(bytes(self.accpwd,'utf-8'))
        return libpwd == h.hexdigest()


class accept:
    def __init__(self,account):
        import libu
        
class reject:
    def __init__(self,content):
        self.content = content
    def export(self):
        return self.content