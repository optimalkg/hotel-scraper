# Profitroom Analyzer - MVP (Etap 1)

MVP aplikacji webowej w Python/Flask do analizy cen na stronach Profitroom, z dashboardem HTML zamiast obsługi przez CMD.

## Stack
- Python
- Flask
- HTML/CSS/lekki JavaScript
- Playwright
- openpyxl
- JSON config

## Struktura projektu
- `app.py` — Flask + API endpointy dashboardu
- `config_manager.py` — trwały zapis/odczyt `config.json`
- `scraper.py` — główny przepływ analizy hotel po hotelu
- `popup_handler.py` — sekwencja domykania popupów (2 iteracje)
- `parser.py` — stub parsera ofert/pokoi do rozbudowy
- `excel_writer.py` — tworzenie i przyrostowy zapis `wyniki_analizy.xlsx`
- `templates/index.html` — dashboard
- `static/style.css` — style
- `static/app.js` — logika interakcji UI i wywołań API
- `requirements.txt` — zależności

## Konfiguracja domyślna
Przy pierwszym uruchomieniu tworzony jest `config.json` z domyślnymi hotelami i datami:

- AQUARIUS — `https://booking.profitroom.com/pl/hotelaquariusspa/pricelist/rooms/?currency=PLN`
- HAVET — `https://booking.profitroom.com/pl/havethotelresortspadzwirzyno1/pricelist/rooms/?currency=PLN`
- GRAND — `https://booking.profitroom.com/pl/grandlubiczuzdrowiskoustka3/pricelist/rooms/?currency=PLN`

Daty:
- `check-in = 2026-05-11`
- `check-out = 2026-05-14`

## Uruchomienie
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
python app.py
```

Dashboard będzie dostępny pod adresem: `http://127.0.0.1:5000`

## Zakres etapu 1 (zaimplementowane)
1. Dashboard HTML z:
   - listą hoteli (nazwa + link)
   - dodawaniem/edycją/usuwaniem hoteli
   - polami dat check-in/check-out
   - przyciskami „Zapisz ustawienia” i „Uruchom analizę”
2. Trwały zapis ustawień do `config.json`.
3. Playwright:
   - `headless=False`
   - timeout 60 s
   - 1 retry
   - pauza 2 sekundy między hotelami
4. Popup handler:
   - próba kliknięcia „ZAAKCEPTUJ WSZYSTKIE”
   - próba kliknięcia przycisków zamknięcia popupów marketingowych
   - wysłanie Escape
   - sekwencja powtórzona 2 razy
5. Przepływ analizy hotel po hotelu:
   - otwarcie strony
   - podmiana `check-in` i `check-out` w URL
   - próba kliknięcia „ZASTOSUJ”
   - wywołanie parsera-stuba (bez pełnej logiki pokojów/ofert)
6. Excel:
   - tworzenie `wyniki_analizy.xlsx`
   - zdefiniowane kolumny
   - zapis po każdym hotelu

## Bezpieczeństwo zachowania
- Aktualny kod **nigdy nie klika przycisku „REZERWUJ”**.

## Open questions / next steps
1. Ujednolicenie selektorów Profitroom:
   - różne wdrożenia mogą mieć inne nazwy/casing przycisków i popupów.
2. Logika parsera ofert:
   - doprecyzować definicję i selekcję ofert RACK vs PAKIET,
   - obsłużyć wiele wariantów pokoi i walidację dostępności.
3. Strategia zapisu danych:
   - czy w Excelu nadpisywać poprzednie przebiegi czy budować historię,
   - czy dodać unikalny identyfikator sesji analizy.
4. Zachowanie UI podczas długiej analizy:
   - obecnie analiza jest synchroniczna i blokuje request,
   - w kolejnym etapie można dodać job queue / worker.
5. Walidacje biznesowe dat i URL:
   - np. check-out > check-in, obsługa pustych list hoteli,
   - walidacja domeny i składni URL.
