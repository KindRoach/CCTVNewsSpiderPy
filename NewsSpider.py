import bs4
import time
import requests

news_pages = list()

# next_uri = "http://mrxwlb.com/category/mrxwlb-text/"
next_uri = "http://mrxwlb.com/category/mrxwlb-text/page/50/"
while next_uri != "":
    res_str = requests.get(next_uri).content.decode("utf-8")
    soup = bs4.BeautifulSoup(res_str, "html.parser")
    for h1 in soup.find_all("h1", class_="entry-title"):
        news_pages.append(h1.a["href"])
    next_page_elemnts = soup.find_all("a", class_="next page-numbers")
    if len(next_page_elemnts) > 0:
        next_uri = next_page_elemnts[0]["href"]
    else:
        next_uri = ""
    print("{} news page uri collected!".format(len(news_pages)))

correct_num = 0
error_num = 0
erroUris = list()

for page in news_pages:
    try:
        res_str = requests.get(page).content.decode("utf-8")
        soup = bs4.BeautifulSoup(res_str, "html.parser")
        content = str()
        for p in soup.find_all("p"):
            content += '\r' + p.text
        correct_num += 1
        news_date = soup.find_all("time", class_="entry-date")[0].text
        with open(r"data/news/" + news_date + ".txt", 'w', encoding="utf-8") as out_f:
            out_f.write(content)
    except Exception as e:
        erroUris.append(page)
        error_num += 1
    finally:
        print("success/error/total:{}/{}/{}".format(correct_num, error_num, len(news_pages)))
