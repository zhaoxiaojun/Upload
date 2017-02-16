#coding=utf-8

"""
test paramiko lib
"""
import paramiko
import os

#RSA密钥授权登录
a = paramiko.SSHClient()
a.set_missing_host_key_policy(paramiko.AutoAddPolicy())
a.connect(hostname='192.168.64.129',port=22,username="root",key_filename="C:\\Users\\22950\\skey")
b,c,d = a.exec_command("ls")
print c.readlines()
e = a.open_sftp()
try:
    e.stat("/home/adolph/Videos/11.txt")
    print "存在"
    a.exec_command("rm -rf xxxx.txt")
except Exception,e:
    print "文件不存在"
a.close()
#密码登录
# a = paramiko.SSHClient()
# a.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# a.connect(hostname='192.168.64.129',port=22,username="root",password="123456")
# b,c,d = a.exec_command("ls -al")
# print c.readlines()

#从Linux服务器端下载文件至本地（windows）
"""
密码或者密钥登录
"""
# t = paramiko.Transport(("192.168.64.129",22))
# t.connect(username="root",pkey=paramiko.RSAKey.from_private_key_file("C:\\Users\\22950\\skey"))
# # t.connect(username="root",password="123456")
# sftp = paramiko.SFTPClient.from_transport(t)
# rmpath = "/root/install.log"
# localpath = os.path.dirname(os.path.abspath(__file__)) + os.sep + "install.log"
# sftp.get(rmpath,localpath)
# t.close()

#从本地（windows）上传文件至Linux服务器
"""
密码或者密钥登录
"""
t = paramiko.Transport(("192.168.64.129",22))
t.connect(username="root",pkey=paramiko.RSAKey.from_private_key_file("C:\\Users\\22950\\skey"))
# t.connect(username="root",password="123456")
sftp = paramiko.SFTPClient.from_transport(t)
rmpath = "/home/adolph/TestUpload.war"
localpath = os.path.dirname(os.path.abspath(__file__)) + os.sep + "TestUpload.war"
sftp.put(localpath,rmpath)
t.close()