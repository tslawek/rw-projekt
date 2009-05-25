#ecoding=utf-8

import re
import corpus

def localesub(pattern, replacement, string):
    pattern = re.compile(pattern, re.LOCALE)
    return re.sub(pattern, replacement, string)

def test_strip_info():
    assert strip_info("[[link]]") == "[[link]]"
    assert strip_info("[[a:s]]") == ""
    assert strip_info("[[link]] [[a:s]]") == "[[link]] "
    assert strip_info("[[a:s]] [[link]]") == " [[link]]"

    assert strip_info("jeden [[link]]") == "jeden [[link]]"
    assert strip_info("jeden [[link]] dwa") == "jeden [[link]] dwa"
    assert strip_info("jeden [[link]] [[Kategoria:Polacy]] dwa") == "jeden [[link]]  dwa"
    assert strip_info("[[Plik:Pierogi frying.jpg|thumb|246px|Pierogi]]") == ""
    

def strip_info(text):
    return localesub(r"\[\[[^\[\]]+:[^\[\]]+\]\]", "", text)

def test_strip_links():
    assert strip_links("[[20]]") == "20"
    assert strip_links("[[1920|20]]") == "20"
    assert strip_links("[[Flaga Rzeczypospolitej Polskiej|Flaga Polski]]") == "Flaga Polski"
    assert strip_links("[[Łotysze|Łotyszów]]") == "Łotyszów"
    assert strip_links("jeden [[Flaga Rzeczypospolitej Polskiej|Flaga Polski]] dwa") == "jeden Flaga Polski dwa"

def strip_links(text):
    return localesub(r"\[\[(?:[^\[\]]*\|)?([^\[\]]*)\]\]", r"\1", text)

def test_strip_markup():
    assert strip_markup("'''asdf'''") == "asdf"
    assert strip_markup("* asdf") == "asdf"
    assert strip_markup("jeden {{ adsf \n asdf \n }} dwa") == "jeden  dwa"
    _in = """* Albin Janusz, ''"Polski ruch narodowy na Łotwie w latach 1919-40"'', [[Wrocław]] [[1993]], ISBN 83-229-0901-2"""
    out = """Albin Janusz, "Polski ruch narodowy na Łotwie w latach 1919-40", [[Wrocław]] [[1993]], ISBN 83-229-0901-2"""
    assert strip_markup(_in) == out

def strip_markup(text):
    text = re.sub(re.compile("{{[^}}]+}}", re.M), "", text)
    text = localesub("'''", "", text)
    text = localesub("''", "", text)
    text = localesub("=== (.+?) ===", r"\1", text)
    text = localesub("== (.+?) ==", r"\1", text)
    text = localesub("{{.+?}}", "", text)
    text = re.sub(re.compile("^\* ", re.M), "", text)
    return text

def test_strip_wiki_markup():
    print repr(strip_wiki_markup(corpus.gim))
    print repr(corpus.gim_stripped)
    assert strip_wiki_markup(corpus.gim) == corpus.gim_stripped

def strip_wiki_markup(text):
    text = strip_markup(text)
    text = strip_info(text)
    text = strip_links(text)
    return text

if __name__ == "__main__":
    print strip_wiki_markup(corpus.poland)
