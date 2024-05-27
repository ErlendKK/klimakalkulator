Appen er et enkelt regneprogram for klimagassberegninger i bygningsprosjekter.

Serversiden bruker en sqlite database "Userdata", med 4 tabeller "Users", "Projects", "Products", og "EmissionFactors". Produktdata, inkl. utlsippsfaktorer, hentes fra API-en til Eco Portal.


### Funksjonalitet

# Nav Header
- Sticky header som inneholder overskrift og logo, samt linker til visningene "Prosjekter", "Produkter", og "Resultater". Dersom brukeren ikke er logget inn, ligger det en link for å logge inn samt et bruker-ikon til høyre i headeren. Denne aktiverer en dropdown meny med valgene "Registrer" (åpner modal-komponenten registrationModal), "Log inn" (åpner modal-komponenten LoginnModal), og "info" (router til visningen Home). Dersom brukeren er logget inn, vises navnet til brukeren samt evt. profilbilde på høyre side. Denne aktiverer en drop-down meny

## Session
Når brukere logges inn, opprettes det alltid en session, som bl.a. brukes til authentisering på server-siden. Brukere kan velge om de ønsker å forbli innlogget. Dette valget blir lagret som en del av session-dataen.

Hver gang siden lastes, sender klienten en forespørsel til serveren om å sjekke om session inneholder en bruker som har valgt å forbli tilkoblet. Om det er tilfellet, sendes data (brukerdata, prosjektdata, og evt. profilbilde) for denne brukeren tilbake, og brukeren logges inn.


## Registrere bruker
Inndata til brukerregistrering oppgis gjennom et skjema i et Bootstrap-modalvindu (Component: RegistrationModal) som kan åpnes over et hvilket som helst visning. Brukeren fyller ut et skjema med følgende felter: navn, e-post, passord, bekreftelse av passord, (valgfri) opplasting av profilbilde, samt et valg for å forbli/ ikke forbli innlogget.

# Klientside-håndtering av submit
- Navn: valideres med pattern-attributen og et regex-mønster som kun tillater bokstaver, mellomrom, bindestrek og appostrof.
- Epost: valideres med type-attributten (type="email").
- Passord: krav til lengde (minst 8 tegn) og innhold (kombinasjon av bokstaver og tall) valideres med pattern-attributen og et regex-mønster. Samsvar mellom input-verdiene til "passord" og "gjenta passord" valideres med en funksjon.
- Profilbilde: krav til filtype (JPG/JPEG, PNG, eller GIF) og filstørrelse (maks 5MB) valideres med en funksjon.
- Ved suksessfull validering sendes input-verdiene til serveren (path /users/register) som formData (for å kunne inkludere evt. bildefil). 
- Serveren returnerer et JSON-objekt som inneholder attributtene "status" og "message" (samt brukerdata dersom registreringen var vellykket). Dersom "status" = "success", så logges brukeren inn, og en velkomstmelding vises. Ellers vises en feilmelding basert på innholdet i "message".

# Serverside håndering av bruker-registrerings forespørsler
- Serverside-validering inkluderer de samme punktene som klient-side valideringen, samt en kontroll på at det ikke allerede finnes en bruker med den oppgitte epost-adressen. 
- Dersom forespørselen inneholder et profilbilde (og valideringen av dette er vellykket), gis bildet et nytt, unikt navn (for å sikre ingen navnkonflikt), og lagres på server-mappen "user_data"
- Dersom valideringen var vellykket, lagres inndataene (samt en unik bruker-id, en passord-hash og evt. foto-filnavn) i tabellen Users. Brukeren legges til i session, og et json-object med all bruker-dataen (untatt passord-hashen) og propertien "status" = "success" returneres til klienten.


## Logg inn bruker
Inndata for brukerpålogging oppgis gjennom et skjema i et Bootstrap-modalvindu (Component: LoginModal) som kan åpnes over et hvilket som helst visning. Brukeren fyller ut skjemaet med følgende felter: e-post, passord, og et valg for å forbli/ikke forbli innlogget.

