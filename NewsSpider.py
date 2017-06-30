import bs4
import requests

news_pages = list()
timeout_set = 2

next_uri = "http://mrxwlb.com/category/mrxwlb-text/"
while next_uri != "":
    try:
        res_str = requests.get(
            next_uri, timeout=timeout_set).content.decode("utf-8")
        soup = bs4.BeautifulSoup(res_str, "html.parser")
        for h1 in soup.find_all("h1", class_="entry-title"):
            news_pages.append(h1.a["href"])
        next_page_elemnts = soup.find_all("a", class_="next page-numbers")
        if len(next_page_elemnts) > 0:
            next_uri = next_page_elemnts[0]["href"]
        else:
            next_uri = ""
        print("{} news page uri collected!".format(len(news_pages)))
    except Exception as e:
        print("Retry.")
        continue

finish_num = 0
total_num = len(news_pages)
news_pages.append("")
news_pages = (page for page in news_pages)
next_uri = next(news_pages)

while next_uri != "":
    try:
        res_str = requests.get(next_uri, timeout=timeout_set).content.decode("utf-8")
        soup = bs4.BeautifulSoup(res_str, "html.parser")
        content = str()

        for p in soup.find_all("p"):
            if len(p.find_all("strong")) > 0:
                content += "\r\n\r\n"
            else:
                content += p.text
        finish_num += 1
        news_date = soup.find_all("h1", class_="entry-title")[0].text
        news_date = news_date[news_date.find("2"):news_date.find("日") + 1]
        with open(r"data/news/" + news_date + ".txt", 'w', encoding="utf-8") as out_f:
            out_f.write(content)
        next_uri = next(news_pages)
        print("{}/{} news done!".format(finish_num, total_num))
    except Exception as e:
        print("Retry.")
        continue
