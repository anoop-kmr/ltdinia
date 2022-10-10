import requests,os,time
import json
from bs4 import BeautifulSoup
from os import environ

List = {}
pgno=2

def extractDetails(pno):
  global pgno
  global List
  print(pno)
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
        pgno=studentDict["metadata"]["totalResultCount"]//24
        print(pgno)
      try:
          if "data-main-slot:search-result-" in i:
              x=i[i.find("{"):i.rfind("}")+1].replace("\n", "").replace("  ", "")
              #print(x+'\n\n')
              studentDict = json.loads(x)
              parsed_html = BeautifulSoup(studentDict["html"], "html.parser")
              #print(studentDict["asin"])
              #print(parsed_html.find('div',{'class':"s-title-instructions-style"}).text.strip())
              price=(parsed_html.find('div',{'class':"s-price-instructions-style"}).text.split('₹')[1].strip().replace(",", ""))
              #print(price)
              #pdt={studentDict["asin"]:price}
              if (studentDict["asin"] not in List) or List[studentDict["asin"]]!=price:
                List[studentDict["asin"]]=price
                time.sleep(1)
                req=requests.get('https://api.telegram.org/bot1895716753:AAFFeYc5arNY1XTC-5OcXFMzpvh6VYzq0R8/sendMessage?chat_id=@livchk&text=https://www.amazon.in/dp/'+studentDict["asin"]+'\n'+str(price))
                #print(pdt)
                print(req)
              #break
      except:
          print('err')

  #for student in List:
  #    print(student)
  return pgno

if __name__=="__main__":
  extractDetails(1)
  bot_token=environ['BOT_TOKEN']
  group_id=environ['grp']
  i=1
  while i in range(1,pgno+1):
    pgno=extractDetails(i)
    i=i+1
    if i==pgno:
      i=1
  time.sleep(10)