# Klientside håndtering av submit
- Epost: Valideres med type-attributten (type="email") for å forsikre at brukerens inndata følger formatet til en e-postadresse.
- Passord: Ingen spesifikk validering utover å sjekke at feltet ikke er tomt.
- Ved suksessfull validering sendes input-verdiene til serveren (path /login).
- Serveren returnerer et JSON-objekt som inneholder attributtene "status" og "message" (samt brukerdata hvis påloggingen var vellykket). Dersom "status" = "success", så logges brukeren inn, og en velkomstmelding vises. Ellers vises en feilmelding basert på innholdet i "message". Dersom brukeren har lastet opp et profilbilde, så vil retur-objektet fra en vellykket innlogging inkludere linken til dette.
- Når brukeren er logget inn oppdateres global state (authStore) til å reflektere dataen til denne brukeren. 

# Serverside håndering av innloggings forespørsler
- Serverside-valideringen sjekker om eposten finnes i tabllen Users, og om eposten og passordet matcher.
- Dersom valideringen var vellykket, hentes brukerens data (brukerdata fra tabellen Users og prosjektdata fra tabellen Projects). Brukeren legges til i session, og et json-object med all dataen (untatt passord-hashen) og propertien "status" = "success" returneres til klienten.


## visninger

# Hjem (visning: /home)
- Statisk side med info om programmet.

# Prosjektoversikt (visning: /projets)
- Dersom brukeren ikke er logget inn, viser siden en beskjed om dette. Ellers vises en side hvor brukeren kan administrer prosjektene dine.
-Siden inneholder: en knapp for å opprette nytt prosjekt, som åpner komponenten projectAddModal; en slider for å vise/skjule arkiverte prosjekter; og en tabell med brukerens prosjekter.
- Tabellen kan sorteres i stigende/nedadgående rekkefølge etter valgfri kollonne, og valgt sortering lagres i localStorage og huskes neste gang brukeren logger seg på.
- Dersom brukeren venstre-klikker på ett av prosjektene, så åpnes produktoversikten til dette prosjektet (visning: /products). 
- Hvert tabell-rad inneholder en dropdown-meny, markert med tre prikker, med valgene:
* "Rediger" som åpner komponenten ProjectUpdateModal
* "Lag kopi" som lager en kopi av prosjektet. Dersom dette er første kopi, legges tallet (1) til på slutten av prosejktnavnet. For ytterligere kopier inkrementeres dette tallet. Prosjektdata for det kopierte prosjektet sendes til serveren (/projects/register) og valideres på samme måte som nye prosjekter. Ved vellykket validering legges prosjektet til i tabellen Projects.
* "Arkiver" (for aktive prosjekt) eller "Aktiver" (for akriverte prosjekt): toggler prosjektet-objektets 'active'-property. Arkiverte prosjekter skjules fra tabellen, med mindre slideren 'Vis arkiverte prosjekter' er aktivert. Forsøk på å åpne et arkivert prosjekt resulterer i en advarsel om at prosjektet er arkivert.
* Slett: sender en DELETE request til serveren. Serveren returnerer et JSON-objekt med egenskapene "status" og "message". Dersom "status" = "success", så slettes også prosjektet fra global state på serversiden og en melding om dette vises. Ellers vises en feilmelding basert på innholdet i "message".

# Produktoversikt (visning: /products)
- Dersom brukeren ikke er logget inn, eller ingen prosjekt er aktive, viser siden en beskjed om dette. Ellers vises en side som lar brukeren administrere produktene i det aktive prosjekt.
- Siden inneholder: en knapp for å legge til et nytt produkt, som åpner komponenten ProductAddModal; en tabell over produktene i det aktive prosjektet.
- Tabellen kan sorteres i stigende/nedadgående rekkefølge etter valgfri kollonne, og valgt sortering lagres i localStorage og huskes neste gang brukeren logger seg på.
- Hvert tabell-rad inneholder en dropdown-meny, markert med tre prikker, med valgene:
* "Rediger" som åpner komponenten ProductUpdateModal.
* "Lag kopi" som lager en kopi av produktet. Prosjektdata for det kopierte produktet sendes til serveren (/products/add) og valideres på samme måte som nye produkter. Ved vellykket validering legges prosjektet til i tabellen Projects.
* Slett: sender en DELETE request til serveren. Serveren returnerer et JSON-objekt med egenskapene "status" og "message". Dersom "status" = "success", så slettes også produktet fra global state på serversiden og en melding som bekrefter slettingen vises. Ellers vises en feilmelding basert på innholdet i "message".

