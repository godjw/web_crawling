from urllib.request import *
from bs4 import *
import matplotlib.pyplot as plt


def format_request(url):
    req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0')
    return req

def inputCompanyAndDays():
    print("1:samsung, 2:lge, 3:hyun_car")
    company = int(input('회사를 고르세요 : ')) - 1
    DN = int(input('종가 추출 기간을 입력하세요(20의 배수가 되도록 상향 조정합니다) : '))  # 추출하고자 하는 일별 종가의 수
    PN = (DN + 19) // 20  # 추출 횟수를 20의 배수로 조정
    return company, PN

def extractLastPrice(company, PN):
    # 종가 추출
    pList = []
    for page in range(1, PN + 1):
        wPage = urlopen(format_request(webUrl[company] + str(page)))
        soup = BeautifulSoup(wPage, 'html.parser')
        trList = soup.find_all('tr', {'onmouseover': 'mouseOver(this)'})
        for tr in trList:
            tdList = tr.find_all('td')
            price = int(tdList[1].get_text().replace(',', ''))
            pList.append(price)

    return pList

def makeMA(pList, numMA):
    # Moving Average 계산
    mList = []
    p = pList[0]
    mSum = p * numMA
    Q = [p for _ in range(numMA)]
    for M in pList:
        mSum -= Q.pop(0)
        mSum += M
        mList.append(mSum/numMA)
        Q.append(M)

    return mList

def drawGraph(company, PN, pList, MA5, MA20, MA60):
    if company == 0:
        l = "samsung"
    elif company == 1:
        l = "lge"
    elif company == 2:
        l = "hyun_car"

    min = -PN * 20
    x = [i for i in range(min, 0)]
    plt.plot(x, pList, 'r', label = l)
    plt.plot(x, MA5, 'b', label = '5MA')
    plt.plot(x, MA20, 'g', label = '20MA')
    plt.plot(x, MA60, 'y', label = '60MA')
    plt.xlabel('Day')
    plt.ylabel('Price')
    plt.legend(loc = 'upper left')
    plt.grid(True)
    plt.show()


webUrl = ["https://finance.naver.com/item/frgn.nhn?code=005930&page=",
          "https://finance.naver.com/item/frgn.nhn?code=066570&page=",
          "https://finance.naver.com/item/frgn.nhn?code=005380&page="]  # 삼성, LG전자, 현대차 url

if __name__ == "__main__":
    company, PN = inputCompanyAndDays()
    pList = extractLastPrice(company, PN)
    pList.reverse()
    MA5 = makeMA(pList, 5)
    MA20 = makeMA(pList, 20)
    MA60 = makeMA(pList, 60)

    drawGraph(company, PN, pList, MA5, MA20, MA60)