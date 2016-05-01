#coding=GBK
#__author__="Labrusca"

'''
Copyright 2015 labrusca

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
import httplib
import sqlite3
import base64
import wx,re
from webbrowser import open as webopen
from urllib import urlencode
from hashlib import md5
from re import findall
#img2py made
import T,logo
retmp=re.compile('\w+')  #Ϊ�˼���ƥ��
school_url = "http://account.njupt.edu.cn"

versioninfo = "5.0.5"
class TaskBarIcon(wx.TaskBarIcon):
    aboutme = wx.NewId()
    closeme = wx.NewId()
    updateme = wx.NewId()
    pubinfo = wx.NewId()
    def __init__(self, frame):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
        self.SetIcon(T.get_Icon(), '�Ͼ��ʵ��ѧDr.com��֤ϵͳ')
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_taskbar_leftdown)
        self.Bind(wx.EVT_MENU, self.func_updateme, id=self.updateme)
        self.Bind(wx.EVT_MENU, self.func_aboutme, id=self.aboutme)
        self.Bind(wx.EVT_MENU, self.func_closeme, id=self.closeme)
        self.Bind(wx.EVT_MENU, self.func_openpage, id=self.pubinfo)

    def func_updateme(self,event):
        try:
            update_req,mustupdate_req,updateinfo_req = urllib2.Request("http://drcomupdate.sinaapp.com/update"),urllib2.Request("http://drcomupdate.sinaapp.com/ismusttoupdate"),urllib2.Request("http://drcomupdate.sinaapp.com/updateinfo")
            update_req.add_header('User-Agent','Python/2.7.7 SoftwareVersion:%s' % versioninfo)
            mustupdate_req.add_header('User-Agent','Python/2.7.7 SoftwareVersion:%s' % versioninfo)
            updateinfo_req.add_header('User-Agent','Python/2.7.7 SoftwareVersion:%s' % versioninfo)
            update_response = urllib2.urlopen(update_req,timeout=8)
            mustupdate_response = urllib2.urlopen(mustupdate_req,timeout=8)
            updateinfo_response = urllib2.urlopen(updateinfo_req,timeout=8)
        except urllib2.URLError:
            t = Gateway()
            t.showanser("������������������á�")
        except socket.timeout:
            t = Gateway()
            t.showanser("���ӳ�ʱ�������������á�")
        else:
            update_rsp = update_response.read()
            mustupdate_rsp = mustupdate_response.read()
            updateinfo_rsp = updateinfo_response.read()
            if update_rsp != versioninfo:
                if mustupdate_rsp == "yes":
                    dialog = wx.MessageDialog(None,"��⵽�°汾 %s���˴θ������ݣ�\n%s\n�˴θ���Ϊǿ��������������������" % (update_rsp,updateinfo_rsp),'����',wx.YES_DEFAULT|wx.ICON_INFORMATION)
                elif mustupdate_rsp == "no":
                    dialog = wx.MessageDialog(None,"��⵽�°汾 %s���˴θ������ݣ�\n%s\n�Ƿ�������" % (update_rsp,updateinfo_rsp),'����',wx.YES_NO|wx.ICON_INFORMATION)
                elif mustupdate_rsp == "new":
                    dialog = wx.MessageDialog(None,"�������������ֹͣ������ά���������˲���ֹ���ڴ�:\n�¼ܹ����¼�������UI������ƣ�����õ�ȫ�����顪��nw.js��Dr.com�ͻ��ˣ��������أ�",'��ȡnw.js��Dr.com�ͻ���',wx.YES_NO|wx.ICON_INFORMATION)
                result=dialog.ShowModal()
                if result == wx.ID_NO:
                    dialog.Destroy()
                else:
                    webopen("https://git.oschina.net/labrusca/NUPT_Drcom_loginer/repository/archive?ref=%s" % update_rsp)
                dialog.Destroy()

    def func_openpage(self,event):
        webopen(school_url)

    def func_aboutme(self, event):
        wx.MessageBox('�˳�����ѭApache V2.0Э�鿪Դ���й��ڿ�Դ�й�Git@OSC�ֿ�\n�汾��Ϣ��%s' % versioninfo, '����')

    def func_closeme(self,event):
        self.frame.Close()

    def  CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(self.updateme, '��ȡnw.js��Dr.com�ͻ���')
        menu.Append(self.pubinfo, '������ҳ����Ϣ')
        menu.Append(self.aboutme, '����')
        menu.Append(self.closeme, '�˳�')
        return menu
    def on_taskbar_leftdown(self, event):
        if self.frame.IsIconized():
           self.frame.Iconize(False)
        if not self.frame.IsShown():
           self.frame.Show(True)
        self.frame.Raise()

class Gateway(wx.Frame):
    "class for gateway"
    def __init__(self):
        self.Frame=wx.Frame.__init__(self,None,-1,"�Ͼ��ʵ��ѧУ԰��Dr.com��֤�ͻ��� %s" % versioninfo,\
                   pos=(250,200),size=(570,400),style=wx.MINIMIZE_BOX|wx.CAPTION|wx.CLOSE_BOX)
        panel=wx.Panel(self,-1)  
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.updateinfo, self.timer)
        self.Bind(wx.EVT_ICONIZE, self.oniconfiy)
        self.Bind(wx.EVT_CLOSE, self.onclose)
        self.taskBarIcon = TaskBarIcon(self)
        self.SetMinSize((570,400))
        self.SetMaxSize((570,400))
        self.SetIcon(T.get_Icon())
        conn = sqlite3.connect('C:\\save.db')
        curs = conn.cursor()
        try:
            curs.execute('CREATE TABLE account (username VARCHAR(20), password VARCHAR(20), logintype INT)')
            curs.execute('INSERT INTO account (username, password, logintype) VALUES("emanresu","drowssap",0)')
            conn.commit()
        except sqlite3.OperationalError:
            pass
        curs.execute('SELECT * FROM account')
        acc = curs.fetchall()
        #����
        line1 = decrypt(acc[0][0])
        line2 = decrypt(acc[0][1])
        #UI
        wx.StaticBitmap(panel,-1,wx.BitmapFromImage(logo.getjpg()),pos=(325,10))
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
        self.radio_box = wx.RadioBox(panel,-1, "ѡ���½��ʽ",pos=(120,190),size=(240,60),choices=["ѧ��/����", "У԰����"], majorDimension=0, style=wx.RA_SPECIFY_COLS)
        self.radio_box.SetSelection(acc[0][2])
        curs.close()
        conn.close()
        self.loginbutton=wx.Button(panel,-1,u"��¼",pos=(150,280),size=(140,50))
        self.loginbutton.Bind(wx.EVT_BUTTON,self.loginfunc)
        self.logoutbutton=wx.Button(panel,-1,u"ע��",pos=(320,280),size=(140,50))
        self.logoutbutton.Bind(wx.EVT_BUTTON,self.logoutfunc)
        self.loginbutton.Enable(True)
        self.logoutbutton.Enable(False)
        self.UsedTime=wx.StaticText(panel,-1,"��ʹ��ʱ�䣺δ֪",pos=(375,190))
        self.UsedFiux=wx.StaticText(panel,-1,"��ʹ��������δ֪",pos=(375,210))
        self.Balance=wx.StaticText(panel,-1,"��δ֪",pos=(375,230))
        self.sbar = self.CreateStatusBar()
        self.SetMaxSize((570,400))
        self.SetMinSize((570,400))
        self.Center()
        self.sbar.SetStatusText("���ҵ�½У԰������������������~")
        updateinfo=wx.Button(panel,-1,u"�鿴����������",pos=(5,280),size=(100,25))
        updateinfo.Bind(wx.EVT_BUTTON,self.pubinfo)
        sendback=wx.Button(panel,-1,u"��ϵ����",pos=(5,310),size=(80,25))
        sendback.Bind(wx.EVT_BUTTON,self.sendback)
        #�ϴ�δע��ʱ��ִ�У�
        try:
            is_notlogout = search_info()
            self.loginbutton.Enable(False)
            self.logoutbutton.Enable(True)
            self.timer.Start(3000)
        except:
            pass

    def oniconfiy(self, event):
        self.Hide()
        event.Skip()

    def onclose(self, event):
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
                ans=login(newline1,line2,force=self.force.GetValue())
            except socket.gaierror:
                self.showanser(u"������������Ӧ���볢����У԰���ŵ�½��")
                return 0
            except IndexError:
                self.showanser(u"�Ƿ����룬�����û���������")
                return 0
            except socket.timeout:
                self.showanser(u"��ʱ���޷������������ģ�")
                return 0
        elif self.radio_box.GetSelection() == 1:
            ans=login(line1,line2,force=self.force.GetValue())
        if ans == 1:
            self.sbar.SetBackgroundColour('#87CEFA')
            self.sbar.SetStatusText('��½�ɹ���')
            self.loginbutton.Enable(False)
            self.logoutbutton.Enable(True)
            info = search_info()
            self.UsedTime.SetLabel("��ʹ��ʱ�䣺%d Min" % int(info[0]))
            self.UsedFiux.SetLabel("��ʹ��������%.3f MByte" % float(float(info[1])/1024))
            self.Balance.SetLabel("��%.2f RMB" % float(float(info[2])/10000))
            self.taskBarIcon.func_updateme(self)
            self.timer.Start(3000)
        else:
            self.showanser(ans)
        if self.memo.GetValue():
            conn = sqlite3.connect('C:\\save.db')
            curs = conn.cursor()
            curs.execute("update account set username='%s',password='%s',logintype='%d'" % (encrypt(line1),encrypt(line2),self.radio_box.GetSelection()))
            conn.commit()
            curs.close()
            conn.close()

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
            self.sbar.SetBackgroundColour('#FFFFF0')
            self.sbar.SetStatusText('ע���ɹ���')
        else:
            self.showanser(ans)
        self.loginbutton.Enable(True)
        self.logoutbutton.Enable(False)

    def updateinfo(self,event):
        try:
            info = search_info()
        except IndexError:
            self.timer.Stop()
            self.loginbutton.Enable(True)
            self.logoutbutton.Enable(False)
            self.sbar.SetBackgroundColour('#FFFF00')
            self.sbar.SetStatusText("�������ߡ�")
            self.showanser("�����˻����⣬�˺������ߡ�")
        except urllib2.URLError:
            self.timer.Stop()
            self.sbar.SetBackgroundColour('RED')
            self.sbar.SetStatusText("���ݸ���ʧ�ܣ������������ã�")
            self.timer.Start(4000)
        except httplib.BadStatusLine:
            self.timer.Stop()
            self.sbar.SetBackgroundColour('RED')
            self.sbar.SetStatusText("������δ�������ݣ�")
            self.timer.Start(3000)
        except (socket.timeout,socket.error,socket.gaierror):
            self.timer.Stop()
            self.sbar.SetBackgroundColour('RED')
            self.sbar.SetStatusText("���ӳ�ʱ�������������ã�")
            self.timer.Start(4000)
        else:
            self.sbar.SetBackgroundColour('#87CEFA')
            self.sbar.SetStatusText('�ѵ�½')
            self.UsedTime.SetLabel("��ʹ��ʱ�䣺%d Min" % int(info[0]))
            self.UsedFiux.SetLabel("��ʹ��������%.3f MByte" % float(float(info[1])/1024))
            self.Balance.SetLabel("��%.2f RMB" % float(float(info[2])/10000))
            if 0 <float(float(info[2])/10000) <=0.2 :
                self.sbar.SetBackgroundColour('#FFFF00')
                self.sbar.SetStatusText('ע�⣬����Ѳ���0.2Ԫ��Ԥ��ʹ��ʱ�䲻��һСʱ���뼰ʱ��ֵ��')

    def sendback(self,event):
        webopen("mailto:labrusca@live.com")
    def pubinfo(self,event):
        try:
            info_req = urllib2.Request("http://drcomupdate.sinaapp.com/information")
            info_req.add_header('User-Agent','Python/2.7.7 SoftwareVersion:%s' % versioninfo)
            info_response = urllib2.urlopen(info_req,timeout=5)
            info_rsp = info_response.read()
            wx.MessageBox(info_rsp, '������������')
        except urllib2.URLError:
            self.showanser("����������Ӧ�������������á�")
    def othererror(self,errorprint):
        return "UNKONW ERROR:%s,please wait for next verion." % errorprint
    def showanser(self,n):
        dialog=wx.MessageDialog(None,n,'��ʾ',wx.YES_DEFAULT|wx.ICON_ERROR)
        result=dialog.ShowModal()
        if result==wx.ID_YES:
            dialog.Destroy()
        dialog.Destroy()

def turn_num(ID): 
    data = urlencode({'key':ID })   
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = httplib.HTTPConnection('my.njupt.edu.cn',timeout=5)
    conn.request('POST', '/ccs/main/searchUser.do', data, headers)
    httpres = conn.getresponse()
    if httpres.status == 200:
        deal = httpres.read()
        pat = '[0-9]+'
        if re.findall(pat,deal)[1] != "":
            return re.findall(pat,deal)[1]

#passwd is stringed
def login(usr, passwd, url = school_url,force=0):
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
         req.add_header('User-Agent','Python/2.7.7 SoftwareVersion:%s' % versioninfo)
         response = urllib2.urlopen(req, data,timeout=5) #�����Ӧ
         rsp = response.read()
     except urllib2.URLError:
         return u"��½��ʱ�������ԣ�"
     except httplib.BadStatusLine:
         return u"������δ�������ݣ�"
     except socket.timeout:
         return u"���Ӵ��������ԣ�"
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
                     return u"δ֪���󣬴�����룺%s." % errormsga
             else:
                 return u"��½ʧ�ܣ�����ȷ���˺ż��������ȷ�ԡ�"
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
   
def calpwd(init_pwd):   #ʹ��md5�����������
     pid = '1'
     calg='12345678'
     tmp = pid + init_pwd + calg
     pwd = md5(tmp).hexdigest() + calg + pid
     return pwd 

def logout():
    try:
        response = urllib2.urlopen(school_url + "/F.htm",timeout=5)
        rsp = response.read()
    except urllib2.URLError:
        return u"ע��ʧ�ܣ���������Ӧ��"
    except httplib.BadStatusLine:
        return u"������δ�������ݣ�"
    except socket.timeout:
        return u"���Ӵ��������ԣ�"
    temp = findall(r"Msg=(\d+)", rsp)[0]
    if temp == "01":
        logouterror = findall(r"msga=\'(.+)\'", rsp)[0]
        return logouterror
    else:
        return temp

#�ӽ��ܹ��ܣ�δ���汾���޸�
def encrypt(s):
    return base64.encodestring(s)

def decrypt(s):
    return base64.decodestring(s)

def search_info():
    response = urllib2.urlopen(school_url,timeout=8)
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
