from bs4 import BeautifulSoup
import requests
import fake_useragent
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
class champ_stats():
    name =""
    champ_icon=""
    CS = ""
    KDA =""
    winrate =""
    games =""
class sumoner_stats():
    champs = []
    profile_url=""
    nick =""
    icon_url =""
    level = 0
    rank =""
    rank_icon =""
    winrate =""
    win_lose =""
class summoner_info (sumoner_stats):
    def __init__(self):
        super().__init__()
    async def find(self, name:str,tag:str ="auto",region:str ="auto"):
        api_url = 'https://www.op.gg'
        regions = ['ru','euw']
        result = []
        user = fake_useragent.UserAgent().random
        HEADERS2 = {'User_Agent': user}
        for region in regions :
            print(region)
            response1 = requests.get(f"https://www.op.gg/summoners/search?q={name}&region={region}",  headers = HEADERS2).text
            soup = BeautifulSoup(response1, 'html.parser')
            summoners = soup.find_all("li",class_="search-item--pc css-tk3cz9 eeys2jd0")
            if len(summoners) == 0:
                tmp = summoner_info()
                tmp.profile_url = soup.find("link").attrs['href']
                tmp.nick = soup.find('h1', class_= 'css-12ijbdy e1swkqyq0').text
                result.append(tmp)
                #result['url'].append(soup.find("link").attrs['href'])
                #result['name'].append(soup.find('h1', class_= 'css-12ijbdy e1swkqyq0').text)
                continue
            names = soup.find_all("div",class_="css-12ijbdy e1swkqyq0")
            links = soup.find_all("a",class_="summoner-link")
            for i in range(len(names)):
                tmp = summoner_info()
                tmp.profile_url = f"{api_url}{links[i].attrs['href']}"
                tmp.nick = names[i].text
                result.append(tmp)
                #result['url'].append(f"{api_url}{link.attrs['href']}")
                #result['name'].append(name.text)
        return result
    async def champs_info(self):
        options = wd.ChromeOptions()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-certificate-errors-spki-list')
        options.add_argument('--ignore-ssl-errors')
        browser = wd.Chrome(
            options=options
        )
        browser.get(self.profile_url)
        champ_list = browser.find_elements(By.CLASS_NAME, "champion-box")
        for champ in champ_list:
            tmp = champ_stats()
            tmp.champ_icon = champ.find_element(By.TAG_NAME,"img").get_attribute("src")
            tmp.name = champ.find_element(By.TAG_NAME,"img").accessible_name
            tmp.CS = champ.find_element(By.CLASS_NAME,"cs").text
            tmp.KDA = champ.find_element(By.CLASS_NAME,"detail").text
            try:
                tmp.KDA +=f" KDA {champ.find_element(By.CLASS_NAME,"css-954ezp").text.split(":")[0]}"
            except : pass
            try:
                tmp.KDA +=f" KDA {champ.find_element(By.CLASS_NAME,"css-10uuukx").text.split(":")[0]}"
            except : pass
            try : 
                tmp.KDA +=f" KDA {champ.find_element(By.CLASS_NAME,"css-1w55eix").text.split(":")[0]}"
            except : pass
            try:
                tmp.winrate = champ.find_element(By.CLASS_NAME,"css-1nuoroq").text
            except:
                tmp.winrate = champ.find_element(By.CLASS_NAME, "css-b0uosc").text
            tmp.games = champ.find_element(By.CLASS_NAME,"count").text
            self.champs.append(tmp)
    async def fill(self):
        user = fake_useragent.UserAgent().random
        HEADERS2 = {'User_Agent': user}
        response1 = requests.get(self.profile_url,  headers = HEADERS2, ).text
        soup = BeautifulSoup(response1, 'html.parser')
        self.nick = soup.find('strong', class_ = 'css-ao94tw e1swkqyq1').text
        self.icon_url = soup.find('div', class_ = 'profile-icon').find('img').attrs['src'].split('?')[0]
        try:
            self.rank = soup.find('div', class_ = 'tier').text
        except:
            self.rank = "none"
        self.level = int(soup.find('span', class_ = 'level').text)
        try:
            self.winrate = soup.find('div', class_ = 'ratio').text
            self.win_lose = soup.find('div',class_ = "win-lose").text
        except:
            self.winrate = "none"
            self.win_lose = "none"
        self.rank_icon = f"https://opgg-static.akamaized.net/images/medals_new/{self.rank.split(' ')[0]}.png"
    async def test_info(self):
        for champ in self.champs:
            print(champ.name)