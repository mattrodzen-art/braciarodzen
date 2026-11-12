# canva.md - ustawienia Canvy dla Braci Rodzeń

Skopiujcie ten plik do `~/.claude/instagram/canva.md`. Czyta go `/ig-canva`. Bez niego skill za każdym razem szuka brand kitu i wzorca od nowa.

Pola `{{...}}` uzupełnijcie. ID to identyfikatory z naszego konta, bez dostępu do konta nic nie dają.

---

## Konto

- **Brand kit:** `kADpeJxNlvw` (jedyny na koncie)
- **Projekt-wzorzec postów:** `DAG1f_3BmUg` - „Post na Instagram (3:4)”, strony 1080x1350, zbiorczy plik z postami
- **Folder na nowe posty:** {{nazwa albo ID folderu, jeśli chcemy je trzymać w jednym miejscu}}

## Logo

Jest na każdym slajdzie, niezmienione 1:1.

- **Logo główne (twarze):** zasób w Canvie `MAHasYxI46E`, plik 1254x1254 z przezroczystym tłem, przysłany przez nas 12.11.2026. Czarna kreska i białe wypełnienie twarzy, więc działa na jasnym i na ciemnym tle.
- **Miejsce i wielkość na slajdzie 1080x1350:** lewy górny róg, 70 px od krawędzi, 230x230 px.
- **Logo napis (białe „BRACIA RODZEŃ” z gwiazdką):** zasób `MAHaoyw_ES0`, z Dysku Google, folder „Logo - Bracia Rodzeń”, plik `br.png`. Tylko na ciemne tło, gdy nie pasuje logo z twarzami.
- Zmieniamy wyłącznie rozmiar, z zachowaniem proporcji.

## Układ „karta z tekstem”

Sprawdzony w projekcie `DAHasRFwS_w` („5 korzyści low carb”). Każda strona ma nasz krój: nagłówek granatowy na żółtym i tekst biały na czarnych paskach.

- Nową karuzelę w tym układzie robimy przez `merge-designs`: `create_new_design` z jedną stroną z `DAHasRFwS_w`, potem `modify_existing_design` i `insert_pages` po jednej stronie na wywołanie.
- Na każdej stronie podmieniamy dwa teksty (`replace_text`), numer slajdu i ewentualnie źródło.
- Identyfikatory elementów są inne na każdej stronie. Najpierw `read-design` z `design_content`.

## Zdjęcia

Zdjęć, które są już w projektach w Canvie, nie używamy drugi raz.

- **Dysk Google, „Zdjęcia Braci Rodzeń”:** folder `1Yr27WVHW6MII8egM0-jliiU_CgJ0Oj2v`
- **Dysk Google, „Kuchnia Braci Rodzeń”:** folder `1Fp4ph9Ca_GdLnXSfZc-YR2bscm_q8yHA`
- {{inne foldery: wydarzenia, prelegenci}}

## Strony wzorca

Które strony zbiorczego pliku kopiujemy jako układ. Wystarczą trzy, cztery.

| układ | strona | co na niej jest |
| --- | --- | --- |
| okładka / pojedynczy post | 1 | zdjęcie na cały kadr, nagłówek u góry, tekst na dole, strzałka |
| slajd z treścią | {{nr}} | {{...}} |
| podsumowanie (lista) | {{nr}} | {{...}} |
| CTA | {{nr}} | {{...}} |

Najwygodniej zrobić w Canvie osobny, krótki projekt „IG WZORZEC” z czterema czystymi stronami i wpisać tu jego ID. Kopiowanie z pliku, który ma kilkaset stron, działa, ale łatwo o pomyłkę w numerze.

## Styl (opis do generowania)

Spisane z pierwszych stron wzorca i z postów o największym zasięgu (`skills/ig-canva/wzorce.md`). Poprawcie, jeśli się zmieniło.

- Format 1080x1350, zdjęcie na cały kadr (jedzenie, ilustracja medyczna), bez białych marginesów.
- Tekst wersalikami, gruby, bezszeryfowy.
- Nagłówek u góry: granatowy tekst na żółtym podświetleniu.
- Dopowiedzenie na dole: biały tekst na czarnych paskach.
- Żółta strzałka z czarnym obrysem wskazuje to, o czym mowa.
- Kolory: żółty {{#hex}}, granatowy {{#hex}}, czarny, biały.
- Biała karta (żart, dialog): białe tło, czarna zaokrąglona ramka, awatary u góry, pogrubiony tytuł, tekst wyrównany do lewej.
- Font: {{nazwa z brand kitu}}
- Podpis: {{@handle}}, {{gdzie na slajdzie}}

## Czego na grafikach nie ma

- Zdjęć „przed i po” i sylwetek.
- Twarzy osób spoza zespołu bez zgody.
- Logotypów leków i suplementów.
- {{dopiszcie}}
