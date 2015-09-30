# coding=utf-8
__author__ = 'kk'
__localhost__ = ""
__testPort__ = 27017

from SocketServer import ThreadingTCPServer, BaseRequestHandler,StreamRequestHandler
import socket
import json
import traceback

client_list = dict()
client_socket_list = dict()

class baseRequestHandlerr(StreamRequestHandler):
    """
    #from StreamRequestHandler ，rewrite handle
    """
    def handle(self):
        """
        """
        global client_list
        while True:
            #客户端主动断开连接时，self.rfile.readline()会抛出异常
            try:
                #self.rfile类型是socket._fileobject,读写模式是"rb",方法有
                #read,readline,readlines,write(data),writelines(list),close,flush
                data = self.rfile.readline().strip()
                print "receive from (%r):%r" % (self.client_address, data)
                if len(data) == 0 and data !='\r\n' and data != '\n':
                    print "close(%r):%r" % (self.client_address, data)
                    ThreadingTCPServer.close_request(self.request)


                if 'login:' in data:
                    client_list[str(self.client_address[1])] = data.split(':')[1]
                    client_socket_list[str(self.client_address[1])] = self.request
                    print 'login:', client_list

                if 'online' in data:
                    ol = [value for key, value in client_list.items()]
                    print 'online:', ol
                    self.request.sendall(json.dumps(ol))

                if 'start' in data:
                    for key, value in client_socket_list.items():
                        if key != str(self.client_address[1]):
                            print 'send start to:', key
                            print 'send start to value:', value
                            value.sendall("start")

                #self.wfile类型是socket._fileobject,读写模式是"wb"
                #self.wfile.write(data.upper())

                # #转换成大写后写回(发生到)客户端
                # #self.request.sendall(data.upper())
            except EOFError:
                print "cut from (%r):%r,offline" % (self.client_address, data)
                del client_list[str(self.client_address[1])]
                del client_socket_list[str(self.client_address[1])]
                break
            except socket.error, e:
                print "x(%r):%r,offline" % (self.client_address, data)
                del client_list[str(self.client_address[1])]
                del client_socket_list[str(self.client_address[1])]
                break
            except:
                print "z(%r) offline" % (self.client_address,)
                del client_list[str(self.client_address[1])]
                del client_socket_list[str(self.client_address[1])]
                break

if __name__ == "__main__":
    addr = (__localhost__, __testPort__)
    #购置TCPServer对象，
    server = ThreadingTCPServer(addr, baseRequestHandlerr,bind_and_activate=False)
    server.allow_reuse_address = True
    server.server_bind()
    server.server_activate()
    #启动服务监听
    print 'start,port 27017'
    server.serve_forever()
