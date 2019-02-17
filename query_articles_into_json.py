from newspaper import Article, ArticleException
from newsapi import NewsApiClient
import sys
import json
import time


def get_article(url):
    article = Article(url)
    article.download()
    article.parse()
    return article


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
    query_string = 'venezuela maduro'
    filename = 'venezuela'
    results_filename = filename + '-newsapi-results'
    articles_filename = filename + '-articles'

    start_time = time.time()
    search_results = search_articles(query_string)
    writeToJSONFile('newsapi-results', results_filename, search_results)
    end_time = time.time()
    newsapi_query_duration = (end_time - start_time)
    print('time to get query results: ' + str(newsapi_query_duration) + 's')

    urls = [result['url'] for result in search_results['articles']]

    articles = []

    start_time = time.time()
    for url in urls:
        try:
            article = get_article(url)
            articles.append({
                'url': article.url,
                'source': article.source_url,
                'title': article.title,
                'text': article.text
            })
        except (ArticleException):
            print('Error: failed to get article from url: ' + url)
    end_time = time.time()
    article_download_duration = (end_time - start_time)
    print('time to download articles: ' + str(article_download_duration) + 's')

    writeToJSONFile('scraped-articles', articles_filename, articles)

    print('total results: ' + str(search_results['totalResults']))


main()
