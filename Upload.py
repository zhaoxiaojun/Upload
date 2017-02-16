#coding=utf-8

import paramiko
import os
import ConfigParser
import codecs
import datetime


class Config(object):
    path = os.path.dirname(os.path.abspath(__file__)) + os.sep + "config.ini"
    if not os.path.isfile(path):
       raise Exception,"config file is missing"

    ConfigIns = ConfigParser.ConfigParser()
    ConfigIns.readfp(codecs.open(path,"r","utf-8"))


    def get_serverinfo(self):
        return self.ConfigIns.get("server","serverinfo")

    def get_remotepath(self):
        return self.ConfigIns.get("file","remotepath")

    def get_localpath(self):
        return self.ConfigIns.get("file","localpath")

    def get_secretkey_path(self):
        return self.ConfigIns.get("key","keypath")

    def get_serverinfo_list(self):
        a = eval(self.get_serverinfo())
        return a.keys(),a.values()


# 连接SSH类
# class ConnectSSH(object):
#     def __init__(self):
#         self.server_dict = eval(Config().get_serverinfo())
#         self.secretkey = eval(Config().get_secretkey_path())
#         self.command = eval(Config().get_remotepath())
#
#     def connectSSH(self):
#         """连接到SSH服务"""
#         if self.server_dict:
#             for ip,value in self.server_dict.items():
#                 self.conn = paramiko.SSHClient()
#                 self.conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#                 try:
#                     self.conn.connect(hostname=ip,port=value['port'],username=value['username'],key_filename=self.secretkey)
#                 except Exception,e:
#                     print e
#         return self.conn


# 连接到SFTP类
class ConnectSFTP(object):
    def __init__(self):
        self.server_dict = eval(Config().get_serverinfo())
        self.secretkey = eval(Config().get_secretkey_path())
        self.localpath = eval(Config().get_localpath())
        self.remotepath = eval(Config().get_remotepath())


    def connectSFTP(self):
        """连接到SFTP服务"""
        if self.server_dict:
            for ip,value in self.server_dict.items():
                conn = paramiko.Transport((ip, value['port']))
                conn.connect(username=value['username'], pkey=paramiko.RSAKey.from_private_key_file(self.secretkey))
                sftp = paramiko.SFTPClient.from_transport(conn)
                self.sftp = sftp
                return self.sftp

    def upload(self):
        try:
            t = self.connectSFTP()
            print 'upload file start %s ' % datetime.datetime.now()
            for root, dirs, files in os.walk(self.localpath):
                for filespath in files:
                    local_file = os.path.join(root, filespath)
                    a = local_file.replace(self.localpath, '')
                    remote_file = os.path.join(self.remotepath, a)
                    try:
                        t.put(local_file, remote_file)
                    except Exception, e:
                        t.mkdir(os.path.split(remote_file)[0])
                        t.put(local_file, remote_file)
                    print "upload %s to remote %s" % (local_file, remote_file)
                for name in dirs:
                    local_path = os.path.join(root, name)
                    a = local_path.replace(self.localpath, '')
                    remote_path = os.path.join(self.remotepath, a)
                    try:
                        t.mkdir(remote_path)
                        print "mkdir path %s" % remote_path
                    except Exception, e:
                        print e
            print 'upload file success %s ' % datetime.datetime.now()
            t.close()
        except Exception, e:
            print e





if __name__ == "__main__":
    ConnectSFTP().upload()


