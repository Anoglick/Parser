from datetime import datetime

from bs4 import BeautifulSoup
import aiohttp, asyncio

from db import Manager

async def fetch(session, url, headers):
    async with session.get(url, headers=headers) as response:
        return await response.text()

async def articles_parser(url, headers):
        async with aiohttp.ClientSession() as session:
            response = await fetch(session, url, headers)
            soup = BeautifulSoup(response, "lxml")
            urls = []

            articles = soup.find(class_='tm-articles-list').find_all(class_="tm-articles-list__item")
            for article in articles:
                title = article.find(class_="tm-title__link").text
                url_of_the_article = url + article.find(class_="tm-title__link").get("href").split("/")[-2]
                urls.append((title, url_of_the_article))

                await asyncio.sleep(0.2) 

            return urls

async def article_data_parser(session, url, headers):
    response = await fetch(session, url, headers)
    soup = BeautifulSoup(response, "lxml")
    
    time_element = soup.find("span", class_="tm-article-datetime-published") if soup.find("span", class_="tm-article-datetime-published") else None
    author = soup.find("span", class_="tm-user-info__user tm-user-info__user_appearance-default")
    authors_name = author.find("a", class_="tm-user-info__username").text
    author_url = "https://habr.com" + author.find("a").get("href")
    
    if time_element:
        date = time_element.find("time")["datetime"]
        time_element = datetime.fromisoformat(date.replace("Z", "+00:00"))
    
    return {"dateTime": time_element.isoformat(), "author": authors_name, "authot_url": author_url}

async def start():
    url = "https://habr.com/ru/articles/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0"
        }

    Manager.create_tables("data/hub_articles.db")
    urls = await articles_parser(url, headers)
    Manager.save_articls_urls(urls)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for id, title, link in Manager.feach_data():
            tasks.append(article_data_parser(session, link, headers))
        results = await asyncio.gather(*tasks)

        for i, (id, title, link) in enumerate(Manager.feach_data()):
            Manager.save_articles(title, link, results[i], id)

async def main():
    while True:
        await start()
        await asyncio.sleep(600)

if __name__ == "__main__":
    asyncio.run(main())