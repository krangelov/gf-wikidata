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
countries, cities, universities and professions.

For the NLG we don't need to write an application grammar. You can use
the RGL api and extended version of the GF language, which can access Wikidata directly. Look at 
[country.gf](country.gf), [city.gf](city.gf) and [person.gf](person.gf) for
examples.

There is also a web interface here:

https://cloud.grammaticalframework.org/wordnet/app/wikidata/

Try searching for countries and cities! The response may be slow since it takes time to fetch the data from Wikidata.
