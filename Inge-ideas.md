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

Kako radi 2

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

### CHAT GPT prijedlog 3
“HydroBike Zagreb”
👉 App za bicikliste i rekreativce koji optimizira rutu po:
dostupnosti vode 💧
kvaliteti vožnje 🚴
kontinuitetu staza
🎯 Problem (jasan i stvaran)

U Zagrebu:

ne znaš gdje možeš napuniti vodu
ne znaš gdje su stvarno povezane bike staze
često završiš:
na lošoj cesti
bez vode
u prekidu rute

👉 posebno problem za:

rekreativce
trkače
turiste
e-bike korisnike
✅ Rješenje (jednostavno i fokusirano)

Mapa + routing koji daje:

1) “Hydration-aware route”

👉 ruta koja:

prolazi kroz pojilice svakih X km
izbjegava “suhe zone”
2) “Bike continuity score”

👉 koliko je ruta zapravo:

na pravim biciklističkim stazama
bez prekida / silaska na cestu
3) “Refill network”

👉 vizualizacija:

dostupnosti vode u gradu
coverage mapa (gdje si “sigurna”)
🔥 Zašto je ovo dobro (hackathon-wise)
fokusirano → možeš napraviti poliran demo
jasno → odmah razumljivo
vizualno → heatmap + ruta = efektno
nema direktne konkurencije (Google to NE radi)
⚙️ Kako implementirati (realno u 1–2 dana)
1) Data model

Spoji sve u jedan graph:

nodes:
bike stationi
pojilice
edges:
biciklističke staze
2) Routing logika (ključ)

Modificirani Dijkstra:

cost function:

cost = distance 
     + penalty_if_no_bike_lane
     + penalty_if_no_water_nearby

👉 ili čak:

constraint:
max 2 km bez pojilice
3) Vizualizacija

Koristi:

Leaflet

Layeri:

staze (linije)
pojilice (plave točke)
bike stationi (zeleno)
4) Killer feature (lagan za napraviti)
“Dehydration risk”
označi dijelove grada gdje:
nema pojilice u radiusu npr. 1 km

👉 to je brutalno vizualno

🧠 Pitch (konkretno)

“Zagreb ima odličnu infrastrukturu za bicikle, ali nema osnovnu stvar — informaciju gdje možeš doći do vode.
Mi smo to pretvorili u routing engine koji ne optimizira samo kretanje, nego i preživljavanje ljeti.”

💡 Bonus ideje (ako stigneš)
“sport mode”:
ruta koja prolazi kroz parkove
“tourist mode”:
lagana ruta + voda + atrakcije (možeš kasnije dodati)
“bike station balancing”:
gdje ima slobodnih bicikala (ako imaš podatke)
🎯 Realna procjena

Ovo možeš:

napraviti brzo
vizualno pokazati
objasniti bez puno tehničkog konteksta

👉 i najvažnije:
nije generički projekt