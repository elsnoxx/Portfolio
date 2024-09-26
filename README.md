# Todo

- dodelat logovani akci nejakou funkci, ktera bude zapisovat do logu, nezapomenout ji pak pridat do funkce logdelete
- vytvorit jobu, ktera vytvori grafy obrazky nebo svg, ktere se pak budou zobrazovat na strance, aby se predeslo dlouhemu zpracovani a nacitani
- stock prediction https://www.youtube.com/watch?v=0E_31WqVzCY
- fear and greed pro akcie https://edition.cnn.com/markets/fear-and-greed - hotovo, ale premenit na to aby se generoval jednou denne obrazek abych to nebylo odkazane tolik na API
J9GRUCXHP98P9QFK

- 


- Akcie
        - dodelat vypocet DCF
        - Vymyslet dalsi hoditi ukazatele akcii


- Monitoring
        - vylepsit zobrazeni, grafy teloty loadu CPU a RAM
        - pohrat si s modal aby fungoval jak mel

- https://www.youtube.com/watch?v=z0AfnEPyvAs
- https://www.youtube.com/watch?v=OqCqFfLfFsk

## Metriky

Tento dokument obsahuje dvě hlavní sekce pro hodnocení, zda je akcie vhodná ke koupi. Zaměříme se na **technickou analýzu** a **výpočetní techniky**.

## 1. Technická analýza (vyčítání z grafu)
Technická analýza se zaměřuje na analýzu historických cenových dat a objemu obchodů pomocí grafů. Klíčové indikátory zahrnují:

- **Trend**: Zjišťuje, zda je cena v dlouhodobém rostoucím, klesajícím nebo bočním trendu.
- **Support a Resistance**: Identifikace cenových úrovní, kde cena často našla podporu nebo odpor.
- **Klouzavé průměry (SMA, EMA)**: Výpočet průměrné ceny akcie za určité časové období, které pomáhají odhalit trend.
- **Indikátory (RSI, MACD)**: Nástroje pro měření hybnosti a překoupenosti/přeprodanosti akcie.
- **Svíčkové formace**: Vzory ve svíčkových grafech, které mohou signalizovat změny v cenovém vývoji.

## 2. Výpočetní techniky
Tato sekce se zaměřuje na finanční ukazatele a poměry, které hodnotí vnitřní hodnotu akcie.

- **Poměrové ukazatele (P/E, P/B, P/S)**: Poměry mezi cenou akcie a ziskem (P/E), účetní hodnotou (P/B) nebo tržbami (P/S).
- **Dividendy a výnosy**: Hodnocení dividendového výnosu a jeho stability.
- **Free Cash Flow (FCF)**: Ukazuje, kolik volných peněžních toků firma generuje po odečtení investičních výdajů.
- **ROE, ROA, ROI**: Ukazatele ziskovosti, které měří, jak efektivně firma využívá kapitál a aktiva k tvorbě zisku.
- **Debt-to-Equity Ratio**: Poměr dluhu vůči vlastnímu kapitálu, který určuje finanční stabilitu firmy a její schopnost splácet závazky.

Obě sekce společně poskytují ucelený přehled o vhodnosti akcie pro nákup.


## Done
- crypto screener



# Server

- tutorial na nastevni serveru na raspi https://www.youtube.com/watch?v=BpcK5jON6Cg

pouzito raspi, ngnix jako server a gunicorn3 pro spuzeti aplikace

nginex server settings

```
server {
        listen 80;
        location / {
                proxy_pass http://127.0.0.1:8000;
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
}
```

ke spusteni gunicorn3 pouzxit prikaz 
        - gunicorn3 --workers=3 app:app --daemon