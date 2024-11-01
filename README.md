# setup
(want je krijgt niet mn .env)

1. Maak .env file
2. Zet de volgende waardes:
   - DB_HOST, host van de database (port 3306)
   - DB_USER, user die wordt gebruikt, moet toegang hebben tot database en permissions hebben
   - DB_PASSWORD, wachtwoord voor user
   - DB_DATABASE, naam van de database die wordt gebruikt
3. install dependencies
   - pip3 install -r requirements.txt
4. run code
   - python3 app.py
   - python3 -m flask run


# Benodingdheden voor opdracht:


De realisatie is volledig gebaseerd op het design.
   - alleen in kleine manieren veranderd

De (basis) pagina layout dient op elke pagina hetzelfde te zijn.
   - Zie layout.html

De website moet responsive zijn en dus mee schalen met het schermformaat (TV, Laptop, Tablet, Mobiel).
   - alle paginas zijn flexbox

De website mag geen dode links/URL's bevatten.
   - yep

Een gebruiker moet te allen tijde naar elke pagina kunnen navigeren.
   - zoekbalk is altijd beschikbaar
   - je kan in user dropdown altijd naar je eigen profiel
   - Je kan doormiddel van op de Talland Blog tekst in de navbar naar de home pagina

Op de website dient duidelijk te zijn vermeld wie het heeft ontwikkeld (footer).
   - footer

Bij gebruik van externe tekst/afbeeldingen dien je de bron te vermelden (bijv. bron: https://site.com).
   - oops allemaal zelf gemaakt

# gebruikte technieken:
- Python
  - Flask
  - MySql
- HTML, CSS, JS
- Jinja2 (Flask)
- git


