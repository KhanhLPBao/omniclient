from strhash import codeengine
from system import blockengine
import sys
outdir = '/mnt/share/source/debug/omniclient/interface_response'
with open(f'{outdir}/output.txt','w') as out:
    args = sys.argv
    filename = args[-1]
    filecontent = blockengine.requestblock(filename)
    title = filecontent.block_export()[0][0]
    match title:
        case 'Connecting':
            response = codeengine.decode(filename).confirm_client()