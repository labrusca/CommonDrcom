#coding=GBK
#__author__="Labrusca"

'''
Copyright 2014 labrusca

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

'''


import time
import socket
import urllib2
import wx,re
from webbrowser import open as webopen
from httplib import HTTPConnection
from urllib import urlencode
from hashlib import md5
from re import findall
retmp=re.compile('\w+')  #Ϊ�˼���ƥ��

is_logined = 0 #�ѵ�½���

class TaskBarIcon(wx.TaskBarIcon):
    ID_Hello = wx.NewId()
    def __init__(self, frame):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
        self.SetIcon(wx.Icon(name='T.dll', type=wx.BITMAP_TYPE_ICO), 'TaskBarIcon!')
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarLeftDClick)

    def OnTaskBarLeftDClick(self, event):
        if self.frame.IsIconized():
           self.frame.Iconize(False)
        if not self.frame.IsShown():
           self.frame.Show(True)
        self.frame.Raise()

class Gateway(wx.Frame):
    "class for gateway"
    def __init__(self):
        self.Frame=wx.Frame.__init__(self,None,-1,"�Ͼ��ʵ��ѧУ԰��Dr.com��֤ϵͳV4.1  ��������",\
                   pos=(250,200),size=(570,380),style=wx.MINIMIZE_BOX|wx.CAPTION|wx.CLOSE_BOX)
        panel=wx.Panel(self,-1)  
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.updateinfo, self.timer)
        self.Bind(wx.EVT_ICONIZE, self.OnIconfiy)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.taskBarIcon = TaskBarIcon(self)
        self.SetMinSize((570,380))
        self.SetMaxSize((570,380))
        imge = wx.Icon('logo.dll', wx.BITMAP_TYPE_JPEG)
        self.SetIcon(imge)
        #get memory from config or initial cofig
        try:
            f=open("Save.configfile",'r')
        except IOError:
            f=open("Save.configfile",'w')
            f.write("emansru\ndwssap")
            f.close()  #д���������Զ������ļ�����
            f=open("Save.configfile",'r')
        #����
        line1 = decrypt(f.readline())
        line2 = decrypt(f.readline())
        f.close()
        #UI
        img1 = wx.Image('logo.dll', wx.BITMAP_TYPE_ANY)
        wx.StaticBitmap(panel,-1,wx.BitmapFromImage(img1),pos=(325,10))
        panel.SetBackgroundColour('#FFFFFF')
        font=wx.Font(14,wx.DEFAULT,wx.NORMAL,wx.NORMAL)
        font2=wx.Font(12,wx.DEFAULT,wx.NORMAL,wx.NORMAL)
        style=wx.TextAttr(font=font)
        user=wx.StaticText(panel,-1,u"�û�����",pos=(20,30)).SetFont(font)
        password=wx.StaticText(panel,-1,u"  ���룺",pos=(20,70)).SetFont(font)
        self.usrvalue=wx.TextCtrl(panel,-1,line1,pos=(120,30),size=(180,30))
        self.usrvalue.SetFont(font)
        self.passwdvalue=wx.TextCtrl(panel,-1,line2,pos=(120,70),size=(180,30),style=wx.PASSWORD)
        self.passwdvalue.SetFont(font)
        self.memo=wx.CheckBox(panel,-1,u"�Զ�����",pos=(120,120),size=(80,30))
        self.memo.SetFont(font2)
        self.memo.SetValue(1)
        self.force=wx.CheckBox(panel,-1,u"(�˺�����ʹ��ʱ)ǿ�е�¼",pos=(120,150),size=(240,30))
        self.force.SetFont(font2)
        self.radio_box = wx.RadioBox(panel,-1, "ѡ���½��ʽ",pos=(120,190),size=(240,60),choices=["ѧ��", "У԰��"], majorDimension=0, style=wx.RA_SPECIFY_COLS)
        self.loginbutton=wx.Button(panel,-1,u"��¼",pos=(150,280),size=(140,50))
        self.loginbutton.Bind(wx.EVT_BUTTON,self.loginfunc)
        self.logoutbutton=wx.Button(panel,-1,u"ע��",pos=(320,280),size=(140,50))
        self.logoutbutton.Bind(wx.EVT_BUTTON,self.logoutfunc)
        self.loginbutton.Enable(True)
        self.logoutbutton.Enable(False)
        self.UsedTime=wx.StaticText(panel,-1,"��ʹ��ʱ�䣺δ֪",pos=(375,190))
        self.UsedFiux=wx.StaticText(panel,-1,"��ʹ��������δ֪",pos=(375,210))
        self.Balance=wx.StaticText(panel,-1,"��δ֪",pos=(375,230))
        updateinfo=wx.Button(panel,-1,u"������ҳ��Ϣ",pos=(5,280),size=(80,25))
        updateinfo.Bind(wx.EVT_BUTTON,self.openpage)
        sendback=wx.Button(panel,-1,u"��ϵ����",pos=(5,310),size=(80,25))
        sendback.Bind(wx.EVT_BUTTON,self.sendback)
        try:
            test = search_info()
            autologout = logout()
            if autologout == "14":
                self.showanser(u'��ע�⣬�ϴε�½��δע����ϵͳ���Զ�ע����')
            else:
                self.showanser(self.othererror())
        except:
            pass

    def OnIconfiy(self, event):
        self.Hide()
        event.Skip()

    def OnClose(self, event):
        if is_logined == 1:
            self.showanser(u"����ע���˺ţ��ٹرճ���")
        else:
            self.taskBarIcon.Destroy()
            self.Destroy()

    #functions
    def loginfunc(self,event):
        try:
            line1=re.search(retmp,self.usrvalue.GetValue()).group()
            line2=re.search(retmp,self.passwdvalue.GetValue()).group()
        except AttributeError:
            self.showanser(u'����Ƿ�')
            return
        if self.radio_box.GetSelection() == 0:
            try:
                newline1 = turn_num(line1)
            except socket.gaierror:
                self.showanser(u"������������Ӧ���뻻��У԰����ʽ��½��")
            ans=login(newline1,line2,force=self.force.GetValue())
        elif self.radio_box.GetSelection() == 1:
            ans=login(line1,line2,force=self.force.GetValue())
        if ans == 1:
            is_logined = 1
            self.showanser(u"��½�ɹ�")
            self.loginbutton.Enable(False)
            self.logoutbutton.Enable(True)
            info = search_info()
            self.UsedTime.SetLabel("��ʹ��ʱ�䣺%d Min" % int(info[0]))
            self.UsedFiux.SetLabel("��ʹ��������%.3f MByte" % float(float(info[1])/1024))
            self.Balance.SetLabel("��%.2f RMB" % float(float(info[2])/10000))
            self.timer.Start(1000)
        else:
            self.showanser(ans)
        if self.memo.GetValue():
            f=open("Save.configfile",'w')
            #�򵥼���
            f.write("%s\n%s"%(encrypt(line1),encrypt(line2)))
            f.close()

    def logoutfunc(self,event):
        self.timer.Stop()
        try:
            info = search_info()
            self.UsedTime.SetLabel("��ʹ��ʱ�䣺%d Min" % int(info[0]))
            self.UsedFiux.SetLabel("��ʹ��������%.3f MByte" % float(float(info[1])/1024))
            self.Balance.SetLabel("��%.2f RMB" % float(float(info[2])/10000))
        except:
            self.UsedTime.SetLabel("��ʹ��ʱ�䣺�޷���ȡ����")
            self.UsedFiux.SetLabel("��ʹ���������޷���ȡ����")
            self.Balance.SetLabel("���޷���ȡ����")
        ans=logout()
        if ans =="14":
            is_logined = 0
            self.showanser(u"ע���ɹ�")
        else:
            self.showanser(ans)
        self.loginbutton.Enable(True)
        self.logoutbutton.Enable(False)

    def updateinfo(self,event):
        try:
            info = search_info()
        except:
            self.timer.Stop()
            self.showanser(self.othererror())
        self.UsedTime.SetLabel("��ʹ��ʱ�䣺%d Min" % int(info[0]))
        self.UsedFiux.SetLabel("��ʹ��������%.3f MByte" % float(float(info[1])/1024))
        self.Balance.SetLabel("��%.2f RMB" % float(float(info[2])/10000))
    def sendback(self,event):
        webopen("mailto:labrusca@live.com")
    def openpage(self,event):
        webopen("http://account.njupt.edu.cn")
    def othererror(self):
        return "UNKONW ERROR,please wait for next verion."
    def showanser(self,n):
        dialog=wx.MessageDialog(None,n,'ANSWER',wx.YES_DEFAULT|wx.ICON_INFORMATION)
        result=dialog.ShowModal()
        if result==wx.ID_YES:
            dialog.Destroy()
        else:
            pass
        dialog.Destroy()

