import requests
import xmltodict


def disney_id(movie=None):
    if movie is None:
        return 'No movie selected.'
    sparql_query = f"""
            SELECT ?movie ?title ?disney_id WHERE
            {{  
              ?item wdt:P31/wdt:P279* wd:Q11424;
                    wdt:P1476 ?title;
                    wdt:P7595 ?disney_id.
            FILTER(contains(?title, '{movie}'))
              SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
        """
    url = 'https://query.wikidata.org/sparql'
    res = requests.get(url, params={'format': 'json,', 'query': sparql_query})
    xml_dict = xmltodict.parse(res.content)
    results = xml_dict['sparql']['results']
    for r in results['result']:
        for z in r['binding']:
            if z['@name'] == 'disney_id':
                temp_id = z['literal']
            if isinstance(z['literal'], dict):
                title = z['literal']['#text']
                if title == movie:
                    disney_plus_id = temp_id
                else:
                    pass
    return disney_plus_id


if __name__ == '__main__':
    print(disney_id('Toy Story 2'))