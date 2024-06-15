# Klimakalkulator: Klimagassberegninger i byggeprosjekter

## Om

Serversiden er skrevet i Flask.py med en postgreSQL database bestående av 4 tabeller: "ssers", "projects", "products", og "emission_factors". Produktdata (inkl. utlsippsfaktorer) hentes fra API-en til Eco Portal. Klientsiden er skrevet med Vue 3 (Options API) Single File Components og Bootstrap 5, med Vite, Vue-router, og Pinia.

# Installasjon

#### Last ned repoet
```sh
git clone https://github.com/dat310-2024/Klimakalkulator.git
```

### Anbefalt Installasjon (krever npm)

#### Sett appens rot-mappe som current directory
```sh
cd Klimakalkulator
```

#### Installer python dependencies (se server/requirements.txt)
```sh
npm run setup
```

#### Sett opp backend-serveren og opprett databasen userdata.db
```sh
npm run init-server
```

#### Valgfritt: Åpne en ny Terminal og Populer databasen med testdata
```sh
npm run test-db
```

### Alternativ installasjon

#### Sett appens rot-mappe som current directory
```sh
cd Klimakalkulator
```

#### Installer python dependencies (se server/requirements.txt)
```sh
pip install -r server/requirements.txt
```

#### Naviger til server/scripts, og kjør filen create_db.py
```sh
cd server/scripts
python create_db.py
```

#### Valgfritt: Populerer databasen med testdata
```sh
python test_db.py
```

#### Naviger tilbake til /server og start backend-serveren
```sh
cd ..
python app.py
```

### Åpne applikasjonen
Åpne http://127.0.0.1:5000/ i nettleseren.

####
Testbrukere 

| Epost       | Passord      | Anbefalt for å teste appen    |
|-------------|--------------|-------------------------------|
| a@a.a       | aaaaaaaa     | JA                            |
| b@b.b       | bbbbbbbb     | NEI                           |
| c@c.c       | cccccccc     | NEI                           |


# Server API

| Endpoint                                    | Metode       |
|---------------------------------------------|--------------|
| `/users/register`                           | `POST`       |
| `/login`                                    | `POST`       |
| `/logout`                                   | `POST`       |
| `/session`                                  | `GET`        |
| `/projects/register`                        | `POST`       |
| `/projects/update`                          | `PUT`        |
| `/projects/delete/<project_id>`             | `DELETE`     |
| `/products/add`                             | `POST`       |
| `/products/delete/<product_id>`             | `DELETE`     |
| `/products/update`                          | `PUT`        |
| `/products/emission-data/<uuid>`            | `GET`        |
| `/products/list`                            | `GET`        |


# Funksjonalitet

## Nav Header
- Sticky header som inneholder overskrift og logo, samt linker til visningene "Prosjekter", "Produkter", og "Resultater". Dersom brukeren ikke er logget inn, ligger det en link for å logge inn samt et bruker-ikon til høyre i headeren. Denne aktiverer en dropdown meny med valgene "Registrer" (åpner modal-komponenten registrationModal), "Log inn" (åpner modal-komponenten LoginnModal), og "info" (router til visningen Home). Dersom brukeren er logget inn, vises navnet til brukeren samt evt. profilbilde på høyre side. Denne aktiverer en drop-down meny

### Session
Når brukere logges inn, opprettes det alltid en session, som bl.a. brukes til authentisering på server-siden. Brukere kan velge om de ønsker å forbli innlogget. Dette valget blir lagret som en del av session-dataen.

Hver gang siden lastes, sender klienten en forespørsel til serveren om å sjekke om session inneholder en bruker som har valgt å forbli tilkoblet. Om det er tilfellet, sendes data (brukerdata, prosjektdata, og evt. profilbilde) for denne brukeren tilbake, og brukeren logges inn.


## Registrere bruker
Inndata til brukerregistrering oppgis gjennom et skjema i et Bootstrap-modalvindu (Component: RegistrationModal) som kan åpnes over et hvilket som helst visning. Brukeren fyller ut et skjema med følgende felter: navn, e-post, passord, bekreftelse av passord, (valgfri) opplasting av profilbilde, samt et valg for å forbli/ ikke forbli innlogget.

