def encode_matrix(seed):
    import hashlib
    import random
    import re
    from typing import TypedDict    
    ran_elements = {
        'source_str_lower':'abcdefghijklmnopqrstuvwxyz',
        'source_str_UPPER':'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'source_str_number':'0123456789',
        'source_str_symbol':'-*~+.[]<>?=',
    }    
    match seed:
        case 'Token Request':   #Token is randomly generated 16 lower, upper and number character
            import glob
            import os
            req_output = "/mnt/share/source/debug/omniclient/output"
            already_exists = [
                os.path.basename(_f).split('.')[0] \
                    for _f in glob.glob(req_output)
                ]      
            ran_source = ('').join([_a for __a,_a in ran_elements.items()])
            _z = True
            while _z:    
                token = ''.join(random.choice(ran_source) for i in range(16))
                if token != 'Token Request':
                    _z = False
            return token
        case other:
            encoded_length = 4  #length of digest str
           
            ran_elements['source_endline'] = '|'
            ran_elements['source_space'] = ' '

            ran_source = ('').join([_a for __a,_a in ran_elements.items()])
            already_exists = []
            matrix = {
                f'{_d}{_e}':None for (_n,_b) in ran_elements.items() \
                    for (_n,_c) in ran_elements.items() \
                    for _d in _b for _e in _c
            }
            random.seed(seed)
            for match in matrix:
                represent_match = 1
                while represent_match == 1:
                    represent = ''.join(random.choice(ran_source) for _ in range(encoded_length))
                    if represent not in already_exists:
                        matrix[match] = represent
                        already_exists.append(represent)
                        represent_match = 0
            return matrix