# Resultater (visning: /results)
- Inneholder en tabell som sammenstiller prosjektets klimagassutslipp fordelt på bygningsdel og livssyklusstadium (iht. faser i NS 3720). Tallene kan vises som "kg CO2e", "tonn CO2e", eller "kg CO2e per m2 per år".
- Resultatene fremstilles også som et kakediagram som viser fordeling av utlsipp på bygingsdeler. Brukeren kan klikke-bort en eller flere bygningsdeler, for å se fordeling av de resterende utslippene.


## Prosject-Modaler (ProjectAddModal og ProjectUpdateModal)
Inndata for registrering av nye prosjekter oppgis gjennom et skjema i et Bootstrap-modalvindu (Komponent: ProjectUpdateModal) som kan åpnes over enhver visning. Brukeren fyller ut et skjema med følgende felter: prosjektnavn, adresse, bruttoareal (BTA), bygningskategori, prosjektstart (år), analyseperiode (år).

# Klientside håndtering av submit
- Prosjektnavn: Valideres med attributten required og en maxlength attribtutt satt til 100 (ingen begrensninger på innhold).
- Adresse: Valideres med attributten required og en maxlength attribtutt satt til 100 (ingen begrensninger på innhold).
- Bruttoareal (BTA): Valideres med type="number", en min-attributt satt til 1 for å sikre at verdien er positiv, og en maxlength-attribtutt satt til 100.
- Bygningskategori: Valideres  med attributten required. Kategori velges fra en nedtrekksliste som inneholder forhåndsdefinerte kategorier basert på klimagassreferansene i BREEAM-NOR 6.1.
- Prosjektstart (år): Type er satt lik "text" av estetiske grunner, og format (heltall) valideres med attributtene pattern, required, en maxlength attribtutt satt til 100, og en min-attributt satt til året 2000. 
- Analyseperiode (år): Valideres med type="number" og en min-attributt satt til 1 for å sikre at verdien er positiv.
- Ved suksessfull validering sendes prosjektdataene til serveren (sti /projects/register) som et JSON-objekt som inneholder input-dataene, samt brukerens ID, og datoen prosjektet ble opprettet.
- Serveren returnerer et JSON-objekt som inneholder attributtene "status" og "message" (samt prosjektdetaljer dersom registreringen var vellykket). Dersom "status" = "success", så legges prosjektet til i systemet, og en velkomstmelding vises. Ellers vises en feilmelding basert på innholdet i "message".

# Serverside håndering av forespørsler om å opprette/endre prosjekter
- Forespørsler om å opprette prosjekt: serveren autentiserer forespørselen ved å sjekke at bruker ID-en som ble sendt med forespørselen er i session. 
- Forespørsler om å endre prosjekt: serveren autentiserer forespørselen ved å sjekke at bruker ID-en som er registrert på prosjektet er i session.
- Serveren validerer videre at json objektet inneholder alle obligatoriske verdier for å opprette/oppdatere et prosjekt.
- Dersom autentiseringen eller valideringen mislykkes, returnerer serveren et json objekt med egenskapene status = "failed" og en melding "message" som vises til brukeren.
- Ellers lagres inndataene i tabellen Projects. Ved opprettelse av prosjekt, opprettes samtidig en unik project-id. Serveren returnerer et JSON-objekt som inneholder denne ID-en , samt, status="success"


## Produkt-Modaler (ProductAddModal og ProductUpdateModal)



## REST API
'/users/register', methods=['POST']
'/login', methods=['POST']
'/logout', methods=['POST']
'/session', methods=['GET']

'/projects/register', methods=['POST']
'/projects/update', methods=['PUT']
'/projects/delete/<project_id>', methods=['DELETE']

'/products/add', methods=['POST']
'/products/delete/<product_id>', methods=['DELETE']
'/products/update', methods=['PUT']
'/products/emission-data/<uuid>', methods=['GET']
'/products/list', methods=['GET']



## Credits:
* Thanks to leocaseiro https://dcblog.dev/stop-bootstrap-drop-menus-being-cut-off-in-responsive-tables for sharing his work-around for a bug conserning dropdown-menus in tables with the Bootstrap "table-responsive" attribute.

* Modals: created based on the boilerplate found here: https://getbootstrap.com/docs/5.0/components/modal/
* Pie Chart: created based on the boilerplate found here: https://vue-chartjs.org/guide/
* function getTodaysDate(): based on these examples: https://www.scaler.com/topics/get-current-date-in-javascript/
* Regex for passord: https://dev.to/temmietope/regex-for-passwords-3c1f
