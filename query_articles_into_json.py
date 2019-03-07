from newspaper import Article, ArticleException
from newsapi import NewsApiClient
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
        print('Error: failed to get article from url: ' + old_article['url'])
    finally:
        return formatted_article


def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)


def search_articles(query_string):
    newsapi = NewsApiClient(api_key='391c4cadc42a4a42aaf1ea266df4adfc')

    top_headlines = newsapi.get_everything(
        q=query_string, language='en', sort_by='popularity', page_size=100)
    return top_headlines


def main():
    query_string = 'government shutdown'
    filename = 'shutdown'
    results_filename = filename + '-newsapi-results'
    articles_filename = filename + '-articles'

    start_time = time.time()
    search_results = search_articles(query_string)
    writeToJSONFile('newsapi-results', results_filename, search_results)
    end_time = time.time()
    newsapi_query_duration = (end_time - start_time)
    print(len(search_results['articles']), ' articles retrieved.')
    print('time to get query results: ' + str(newsapi_query_duration) + 's')

    articles = []
    start_time = time.time()
    articles = list(map(add_text_and_format, search_results['articles']))
    end_time = time.time()
    article_download_duration = (end_time - start_time)
    print(len(articles), ' successfully processed')
    print('time to download articles: ' + str(article_download_duration) + 's')

    writeToJSONFile('scraped-articles', articles_filename, articles)

    print('total results: ' + str(search_results['totalResults']))


main()