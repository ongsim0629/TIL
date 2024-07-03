import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('mongodb+srv://ongsim0629:subin0629@cluster0.p8xwfrb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.project0

    
# 타겟 URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
url = 'https://www.yes24.com/Product/Category/BestSeller?categoryNumber=001&pageNumber=1&pageSize=50'
data = requests.get(url,headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.

soup = BeautifulSoup(data.text, 'html.parser')
books = soup.select('#yesBestList > li')
db.books.drop()
for i in books:
    title = i.select_one('a.gd_name').text.strip()
    img_url = i.select_one('em.img_bdr > img')['data-original']
    auth = i.select_one('span.authPub > a').text
    href = i.select_one('a.gd_name')['href']
    href = 'https://yes24.com' + href
    # print(rank, title, auth)
    db.books.insert_one({"title" : title, "img_url" : img_url, "auth" : auth, "href" : href, "like" : 0})

print("mission complete!")