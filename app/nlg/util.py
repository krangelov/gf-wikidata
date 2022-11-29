from daison import *
from wordnet.semantics import *
from html import escape

def get_lex_fun(db, qid):
    with db.run("w") as t:
        for synset_id in t.cursor(synsets_qid, qid):
            for lexeme_id in t.cursor(lexemes_synset, synset_id):
                for lexeme in t.cursor(lexemes, lexeme_id):
                    return lexeme.lex_fun
    return None
