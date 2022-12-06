# gf-wikidata
An experimental NLG system which uses [GF WordNet](https://cloud.grammaticalframework.org/wordnet/) to generate articles
about entities in [Wikidata](https://www.wikidata.org). 

The advantage of the approach is that
GF WordNet already provides a lexicon for >20 languages with an
abstract API of >100k words. Of those ~30k words are linked to their
Wikidata items. On top of this core lexicon, I integrated ~600k given
and family names plust ~4 million geographical names from Wikidata. This means
that the total lexicon contains close to 5 million lexical items most of which
are linked with their corresponding Wikidata items.
These are the starting point to generating articles about people,
countries, capitals and cities.

For the NLG we don't need to write an application grammar. You can use
the RGL api and the lexicon directly from Python. Look at 
[nlg.country](app/nlg/country.py), [nlg.capital](app/nlg/capital.py) and [nlg.city](app/nlg/city.py) for
examples.

There is also a mock up web interface here:

https://cloud.grammaticalframework.org/wikidata/index.wsgi

Try searching for countries and cities! The response is currently slow since it takes time to fetch the data from Wikidata. This is something to be improved in the future.
