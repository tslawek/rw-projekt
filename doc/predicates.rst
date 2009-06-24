:mod:`predicates` -- Predykaty
==============================

.. module:: predicates
   :synopsis: Bilbioteka pozwalająca na konstrukcję predykatów

Predykaty pozwalają budować wyrażenia opisujące poszukiwane słowa przy pomocy
prostych elementów podstawowych. Predykaty budowane są na trzech poziomach, przy
pomocy klas dziedziczących z :class:`SinglePredicate`, :class:`MultiPredicate` i
:class:`Placed`.
Każdy kolejny poziom bada dodatkowe informacje na temat tekstu.

Predykaty pojedynczego słowa
----------------------------

Predykaty poziomu pierwszego badają pojedyncze słowa. Wszystkie posiadają metodę
match, która otrzymuje na wejściu badane słowo i zwraca wartość boolowską
opisującą dopasowanie.
W bibliotece zaimplementowano następujące predykaty:

.. class:: ExactWord 

Predykat dopasowujący pojedyncze słowo::
  
  ExactWord("jaskółka").match("jaskółka")    # -> True
  ExactWord("jaskółka").match("jaskółki")    # -> False
  ExactWord("jaskółka").match("europejska")  # -> False

.. class:: StartingWith 

Predykat dopasowujący przedrostek słowa::

  StartingWith("al").match("albrecht")  # -> True
  StartingWith("al").match("durer")     # -> False

.. class:: FormCheck 

Predykat bada formę słowa (etykietę a biblioteki clp), i sprawdza zgodność z
przyrostkiem podanym w argumencie konstruktora. Np FormCheck("A") dopasuje tylko
słowa będące rzeczownikami::

  FormCheck("A").match("papuga")     # -> True
  FormCheck("A").match("papuzi")     # -> False

.. class:: WordAnyForm 

Predykat dopasowujący słowo bez względu na jego odmianę. Przykładowo
WordAnyForm("papuga") zwróci prawdę dla słowa "papuga"::

  WordAnyForm("rycerz").match("rycerze")  # -> True
  WordAnyForm("rycerz").match("ni")       # -> False


Implementacja predykatów pojedynczego słowa
-------------------------------------------

W celu implementacji własnych predykatów pojedynczego słowa, dostarczono klasy
bazowej :class:`SinglePredicate`. 

.. class:: SinglePredicate

Stanowi klasę bazową dla predykatów pojedynczego słowa. Przeładowuje operatory
binarne, co pozwala na łatwe składanie i negowanie predykatów.

W tworzony predykacie należy zaimplementować jedynie metodę match::

  class Capitalized(SinglePredicate):
      def match(self, word):
          return word and word[0].isupper()

Predykaty wielu słów
--------------------

Predykaty wielu słów dziedziczą po klasie :class:`MultiPredicate` i również oferują
metodę match. Jednak w przypadku tych predykatów, metoda match otrzymuje w
argumencie listę słów. Przygotowaliśmy jeden predykat wielu słów i dwie fabryki
pozwalające tworzyć predykaty wielu słów na bazie predykatów pojedynczego słowa.

.. class:: MultiPredicate

Klasa bazowa dla predykatów wielu słów.

.. class:: Verbatim

Predykat łączy słowa otrzymane na wejściu przy użyciu spacji, a następnie
poszukuje w otrzymanym stringu wystąpień łańcucha otrzymanego w konstruktorze::

  Verbatim("sens życia").match(["jaki", "jest", "sens", "życia"]) # -> True
  Verbatim("sens życia").match(["mielonka"])                      # -> False


.. class:: AnyWord

AnyWord otrzymuje w konstruktorze predykat pierwszego poziomu, a jego metoda
match zwraca prawdę, jeśli w przypadku któregokolwiek ze słów z listy udało się
dokonać dopasowania::

  AnyWord(StartingWith("spam")).match(["spam", "spam", "wonderful", "spam"]) # -> True
  AnyWord(StartingWith("spam")).match(["ni", "spamalot", "ni", "ni"])        # -> True
  AnyWord(StartingWith("spam")).match(["ni", "ni", "ni"])                    # -> False

