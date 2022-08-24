import requests,os,time
from urllib.parse import quote_plus
from os import environ

url = "https://www.lootdunia.in/api?query=query%20GetDeals($filter:%20DealsFilter,%20$first:%20Int,%20$after:%20String)%20{%20deals(filter:%20$filter,%20first:%20$first,%20after:%20$after)%20{%20edges%20{%20node%20{%20id%20postName%20stores%20{%20id%20description%20}%20postImage%20postLink%20newPrice%20oldPrice%20extras%20createdOn%20isFeatured%20}%20cursor%20}%20pageInfo%20{%20endCursor%20hasNextPage%20}%20}%20}&variables={%20%22first%22:%201,%20%22after%22:%20null,%20%22filter%22:%20{%20%22isDisabled%22:%20false,%20%22rating%22:%204,%20%22isFeatured%22:%20false%20}%20}"

payload={}
headers = {
  'authority': 'www.lootdunia.in',
  'pragma': 'no-cache',
  'cache-control': 'no-cache',
  'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99"',
  'accept': '*/*',
  'x-requested-with': 'XMLHttpRequest',
  'sec-ch-ua-mobile': '?0',
  'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
  'sec-ch-ua-platform': '"Linux"',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://www.lootdunia.in/',
  'accept-language': 'en-GB,en;q=0.9'
  #'cookie': '_ga=GA1.2.1887507384.1646833650; _gid=GA1.2.1427646947.1646833650; _gat=1; _gat_gtag_UA_106604864_1=1; __gads=ID=27e4bf050a2631bb-22b8f1bce8d000db:T=1646833654:RT=1646833654:S=ALNI_MYsXsUAFPDGYjWhqRln_Q6121lAEw; connect.sid=s%3AXmLcD_vB5ZmzUvjojjCtDHF4FXpuaG3e.vuh5gx3fLNdzdiNKsVc5etwzOTjFnauHF4gQwIbAd%2BA'
}

response = requests.request("GET", url, headers=headers, data=payload)
os.system('clear')
print(response.json()["data"]["deals"]["edges"][0]["node"]["postName"])

bot_token=environ['BOT_TOKEN']
group_id=environ['grp']
#url='http://164.68.96.227/Perk/?m=9118566696'#"http://upbhunaksha.gov.in/bhunaksha/09/plotreportUP.jsp?state=09&giscode=19000959190461&plotno=77"#"http://upsssc.gov.in/Online_App/AdmitCard.aspx?ID=P"
headers1 = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
api_url_telegram = "https://api.telegram.org/bot"+bot_token+"/sendMessage?chat_id={chat_id}&text="
final_telegram_url=api_url_telegram.replace("{chat_id}",group_id)
#print(final_telegram_url)
uid =(response.json()["data"]["deals"]["edges"][0]["node"]["id"])

def strike(text):
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result

def chk():
	response = requests.request("GET", url, headers=headers, data=payload)
	#response=requests.head(url, headers=headers)
	#print(response.status_code)
	nuid=(response.json()["data"]["deals"]["edges"][0]["node"]["id"])
	#print (nuid)
	global uid
	if nuid!=uid:
		uid =response.json()["data"]["deals"]["edges"][0]["node"]["id"]
		name=response.json()["data"]["deals"]["edges"][0]["node"]["postName"].replace('&','%26amp')
		nprice=response.json()["data"]["deals"]["edges"][0]["node"]["newPrice"]
		oprice=response.json()["data"]["deals"]["edges"][0]["node"]["oldPrice"]
		site="https://www.lootdunia.in"+response.json()["data"]["deals"]["edges"][0]["node"]["postLink"]
		res=requests.request("HEAD", site, allow_redirects=False)
		redir=(res.headers["Location"]).replace('&','%26amp')
		message=final_telegram_url+""+name+"\n\n "+str(nprice)+'   '+strike(str(oprice))+"\n\n"+redir+"\n"
		requests.get(message,headers=headers1)
		print(message)
	#else:
	#	print(response)

def exec():
	message="upsssc site is live!!"
	send_message_telegram(message)

def send_message_telegram(message):
	final_telegram_url=api_url_telegram.replace("{chat_id}",group_id)
	#print('here')
	final_telegram_url=final_telegram_url+message;
	#response=requests.get(final_telegram_url)
	message = ('https://api.telegram.org/bot'+ bot_token + '/sendPhoto?chat_id=' 
           + group_id)
	send = requests.post(message, files = files)
	print(send)

if __name__=="__main__":
	while(1==1):
		chk()
		time.sleep(10)