### Klientside-håndtering av submit
- Navn: valideres med pattern-attributen og et regex-mønster som kun tillater bokstaver, mellomrom, bindestrek og appostrof.
- Epost: valideres med type-attributten (type="email").
- Passord: krav til lengde (minst 8 tegn) og innhold (kombinasjon av bokstaver og tall) valideres med pattern-attributen og et regex-mønster. Samsvar mellom input-verdiene til "passord" og "gjenta passord" valideres med en funksjon.
- Profilbilde: krav til filtype (JPG/JPEG, PNG, eller GIF) og filstørrelse (maks 5MB) valideres med en funksjon.
- Ved suksessfull validering sendes input-verdiene til serveren (path /users/register) som formData (for å kunne inkludere evt. bildefil). 
- Serveren returnerer et JSON-objekt som inneholder attributtene "status" og "message" (samt brukerdata dersom registreringen var vellykket). Dersom "status" = "success", så logges brukeren inn, og en velkomstmelding vises. Ellers vises en feilmelding basert på innholdet i "message".

### Serverside håndering av bruker-registrerings forespørsler
- Serverside-validering inkluderer de samme punktene som klient-side valideringen, samt en kontroll på at det ikke allerede finnes en bruker med den oppgitte epost-adressen. 
- Dersom forespørselen inneholder et profilbilde (og valideringen av dette er vellykket), gis bildet et nytt, unikt navn (for å sikre ingen navnkonflikt), og lagres på server-mappen "user_data"
- Dersom valideringen var vellykket, lagres inndataene (samt en unik bruker-id, en passord-hash og evt. foto-filnavn) i tabellen Users. Brukeren legges til i session, og et json-object med all bruker-dataen (untatt passord-hashen) og propertien "status" = "success" returneres til klienten.


## Logg inn bruker
Inndata for brukerpålogging oppgis gjennom et skjema i et Bootstrap-modalvindu (Component: LoginModal) som kan åpnes over et hvilket som helst visning. Brukeren fyller ut skjemaet med følgende felter: e-post, passord, og et valg for å forbli/ikke forbli innlogget.

### Klientside håndtering av submit
- Epost: Valideres med type-attributten (type="email") for å forsikre at brukerens inndata følger formatet til en e-postadresse.
- Passord: Ingen spesifikk validering utover å sjekke at feltet ikke er tomt.
- Ved suksessfull validering sendes input-verdiene til serveren (path /login).
- Serveren returnerer et JSON-objekt som inneholder attributtene "status" og "message" (samt brukerdata hvis påloggingen var vellykket). Dersom "status" = "success", så logges brukeren inn, og en velkomstmelding vises. Ellers vises en feilmelding basert på innholdet i "message". Dersom brukeren har lastet opp et profilbilde, så vil retur-objektet fra en vellykket innlogging inkludere linken til dette.
- Når brukeren er logget inn oppdateres global state (authStore) til å reflektere dataen til denne brukeren. 

### Serverside håndering av innloggings forespørsler
- Serverside-valideringen sjekker om eposten finnes i tabllen Users, og om eposten og passordet matcher.
- Dersom valideringen var vellykket, hentes brukerens data (brukerdata fra tabellen Users og prosjektdata fra tabellen Projects). Brukeren legges til i session, og et json-object med all dataen (untatt passord-hashen) og propertien "status" = "success" returneres til klienten.


## visninger

### Hjem (visning: /home)
- Statisk side med info om programmet.

