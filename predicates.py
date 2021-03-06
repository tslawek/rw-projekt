#encoding=utf-8

from clp.wrapper import *


def test_clp():
	w = Wrapper("clp/lib/libclp.so")
	assert "zamku" in w.all_forms("zamek")



"""
    n słów wczesniej [ słowo ]  n słów dalej
    od    początek, koniec zdania, do
    warunki co do gramatyki (clp)
    negacja warunków

    kazdy warunek (predykat) musi czegoś dotyczyć (miejsca)
    
        porównać do konkretnego stringa,
        należy do zbioru z clp
    
        słowo w dowolnej odmianie, albo konkretny przypadek.
"""

# Combinable ###########################################
class Combinable(object):
    def __or__(self, other):
        return self.or_(self, other)
    def __and__(self, other):
        return self.and_(self, other)
    def __invert__(self):
        return self.not_(self)
    @classmethod
    def _set_operators(cls, and_, or_, not_):
        cls.and_ = and_
        cls.or_ = or_
        cls.not_ = not_
def Combine(relation):
    class Combined(Combinable):
        def __init__(self, a, b):
            self.a, self.b = a, b
            type_a = type(a) if not isinstance(a, Combined) else a._type
            type_b = type(b) if not isinstance(b, Combined) else b._type
            assert type_a is type_b
            self._type = type_a
        def match(self, *args):
            return relation(self.a.match(*args), (self.b.match(*args)))
    return Combined
class Not(Combinable):
    def __init__(self, pred):
        self.pred = pred
    def match(self, *args):
        return not self.pred.match(*args)
Or = Combine(lambda a, b: a or b)
And = Combine(lambda a, b: a and b)
Combinable._set_operators(And, Or, Not)


# SinglePredicates ###########################################
class SinglePredicate(Combinable): pass
class WordAnyForm(SinglePredicate):
    def __init__(self, target):
	self.target = target
        self.w = Wrapper("clp/lib/libclp.so")
    def match(self, word):
        return word in self.w.all_forms(self.target)
class FormCheck(SinglePredicate):
    def __init__(self, form_prefix):
        self.form_prefix = form_prefix
        self.w = Wrapper("clp/lib/libclp.so")
    def match(self, word):

        clp_list = self.w.rec(word)
        if len(clp_list) > 0:
            for id in clp_list:
	        if self.w.label(id)[0] in self.form_prefix:
		    return True
	return False

class StartingWith(SinglePredicate):
    def __init__(self, prefix):
        self.prefix = prefix
    def match(self, word):
        return word.startswith(self.prefix)
class Capitalized(SinglePredicate):
    def match(self, word):
        return word and word[0].isupper()
class ExactWord(SinglePredicate):
    def __init__(self, word):
        self.word = word
    def match(self, word):
        return self.word == word
CAPITALIZED = Capitalized()
def test_single_predicate():

    assert ExactWord("ala").match("ala")
    assert not ExactWord("ala").match("dala")
    assert StartingWith("pre").match("predefiniowac")
    assert not StartingWith("pre").match("alicja")

    assert (ExactWord("ala") & ExactWord("ala")).match("ala")
    assert not (ExactWord("ala") & ExactWord("ola")).match("ala")
    assert (ExactWord("ala") | ExactWord("ola")).match("ala")
    assert (ExactWord("ala") | ExactWord("ola")).match("ola")
    assert WordAnyForm("zamek").match("zamku")
    assert FormCheck("A").match("dom")

class MultiPredicate(Combinable): pass
class Verbatim(MultiPredicate):
    def __init__(self, target):
        self.target = target
    def match(self, words):
        return self.target in " ".join(words)
class AnyWord(MultiPredicate):
    def __init__(self, pred):
        self.pred = pred
    def match(self, words):
        return any(self.pred.match(word) for word in words)
def Collect(manner):
    class Collector(MultiPredicate):
        def __init__(self, pred):
            self.pred = pred
        def match(self, words):
            return manner(self.pred.match(word) for word in words)
    return Collector
AnyWord = Collect(any)
AllWords = Collect(all)

def test_multipred():
    words = "ala ma kota".split()
    assert AnyWord(ExactWord("ala")).match(words)
    assert not AnyWord(ExactWord("ola")).match(words)
    assert AllWords(~(ExactWord("ola"))).match(words)

# Scopes ###########################################

def Before(n):
    def narrow(context):
        range = min(len(context[0]), n)
        return context[0][-range:]
    return narrow
def After(n):
    def narrow(context):
        range = min(len(context[2]), n)
        return context[2][:range]
    return narrow
def ITSELF(context):
    return [context[1]]
ALLBEFORE = Before(float("infinity"))
ALLAFTER = After(float("infinity"))

def test_scope():
    sentence = "a b c d e".split()
    context = sentence[:2], sentence[2], sentence[3:]
    assert ALLBEFORE(context) == ["a", "b"]
    assert Before(1)(context) == ["b"]
    assert ITSELF(context) == ["c"]
    assert After(1)(context) == ["d"]
    assert ALLAFTER(context) == ["d", "e"]


no_nouns = AllWords(~FormCheck("A"))
specific_word = Verbatim("brazylijska")
specific_expression = Verbatim("ma kota")
includes_brazilian = AnyWord(WordAnyForm("brazylijska"))
specific_words = AnyWord(ExactWord("brazylijska") | ExactWord("kolumbijska") | ExactWord("francuska"))

# Placed Predicate ###########################################

class Placed(Combinable):
    def __init__(self, scope, multipred):
        self.scope = scope
        self.pred = multipred
    def match(self, words, n):
        to_examine = self.scope((words[:n], words[n], words[n + 1:]))
        return self.pred.match(to_examine)

adj_bef_and_noun_aft       = Placed(ALLBEFORE, AnyWord(FormCheck("C"))) & Placed(ALLAFTER, AnyWord(FormCheck("A")))
adj_bef_and_noun_immid_aft = Placed(ALLBEFORE, AnyWord(FormCheck("C"))) & Placed(After(1), AnyWord(FormCheck("A")))

def test_placed():
    words = "ala ma kota".split()
    matcher = Placed(ALLBEFORE, AnyWord(ExactWord("ala")))
    assert not matcher.match(words, 0)
    assert matcher.match(words, 1)
    assert matcher.match(words, 2)

    matcher = Placed(ALLBEFORE, AnyWord(ExactWord("ala"))) & Placed(ALLAFTER, AnyWord(ExactWord("kota")))
    assert not matcher.match(words, 0)
    assert matcher.match(words, 1)

def find(matcher, sentence):
    words = sentence.split()
    result = []
    for n in range(len(words)):
        if matcher.match(words, n):
            result.append(words[n])
    return result

def test_finder():
    sentence = "ala ma kota"
    sentence2 = "ala kowalska ma wspanialego kota"
    matcher = Placed(ALLBEFORE, AnyWord(ExactWord("ala"))) & Placed(ALLAFTER, AnyWord(ExactWord("kota")))
    assert find(matcher, sentence) == ["ma"]
    assert find(matcher, sentence2) == ["kowalska", "ma", "wspanialego"]

    matcher = Placed(Before(2), AnyWord(ExactWord("ala"))) & Placed(After(2), AnyWord(ExactWord("kota")))
    assert find(matcher, sentence2) == ["ma"]
