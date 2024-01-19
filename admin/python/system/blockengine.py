class requestblock:
    def __init__(self,inputfile):
        self.outputblock = {}
        with open(inputfile) as i:
            self.block = [_r.rstrip() for _r in i.readlines()]
        try:
            self.blockidx = {
                'title_begin': self.block.index('<title>'),
                'title_end': self.block.index('</title>'),
                'reg_begin': self.block.index('<registry>'),
                'reg_end': self.block.index('</registry>'),
                'input_begin': self.block.index('<input>'),
                'input_end': self.block.index('</input>'),
                'output_begin': self.block.index('<output>'),
                'output_end': self.block.index('</output>')
            }
        except ValueError:
            exit(1)
        self.outputblock = [
            self.block[self.blockidx['title_begin']+1:self.blockidx['title_end']],
            self.block[self.blockidx['reg_begin']+1:self.blockidx['reg_end']],
            self.block[self.blockidx['input_begin']+1:self.blockidx['input_end']],
            self.block[self.blockidx['output_begin']+1:self.blockidx['output_end']]
        ]
    def block_export(self):
        return self.outputblock
    def interfaceseq(self):
        seq = self.outputblock[1]
        seqblock = [(a[0],a[1]) for a in seq.split()]
        output = ''
        for pos,_s in seqblock:
            output += f'{seqblock[pos][1]}'
        return output

    def requestype(self):
        return self.outputblock[0]
class responseblock:
    def __init__(self):
        self.servercomm = '/mnt/share/source/debug/omniclient/interface_request' #directory of server communication folder
    def codeblock_request(self,titleseq,registryseq,inputseq,outputseq):
        requestblock = [
            '<title>',
            titleseq,
            '</title>','<registry>',
            registryseq,
            '</registry>','<input>',
            inputseq,
            '</input>','<output>',
            outputseq,
            '</output>',
            '<END>'
        ]
        return requestblock
    def sequenceblock_request(self,createdtime,lastmodtime,matrix):
        import datetime
        now = int(datetime.datetime.now().timestamp())
        elapsed_sec = now-createdtime
        requestblock = [
            '<title>',
            createdtime,
            '</title>','<registry>',
            lastmodtime,
            '</registry>','<input>',
            f'Elapsed time:{elapsed_sec}',
            '</input>','<output>',
            matrix,
            '</output>',
            '<END>'
        ]
        return requestblock

    def codeblock_export(self,blocktitle,titleseq,registryseq,inputseq,outputseq):
        request_block = self.codeblock_request(titleseq,registryseq,inputseq,outputseq)
        try:
            with open(f'{self.servercomm}/{blocktitle}.response','w') as outputresponse:
                outputresponse.write('\n'.join(request_block))
            return 0
        except Exception as ex:
            return 1
    def sequenceblock_export(self,blocktitle,titleseq,createdtime,lastmodtime,matrix):
        sessiondir = '/mnt/share/source/debug/omniclient/interface_request'
        request_block = self.sequenceblock_request(createdtime,lastmodtime,''.join(matrix))
        seqout = '\n'.join(map(str,request_block))
        with open(f'{sessiondir}/{blocktitle}.seq','w') as sessionstorage:
            sessionstorage.write(''.join(matrix))
            sessionstorage.close()
        try:
            with open(f'{self.servercomm}/{blocktitle}.certificate','w') as outputresponse:
                outputresponse.write(seqout)
            return 0
        except Exception as ex:
            print('Error found: ',str(ex))
            return 1        

if __name__ == '__main__':
    print('YOU CANNOT RUN THIS FILE!!!!')
    exit(1)