def turn_num(ID): 
    data = urlencode({'key':ID })   
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = HTTPConnection('my.njupt.edu.cn',timeout=10)
    conn.request('POST', '/ccs/main/searchUser.do', data, headers)
    httpres = conn.getresponse()
    if httpres.status == 200:
        deal = httpres.read()
        pat = '[0-9]+'
        return re.findall(pat,deal)[1]

#passwd is stringed
def login(usr, passwd, url = "http://account.njupt.edu.cn",force=0):
     data = {} # ��ʼ����
     data["DDDDD"] = usr 
     data["upass"] = calpwd(passwd) #����ת��
     data["R1"] = "0"
     data["R2"] = "1"
     data["para"] = "00"
     data["0MKKey"] = "123456"
     data = urlencode(data)   #����
     if force:
         req=urllib2.Request(url+"/all.htm", data)
     else:
         req=urllib2.Request(url, data)   #������Ӧ
     try:
         response = urllib2.urlopen(req, data,timeout=10) #�����Ӧ
     except urllib2.URLError:
         return u"��½��ʱ�������ԣ�"
     rsp = response.read()
     temp = findall(r"You have successfully logged into our system.", rsp) #��ѯ״̬
     if not temp: #��¼δ�ɹ�
         temp = findall(r"Msg=(\d+)", rsp)[0]
         if temp =="01":
             errormsga = findall(r"msga=\'(.*)\'", rsp)[0]
             if errormsga !="":
                 if errormsga =="error0":
                     return u"��IP������Web��ʽ��¼"
                 elif errormsga =="error1":
                     return u"���˺Ų�����Web��ʽ��¼"
                 else:
                     return u"δ֪���󣬴���ţ�%s." % errormsga
             else:
                 return u"�˺Ż����벻�ԣ�����������"
         elif temp =="02":
             xip = findall(r"xip=\'(\d+)\.(\d+)\.(\d+).(\d+)\.\'", rsp)[0]
             return u"���˺�����ʹ���У�IP��ַ��%s" % xip
         elif temp =="03":
             return u"���˺�ֻ����ָ����ַʹ��"
         elif temp =="04":
             return u"���˺ŷ��ó�֧��ʱ��������������"
         elif temp =="05":
             return u"���˺���ͣʹ��"
         elif temp =="11":
             return u"���˺�ֻ����ָ����ַʹ��"
     else:
         return 1
   
