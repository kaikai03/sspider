# coding=utf-8
__author__ = 'kai_k_000'
__localhost__ = ""
__testPort__ = 27018

import thread

from SocketServer import ThreadingTCPServer, BaseRequestHandler,StreamRequestHandler
import socket
import json
import argparse
import traceback

__respon_format__ = {"res": "1","code": "1","value": "1"}

class TCPClient:
    def __init__(self, pid, ip, port):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((ip, port))
            self.pid = pid
            self.processes = {}
            self.loopStat = True
            self.processes['shutdown'] = self.shutDown
            self.processes['sstatue'] = self.sstatue
            self.processes['bgmPath'] = self.bgmPath
            self.processes['mediaFile'] = self.mediaFile


            self.bgmPath = None
            self.mediaFile = None
        except:
            print "connect error"

    def respone(self, res, code, value):
        print 'send: ', res, code, value
        __respon_format__['res'] = res
        __respon_format__['code'] = code
        __respon_format__['value'] = value
        self.s.sendall(json.dumps(__respon_format__))

    def shutDown(self, items):
        if items == self.pid:
            self.respone('1', 'shutdown', '1')
            self.loopStat = False
        else:
            print items,self.pid
            print 'shutDown error:processID wrong'
            self.respone('1', 'shutdown', '0')

    def sstatue(self, items):
        value = '0'
        if None == self.bgmPath:
            value += '_bgmPath'

        if None == self.mediaFile:
            value += '_mediaFile'

        if len(value) < 2:
            value = '1'

        self.respone('1', 'sstatue', value)

    def bgmPath(self, items):
        print type(items),items
        if isinstance(items, str) or isinstance(items, unicode):
            self.bgmPath = items
            self.respone('1', 'bgmPath', '1')
        else:
            print 'bgmPath, format error'
            self.respone('1', 'bgmPath', '0')

    def mediaFile(self, items):
        print type(items),items
        if isinstance(items, str) or isinstance(items, unicode):
            self.mediaFile = items
            self.respone('1', 'mediaFile', '1')
        else:
            print 'bgmPath, format error'
            self.respone('1', 'mediaFile', '0')


    def handle(self):
        """
        """
        while self.loopStat:
            try:
                data = self.s.recv(1024)
                print "receive from (%r)" % data

                decodejson = json.loads(data)
                print type(decodejson)
                print decodejson
                # print decodejson.get("res",None)

                for key in decodejson.keys():
                    print key
                    proc = self.processes.get(key, "-99")
                    if proc != "-99":
                        print '2'
                        proc(decodejson[key])
                    else:
                        print '3'
                        self.respone('1', key, 'no exite')


            except EOFError:
                print "cut from (%r):%r,offline" % ('xxxx', 'xxxx')
                break
            except socket.error, e:
                print "x(%r):%r,offline" % ('xxxx', 'xxxx')
                break
            except :
                print "offline some error, EX. json format error,or network error"
                break

    def run(self):
        self.handle()


def sk(id, host, port):
    server = TCPClient(id, host, port)
    server.run()



if __name__ == '__main__':
    # p=Process(target=sk).start()
    # thread.start_new_thread(sk, ())
    parser = argparse.ArgumentParser(description='lalalalala')
    parser.add_argument(
        'processID', metavar='str',  type=str,
        help='ID')
    parser.add_argument(
        'controlIp', metavar='str',  type=str,
        help='ip')
    parser.add_argument(
        'controlPort', metavar='int',  type=int,
        help='port')
    args = parser.parse_args()

    print 'start args:', args.processID, args.controlIp, args.controlPort
    print u'目前提供一下接口测试：查询类：sstatue，设置类：bgmPath，mediaFile，命令类：shutdown。'
    print u'具体参数见文档'
    sk(args.processID,args.controlIp, args.controlPort)
    print 'ClientClose'

# {"shutdown":-1}
# {"shutdown":"id"}
# {"sstatue":0}
# {"bgmPath":"asdasd/asd"}
# {"mediaFile":"asdasd.wav"}