from flask import Flask
from flask import render_template
import nltk
import math
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

url_hurriyet_array = []
url_milliyet_array = []
url_sabah_array = []
url_bbc_array = []
hurriyet_news = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
milliyet_news = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
sabah_news = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
bbc_news = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
hurriyet_summary = []
milliyet_summary = []
sabah_summary = []
bbc_summary = []
hurriyet_h1 = []
milliyet_h1 = []
sabah_h1 = []
bbc_h1 = []
last_hurriyet_url = []
last_hurriyet_news = []
last_milliyet_url = []
last_milliyet_news = []
last_sabah_url = []
last_sabah_news = []
last_bbc_url = []
last_bbc_news = []
new_summary = []
taking_sent = []
last_bbc_summary = [" "," "," "," "," "," "," "," "," "," "," "]

def fetchTurkeyData():
    url = "https://covid19bilgi.saglik.gov.tr/tr/haberler/turkiye-deki-gunluk-covid-19-vaka-sayilari.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    datas = [span.text for span in soup.findAll("span", {"class": "_VWvqNvR9 _ _VWvqNvR9"})]

    new_datas = []
    for i in range(0, len(datas), 7):
        new_datas.append(datas[i:i+7])

    daily_datas = []
    for data in new_datas:
        daily_datas.append(data)

    all_datas = []
    for i in range(0, len(daily_datas)):
        for j in range(0, 7):
            all_datas.append(daily_datas[i][j])

    index = 0
    index2 = 0
    for i in all_datas:
        if i == "1 Temmuz 2020":
            index = all_datas.index(i)
        if i == "29 Temmuz 2020":
            index2 = all_datas.index(i)
        else:
            continue

    all_datas_array = all_datas[index:index2]
    covid_datas = []
    for i in range(0, len(all_datas[index:index2]), 7):
        covid_datas.append(all_datas_array[i:i+7])

    return covid_datas[:len(covid_datas)-1]

def fetchTurkeyDataDetail():
    url = "https://covid19bilgi.saglik.gov.tr/tr/haberler/turkiye-deki-gunluk-covid-19-vaka-sayilari.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    datas = [span.text for span in soup.findAll("span", {"class": "_VWvqNvR9 _ _VWvqNvR9"})]

    new_datas = []
    for i in range(0, len(datas), 7):
        new_datas.append(datas[i:i+7])

    daily_datas = []
    for data in new_datas:
        daily_datas.append(data)

    all_datas = []
    for i in range(0, len(daily_datas)):
        for j in range(0, 7):
            all_datas.append(daily_datas[i][j])

    index = 0
    for i in all_datas:
        if i == "29 Temmuz 2020":
            index = all_datas.index(i)
        else:
            continue

    all_datas_array = all_datas[index:]
    covid_detail_datas = []
    for i in range(0, len(all_datas[index:]), 7):
        covid_detail_datas.append(all_datas_array[i:i+7])

    return covid_detail_datas


def fetchTurkeyTodayData():
    url = "https://covid19bilgi.saglik.gov.tr/tr/haberler/turkiye-deki-gunluk-covid-19-vaka-sayilari.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    datas = [span.text for span in soup.findAll("span", {"class": "_VWvqNvR9 _ _VWvqNvR9"})]

    new_datas = []
    for i in range(0, len(datas), 7):
        new_datas.append(datas[i:i+7])

    daily_datas = []
    for data in new_datas:
        daily_datas.append(data)

    covid_datas = daily_datas[1:]
    today_covid_data = len(covid_datas) - 1

    return covid_datas[today_covid_data]


def fetchWorldData():
    country_datas = []
    url = "https://news.google.com/covid19/map?hl=tr&gl=TR&ceid=TR:tr"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    country_names = [span.text for span in soup.findAll("th", {"class": "l3HOY"})]
    datas = [span.text for span in soup.findAll("td", {"class": "l3HOY"})]
    flags = [span.text for span in soup.findAll("img", {"class": "oIC36d"})]

    for i in range(0, len(datas), 5):
        country_datas.append(datas[i:i + 5])

    for i in range(0, len(country_names)):
        country_datas[i].insert(0, country_names[i])

    return country_datas


def fetchWorldTodayData():
    world_covid_datas = []
    url = "https://news.google.com/covid19/map?hl=tr&gl=TR&ceid=TR:tr"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    datas = [span.text for span in soup.findAll("div", {"class": "UvMayb"})]

    for data in datas:
        world_covid_datas.append(data)

    return world_covid_datas


def getHurriyetURL():
    url = "https://www.hurriyet.com.tr/haberleri/covid-19"
    web_site = "https://www.hurriyet.com.tr/"

    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    divs = soup.findAll("div", {"class": "desc"})
    for div in divs:
        sub_url = div.find('a')['href']
        try:
            if sub_url[0:4] != 'http':
                new_url = web_site + sub_url
                url_hurriyet_array.append(new_url)
            elif 'galeri' in sub_url:
                continue
        except:
            continue


