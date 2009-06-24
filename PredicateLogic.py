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
_or = lambda a, b: a or b
_and = lambda a, b: a and b

class SinglePredicate(object):
    def __or__(self, other):
        return Or(self, other)
    def __and__(self, other):
        return And(self, other)
    def __invert__(self):
        return Not(self)
class Not(SinglePredicate):
    def __init__(self, pred):
        self.pred = pred
    def match(self, word):
        return not self.pred.match(word)
def LogicalPair(relation):
    class Logical(SinglePredicate):
        def __init__(self, pred1, pred2):
            self.pred1, self.pred2 = pred1, pred2
        def match(self, word):
            return relation(self.pred1.match(word), (self.pred2.match(word)))
    return Logical
Or = LogicalPair(_or)
And = LogicalPair(_and)

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


class MultiPredicate(object): pass
class Verbatim(MultiPredicate):
    def __init__(self, target):
        self.target = target
    def match_words(self, words):
        return self.target in " ".join(words)
class AnyWord(MultiPredicate):
    def __init__(self, pred):
        self.pred = pred
    def match_words(self, words):
        return any(self.pred.match(word) for word in words)
def Collect(manner):
    class Collector(MultiPredicate):
        def __init__(self, pred):
            self.pred = pred
        def match_words(self, words):
            return manner(self.pred.match(word) for word in words)
    return Collector
AnyWord = Collect(any)
AllWords = Collect(all)

def test_multipred():
    words = "ala ma kota".split()
    assert AnyWord(ExactWord("ala")).match_words(words)
    assert not AnyWord(ExactWord("ola")).match_words(words)
    assert AllWords(~(ExactWord("ola"))).match_words(words)




class Scope(object): pass
class Before(Scope):
    def __init__(self, n):
        self.n = n
    def narrow(self, context):
        range = min(len(context[0]), self.n)
        return context[0][-range:]
class After(Scope):
    def __init__(self, n):
        self.n = n
    def narrow(self, context):
        range = min(len(context[2]), self.n)
        return context[2][:range]
class Itself(Scope):
    def narrow(self, context):
        return [context[1]]
ALLBEFORE = Before(float("infinity"))
ALLAFTER = After(float("infinity"))
ITSELF = Itself()

def test_scope():
    sentence = "a b c d e".split()
    context = sentence[:2], sentence[2], sentence[3:]
    assert ALLBEFORE.narrow(context) == ["a", "b"]
    assert Before(1).narrow(context) == ["b"]
    assert ITSELF.narrow(context) == ["c"]
    assert After(1).narrow(context) == ["d"]
    assert ALLAFTER.narrow(context) == ["d", "e"]


no_nouns = AllWords(~FormCheck("A"))
specific_word = Verbatim("brazylijska")
specific_expression = Verbatim("ma kota")
includes_brazilian = AnyWord(WordAnyForm("brazylijska"))
specific_words = AnyWord(ExactWord("brazylijska") | ExactWord("kolumbijska") | ExactWord("francuska"))

class Placed(object):
    def __init__(self, scope, multipred):
        self.scope = scope
        self.pred = multipred
    def match_word_in_sentence(self, words, n):
        to_examine = self.scope.narrow((words[:n], words[n], words[n + 1:]))
        return self.pred.match_words(to_examine)
    def __and__(self, other):
        return PlacedAnd(self, other)
    def __or__(self, other):
        return PlacedOr(self, other)
    def __invert__(self):
        return PlacedNot(self)
class PlacedNot(object):
    def __init__(self, ca):
        self.ca = ca
    def match_word_in_sentence(self, words, n):
        return not self.ca.match_word_in_sentence(words, n)
def PlacedLogical(oper):
    class ContextAwareOperator(object):
        def __init__(self, ca1, ca2):
            self.ca1, self.ca2 = ca1, ca2
        def match_word_in_sentence(self, words, n):
            return oper(self.ca1.match_word_in_sentence(words, n), self.ca2.match_word_in_sentence(words, n))
    return ContextAwareOperator
PlacedAnd = PlacedLogical(_and)
PlacedOr = PlacedLogical(_or)

adj_bef_and_noun_aft       = Placed(ALLBEFORE, AnyWord(FormCheck("C"))) & Placed(ALLAFTER, AnyWord(FormCheck("A")))
adj_bef_and_noun_immid_aft = Placed(ALLBEFORE, AnyWord(FormCheck("C"))) & Placed(After(1), AnyWord(FormCheck("A")))

def test_placed():
    words = "ala ma kota".split()
    matcher = Placed(ALLBEFORE, AnyWord(ExactWord("ala")))
    assert not matcher.match_word_in_sentence(words, 0)
    assert matcher.match_word_in_sentence(words, 1)
    assert matcher.match_word_in_sentence(words, 2)

    matcher = Placed(ALLBEFORE, AnyWord(ExactWord("ala"))) & Placed(ALLAFTER, AnyWord(ExactWord("kota")))
    assert not matcher.match_word_in_sentence(words, 0)
    assert matcher.match_word_in_sentence(words, 1)

def find(matcher, sentence):
    words = sentence.split()
    result = []
    for n in range(len(words)):
        if matcher.match_word_in_sentence(words, n):
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
