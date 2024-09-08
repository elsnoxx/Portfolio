# Todo

- dodelat logovani akci nejakou funkci, ktera bude zapisovat do logu, nezapomenout ji pak pridat do funkce logdelete
- vytvorit jobu, ktera vytvori grafy obrazky nebo svg, ktere se pak budou zobrazovat na strance, aby se predeslo dlouhemu zpracovani a nacitani
- stock prediction https://www.youtube.com/watch?v=0E_31WqVzCY
- fear and greed pro akcie https://edition.cnn.com/markets/fear-and-greed - hotovo, ale premenit na to aby se generoval jednou denne obrazek abych to nebylo odkazane tolik na API

- server na raspi https://www.youtube.com/watch?v=BpcK5jON6Cg

- https://www.youtube.com/watch?v=z0AfnEPyvAs
- https://www.youtube.com/watch?v=OqCqFfLfFsk


## Done
- crypto screener



# Hostovano

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

ke spusteni gunicorn3 pouzxit prikaz --> gunicorn3 --workers=3 app:app --daemon