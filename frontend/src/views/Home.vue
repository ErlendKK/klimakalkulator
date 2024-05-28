<template>
  <div class="layout">
    <nav-header />
    <main class="container">
      <img src="../assets/stockphoto.jpg" loading="lazy"/>
      <h1>Velkommen til Klimakalkulatoren</h1>

      <h2>Prosjekter</h2>
      <ul>
        <li>Siden inneholder:
          <ul>
            <li>en knapp for å opprette nytt prosjekt, som åpner komponenten projectAddModal;</li>
            <li>en slider for å vise/skjule arkiverte prosjekter; og</li>
            <li>en tabell med brukerens prosjekter.</li>
          </ul>
        </li>
        <li>Tabellen kan sorteres i stigende/nedadgående rekkefølge etter valgfri kollonne, og valgt sortering lagres i localStorage og huskes neste gang brukeren logger seg på.</li>
        <li>Dersom brukeren venstre-klikker på ett av prosjektene, så åpnes produktoversikten til dette prosjektet (visning: /products).</li>
        <li>Hvert tabell-rad inneholder en dropdown-meny, markert med tre prikker, med valgene:
          <ul>
            <li>"Rediger" som åpner komponenten ProjectUpdateModal</li>
            <li>"Lag kopi" som lager en kopi av prosjektet. Dersom dette er første kopi, legges tallet (1) til på slutten av prosejktnavnet. For ytterligere kopier inkrementeres dette tallet. Prosjektdata for det kopierte prosjektet sendes til serveren (/projects/register) og valideres på samme måte som nye prosjekter. Ved vellykket validering legges prosjektet til i tabellen Projects.</li>
            <li>"Arkiver" (for aktive prosjekt) eller "Aktiver" (for arkiverte prosjekt): toggler prosjektet-objektets 'active'-property. Arkiverte prosjekter skjules fra tabellen, med mindre slideren 'Vis arkiverte prosjekter' er aktivert. Forsøk på å åpne et arkivert prosjekt resulterer i en advarsel om at prosjektet er arkivert.</li>
            <li>"Slett": sender en DELETE request til serveren. Serveren returnerer et JSON-objekt med egenskapene "status" og "message". Dersom "status" = "success", så slettes også prosjektet fra global state på serversiden og en melding om dette vises. Ellers vises en feilmelding basert på innholdet i "message".</li>
          </ul>
        </li>
      </ul>

      <h2>Produkter</h2>
      <ul>
        <li>Siden inneholder:
          <ul>
            <li>en knapp for å legge til et nytt produkt, som åpner komponenten ProductAddModal;</li>
            <li>en tabell over produktene i det aktive prosjektet.</li>
          </ul>
        </li>
        <li>Tabellen kan sorteres i stigende/nedadgående rekkefølge etter valgfri kollonne, og valgt sortering lagres i localStorage og huskes neste gang brukeren logger seg på.</li>
        <li>Hvert tabell-rad inneholder en dropdown-meny, markert med tre prikker, med valgene:
          <ul>
            <li>"Rediger" som åpner komponenten ProductUpdateModal.</li>
            <li>"Lag kopi" som lager en kopi av produktet. Prosjektdata for det kopierte produktet sendes til serveren (/products/add) og valideres på samme måte som nye produkter. Ved vellykket validering legges prosjektet til i tabellen Projects.</li>
            <li>"Slett": sender en DELETE request til serveren. Serveren returnerer et JSON-objekt med egenskapene "status" og "message". Dersom "status" = "success", så slettes også produktet fra global state på serversiden og en melding som bekrefter slettingen vises. Ellers vises en feilmelding basert på innholdet i "message".</li>
          </ul>
        </li>
      </ul>

      <h2>Resultater</h2>
      <ul>
        <li>Inneholder en tabell som sammenstiller prosjektets klimagassutslipp fordelt på bygningsdel og livssyklusstadium (iht. faser i NS 3720). Tallene kan vises som "kg CO2e", "tonn CO2e", eller "kg CO2e per m2 per år".</li>
        <li>Resultatene fremstilles også som et kakediagram som viser fordeling av utlsipp på bygingsdeler. Brukeren kan klikke-bort en eller flere bygningsdeler, for å se fordeling av de resterende utslippene.</li>
      </ul>
    </main>
    <nav-footer />
  </div>
</template>
    
<script>
  import NavHeader from '../components/NavHeader.vue'
  import NavFooter from '../components/NavFooter.vue'
  import { useAuthStore } from '../stores/authStore';
  import { computed } from 'vue';
  
  export default {
    name: 'Home',
    components: {
      NavHeader,
      NavFooter,
    },        
    setup() {
      const authStore = useAuthStore();
      const isLoggedInComputed = computed(() => authStore.isLoggedIn);
      const userComputed = computed(() => authStore.user);

      return { isLoggedInComputed, userComputed };
    },
  };
</script>
  
<style scoped>
  main {
      padding-top: 0;
  }
  .container img {
    width: 100%;
    height: auto;
  }
  select{
    font-family: 'FontAwesome', 'sans-serif';
    font-size: 10px;
}
</style>
