
import urllib.request as request
import urllib.error as error 
import urllib.parse as parse
from pprint import pprint
import json
import numpy as np
import time
import os
from bs4 import BeautifulSoup
import socket


class Crawler(object):
    def __init__(self, url, apikey, from_date, end_date, page_size, num_per_section):
        self.url = url 
        self.apiKey = apikey
        self.from_date = from_date 
        self.end_date = end_date
        self.page_size = page_size
        self.numPerSection = num_per_section
        self.sections = [
            'environment',
            'sport',
            'politics',
            'business',
            'technology',
            'science',
            'film',
            'books',
            'music',
            'lifeandstyle',
        ]

    def start(self, pages=1000, order="oldest"):
        articles = []
        ids = {}

        article_id = -1
        for section in self.sections:
            count = 0
            nextSection = False
            for page in np.arange(1, self.numPerSection//self.page_size+10):
                url = self.url

                data = {}
                data['api-key'] = self.apiKey
                data['from-date'] = self.from_date
                data['to-date'] = self.end_date
                data['page-size'] = self.page_size 
                data['order-by'] = order
                data['page'] = page
                data['section'] = section
                url_values = parse.urlencode(data)

                # add api key
                url = url + "?" + url_values
                print("Current Section: ", section, "Current Page: ", page, "Current article number: ", len(articles))
                try:
                    with request.urlopen(url) as response:
                        content = response.read()
                        content = content.decode('utf-8')
                        content = json.loads(content)
                        pagenum = content['response']['currentPage']
                        results = content['response']['results']

                        for each in results:
                            id_ = each['id']
                            if id_ in ids:
                                continue
                            else:
                                article_id += 1
                            sectionid = each['sectionId']
                            weburl = each['webUrl']
                            date = each['webPublicationDate']
                            title = each['webTitle']
                            articles.append({
                                'sectionId': sectionid,
                                'articleId': article_id,
                                'date': date,
                                'title': title,
                                'weburl': weburl,
                                'origid': id_
                            })
                            count += 1
                            if count >= self.numPerSection:
                                nextSection = True
                                break
                except error.HTTPError as e:
                    continue
                time.sleep(1)
                if nextSection:
                    nextSection = False 
                    break

        print("number of articles: ", len(articles))
    
        with open('guadianMetaData.jsonl', 'w') as f:
            for each in articles:
                json.dump(each, f)
                f.write('\n')
        
    def filter(self, path):
        filtered_articles = []
        with open(path, 'r') as f:
            for line in f:
                article = json.loads(line)
                if article['section'] is None:
                    continue
                else:
                    filtered_articles.append(article)
        
        print(len(filtered_articles))
        with open('guardian_filtered.jsonl', 'w') as f:
            for each in filtered_articles:
                json.dump(each, f)
                f.write('\n')
        
    def start_crawling(self, metapath, start_id=-1):
        if not os.path.exists('guardian2'):
            os.makedirs('guardian2')
        sectionDic = dict()
        
        with open(metapath, 'r') as f:
            for line in f:
                meta = json.loads(line)
                url = meta['weburl']
                id_ = meta['articleId']
                
                #***************
                
                section = meta['sectionId']
                if section not in sectionDic:
                    sectionDic[section] = 0
                sectionDic[section] +=1
                
                if sectionDic[section] > 50: #limiting how mnay documents per class
                    continue
                print(str(sectionDic[section]) + ' '+ section)
                #***************
                
                # print(url)
                print("article id: ", id_, flush=True)
                if id_ < start_id:
                    continue
                try:
                    req = request.Request(
                        url, 
                        data=None, 
                        headers={
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                        }
                    )
                    with request.urlopen(req) as response:
                        content = response.read()
                        content = content.decode('utf-8')
                        soup = BeautifulSoup(content, 'lxml')
                        target = soup.find_all("div", class_="content__article-body from-content-api js-article__body")
                        target2 = soup.find_all('meta', itemprop="description")
                        if len(target2) > 0:
                            description = target2[0]['content']
                        else:
                            description = ""

                        if len(target) == 0:
                            print("No content found!", flush=True)
                            continue
                        paragraphs = target[0].find_all("p")
                        clean_paragraph = []
                        for each in paragraphs:
                            clean_paragraph.append(each.text)
                        clean_paragraph.insert(0, description)
                        text = '\n\n'.join(clean_paragraph)
                        with open(os.path.join('guardian2', str(id_))+'_'+ section , 'w') as f1:
                            f1.write(text)
                        time.sleep(np.random.randint(1, 6))
                except error.HTTPError as e:
                    print(e)
                    continue
                except error.URLError as e:
                    print(e)
                    continue
                except socket.gaierror as e:
                    print(e)
                    continue


if __name__ == '__main__':
    crawler = Crawler(
        url = "http://content.guardianapis.com/search",
        apikey='39d76b5d-b396-4bdc-ad41-8fa6f3c70df2',
        from_date='2016-01-01',
        end_date='2018-01-01',
        page_size=200, 
        num_per_section=10000
    )

    # crawler.start(order="oldest")
    # crawler.filter('newyorktimes.jsonl')
    crawler.start_crawling('guadianMetaData.jsonl', start_id=22597)
