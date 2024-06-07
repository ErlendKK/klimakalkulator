const klimagassreferanser = {
    "Boligbygg": 8.0, 
    "Kontor": 6.8, 
    "Skole": 6.4, 
    "Forretningsbygg": 6.0, 
    "Sykehjem": 6.8, 
    "Oppvarmet kjeller": 5.2, 
    "Uoppvarmet kjeller": 3.6
};

const bygningsdeler = [
    {
      bygningsdel: "Grunn og fundamenter",
      nummer: 21,
      produktgrupper: [
        { gruppe: "Grunnforsterking", nummer: 213 },
        { gruppe: "Støttekonstruksjoner", nummer: 214 },
        { gruppe: "Pelefundamentering", nummer: 215 },
        { gruppe: "Fundamenter", nummer: 216 }
      ]
    },
    {
      bygningsdel: "Bæresystemer",
      nummer: 22,
      produktgrupper: [
        { gruppe: "Separate søyler", nummer: 222 },
        { gruppe: "Separate bjelker", nummer: 223 },
        { gruppe: "Avstivende konstruksjoner", nummer: 224 },
        { gruppe: "Brannbeskyttelse", nummer: 225 },
        { gruppe: "Gips osv.", nummer: 226 }
      ]
    },
    {
      bygningsdel: "Yttervegger",
      nummer: 23,
      produktgrupper: [
        { gruppe: "Bærende konstruksjoner", nummer: 231 },
        { gruppe: "Bindingsverk, støttekonstruksjon osv.", nummer: 232 },
        { gruppe: "Vindsperre", nummer: 231 },
        { gruppe: "Isolasjon", nummer: 232 },
        { gruppe: "Dampsperre", nummer: 231 },
        { gruppe: "Gips osv.", nummer: 232 },
        { gruppe: "Vinduer/glassfasade", nummer: 233 },
        { gruppe: "Dører", nummer: 234 },
        { gruppe: "Utvendig kledning", nummer: 235 },
        { gruppe: "Innvendige overflater og kledninger", nummer: 236 },
        { gruppe: "Solavskjerming", nummer: 237 }
      ]
    },
    {
      bygningsdel: "Innervegger",
      nummer: 24,
      produktgrupper: [
        { gruppe: "Bærende konstruksjoner", nummer: 241 },
        { gruppe: "Bindingsverk, støttekonstruksjon osv.", nummer: 242 },
        { gruppe: "Isolasjon", nummer: 241 },
        { gruppe: "Systemvegger", nummer: 243 },
        { gruppe: "Vinduer/glass", nummer: 244 },
        { gruppe: "Dører", nummer: 244 },
        { gruppe: "Innvendige overflater og kledninger", nummer: 246 }
      ]
    },
    {
      bygningsdel: "Dekker",
      nummer: 25,
      produktgrupper: [
        { gruppe: "Dekker", nummer: 251 },
        { gruppe: "Radonsperre", nummer: 252 },
        { gruppe: "Gulv/betong", nummer: 252 },
        { gruppe: "Isolasjon", nummer: 252 },
        { gruppe: "Påstøp, oppforet gulv", nummer: 253 },
        { gruppe: "Installasjonsgulv og gulvsystemer", nummer: 254 },
        { gruppe: "Nødvendig forbehandling for gulvbelegg", nummer: 255 },
        { gruppe: "Gulvbelegg, flis, parkett, maling osv.", nummer: 255 },
        { gruppe: "Himling", nummer: 256 }
      ]
    },
    {
      bygningsdel: "Yttertak",
      nummer: 26,
      produktgrupper: [
        { gruppe: "Hovedkonstruksjon", nummer: 261 },
        { gruppe: "Vindsperre", nummer: 261 },
        { gruppe: "Dampsperre", nummer: 261 },
        { gruppe: "Undertaksbelegg", nummer: 261 },
        { gruppe: "Isolasjon", nummer: 262 },
        { gruppe: "Taktekning", nummer: 263 },
        { gruppe: "Glasstak/overlys", nummer: 266 },
        { gruppe: "Himling/innvendig overflate", nummer: 267 }
      ]
    },
    {
      bygningsdel: "Trapper, balkonger m.m.",
      nummer: 28,
      produktgrupper: [
        { gruppe: "Innvendige trapper", nummer: 281 },
        { gruppe: "Belegg/overflatebehandling innvendige trapper", nummer: 281 },
        { gruppe: "Utvendige trapper", nummer: 282 },
        { gruppe: "Belegg/overflatebehandling utvendige trapper", nummer: 282 },
        { gruppe: "Balkonger/verandaer", nummer: 284 },
        { gruppe: "Tribuner og amfier", nummer: 285 }
      ]
    },
    {
      bygningsdel: "Utendørs konstruksjoner",
      nummer: 72,
      produktgrupper: [
        { gruppe: "Støttemur", nummer: 721 },
        { gruppe: "Støyskjerm", nummer: 721 },
        { gruppe: "Trapper og ramper", nummer: 722 },
        { gruppe: "Gjerder", nummer: 725 },
        { gruppe: "Støyskjerm", nummer: 725 }
      ]
    }
  ];


export { klimagassreferanser, bygningsdeler };