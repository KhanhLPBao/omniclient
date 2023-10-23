#!/usr/env python3.10.13
import json
import sys
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


def login(infor:list):
    try:
        with open(f'{account_storage}/{infor[1]}.json') as account:
            ref_info = json.load(account)
            if ref_info == infor[2]:
                print('accept')
            else:
                print('deny')
    except FileNotFoundError:
        print('deny')

def registration(infor:list):
    try:
        with open(f'{account_storage}/{infor[1]}.json') as _tmp_check:
            _tmp_check.close()
        print('already')    #File already exists
    except FileNotFoundError:
        import subprocess as sub
        hash_pwd = hash(sub.getoutput(f'python {packagedir}/account/hashstring.py decode {infor[2]} {infor[1]}'))
        try:
            with open(f'{account_storage}/{infor[1]}.json') as acc_reg:
                json.dump({
                    'pass':hash_pwd,
                    'prog':'',
                    'permission':'',
                }, acc_reg)
            print('Done')
        except Exception as error:
            print(error)