<template>
  <div class="layout">
    <nav-header />
    <main class="container">
      <img src="../assets/stockphoto.jpg" loading="lazy"/>
      <h1>Velkommen til Klimakalkulatoren</h1>

      <div class="card mb-3">
        <div class="card-body">
          <h3 class="card-title">Prosjekter</h3>
          <p class="card-text">Fanen inneholder:</p>
            <ul>
              <li>En knapp for å opprette nytt prosjekt</li>
              <li>En slider for å vise/skjule arkiverte prosjekter</li>
              <li>En tabell med brukerens prosjekter</li>
            </ul>
          <p class="card-text">Tabellen kan sorteres i stigende/nedadgående rekkefølge etter valgfri kollonne, og valgt sortering lagres i localStorage og huskes neste gang brukeren logger seg på. Dersom brukeren venstre-klikker på ett av prosjektene, så åpnes produktoversikten til dette prosjektet (visning: /products).</p>
          <p class="card-text">Hvert tabell-rad inneholder en dropdown-meny, markert med tre prikker, med valgene:</p>
          <ul>
            <li>"Rediger" som åpner komponenten ProjectUpdateModal</li>
            <li>"Lag kopi" som lager en kopi av prosjektet. Prosjektdata for det kopierte prosjektet sendes til serveren og valideres på samme måte som nye prosjekter. Ved vellykket validering legges prosjektet til i tabellen Projects.</li>
            <li>"Arkiver" (for aktive prosjekt) eller "Aktiver" (for arkiverte prosjekt). Arkiverte prosjekter skjules fra tabellen, med mindre slideren 'Vis arkiverte prosjekter' er huket av.</li>
            <li>"Slett": sender en DELETE request til serveren. Serveren returnerer "status" og "message". Dersom "status" = "success", så slettes også prosjektet fra global state på klientsiden og en melding om dette vises. Ellers vises en feilmelding basert på innholdet i "message".</li>
          </ul>
        </div>
      </div>

      <div class="card mb-3">
        <div class="card-body">
          <h3 class="card-title">Produkter</h3>
          <p class="card-text">Fanen inneholder:</p>
            <ul>
              <li>En knapp for å legge til et nytt produkt</li>
              <li>En tabell over produktene i det aktive prosjektet</li>
            </ul>
          <p class="card-text">Tabellen kan sorteres i stigende/nedadgående rekkefølge etter valgfri kollonne, og valgt sortering lagres i localStorage og huskes neste gang brukeren logger seg på. Hvert tabell-rad inneholder en dropdown-meny (markert med tre prikker) med valgene:</p>
          <ul>
            <li>"Rediger" som åpner komponenten ProductUpdateModal.</li>
            <li>"Lag kopi" som lager en kopi av produktet. Prosjektdata for det kopierte produktet sendes til serveren og valideres på samme måte som nye produkter. Ved vellykket validering legges prosjektet til i tabellen Projects.</li>
            <li>"Slett": sender en DELETE request til serveren. Serveren returnerer "status" og "message". Dersom "status" = "success", så slettes produktet fra global state på klientsiden og en melding om dette vises. Ellers vises en feilmelding basert på innholdet i "message".</li>
          </ul>
        </div>
      </div>

      <div class="card mb-3">
        <div class="card-body">
          <h3 class="card-title">Resultater</h3>
          <p class="card-text">Fanen inneholder:</p>
          <ul>
            <li>En tabell som sammenstiller prosjektets klimagassutslipp fordelt på bygningsdel og livssyklusstadium (iht. faser i NS 3720). Tallene kan vises som "kg CO2e", "tonn CO2e", eller "kg CO2e per m2 per år".</li>
            <li>Resultatene fremstilles også som et kakediagram som viser fordeling av utlsipp på bygingsdeler. Brukeren kan klikke-bort en eller flere bygningsdeler, for å se fordeling av de resterende utslippene.</li>
          </ul>
        </div>
      </div>

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
h1 {
  margin-bottom: 2rem;
  margin-top: 0.7rem;
}
</style>
