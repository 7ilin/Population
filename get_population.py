#-*- coding: utf-8 -*-

import urllib2
import bs4
import json
import io
import re

regions_url = "http://grandukraine.com/goroda-i-sela-ukrainyi/goroda-ukrainyi-po-oblastyam.html"
wiki_url = u"https://ru.wikipedia.org/wiki/"


def main():
    population = {}
    page = urllib2.urlopen(regions_url)
    soup = bs4.BeautifulSoup(page)

    content = soup.findAll("div", {"class": "entry-content"})[0]
    spans = content.findAll("span", {"style": "line-height: normal;"})
    for span in spans:
        regions = span.findAll("strong")
        if not regions:
            continue
        region = regions[0]
        region_name = region.text
        if region_name not in population:
            population[region_name] = {}
        for node in span.contents:
            if node in regions[1:]:
                region_name = node.text
                if region_name not in population:
                    population[region_name] = {}
                continue
            if isinstance(node, bs4.element.NavigableString) and node.strip():
                city_name = node.strip()
                if u'область' in city_name:
                    region_name = city_name
                    if region_name not in population:
                        population[region_name] = {}
                    continue
                peoples = get_peoples(city_name)
                population[region_name][city_name] = peoples

    with io.open('data.json', 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(population, ensure_ascii=False, sort_keys=True, indent=4)))


def get_peoples(city_name):
    try:
        page = urllib2.urlopen((wiki_url+city_name).encode('utf-8'))
        soup = bs4.BeautifulSoup(page)
        infobox = soup.findAll("table", {"class": "infobox vcard"})[0]
        table = infobox.findAll("table", {"cellspacing": "1"})[0]
        trs = table.findAll("tr")
        for tr in trs:
            tds = tr.findAll("td")
            if len(tds)>1 and tds[0].text.strip() == u'Страна':
                if u'Украина' not in tds[1].text.strip():
                    return 'unknown'
            if len(tds)>1 and tds[0].text.strip() == u'Население':
                mul = 1
                text = tds[1].text.strip()
                if u'тыс' in text:
                    mul = 10**3
                elif u'млн' in text:
                    mul = 10**6
                print text,
                str_peoples = text.split('[')[0].split('(')[0]
                list_str = re.findall(r'\d*\,*\d+', str_peoples)
                print '\t\t->', list_str,
                number_str = ''.join(list_str).replace(',', '.')
                peoples = int(float(number_str) * mul)
                print '\t\t->', peoples
                return peoples
    except:
        pass
    return 'unknown'


if __name__ == '__main__':
    main()