def getHurriyetNews(new_url_array):
    i = -1
    for url in new_url_array:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        div_h1 = soup.findAll("div", {"class": "col-md-10 col-md-offset-1"})
        div_h2 = soup.findAll("h2", {"class": "rhd-article-spot"})
        div_p = soup.findAll("div", {"class": "rhd-all-article-detail"})

        i = i + 1

        if len(div_h1) == 0:
            new_url_array[i] = " "
        else:
            for h1 in div_h1:
                hurriyet_h1.append(h1.text)
                hurriyet_news.insert(i, hurriyet_news[i] + h1.text + ". ")
                hurriyet_news.pop(i + 1)
            for h2 in div_h2:
                hurriyet_news.insert(i, hurriyet_news[i] + h2.text + " ")
                hurriyet_news.pop(i + 1)
            for p in div_p:
                hurriyet_news.insert(i, hurriyet_news[i] + p.text)
                hurriyet_news.pop(i + 1)


def getMilliyetURL():
    url= "https://www.milliyet.com.tr/haberler/covid-19"
    web_site = "https://www.milliyet.com.tr"

    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    divs = soup.findAll("div", {"class": "news__item col-md-12 col-sm-6"})
    for div in divs:
        sub_url = div.find('a')['href']
        try:
            if sub_url[0:4] != 'http':
                new_url = web_site + sub_url
                url_milliyet_array.append(new_url)
            elif 'galeri' in sub_url:
                continue
        except:
            continue


def getMilliyetNews(new_url_array):
    i = -1
    for url in new_url_array:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        div_h1 = soup.findAll("h1", {"class": "nd-article__title"})
        div_h2 = soup.findAll("h2", {"class": "nd-article__spot"})
        div_p = soup.findAll("div", {"class": "nd-article__content"})

        i = i + 1
        if len(div_h1) == 0:
            new_url_array[i] = " "
        else:
            for h1 in div_h1:
                milliyet_h1.append(h1.text)
                milliyet_news.insert(i, milliyet_news[i] + h1.text + ". ")
                milliyet_news.pop(i + 1)
            for h2 in div_h2:
                if h2.text == " ":
                    milliyet_h1.pop()
                else:
                    milliyet_news.insert(i, milliyet_news[i] + h2.text + " ")
                    milliyet_news.pop(i + 1)
            for p in div_p:
                milliyet_news.insert(i, milliyet_news[i] + p.text)
                milliyet_news.pop(i + 1)


def getSabahURL():
    url = "https://www.sabah.com.tr/arama?query=covid19"
    web_site = "https://www.sabah.com.tr"

    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    divs = soup.findAll("div", {"class": "col-lg-4 col-md-6 col-sm-6 view20"})
    for div in divs:
        sub_url = div.find('a')['href']
        try:
            if sub_url[0:4] != 'http':
                new_url = web_site + sub_url
                url_sabah_array.append(new_url)
            elif 'galeri' in sub_url:
                continue
        except:
            continue


def getSabahNews(new_url_array):
    i = -1
    for url in new_url_array:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        div_h1 = soup.findAll("h1", {"class": "pageTitle"})
        div_p = soup.findAll("div", {"class": "newsDetailText"})

        i = i + 1
        if len(div_h1) == 0:
            new_url_array[i] = " "
        else:
            for h1 in div_h1:
                sabah_h1.append(h1.text)
                sabah_news.insert(i, sabah_news[i] + h1.text + ". ")
                sabah_news.pop(i + 1)
            for p in div_p:
                sabah_news.insert(i, sabah_news[i] + p.text.strip())
                sabah_news.pop(i + 1)


def getBBCURL():
    url = "https://www.bbc.com/news/coronavirus"
    web_site = "https://www.bbc.com/"

    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    divs = soup.findAll("div", {"class": "gel-layout__item gel-1/3@m gel-1/4@l gel-1/5@xxl nw-o-keyline nw-o-no-keyline@m"})
    for div in divs:
        sub_url = div.find('a')['href']
        try:
            if sub_url[0:4] != 'http':
                new_url = web_site + sub_url
                url_bbc_array.append(new_url)
            elif 'galeri' in sub_url:
                continue
        except:
            continue


def getBBCNews(new_url_array):
    i = -1
    for url in new_url_array:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        div_h1 = soup.findAll("h1", {"class": "story-body__h1"})

        i = i + 1
        if len(div_h1) == 0:
            new_url_array[i] = " "
        else:
            for h1 in div_h1:
                bbc_h1.append(h1.text)


