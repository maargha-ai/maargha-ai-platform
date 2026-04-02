import feedparser

SOURCES = [
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
]


def scrape_tech_news():
    results = []

    for url in SOURCES:
        try:
            feed = feedparser.parse(url)

            for entry in feed.entries[:5]:
                results.append(
                    {
                        "title": entry.title,
                        "link": entry.link,
                        "source": feed.feed.get("title", "Tech News"),
                    }
                )

        except Exception as e:
            print("[TECH NEWS ERROR]", e)

    return results
