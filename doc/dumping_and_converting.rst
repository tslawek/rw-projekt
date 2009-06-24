:mod:`xml2txt` -- Parsowanie wikipedi
=====================================

.. module:: xml2txt
   :synopsis: Biblioteka pozwalajaca na konwersję wikipedi do pliku tekstowego

Celem projektu było pozystkiwanie wiedzy z wikipedi, do tego celu niezbędne jest posiadzanie łatwego dostępu do jej zawartośći.

W tym celu pobieramy aktualny zrzut wikipedi ze strony: http://download.wikimedia.org/plwiki/.
Następnie rozpakowujemy jego zawartość i dostajemy w wyniku zrzut wikipedi w postaci jednego dużego pliku XML.

Parsowanie XML
--------------

Plik xml zawierający zrzut wikipedi ma bardzo duży rozmiar, dlatego do jego przetwarzania nie mogliśmy użyć zwyczajnych narzędzi to pracy na plikach xml'owych.
Dlatego skorzystaliśmy z biblioteki lxml której zalety oraz użycie opisane jest na stroie: http://www.ibm.com/developerworks/xml/library/x-hiperfparse/.

Podstawową jej zaletą jest fakt, iż potrafi ona uzyskać potrzebne informacje z pliku xml bez potrzeby jego wcześniejszczego sparsowania co wiąże się z wczytaniem go do pamięci operacyjnej.


XML'owy zrzut wikipedi dla każdego artykułu zawiera takie informacje jak:
        1). numer id artykułu 
        2). numer rewizji artykułu
        3). tytuł artykułu
        4). zawartość.

Na podstawie tych informacji przeprowadzamy zarzucenie treści artykułów do plików xml.

Konfiguracja parsowania wikipedi
--------------------------------

Wikipedia zawiera w swoich artykułach oprócz samej treści, również wiele innych informacji, np zdjęcia, tabele. Oraz w swoim markupie zawiera takie elementy jak pogrubienia, akapity i wiele innych.

Docelowo chcemy przekształcić artykuł zapisany w formie markupów wikipedi naczysty tekst.
Aby zadecydowac które z elementów makrapu mamy wykorzystać a które pomijać stworzyliśmy plik konfiguracyjny w którym to określamy.

Plik ten zawiera takie pola jak:
- czy parsować tabele
- czy pozyskac informację o kategori artylułu
- czy pozyskać informację o słowach wyróżnionych

oraz definjuje dodatkowo w jaki sposób mają być zapisane te metadane. Dokonuje się tego poprzez zdefiniowanie specjalnych separatorów. 

Usuwanie znaczników wikipedi
----------------------------

Poczatkowo dużym problemem okazało się zagadnienie pozbycia się zanczników stosowanych do zapisu tekstu wikipedi. 
W tym celu skorzystaliśmy z biblioteki mwlibhttp://code.pediapress.com/wiki/wiki/mwlib w celu parsowanie treści artykułu. Dodatkowo na podstawie zawartego w bibliotece narzędzia do zapisywania parsowanego tekstu otrzymaliśmy komplentne narzędzie służące do parsowania oraz usuwanie znaczników z wikipedi. Dodatkow podczas procesu parsowania pozyskujemy metadane takie jak np. wyróżnione w tekście słowa.

