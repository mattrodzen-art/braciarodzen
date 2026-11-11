---
name: ig-plan
description: >-
  Planuje tydzień na Instagramie: co publikujemy, w jakim formacie, kiedy,
  i z kim wchodzimy w interakcje. Używaj przy „zaplanuj tydzień”, „co
  wrzucić”, „kalendarz treści”, „nie mamy o czym publikować”, albo gdy
  potrzebny jest harmonogram i lista kont do komentowania.
---

# ig-plan

Centrum dowodzenia. Reszta pakietu wykonuje, ten skill decyduje, co. Raz w tygodniu, zawsze tego samego dnia.

## Wejście

Przeczytaj `~/.claude/instagram/voice.md`, `swipe.md`, `log.md` i `plan.md`, jeśli są. Swipe file to nasze dowody z `/ig-viral` i ma pierwszeństwo przed czymkolwiek w tym pliku. Log chroni przed powtórzeniem tematu z ostatnich dwóch tygodni.

Jeśli ich nie ma, zapytaj o cztery rzeczy i zapisz:

1. Co sprzedajemy i komu (magazyn, Akademia, konferencje, kanał YouTube).
2. Trzy, cztery tematy, z których chcemy być znani.
3. Co się naprawdę wydarzyło w tym tygodniu: nagranie, pomiar, pytanie od widza, rozmowa z lekarzem, konferencja, nowe badanie. Stąd biorą się posty.
4. Dziesięć kont, przed którymi warto być widocznym.

Jeśli w tygodniu wychodzi film na YouTube albo był live, zaplanuj jego pocięcie przez `/ig-repurpose` zamiast wymyślać od zera.

## Co publikujemy

Cztery, pięć postów tygodniowo, z czego co najmniej trzy rolki. Rolki docierają do ludzi, którzy nas nie obserwują. Karuzele idą w głąb z tymi, którzy już obserwują. Relacje są codzienne i planowane osobno.

Mieszamy, nigdy dwa tego samego typu pod rząd:

| typ | ile | zadanie |
| --- | --- | --- |
| **Dowód** | 1/tydz. | coś, co się wydarzyło, z liczbą (pomiar, wynik, przypadek za zgodą). Rolka. |
| **Nauka** | 1-2/tydz. | jedna rzecz, którą widz może zrobić dziś. Rolka albo karuzela. |
| **Opinia** | 1/tydz. | stanowisko, za które ktoś może przestać obserwować (np. krytyka zaleceń). Rolka. |
| **Historia** | 1/2 tyg. | scena z kosztem. Rolka. |
| **Oferta** | 1/2 tyg. | co oferujemy, wprost, bez przepraszania. Karuzela albo relacje. |

Dla każdego slotu: temat, konkretny kąt z tego, co się wydarzyło, format i numer formuły z `ig-reel/hooks.json`. Nie temat, kąt. „Insulina” to nie plan. „Glukoza po owsiance kontra jajecznica, nasz pomiar z wtorku” to rolka.

## Kiedy

Kiedy nasi odbiorcy nie śpią i nie są w pracy. Dla odbiorców konsumenckich zwykle wczesny wieczór, czasu polskiego.

Jeśli w sesji jest connector **Metricool**, pobierz najlepsze godziny dla Instagrama (`getBestTimeToPostByNetwork`) i oprzyj na nich plan. To nasze dane, lepsze niż ogólne.

Ale powiedz to wprost: **godzina znaczy dużo mniej niż pierwsze dwie sekundy.** Jeśli optymalizujemy godziny, zanim hooki działają, poprawiamy nie to, co trzeba.

## Runda interakcji (obowiązkowa)

20 minut dziennie, przed publikacją. Lista 10 kont:

- **5 zasięgowych** - konta z publicznością, którą chcemy mieć, gdzie dobry komentarz jest widoczny. Komentujemy wcześnie.
- **3 równorzędne** - podobny rozmiar, podobna dziedzina (inni edukatorzy, lekarze, dietetycy). Ta grupa się odwzajemnia.
- **2 współpracowe** - konta, z którymi realnie może być collab, wywiad albo wspólny live. Komentujemy tygodniami, zanim napiszemy DM.

Listę przekaż do `/ig-comment`.

## Wynik

```
TYDZIEŃ 17 LISTOPADA

PN   tylko interakcje (20 min, lista niżej)
WT   19:30  ROLKA     DOWÓD    #17 Pojedynek      - owsianka vs jajecznica, nasz pomiar
ŚR   relacje + interakcje
CZ   19:00  KARUZELA  NAUKA    opis B             - 4 slajdy: co podnosi insulinę
PT   19:30  ROLKA     OPINIA   #22 Odwrócone      - „najważniejszy posiłek dnia”
SB   -
ND   18:00  ROLKA     HISTORIA #21 Środek zdania  - pytanie z gabinetu

RELACJE  codziennie 3-5 klatek, pytania w czwartek.

INTERAKCJE (5 / 3 / 2)
  ...

Napisz „pisz wtorek”, a przygotuję szkic.
```

Zapisz plan do `~/.claude/instagram/plan.md`, żeby inne skille go widziały.

Nic nie jest planowane w żadnym narzędziu ani publikowane. Wyjątek: jeśli o to poprosimy i jest Metricool, gotowy post można dodać jako szkic **do akceptacji** (`createScheduledPostForReview`), dopiero po wyraźnym „tak” z tekstem i godziną przed oczami.
