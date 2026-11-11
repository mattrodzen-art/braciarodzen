# canva.md - ustawienia Canvy dla Braci Rodzeń

Skopiujcie ten plik do `~/.claude/instagram/canva.md`. Czyta go `/ig-canva`. Bez niego skill za każdym razem szuka brand kitu i wzorca od nowa.

Pola `{{...}}` uzupełnijcie. ID to identyfikatory z naszego konta, bez dostępu do konta nic nie dają.

---

## Konto

- **Brand kit:** `kADpeJxNlvw` (jedyny na koncie)
- **Projekt-wzorzec postów:** `DAG1f_3BmUg` - „Post na Instagram (3:4)”, strony 1080x1350, zbiorczy plik z postami
- **Folder na nowe posty:** {{nazwa albo ID folderu, jeśli chcemy je trzymać w jednym miejscu}}

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

Spisane z pierwszych stron wzorca. Poprawcie, jeśli się zmieniło.

- Format 1080x1350, zdjęcie na cały kadr (jedzenie, ilustracja medyczna), bez białych marginesów.
- Tekst wersalikami, gruby, bezszeryfowy.
- Nagłówek u góry: granatowy tekst na żółtym podświetleniu.
- Dopowiedzenie na dole: biały tekst na czarnych paskach.
- Żółta strzałka z czarnym obrysem wskazuje to, o czym mowa.
- Kolory: żółty {{#hex}}, granatowy {{#hex}}, czarny, biały.
- Font: {{nazwa z brand kitu}}
- Podpis: {{@handle}}, {{gdzie na slajdzie}}

## Czego na grafikach nie ma

- Zdjęć „przed i po” i sylwetek.
- Twarzy osób spoza zespołu bez zgody.
- Logotypów leków i suplementów.
- {{dopiszcie}}
