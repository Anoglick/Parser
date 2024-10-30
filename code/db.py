import sqlite3

class ManagerDB:
    def create_tables(self, name):
        conn = sqlite3.connect(name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hubs (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                url TEXT NOT NULL UNIQUE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                date TEXT NOT NULL,
                url TEXT NOT NULL UNIQUE,
                authors_name TEXT NOT NULL,
                author_url TEXT NOT NULL,
                hub_id INTEGER,
                FOREIGN KEY (hub_id) REFERENCES hubs(id)
            )
        ''')

        conn.commit()
        conn.close()

    def save_articls_urls(self, urls):
        conn = sqlite3.connect("data/hub_articles.db")
        cursor = conn.cursor()

        for title, url in urls:
            print(f"Статья: {title} - {url}")
            cursor.execute("INSERT OR IGNORE INTO hubs (title, url) VALUES (?, ?)", (title, url,))
            print("Статья добавлена в базу данных\n")
        
        conn.commit()
        conn.close()

    def save_articles(self, title, url, data, id):
        conn = sqlite3.connect("data/hub_articles.db")
        cursor = conn.cursor()
        print(f"Информация о статье:\nНазвание: {title}\nДата: {data["dateTime"]}\nСсылка: {url}\nАвтор: {data["author"]}\nСсылка на автора: {data["authot_url"]}")
        cursor.execute(
            "INSERT OR IGNORE INTO articles (title, date, url, authors_name, author_url, hub_id) VALUES (?, ?, ?, ?, ?, ?)", 
            (title, data["dateTime"], url, data["author"], data["authot_url"], id,)
        )
        print("Информация добавлена\n")

        conn.commit()
        conn.close()

    def feach_data(self):
        conn = sqlite3.connect("data/hub_articles.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, url FROM hubs")
        articles = cursor.fetchall() 

        conn.close()
        return articles
    
Manager = ManagerDB()