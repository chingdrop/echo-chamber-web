import logging
from bs4 import BeautifulSoup
from time import sleep
from urllib.parse import unquote
from celery import shared_task
from fake_useragent import UserAgent

from config.django.rest import RestAdapter
from .models import GoogleSearchConfig, GoogleSearchResult


class GoogleSearch:
    def __init__(self, proxy=None, logger=None):
        ua = UserAgent()
        headers = {
            "User-Agent": ua.chrome,
            "Accept": "*/*",
        }
        proxies = (
            {"https": proxy, "http": proxy}
            if proxy
            and (
                proxy.startswith("https")
                or proxy.startswith("http")
                or proxy.startswith("socks5")
            )
            else None
        )
        self.rest = RestAdapter(headers=headers, proxies=proxies, logger=logger)
        self.logger = logger or logging.getLogger(__name__)

    def _request(
        self, term: str, results: int, lang: str, start: int, safe: str, region: str
    ):
        params = {
            "q": term,
            "num": results + 2,
            "hl": lang,
            "start": start,
            "safe": safe,
            "gl": region,
        }
        cookies = {
            "CONSENT": "PENDING+987",
            "SOCS": "CAESHAgBEhIaAB",
        }
        return self.rest.get(
            "https://www.google.com/search", params=params, cookies=cookies, timeout=5
        )

    def _parse_results(self, response):
        soup = BeautifulSoup(response, "html.parser")
        result_block = soup.find_all("div", class_="ezO2md")
        for result in result_block:
            link_tag = result.find("a", href=True)
            title_tag = link_tag.find("span", class_="CVA68e") if link_tag else None
            description_tag = result.find("span", class_="FrIlee")

            if link_tag and title_tag and description_tag:
                link = unquote(link_tag["href"].split("&")[0].replace("/url?q=", ""))
                title = title_tag.text if title_tag else ""
                description = description_tag.text if description_tag else ""
                yield {"link": link, "title": title, "description": description}

    def search(self, term, results, safe, start, lang, region, unique=False):
        fetched_results = 0
        fetched_links = set()

        while fetched_results < results:
            response_text = self._request(term, results, safe, start, lang, region)
            if not response_text:
                break  # Stop the search if the request fails

            new_results = 0
            for search_result in self._parse_results(response_text):
                if search_result.link in fetched_links and unique:
                    continue  # Skip this result if the link is not unique

                fetched_links.add(search_result.link)
                fetched_results += 1
                new_results += 1
                yield search_result

                if fetched_results >= results:
                    return  # Stop if we have fetched the desired number of results

            if new_results == 0:
                logging.info(
                    f"Only {fetched_results} results found for query requiring {results} results."
                )
                break  # Break the loop if no new results were found in this iteration

            start += 10
            sleep(120)  # Avoid hitting Google's rate limits


@shared_task
def google_search_task(term, results, safe, start, lang, region, unique=False):
    goog = GoogleSearch()
    return list(goog.search(term, results, safe, start, lang, region, unique))

@shared_task
def process_search_results_task(results, config_id):
    config = GoogleSearchConfig.objects.get(id=config_id)
    for result in results:
        GoogleSearchResult.objects.create(
            config=config,
            link=result['link'],
            title=result['title'],
            description=result['description']
        )
    return {"status": "completed", "config_id": config_id}