.. class:: AllWords

AllWords otrzymuje w konstruktorze predykat pierwszego poziomu, a jego metods
match zwraca prawdę, jeśli wszystkie słowa z listy zostaną dopasowane. Użyteczne
w przypadku warunków zanegowanych::

  AllWords(~WordAnyForm("inkwizycja")).match(["nikt", "się", "nie", "spodziewa"]) # -> True
  AllWords(~WordAnyForm("inkwizycja")).match(["hiszpańskiej", "inkwizycji"])      # -> False


Predykaty z kontekstem
----------------------

Predykaty trzeciego poziomu badają wyróżnione słowo w danej liście słów.
Tworzy się je przy pomocy klasy Placed, w argumentach podając kontekst (zakres),
który ma być brany pod uwagę i predykat wielu słów, który należy dopasować.

Zakresy
"""""""
W bibliotece zdefiniowanych jest 5 zakresów:

.. data:: ALLBEFORE

Wszystkie poprzedzające słowa w zdaniu.

.. data:: ALLAFTER

Wszystkie następujące słowa w zdaniu.

.. data:: ITSELF

Wskazane słowo.

.. function:: Before(n)

N poprzedzających słów.

.. function:: After(n)

N następujących słów.


Budowanie kontekstów z zakresem
"""""""""""""""""""""""""""""""
Aby zbudować kontekst z zakresem, należy użyć klasy :class:`Placed`.

.. class:: Placed
Klasa opisująca predykaty z zakresem.

.. method:: Placed.__init__(self, scope, multipredicate)
Placed w konstruktorze otrzymuje zakres, oraz predykat wielu słów. Przykładowo,
aby otrzymać predykat dopasowujący słowo tylko jeśli przed nim występuje
rzeczownik, należy wpisać::
  
  Placed(ALLBEFORE, AnyWord(FormCheck("A")))

.. method:: Placed.match(self, words, n)
Metoda wyciąga w podanej listy słów kontekst (scope, z którym zainstancjonowano
predykat) względem słowa na pozycji n, po czym wykonuje na uzyskanej liście swój
predykat wielu słów (multipredicate z konstruktora)::

  noun_before = Placed(ALLBEFORE, AnyWord(FormCheck("A")))
  sentence = ["mój", "poduszkowiec", "jest", "pełen", "węgorzy"]
  noun_before.match(sentence, 3)   # -> True

Składanie i negowanie predykatów
--------------------------------
Predykaty tego samego typu można składać i negować przy pomocy operatorów &, \|
i ~. Przykładowo::

  ~StartingWith("r") # Nie zaczynające się na "r"
  StartingWith("a") | StartingWith("b") # Zaczynające się na "a" lub "b"
  FormCheck("c") & StartingWith("k") # przymiotniki na literę k

  ~AnyWord(ExactWord("cheddar")) # nie występuje słowo "cheddar"
  AllWords(~ExactWord("cheddar")) # to samo inaczej (z prawa deMorgana)

  AnyWord(ExactWord("afrykański")) | AnyWord(ExactWord("europejski")) 
          # w liście występuje któreś ze słów "afrykański" lub "europejski"

  AnyWord(ExactWord("brazylijski")) & AnyWord(ExactWord("kolumbijski")) 
          # w liście występują oba słowa

Można również składać predykaty z zakresem. Np. ten kod stworzy predykat
dopasowujący słowa na literę "w", z rzeczownikiem przed nimi i przymiotnikiem
zaraz po nich::

  noun_before = Placed(ALLBEFORE, AnyWord(FormCheck("A")))
  adj_immid_after = Placed(After(1), AnyWord(FormCheck("C")))
  starts_with_w = Placed(ITSELF, AnyWord(StartingWith("w"))) 

  sophisticated_condition = starts_with_w & noun_before & adj_immid_after
