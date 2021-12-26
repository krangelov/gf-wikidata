# gf-wikidata
A repository for experiments in integration with the lexemes in wikidata

TODO List:

- [ ] Wikidata contains more languages than GF. For each lexeme Wikidata lists all inflection forms. For languages that exist in GF create a mapping of how the GF forms are represented in Wikidata. For languages that doesn't exist in GF, the information in Wikidata is enough to automatically create the Cat module and parts of Res and Paradigms. To this we should add Harald's numerals library. In this way, we will get ~200 resource grammars.
- [ ] Both Wikidata and GF WordNet contain mappings to WordNet. Use that to find a matching between the two resources.
- [ ] Develop a tool which can generate a grammar from Wikidata by using the resources created in the previous two bullets.
- [ ] GF WordNet contains information that does not exist in Wikidata. Identify it an donate it to Wikidata
- [ ] Update the grammar generator to use the new information from GF WordNet. If everything goes well the resulting grammar should be strictly a superset of GF WordNet with more languages and more lexica.

