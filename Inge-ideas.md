# Bolnice

## Realne ideje
1. Aplikacija CEZIH koja ima preglednije sučelje (https://liste.cezih.hr/PrviTermin?pId=459&regId=114)
    - Kao Allianz za kartom bolnica te lako vidjljivim slobodnim terminima (https://dozo.allianz.hr/login)
    - Može se koristiti sličan princip kao na aplikacijama za rezerviranje apartmana gdje su slobodni temini jasno vidljivi u kalendaru 
2. Lista dolazaka: Kao u Fiziodent privatnoj ordinaciji 
    1. Na šalteru sestra zabilježi u tablicu dolazak pacijenta u kliniku
    2. Tablica je dijeljena s doktorom te doktor vidi vrijeme čekanja u tablici
        - Vijeme koje je duže od 10 minuta postaje narančasto
        - Nakon 20 minuta crveno - indikacija da pacijent predugo čeka
3. Dostupnost uputnica
    - Problem nastaje kada stariji ljudi moraju pronaći uputnicu u mailovima - ali mislim da je to već riješeno 


## SF ideje
1.  Face recognition pri ulasku u bolnicu + Ideja 2 (Lista dolazaka)

## Zanimljivi javni podaci
- Grafiti na javnim i privatnim površinama - Potrebno je terensko prikupljanje slika - NIJE IZVEDIVO
- Geolokacije tramvajskih stajališta ZET - https://data.gov.hr/ckan/hr/dataset/geoportal-tramvajska-stajalista-zet
- Geoportal sportskih objekata grada Zagreba
- Geolokacije sustava javnih bicikala.
- Geolokacije biciklističkih staza grada Zagreba.
- Zone prema Pravilniku o određivanju naknada za postavljanje ploča s natpisom, plakata, reklama i reklamnih panoa.
- Geolokacije nadzornih kamera
- Geolokacije električnih punionica na području grada Zagreba
- Prikaz povijesnih granica grada Zagreba u periodu od 1850. - 1992. godine.
- Lokacije pojilica s pitkom vodom na području Grada Zagreba

### CHAT GPT prijedlog 1

“Urban Flow Optimizer”
Problem

Grad ima:

tram stajališta
bike sustav
biciklističke staze
EV punionice

→ ali NEMA integriran pogled kako se ljudi stvarno kreću.

Rješenje

App koji daje:
👉 optimalnu multimodalnu rutu (tram + bike + pješke)
uz realne constraintove grada

Ključne funkcionalnosti
preporuka:
tram → bicikl → pješke
uzima u obzir:
dostupnost bicikala (lokacije stanica)
biciklističke staze
udaljenost do pojilica (UX bonus)
EV punionice (za e-bike / e-scooter proširenje)

➡️ slično kao Google Maps, ali:

fokusirano na Zagreb + lokalne specifičnosti
koristi open data (što je hackathon plus)
Tehnički stack
graph model:
nodes = stajališta + bike station + punionice
edges = staze + udaljenosti
algoritam:
Dijkstra / A*
vizualizacija:
Leaflet
“Wow faktor”
eco score (CO₂ saving)
“hydration-aware routing” (pojilice)
“bike friendly index” po kvartu

### CHAT GPT prijedlog 2

“Ad Placement Intelligence” (B2B, vrlo pametno)

Ovo je najbliže realnom biznisu.

Problem

Grad ima:

zone za reklame
prometne tokove (proxy preko tram/bike)

→ ali oglašavanje se ne optimizira data-driven

Rješenje

Tool koji kaže:
👉 gdje postaviti reklamu za max exposure

Kako radi

Kombinira:

tram stajališta (foot traffic proxy)
bike station usage (mobilnost)
sportske objekte (event-driven traffic)
zone dozvola (constraint)
Output
“Top 10 lokacija za billboard”
ROI score
Bonus
segmentacija:
sportaši
commuteri
turisti