### Prosjektoversikt (visning: /projets)
- Dersom brukeren ikke er logget inn, viser siden en beskjed om dette. Ellers vises en side hvor brukeren kan administrer prosjektene dine.
-Siden inneholder: en knapp for å opprette nytt prosjekt, som åpner komponenten projectAddModal; en slider for å vise/skjule arkiverte prosjekter; og en tabell med brukerens prosjekter.
- Tabellen kan sorteres i stigende/nedadgående rekkefølge etter valgfri kollonne, og valgt sortering lagres i localStorage og huskes neste gang brukeren logger seg på.
- Dersom brukeren venstre-klikker på ett av prosjektene, så åpnes produktoversikten til dette prosjektet (visning: /products). 
- Hvert tabell-rad inneholder en dropdown-meny, markert med tre prikker, med valgene:
* "Rediger" som åpner komponenten ProjectUpdateModal
* "Lag kopi" som lager en kopi av prosjektet. Dersom dette er første kopi, legges tallet (1) til på slutten av prosejktnavnet. For ytterligere kopier inkrementeres dette tallet. Prosjektdata for det kopierte prosjektet sendes til serveren (/projects/register) og valideres på samme måte som nye prosjekter. Ved vellykket validering legges prosjektet til i tabellen Projects.
* "Arkiver" (for aktive prosjekt) eller "Aktiver" (for akriverte prosjekt): toggler prosjektet-objektets 'active'-property. Arkiverte prosjekter skjules fra tabellen, med mindre slideren 'Vis arkiverte prosjekter' er aktivert. Forsøk på å åpne et arkivert prosjekt resulterer i en advarsel om at prosjektet er arkivert.
* Slett: sender en DELETE request til serveren. Serveren returnerer et JSON-objekt med egenskapene "status" og "message". Dersom "status" = "success", så slettes også prosjektet fra global state på klientsiden og en melding om dette vises. Ellers vises en feilmelding basert på innholdet i "message".

### Produktoversikt (visning: /products)
- Dersom brukeren ikke er logget inn, eller ingen prosjekt er aktive, viser siden en beskjed om dette. Ellers vises en side som lar brukeren administrere produktene i det aktive prosjekt.
- Siden inneholder: en knapp for å legge til et nytt produkt, som åpner komponenten ProductAddModal; en tabell over produktene i det aktive prosjektet.
- Tabellen kan sorteres i stigende/nedadgående rekkefølge etter valgfri kollonne, og valgt sortering lagres i localStorage og huskes neste gang brukeren logger seg på.
- Hvert tabell-rad inneholder en dropdown-meny, markert med tre prikker, med valgene:
* "Rediger" som åpner komponenten ProductUpdateModal.
* "Lag kopi" som lager en kopi av produktet. Prosjektdata for det kopierte produktet sendes til serveren (/products/add) og valideres på samme måte som nye produkter. Ved vellykket validering legges prosjektet til i tabellen Projects.
* Slett: sender en DELETE request til serveren. Serveren returnerer et JSON-objekt med egenskapene "status" og "message". Dersom "status" = "success", så slettes også produktet fra global state på klientsiden og en melding som bekrefter slettingen vises. Ellers vises en feilmelding basert på innholdet i "message".

### Resultater (visning: /results)
- Inneholder en tabell som sammenstiller prosjektets klimagassutslipp fordelt på bygningsdel og livssyklusstadium (iht. faser i NS 3720). Tallene kan vises som "kg CO2e", "tonn CO2e", eller "kg CO2e per m2 per år".
- Resultatene fremstilles også som et kakediagram som viser fordeling av utlsipp på bygingsdeler. Brukeren kan klikke-bort en eller flere bygningsdeler, for å se fordeling av de resterende utslippene.


## Prosject-Modaler (ProjectAddModal og ProjectUpdateModal)
Inndata for registrering av nye prosjekter oppgis gjennom et skjema i et Bootstrap-modalvindu som kan åpnes over enhver visning. Skjemaet har følgende felt: prosjektnavn, adresse, bruttoareal (BTA), bygningskategori, prosjektstart (år), analyseperiode (år).

### Klientside håndtering av submit
- Prosjektnavn: Valideres med attributten required og en maxlength attribtutt satt til 100 (ingen begrensninger på innhold).
- Adresse: Valideres med attributten required og en maxlength attribtutt satt til 100 (ingen begrensninger på innhold).
- Bruttoareal (BTA): Valideres med type="number", en min-attributt satt til 1 for å sikre at verdien er positiv, og en maxlength-attribtutt satt til 100.
- Bygningskategori: Valideres  med attributten required. Kategori velges fra en nedtrekksliste som inneholder forhåndsdefinerte kategorier basert på klimagassreferansene i BREEAM-NOR 6.1.
- Prosjektstart (år): Type er satt lik "text" av estetiske grunner, og format (heltall) valideres med attributtene pattern, required, en maxlength attribtutt satt til 100, og en min-attributt satt til året 2000. 
- Analyseperiode (år): Valideres med type="number" og en min-attributt satt til 1 for å sikre at verdien er positiv.
- Ved suksessfull validering sendes prosjektdataene til serveren (sti /projects/register) som et JSON-objekt som inneholder input-dataene, samt brukerens ID, og datoen prosjektet ble opprettet.
- Serveren returnerer et JSON-objekt som inneholder attributtene "status" og "message" (samt prosjektdetaljer dersom registreringen var vellykket). Dersom "status" = "success", så legges prosjektet til i systemet, og en velkomstmelding vises. Ellers vises en feilmelding basert på innholdet i "message".

