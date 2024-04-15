#!/home/xfel/xfelopr/local/anaconda3/bin/python3

#	python check.py ical_setting.xlsx ScreenInfo.xlsm
#	./check_alive.py ical_setting.xlsx ScreenInfo.xlsm

#	nohup /home/xfel/xfelopr/local/anaconda3/bin/python3 check_alive.py ical_setting.xlsx ScreenInfo.xlsm &

# Formatter     Shift+Alt+F

#import requests
#from requests.exceptions import Timeout
#import re
import pandas as pd
import sys
#from matplotlib.dates import DateFormatter
#from icalendar import Calendar, Event

import datetime

#import plotly.figure_factory as ff
#import plotly
#import random
import os
#import shutil

#import webbrowser
import time


import sys
import time
import subprocess	

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import signal
print('My PID is:', os.getpid())
def receive_signal(signum, stack):
    print('Received:', signum)
    f = open('check_alive.log', 'a')
    f.write("Received:	" + str(signum)  + "\n")
    f.close()
    sys.exit()

signal.signal(signal.SIGHUP, receive_signal)
signal.signal(signal.SIGINT, receive_signal)
signal.signal(signal.SIGQUIT, receive_signal)
signal.signal(signal.SIGILL, receive_signal)
signal.signal(signal.SIGTRAP, receive_signal)
signal.signal(signal.SIGABRT, receive_signal)
signal.signal(signal.SIGBUS, receive_signal)
signal.signal(signal.SIGFPE, receive_signal)
#signal.signal(signal.SIGKILL, receive_signal)
signal.signal(signal.SIGUSR1, receive_signal)
signal.signal(signal.SIGSEGV, receive_signal)
signal.signal(signal.SIGUSR2, receive_signal)
signal.signal(signal.SIGPIPE, receive_signal)
signal.signal(signal.SIGALRM, receive_signal)
signal.signal(signal.SIGTERM, receive_signal)
#signal.signal(signal.SIGSTKFLT, receive_signal)
#-signal.signal(signal.SIGCHLD, receive_signal)
signal.signal(signal.SIGCONT, receive_signal)
#signal.signal(signal.SIGSTOP, receive_signal)
signal.signal(signal.SIGTSTP, receive_signal)
#~signal.signal(signal.SIGTTIN, receive_signal)	
signal.signal(signal.SIGTTOU, receive_signal)
signal.signal(signal.SIGURG, receive_signal)
signal.signal(signal.SIGXCPU, receive_signal)
signal.signal(signal.SIGXFSZ, receive_signal)
signal.signal(signal.SIGVTALRM, receive_signal)
signal.signal(signal.SIGPROF, receive_signal)
signal.signal(signal.SIGWINCH, receive_signal)
signal.signal(signal.SIGIO, receive_signal)
signal.signal(signal.SIGPWR, receive_signal)
signal.signal(signal.SIGSYS, receive_signal)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



args = sys.argv
print("arg1:" + args[1])
config_file_setting = args[1]
config_file_sig = args[2]

df_set = pd.read_excel(config_file_setting,
                       sheet_name="setting", header=None, index_col=0)
print(df_set)

print(config_file_sig)
df_sig = pd.read_excel(config_file_sig, sheet_name="SCSS_GigE")
print(df_sig)


"""  -------------------------------------------------------------------------------------  """


def get_acc_sync(url):

    # print(url)
    try:
        res = requests.get(url, timeout=(30.0, 30.0))
    except Exception as e:
        #print('Exception!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!@get_acc_sync	' + url)
        print(e.args)
        return ''
    else:
        res.raise_for_status()
        return res.text


class SigInfo:
    def __init__(self):
        self.srv = ''
        self.url = ''
        self.sname = ''
        self.sid = 0
        self.sta = ''
        self.sto = ''
        self.time = ''
        self.val = ''
        self.sortedval = []
        self.rave = []
        self.rave_sigma = []
        self.d = {}
        self.t = {}
        self.mu = 0
        self.icaldata = ''
        self.sigma = 0


sig = [SigInfo() for _ in range(len(df_sig))]

JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')

now = datetime.datetime.now()

#cp = subprocess.run(["ssh", "xfelopr@scimg-bl1-01","arv-tool-0.6","-a","192.168.0.1"], capture_output=True, text=True)
#print("stdout:", cp.stdout)
#print("stderr:", cp.stderr)

#cp = subprocess.run(["ssh", "xfelopr@scimg-bl1-01","arv-tool-0.6","-a","192.168.1.1"], capture_output=True, text=True)
#print("stdout:", cp.stdout)
#print("stderr:", cp.stderr)

f = open('check_alive.log', 'a')
f.write("START:	" + str(now)  + "--------------------------\n")
f.close()


while True:
    for n, s in enumerate(sig, 0):
#    print(str(df_sig.loc[n]['plc']) + "	" + str(df_sig.loc[n]['ip']))
        cp = subprocess.run(["ssh", str(df_sig.loc[n]['plc']),"arv-tool-0.6","-a",str(df_sig.loc[n]['ip'])], capture_output=True, text=True)
        now = datetime.datetime.now()
#    print("OK!	stdout:", cp.stdout)
#    print("ERR!	stderr:", cp.stderr)
        if not cp.stderr:
            print("OK:	" + str(now) + "	" + str(df_sig.loc[n]['name']) + "	" + str(df_sig.loc[n]['plc']) + "	" + str(df_sig.loc[n]['ip']))
#	- DEBUG -
            f = open('check_alive.log', 'a')
            f.write("OK:	" + str(now) + "	" + str(df_sig.loc[n]['name']) + "	" + str(df_sig.loc[n]['plc']) + "	" + str(df_sig.loc[n]['ip']) + "\n")
            f.close()
#	- DEBUG -
        else:
            print("DOWN:	" + str(now) + "	" + str(df_sig.loc[n]['name']) + "	" + str(df_sig.loc[n]['plc']) + "	" + str(df_sig.loc[n]['ip']))
            f = open('check_alive.log', 'a')
            f.write("DOWN:	" + str(now) + "	" + str(df_sig.loc[n]['name']) + "	" + str(df_sig.loc[n]['plc']) + "	" + str(df_sig.loc[n]['ip']) + "\n")
            f.close()

            cm0 = subprocess.run(["tellms", "put/"+str(df_sig.loc[n]['cmd_port'])+"/off"], capture_output=True, text=True)
            print(cm0.stderr)
            print(cm0.stdout)
            time.sleep(10)
            cm0 = subprocess.run(["tellms", "put/"+str(df_sig.loc[n]['cmd_port'])+"/on"], capture_output=True, text=True)
            print(cm0.stderr)
            print(cm0.stdout)
            time.sleep(30)

            cm0 = subprocess.run(["tellms", "put/"+str(df_sig.loc[n]['cname'])+"_param/format_Mono10"], capture_output=True, text=True)
            print(cm0.stderr)
            print(cm0.stdout)
            time.sleep(10)

            cm0 = subprocess.run(["tellms", "put/"+str(df_sig.loc[n]['cname'])+"_param/trigsource_Line5"], capture_output=True, text=True)
            print(cm0.stderr)
            print(cm0.stdout)
            time.sleep(10)

            cm0 = subprocess.run(["tellms", "put/"+str(df_sig.loc[n]['cname'])+"_param/trigmode_1"], capture_output=True, text=True)
            print(cm0.stderr)
            print(cm0.stdout)
            time.sleep(10)


    f = open('check_alive.log', 'a')
    f.write("\n")
    f.close()

    time.sleep(3600)










