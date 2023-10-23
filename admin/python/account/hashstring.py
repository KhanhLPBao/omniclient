import os
#
import sys
method = sys.argv[1]
packagedir = os.path.dirname(os.path.abspath(__file__))
packagedir = packagedir.replace('/account','')
sys.path.append(packagedir)
#
#
from strhash.encode_matrix import encode_matrix
data_output = ''
match method:
    case 'encode':
        data_input = sys.argv[2]
        token = sys.argv[3]
        encode_matrix = encode_matrix(token)
        for line in data_input.split('\n'):
            for _i in range(0,len(line),2):
                char_first = line[_i]
                if _i == len(line) - 1:     #End of line
                    char_next = '|'
                else:
                    char_next = line[_i+1]
                try:
                    data_output += encode_matrix[f'{char_first}{char_next}']
                except KeyError:
                    data_output += '<Unidentified combination>'
                    print(5)
        print(data_output)
    case 'decode':
        data_input = sys.argv[2]
        token = sys.argv[3]
        encode_matrix = encode_matrix(token)
        data_input_split = [data_input[i:i+4] for i in range(0, len(data_input), 4)]
        data_input_check = [len(_a) == 4 for _a in data_input_split]
        if False not in data_input_check:   #All condition met
            for _c in data_input_split:
                ematch = None
                for (_z,_b) in encode_matrix.items():
                    if _c == _b:
                        ematch = _z
                        break
                    else:
                        ematch = '<ERROR! Digest elements not matched>'
                match ematch:
                    case None:
                        data_output += '<ERROR! Digest elements not matched>'
                        print(5)
                    case other:
                        data_output += ematch
            print(data_output)
        else:
            print(5)    # ERROR, not all combinations are 4-elements
    case 'token':
        encode_matrix = encode_matrix('Token Request')
        print(encode_matrix)           