### Serverside håndering av forespørsler om å opprette/endre prosjekter
- Brukeren autentiseres ved å sjekke at bruker ID-en som er registrert på prosjektet er i session.
- Forespørselen valideres ved å sjekke at den inneholder alle obligatoriske verdier og disse oppfølger minstekrav til format og innhold. For PUT-forespørsler sjekkes det i tillegg at prosjektet finnes i tabellen.
- Dersom autentiseringen eller valideringen mislykkes, returnerer serveren en status-meling som vises til brukeren.
- Ellers tildeles prosjektet en unik project-id som lagre, sammen med inndataene, i tabellen Projects. Serveren returnerer et JSON-objekt som inneholder prosjekt data, samt en status melding.


## Produkt-Modaler (ProductAddModal og ProductUpdateModal)
Inndata for registrering av nye produkter oppgis gjennom et skjema i et Bootstrap-modalvindu (Komponent: ProductModal) som kan åpnes over enhver visning. Brukeren fyller ut et skjema med følgende felter: bygningsdel, produktgruppe, produkttype, produkt, mengde, enhet, utskiftingsintervall, vedlikeholdsutslipp.

### Klientside håndtering av submit
- Bygningsdel: Valideres med attributten required. Velges fra en nedtrekksliste som inneholder forhåndsdefinerte bygningsdeler.
- Produktgruppe: Valideres med attributten required. Produktgrupper filtreres basert på valgt bygningsdel og velges fra en nedtrekksliste.
- Produkttype: Valideres med attributten required. Produkttyper filtreres basert på tilgjengelige data fra Eco Portal og velges fra en nedtrekksliste.
- Produkt: Valideres med attributten required. Produkter filtreres basert på valgt produkttype og velges fra en nedtrekksliste. Ved valg av produkt lastes tilhørende utslippsdata fra Eco Portal.
-  Mengde: Valideres med attributten required og type="number" for å sikre at verdien er positiv.
- Enhet: Enheten for produktet vises basert på valgt produkt.
- Utskiftingsintervall: Valideres med attributten required og type="number".
- Vedlikeholdsutslipp: Valideres med attributten required og type="number".

Ved suksessfull validering sendes produktdataene til serveren (sti /products/register) som et JSON-objekt som inneholder input-dataene, samt brukerens ID og datoen produktet ble opprettet.
Serveren returnerer et JSON-objekt som inneholder attributtene "status" og "message" (samt produktdetaljer dersom registreringen var vellykket). Dersom "status" = "success", så legges produktet til i systemet, og en bekreftelsesmelding vises. Ellers vises en feilmelding basert på innholdet i "message".

### Serverside håndering av forespørsler om å opprette/endre produkter
- Brukeren autentiseres ved å sjekke at bruker ID-en som er registrert på prosjektet er i session.
- Forespørselen valideres ved å sjekke at den inneholder alle obligatoriske verdier og disse oppfølger minstekrav til format og innhold. For PUT-forespørsler sjekkes det i tillegg at produktet finnes i tabellen.
- Dersom autentiseringen eller valideringen mislykkes, returnerer serveren en status-meling som vises til brukeren.
- Ellers tildeles produktet en unik product-id som lagres, sammen med inndataene, i tabellen Products. Serveren returnerer et JSON-objekt som inneholder product-data, samt en status melding.


## Credits:
* Thanks to leocaseiro (https://dcblog.dev/stop-bootstrap-drop-menus-being-cut-off-in-responsive-tables) for sharing his work-around for a bug conserning dropdown-menus in tables with the Bootstrap "table-responsive" attribute.
* Modals: based on the boilerplate found here: https://getbootstrap.com/docs/5.0/components/modal/
* Pie Chart: based on the boilerplate found here: https://vue-chartjs.org/guide/
* function getTodaysDate(): based on these examples: https://www.scaler.com/topics/get-current-date-in-javascript/
* Regex for passord: https://dev.to/temmietope/regex-for-passwords-3c1f