def getBBCNewsDetail(new_url_array):
    i = -1
    for url in new_url_array:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        div_h1 = soup.findAll("h1", {"class": "story-body__h1"})
        div_p  = soup.findAll("div", {"class": "story-body__inner"})[0].findAll('p')

        i = i + 1
        if len(div_h1) == 0:
            new_url_array[i] = " "
        else:
            for h1 in div_h1:
                last_bbc_news.insert(i, last_bbc_news[i] + h1.text)
                last_bbc_news.pop(i + 1)
            for p in div_p:
                last_bbc_news.insert(i, last_bbc_news[i] + p.text.strip())
                last_bbc_news.pop(i + 1)


def getSummary(text):
    countWords = {}
    countSentences = {}
    repetition = []
    summary = ""

    words = text.split(" ")
    sentences = text.split(".")

    # Kelimelerin toplamda kaç tane geçtiğini sayıyor. Her kelimeye tekrarına göre puan veriyor.
    # It counts how many same words have passed in total. It gives points to each word according to its repetition.
    for word in words:
        if countWords.get(word) is not None:
            countWords[word] += 1
        else:
            countWords[word] = 1

    # 2 den fazla geçen kelimeleri alıyor. Testlerde 2 en doğru sonucu verdi, değişebilir.
    # It takes more than 2 passing words. In the tests, 2 gave the most accurate result, it may vary.
    for word in countWords:
        if countWords.get(word) > 2:
            repetition.append(word)

    # Kelimelerin puanları ile cümleleri puanlandırıyor. Cümlelerin puanlarını elde ediyor.
    # Scoring sentences with the scores of words. Obtains the scores of sentences.
    for sentence in sentences:
        for word in repetition:
            if sentence.find(word) > -1:
                if countSentences.get(sentences.index(sentence)) is not None:
                    countSentences[sentences.index(sentence)] += 1
                else:
                    countSentences[sentences.index(sentence)] = 1

    # Puanı belirli sayıdan fazla olan cümleleri yazıyor.
    # It writes sentences that have scores with more than a certain number.
    for a in countSentences:  # Bu kısım yani Özetleme Düzeyi Metin Boyutu ve İçeriğine göre değiştirilecek.
        if countSentences[a] > 3:  # This section will be changed according to the Summarization Level Text Size and Content.
            summary += sentences[int(a)]
    return summary


def getEnglishSummary(data):
    # print data
    a = []
    sent = []
    splitingSent = []
    for i in range(len(data) - 1):
        if (data[i] == '.' or data[i] == '?' or data[i] == '!') and data[i + 1].isupper():
            a.append(data[i])
            splitingSent.append(''.join(a).split())
            sent.append(''.join(a))
            a = []
        else:
            if data[i] != ',' and data[i] != ';' and data[i] != '\n' and data[i] != '\r':
                a.append(data[i])
            if i + 1 == len(data) - 1:
                a.append(data[i + 1])
                splitingSent.append(''.join(a).split())
                sent.append(''.join(a))

    words = nltk.word_tokenize(data)
    pos = nltk.pos_tag(words)
    nouns = []
    for i in range(len(pos)):
        if pos[i][1] == 'NN' or pos[i][1] == 'NNP' or pos[i][1] == 'NNS' or pos[i][1] == 'NNPS':
            nouns.append(pos[i][0])
    # print(nouns)
    LengthOfPara = len(sent)
    NoOfNoun = len(nouns)

    for i in range(LengthOfPara):
        for j in range(len(splitingSent[i])):
            if splitingSent[i][j] == 'He' or splitingSent[i][j] == 'he':
                splitingSent[i][j] = 'Rooney'

    EachSent = []
    for i in range(LengthOfPara):
        save = []
        for j in nouns:
            if j in splitingSent[i]:
                save.append(j)
        EachSent.append(save)

    dis = []
    for i in range(LengthOfPara):
        el = len(EachSent[i])
        if el > 1:
            # print el, EachSent[i]
            for j in range(el):
                for k in range(j + 1, el):
                    pot = []
                    p = nouns.index(EachSent[i][j])
                    pot.append(p)
                    q = nouns.index(EachSent[i][k])
                    pot.append(q)
                    d = abs(splitingSent[i].index(EachSent[i][j]) - splitingSent[i].index(EachSent[i][k]))
                    pot.append(d)
                    dis.append(pot)

    Rel = []
    for i in range(NoOfNoun):
        sm = 0
        for j in range(len(dis)):
            if dis[j][0] == i or dis[j][1] == i:
                sm += dis[j][2]
        # keepRel=[]
        # keepRel.append(i)
        # keepRel.append(sum)
        Rel.append(sm)

    scoreOfEachSent = []
    for i in range(LengthOfPara):
        el = len(EachSent[i])
        total = 0
        if el > 1:
            for j in range(el):
                index = nouns.index(EachSent[i][j])
                total += Rel[index]
            keepSent = []
            keepSent.append(i)
            keepSent.append(total)
            # print keepSent
            scoreOfEachSent.append(keepSent)
    afterSort = []
    l = len(scoreOfEachSent)
    for i in range(l):
        afterSort.append((scoreOfEachSent[i][0], scoreOfEachSent[i][1]))

    afterSort.sort(key=lambda x: x[1])
    afterSort.reverse()
    takingSent = []

    takingWhichSent = math.ceil(LengthOfPara / 3)
    for i in range(len(afterSort)):
        if i < takingWhichSent:
            takingSent.append(afterSort[i][0])
    takingSent.sort()

    taking_sent.append(len(takingSent))
    for i in takingSent:
        new_summary.append(sent[i])


