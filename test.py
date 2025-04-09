import asyncio
from crawl4ai import *

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            # url="https://uanalyze.com.tw/articles/9506712981?fbclid=IwZXh0bgNhZW0CMTEAAR1kSIix2EMkDjcakVooyedUGyojZobpGzO9nJz0soaf-yFIZie5Hw2Olh8_aem_-Q_sYwYvQOqvuLp3GHY_MA",
            url = "https://uanalyze.com.tw/articles/6651112188?fbclid=IwZXh0bgNhZW0CMTEAAR3u49-1yV2KsacXvgVWOX075TVxneU8FSCa-vVx7LKxZaWC4eFDsWjmOWQ_aem_y-qYGvhjwvekiJWk1UqPLQ"
        )
        # print(result.markdown)
        print(result.cleaned_html)

if __name__ == "__main__":
    asyncio.run(main())