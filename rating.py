import re
import mechanize
from BeautifulSoup import BeautifulSoup
import sys

def stripRight(string, char):
    if string[-1] == char:
        return string[:-1]
    return string
def urlFormat(string):
    if string[0] != '/':
        return '/'+string
    return string

br = mechanize.Browser()
br.set_handle_robots(False)

def printRating(soup):
    rating = soup.findAll('div',{'class':'titlePageSprite star-box-giga-star'})
    if not rating:
        print '\tRating: ' + 'None'
    else:
        print '\tRating: ' + rating[0].contents[0]

def parseEpisode(relLink):
    rep = br.open('http://www.imdb.com'+ relLink)
    soup4 = BeautifulSoup(rep.read())
    printRating(soup4)

def parseSeason(relLink):
    response = br.open('http://www.imdb.com'+ relLink)
    soupSeason = BeautifulSoup(response.read())
    noOfEpisodes = soupSeason.findAll('meta',{'itemprop':'numberofEpisodes'})[0]
    print '\nSeason\nNo of Episodes :' + noOfEpisodes['content']
    episodes = soupSeason.findAll('a',{'itemprop':'name'})
    for epi in episodes:
       print '\t Title: '+ epi['title']
       parseEpisode(epi['href'])
item =''
for each in  sys.argv[1:]:
    if not item:
        item = each
    else:
        item = item +'+'+ each
br.open("http://www.imdb.com/find?q=%s&s=all"%item)
#print 'Title:' + br.title()

searchUrl = ''
for link in br.links():
    if not 'title' in link.url or not 'fn_al_tt_1' in link.url:
        continue
    searchUrl = link
    break

response = br.follow_link(searchUrl)
soupmain = BeautifulSoup(response.read())
print 'Name : ' + soupmain.findAll('span',{'class':'itemprop','itemprop':'name'}) [0].contents[0]
print 'Genre: ' + soupmain.findAll('span',{'class':'itemprop','itemprop':'genre'})[0].contents[0]

printRating(soupmain)
seasons = soupmain.findAll('a',{'href':re.compile(r"season")})
for season in  seasons:
   parseSeason(season['href'])
                                                                                                                      