@app.route('/home.html')
def home():
    covid_datas = fetchTurkeyData()
    covid_detail_datas = fetchTurkeyDataDetail()
    today_datas = fetchTurkeyTodayData()

    return render_template("home.html", covid_datas=covid_datas, today_datas=today_datas, covid_detail_datas=covid_detail_datas)


@app.route('/hurriyet.html')
def hurriyet():
    getHurriyetURL()
    hurriyet_urls = url_hurriyet_array[:20]
    getHurriyetNews(hurriyet_urls)

    for hurriyet_url in hurriyet_urls:
        if hurriyet_url != " ":
            last_hurriyet_url.append(hurriyet_url)
        else:
            continue

    for hurriyet_new in hurriyet_news:
        if hurriyet_new != " ":
            last_hurriyet_news.append(hurriyet_new)
        else:
            continue

    for i in last_hurriyet_news:
        hurriyet_summary.append(getSummary(i))

    length = len(last_hurriyet_url)

    return render_template("hurriyet.html", last_hurriyet_url=last_hurriyet_url, hurriyet_h1=hurriyet_h1, last_hurriyet_news=last_hurriyet_news, hurriyet_summary=hurriyet_summary, length=length)


@app.route('/milliyet.html')
def milliyet():
    getMilliyetURL()
    milliyet_urls = url_milliyet_array[:20]
    getMilliyetNews(milliyet_urls)

    for milliyet_url in milliyet_urls:
        if milliyet_url != " ":
            last_milliyet_url.append(milliyet_url)
        else:
            continue

    for milliyet_new in milliyet_news:
        if milliyet_new != " ":
            last_milliyet_news.append(milliyet_new)
        else:
            continue

    for i in last_milliyet_news:
        milliyet_summary.append(getSummary(i))

    length = len(last_milliyet_url)

    return render_template("milliyet.html", last_milliyet_url=last_milliyet_url, milliyet_h1=milliyet_h1, last_milliyet_news=last_milliyet_news, milliyet_summary=milliyet_summary, length=length)


@app.route('/sabah.html')
def sabah():
    getSabahURL()
    sabah_urls = url_sabah_array[:20]
    getSabahNews(sabah_urls)

    for sabah_url in sabah_urls:
        if sabah_url != " ":
            last_sabah_url.append(sabah_url)
        else:
            continue

    for sabah_new in sabah_news:
        if sabah_new != " ":
            last_sabah_news.append(sabah_new)
        else:
            continue

    for i in last_sabah_news:
        sabah_summary.append(getSummary(i))

    length = len(last_sabah_url)

    return render_template("sabah.html", last_sabah_url=last_sabah_url, sabah_h1=sabah_h1, last_sabah_news=last_sabah_news, sabah_summary=sabah_summary, length=length)


@app.route('/bbc.html')
def bbc():
    sent_length = []
    world_covid_datas = fetchWorldTodayData()
    country_datas = fetchWorldData()
    for country_data in country_datas:
        country_data.pop(2)

    getBBCURL()
    bbc_urls = url_bbc_array[:15]
    getBBCNews(bbc_urls)

    for bbc_url in bbc_urls:
        if bbc_url != " ":
            last_bbc_url.append(bbc_url)
        else:
            continue

    for i in range(0, len(last_bbc_url)):
        last_bbc_news.append(" ")

    getBBCNewsDetail(last_bbc_url)

    for i in last_bbc_news:
        getEnglishSummary(i)

    for sents in taking_sent:
        sent_length.append(sents)

    j = 0
    for i in sent_length:
        bbc_summary.append(new_summary[j:j + i])
        j = j + i

    counter = 0
    for array in bbc_summary:
        for i in array:
            last_bbc_summary.insert(counter, last_bbc_summary[counter] + i)
            last_bbc_summary.pop(counter + 1)
        counter = counter + 1

    length = len(last_bbc_url)

    return render_template("bbc.html", world_covid_datas=world_covid_datas, country_datas=country_datas, last_bbc_url=last_bbc_url, bbc_h1=bbc_h1, last_bbc_news=last_bbc_news, last_bbc_summary=last_bbc_summary, length=length)


if __name__ == '__main__':
    app.run(debug=True)



