import requests,os,time
import json,base64
from bs4 import BeautifulSoup
from os import environ

import random
import http.server
import socketserver
import threading
import subprocess

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler


List = {}
pgno=2
#lowest_price={}
bot_token=environ['BOT_TOKEN']
group_id=environ['grp']
git_token=environ['GIT_TOKEN']

git_data = requests.get('https://github.com/anoop-kmr/ltdinia/raw/feature/updated_prices/lowest.txt')
lp = json.loads(git_data.text)
with open('lowest.txt','wt',encoding='utf-8') as fw:
  fw.write(json.dumps(lp))
  fw.close()

def push_to_github(filename, repo, branch, token):
    url="https://api.github.com/repos/"+repo+"/contents/"+filename

    base64content=base64.b64encode(open(filename,"rb").read())

    data = requests.get(url+'?ref='+branch, headers = {"Authorization": "token "+token}).json()
    sha = data['sha']

    if base64content.decode('utf-8')+"\n" != data['content']:
        message = json.dumps({"message":"update",
                            "branch": branch,
                            "content": base64content.decode("utf-8") ,
                            "sha": sha
                            })

        resp=requests.put(url, data = message, headers = {"Content-Type": "application/json", "Authorization": "token "+token})

        print(resp)
    else:
        print("nothing to update")

def extractDetails(pno):
  global pgno
  global List
  global bot_token
  global group_id
  with open('lowest.txt',encoding='utf-8') as f:
    data = f.read()
    f.close()
    #print(data)
  #data=i[i.find("{"):i.rfind("}")+1].replace("\n", "").replace("  ", "")
  lowest_price = json.loads(data)
  print(pno)
  #url = "https://www.amazon.in/s/query?i=merchant-items&me=A1X54IAKXCWO8D&page="+str(pno)+"&marketplaceID=A21TJRUUN4KGV"
  url = "https://www.amazon.in/s/query?page="+str(pno)+"&rh=n%3A976419031%2Cp_n_condition-type%3A13736826031%2Cp_6%3AA1X54IAKXCWO8D"

  payload = json.dumps({
    "customer-action": "pagination"
  })
  headers = {
    'authority': 'www.amazon.in',
    'accept': 'text/html,*/*',
    'accept-language': 'en-GB,en;q=0.9',
    'content-type': 'application/json',
    'dnt': '1',
    'sec-ch-ua': '"Chromium";v="103", ".Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36',
    'Cookie': ''
  }
  
  try:
    response = requests.request("POST", url, headers=headers, data=payload, allow_redirects=False)

    cook=''
    for c in response.cookies:
        cook+=c.name +"="+ c.value
    headers['Cookie']=cook

    #print(response.text.split('\n&&&\n'))


    for i in response.text.split('\n&&&\n'):
        res = i.strip('][').split(', ')
        #res=json.loads(i)
        if "data-search-metadata" in i:
          x=i[i.find("{"):i.rfind("}")+1].replace("\n", "").replace("  ", "")
          studentDict = json.loads(x)
          #print(studentDict["metadata"]["totalResultCount"]//24)
          pgno=(studentDict["metadata"]["totalResultCount"]//studentDict["metadata"]["asinOnPageCount"] if (studentDict["metadata"]["asinOnPageCount"] != 0) else studentDict["metadata"]["totalResultCount"]//16)
          #print(pgno)
        try:
            if "data-main-slot:search-result-" in i:
                msg=""
                x=i[i.find("{"):i.rfind("}")+1].replace("\n", "").replace("  ", "")
                #print(x+'\n\n')
                studentDict = json.loads(x)
                parsed_html = BeautifulSoup(studentDict["html"], "html.parser")
                #print(studentDict["asin"])
                #print(parsed_html.find('div',{'class':"s-title-instructions-style"}).text.strip())
                price=int(float(parsed_html.find('div',{'class':"s-price-instructions-style"}).text.split('₹')[1].strip().replace(",", "")))
                pct=int(float(parsed_html.find('div',{'class':"s-price-instructions-style"}).text.split('(')[1].split('%')[0].strip()))
                #print(price)
                try:
                  cpn=parsed_html.find('span',{'class':"s-coupon-clipped"}).text.strip()
                  msg+="\n"+str(cpn)
                except:
                  print("No Coupon")
                try:
                  bnk=parsed_html.find('span',{'class':"a-truncate-full"}).text.strip()
                  msg+="\n"+str(bnk)
                except:
                  print("No Bank Offers")
                #pdt={studentDict["asin"]:price}
                if (studentDict["asin"] not in List) or List[studentDict["asin"]]!=price:
                  List[studentDict["asin"]]=price
                  #time.sleep(3)
                  #msg=""
                  if (studentDict["asin"] not in lowest_price) or int(lowest_price[studentDict["asin"]])>price:
                    lowest_price[studentDict["asin"]]=price
                    msg+="\nLowest Price !!"
                    time.sleep(random.randint(4,12))
                    req=requests.get('https://api.telegram.org/bot'+bot_token+'/sendMessage?chat_id='+group_id+'&text=https://www.amazon.in/dp/'+studentDict["asin"]+'/ref=ox_sc_saved_title_7?smid=A1X54IAKXCWO8D\n'+str(price)+'\n'+str(pct)+'% off'+msg)
                  elif int(lowest_price[studentDict["asin"]])<price:
                    msg+="\nLowest Price: "+str(lowest_price[studentDict["asin"]])
                    time.sleep(random.randint(4,12))
                    req=requests.get('https://api.telegram.org/bot'+bot_token+'/sendMessage?chat_id='+group_id+'&disable_notification=true&text=https://www.amazon.in/dp/'+studentDict["asin"]+'/ref=ox_sc_saved_title_7?smid=A1X54IAKXCWO8D\n'+str(price)+'\n'+str(pct)+'% off'+msg)
                  #print(pdt)
                  #print(req)
                  #print(len(List),len(lowest_price))
                #break
        except:
            print('err')
  except:
    print("Connection Error")

  #for student in List:
  #    print(student)
  #print(str(lowest_price))
  with open('lowest.txt','wt',encoding='utf-8') as fw:
    fw.write(json.dumps(lowest_price))
    fw.close()
#   print(requests.head("https://ltdinia.onrender.com/"))
  return pgno

#if __name__=="__main__":
extractDetails(1)
#time.sleep(10)
i=1
def extr():
  global i,pgno,git_token
  print("Thread Running!!")
  while i in range(1,pgno+2):
    #threading.Thread(target=extractDetails,args=[i]).start()
    pgno=extractDetails(i)
    i=i+1
    if i==pgno+1:
      i=1
      time.sleep(random.randint(20,100))
      filename="lowest.txt"
      repo = "anoop-kmr/ltdinia"
      branch="feature/updated_prices"
      push_to_github(filename, repo, branch, git_token)
#       print(subprocess.run(["./upd_price.sh",git_token]))
thr = threading.Thread(None, extr)
thr.start()
print('Waiting for the thread...')

def self_ping():
  while True:
    time.sleep(random.randint(500,700))
    print(requests.get("https://ltdinia.onrender.com/"))
thread3 = threading.Thread(None, self_ping)
thread3.start()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
  print("serving at port", PORT)
  try:
    httpd.serve_forever()
  except:
    time.sleep(5)
    print("Error in serving http request")
  #thread2 = threading.Thread(None, httpd.serve_forever)
  #thread2.start()
#thread.join()
#thread2.join()
time.sleep(10)
