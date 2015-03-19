#encoding=utf-8
from os.path import abspath, dirname, join
import urllib2, re

PREFIX = join(dirname(abspath(__file__)))
HTTP = 'http://www.huxiu.com%s'
#remove HTML tags , eg: <a>, <span> ....
STRIP_TAG_PAT = re.compile(r'<.*?>')


def common_reptile(url, url_pat):
    content = urllib2.urlopen(url).read()
    #get article title
    urls_pat = re.compile(url_pat)
    site_Urls = re.findall(urls_pat, content)
    return site_Urls


#get per tag contains articles
def article(url):
    artilestring = ''
    count = 0

    site_Urls = common_reptile(HTTP % url, r'<h3>(.*?)</h3>')

    for i in site_Urls:
        count += 1
        i = re.sub(STRIP_TAG_PAT, '', i)
        artilestring = artilestring + '  ' + str(count) + '. ' + i + '\n'
    return artilestring


#get all tags
def tags():
    site_Urls = common_reptile(HTTP % '/tagslist/all.html', r'<li class="js-tag-w">(.*?)</a>')

    rfile = open(join(PREFIX, 'huxiu.txt'), 'a+')

    for u in site_Urls:
        articlestring = article(u.split('"')[1])
        u = re.sub(STRIP_TAG_PAT, '', u)
        rfile.write(u + '\n' + articlestring + '\n')
    rfile.close()

if __name__ == '__main__':
    tags()
