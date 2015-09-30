# coding=utf-8
__author__ = 'kk'

import os
__base_dir__ = os.path.dirname(__file__)
__data_fs__ = os.path.join(__base_dir__, 'Data.fs')


from ZODB import FileStorage, DB
import transaction
from BTrees.OOBTree import OOBTree

from ZODB.POSException import VersionLockError


class MyZODB(object):
    def __init__(self, path):
        self.storage = FileStorage.FileStorage(path)
        self.db = DB(self.storage)
        self.connection = self.db.open() #vers_conn = db.open(version='Working version')
        self.dbroot = self.connection.root()

    def close(self):
        self.connection.close()
        self.db.close()
        self.storage.close()

    def create_db(self, DBName):
        if not self.dbroot.has_key(DBName):
            self.dbroot[DBName] = OOBTree()
            return True
        else:
            return False

if __name__ == "__main__":
    db = MyZODB('__data_fs__')

    dbroot = db.dbroot
    print dbroot._p_changed
    dbroot['a_number'] = 3
    print dbroot._p_changed
    dbroot['a_string'] = 'Gift'
    dbroot['a_list'] = [1, 2, 3, 5, 7, 12]
    dbroot['a_dictionary'] = {1918: 'Red Sox', 1919: 'Reds'}
    dbroot['deeply_nested'] = {
        1918: [('Red Sox', 4), ('Cubs', 2)],
        1919: [('Reds', 5), ('White Sox', 3)],
    }

    print dbroot._p_changed

    try:
        transaction.commit()
    except VersionLockError, (obj_id, version):
        print ('Cannot commit; object %s locked by version %s' % (obj_id, version))
    print dbroot._p_changed
    a = dbroot['deeply_nested']
    a[1918][0] = 10
    print dbroot._p_changed
    dbroot._p_changed = True
    transaction.commit()
    print dbroot._p_changed


    for key in dbroot.keys():
        print key + ':', dbroot[key]

    # del dbroot['a_number'] #注意所有操作都需要transaction.commit()来提交

    #修改
    #a_dictionary = dbroot['a_dictionary']
    #a_dictionary[1920] = 'Indians'
    #db._p_changed = 1       这个方法只能改dic\list之类的复杂对象，纯数字不行
    #  #transaction.commit()

    #from persistent import Persistent 持久化必须继承这个类
    #例如下次再读取
    # for key in dbroot.keys():
    #       obj = dbroot[key]
    #       if isinstance(obj,  类名 ):
    #         print "Host:", obj.name
    #         print "  IP address:", obj.ip, "  Interfaces:", obj.interfaces

    # host = dbroot['www.example.com']
    # host.interfaces.append('eth2') #使用复杂对象修改时需要下面一行，否则可以省略的
    # host._p_changed = True
    # transaction.commit()
    # transaction.abort()  #提交前可放弃修改
    db.close()
pass

# storage = FileStorage('Data.fs')
# db = DB(storage)
# connection = db.open()
# root = connection.root()
# sim_sorted = root[0]
#
# # substitute the last element in every list of every key (indicated by 0 above) by 1
# # This code exhausts all the memory, never get to the 2nd part i.e. the sorting
# for x in sim_sorted.iterkeys():
#     for i,y in enumerate(sim_sorted[x]):
#         y[3] = 1
#         if i%5000 ==0
#             transaction.savepoint()

# Sort all the lists associated with every key in he reverse order using middle element as key
# [sim_sorted[keys].sort(key = lambda x:(-x[1])) for keys in sim_sorted.iterkeys()]

# for x in sim_sorted.iterkeys():
#     for y in sim_sorted[x]:
#         y[3] = 1
#     sim_sorted[x].sort(key=lambda y: -y[1])
#     transaction.savepoint()