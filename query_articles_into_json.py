from newspaper import Article, ArticleException
from newsapi.newsapi_client import NewsApiClient
import sys
import json
import time

import asyncio


def add_text_and_format(old_article):
    formatted_article = {}
    try:
        newspaper_article = Article(old_article['url'])
        newspaper_article.download()
        newspaper_article.parse()
        formatted_article = {
            'title': old_article['title'],
            'description': old_article['description'],
            'text': newspaper_article.text,
            'date': old_article['publishedAt'],
            'url': old_article['url']
        }
    except (ArticleException):
        print('Error: article skipped due to failure parsing: ' + old_article['url'])
    finally:
        return formatted_article


def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)


def search_articles(query_string, domain_blacklist_string, domain_whitelist_string):
    newsapi = NewsApiClient(api_key='391c4cadc42a4a42aaf1ea266df4adfc')

    headlines = newsapi.get_everything(
        q=query_string, 
        language='en', 
        sort_by='relevancy', 
        page_size=100,
        domains=domain_whitelist_string
        # exclude_domains=domain_blacklist_string
    )
    return headlines 

# convert this to whitelist of domains?
def get_whitelist():
    filepath = './sources/whitelist.json'
    whitelist = []
    with open(filepath) as json_file:
        data = json.load(json_file)
        whitelist = data["domains"]
    return ",".join(whitelist)

def main():
    domain_blacklist = 'castanet.net,calculatedriskblog.com'
    domain_whitelist = get_whitelist()

    query_string = 'Venezuela Crisis 2019'
    filename = 'venezuela'
    results_filename = filename + '-newsapi-results'
    articles_filename = filename + '-articles'

    start_time = time.time()
    search_results = search_articles(query_string, domain_blacklist, domain_whitelist)
    writeToJSONFile('newsapi-results', results_filename, search_results)
    end_time = time.time()
    newsapi_query_duration = (end_time - start_time)
    print(len(search_results['articles']), ' articles retrieved.')
    print('time to get query results: ' + str(newsapi_query_duration) + 's')

    articles = []
    start_time = time.time()
    articles = list(map(add_text_and_format, search_results['articles']))
    articles = list(filter(None, articles))
    end_time = time.time()
    article_download_duration = (end_time - start_time)
    print(len(articles), ' successfully processed')
    print('time to download articles: ' + str(article_download_duration) + 's')

    writeToJSONFile('scraped-articles', articles_filename, articles)

    print('total results: ' + str(search_results['totalResults']))
    print('len of articles: ', len(articles))


main()
# print(get_whitelist())