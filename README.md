# gf-wikidata
An experimental NLG system which uses GF WordNet to generate articles
about entities in Wikidata. 

The advantage of the approach is that
GF WordNet already provides a lexicon for >20 languages with an
abstract API of >100k words. Of those ~30k words are linked to their
Wikidata items. On top of this core lexicon, I added ~600k given
and family names plust ~4 million geographical names. This means
that the total lexicon contains close to 5 million lexical items.
These are the starting point to generating articles about people,
countries, capitals and cities.

For the NLG we don't need to write an application grammar. You can use
the RGL api and the lexicon directly from Python. Look at 
app/nlg/countries.py, app/nlg/capital.py and app/nlg/cities.py for
examples.

There is also a mock up web interface here:

https://cloud.grammaticalframework.org/wikidata/index.wsgi?id=Q6506&lang=en
