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

  const resultList = [
    { bygningsdel: 'Grunn og fundamenter', 'A1-A3': 300, 'A4': 150, 'B4': 75, 'B5': 75, 'C': 200, total: 0, andel: '0%' },
    { bygningsdel: 'Yttervegger', 'A1-A3': 250, 'A4': 125, 'B4': 60, 'B5': 60, 'C': 180, total: 0, andel: '0%' },
    { bygningsdel: 'Innervegger', 'A1-A3': 220, 'A4': 110, 'B4': 55, 'B5': 55, 'C': 160, total: 0, andel: '0%' },
    { bygningsdel: 'Dekker', 'A1-A3': 200, 'A4': 100, 'B4': 50, 'B5': 50, 'C': 150, total: 0, andel: '0%' },
    { bygningsdel: 'Yttertak', 'A1-A3': 280, 'A4': 140, 'B4': 70, 'B5': 70, 'C': 210, total: 0, andel: '0%' },
    { bygningsdel: 'Trapper, balkonger m.m.', 'A1-A3': 160, 'A4': 80, 'B4': 40, 'B5': 40, 'C': 120, total: 0, andel: '0%' },
    { bygningsdel: 'Utendørs konstruksjoner', 'A1-A3': 100, 'A4': 50, 'B4': 25, 'B5': 25, 'C': 75, total: 0, andel: '0%' },
    { bygningsdel: 'Totalt', 'A1-A3': 0, 'A4': 0, 'B4': 0, 'B5': 0, 'C': 0, total: 0, andel: '0%' }
  ]

export { klimagassreferanser, bygningsdeler };