def calpwd(init_pwd):   #ʹ��md5��������ת��
     pid = '1'
     calg='12345678'
     tmp = pid + init_pwd + calg
     #print "tmp=",tmp
     pwd = md5(tmp).hexdigest() + calg + pid
     #print "pwd=",pwd
     return pwd 

def logout():
    try:
        response = urllib2.urlopen("http://account.njupt.edu.cn/F.htm",timeout=10)
    except urllib2.URLError:
        return u"ע��ʧ�ܣ���������Ӧ��"
    rsp = response.read()
    temp = findall(r"Msg=(\d+)", rsp)[0]
    if temp == "01":
        response = urllib2.urlopen("http://192.168.168.168/F.htm")     #��account.njupt.edu.cn������Ϊ����IP��ַ
        rsp = response.read()
        logouterror = findall(r"msga=\'(.+)\'", rsp)[0]
        return logouterror
    else:
        return temp

def encrypt(s):
    f = ''
    for n in range(0,len(s)):
        f = s[::-1]
    return f

def decrypt(s):    #WTF?!
    return encrypt(s)

def search_info():
    try:
        response = urllib2.urlopen("http://account.njupt.edu.cn")
    except urllib2.URLError:
        t=["��ʱ","��ʱ","��ʱ"]
    rsp = response.read()
    t = [0,0,0]
    t[0] = findall(r"time=\'(\d+)", rsp)[0]
    t[1] = findall(r"flow=\'(\d+)", rsp)[0]
    t[2] = findall(r"fee=\'(\d+)", rsp)[0]
    return t

if __name__ == '__main__':
        app=wx.App()
        Gateway().Show()
        app.MainLoop()
