# Piano d'azione — Sfida 1 € → 64 raddoppi (versione 2, 05/11/2026)

Legenda: **[F]** fatto con fonte · **[I]** inferenza · **[S]** stima con ipotesi dichiarate · **[O]** opinione di Claude.
Questo documento non è consulenza fiscale o legale: i punti marcati «da confermare» vanno verificati per iscritto con il commercialista.

## 1. Cosa è cambiato

Il commercialista indica che, almeno all'inizio, conviene vendere tramite piattaforme esterne e **non usare la partita IVA** del proprietario per queste vendite.

Conseguenze sul piano:

1. **Niente checkout proprio e niente Stripe in conto proprio.** Con un processore di pagamento diretto il venditore resta responsabile di IVA e adempimenti. Si usano solo piattaforme che fanno da *merchant of record* (MoR), cioè che risultano venditrici verso il cliente e gestiscono IVA e fatturazione ai clienti finali. [F: Fungies, Paddle docs, Gumroad]
2. **Il reddito resta da dichiarare.** Il MoR non toglie l'obbligo di dichiarare ciò che si incassa. [F: topbubbleindex, fonte secondaria] Il trattamento fiscale e previdenziale dei payout va definito con il commercialista.
3. **Un nuovo vincolo di processo:** i raddoppi non dipendono più solo dal mercato, ma anche dal fatto che l'attività resti qualificabile come occasionale (vedi §3).

## 2. Piattaforme: cosa risulta verificato

| Piattaforma | MoR | Costo dichiarato | Note rilevanti | Giudizio [O] |
|---|---|---|---|---|
| **Gumroad** | Sì, dal 1/1/2025 [F: gumroad.com/pricing] | 10% + 0,50 $ (30% se il cliente arriva dal marketplace Discover) [F] | Pagamenti con carta: minimo 100 $, blocco di 7 giorni, revisione al primo payout [F: cartmango, singola recensione] | **Prima scelta** per semplicità; attenzione ai tempi di payout |
| **Lemon Squeezy** | Sì | 5% + 0,50 $ [F] | Di proprietà di Stripe; a gennaio 2026 il CEO ha ammesso supporto più lento e aggiornamenti meno frequenti, con migrazione verso Stripe Managed Payments [F: blog ufficiale, dodopayments] | Sconsigliata per un account nuovo |
| **Stripe Managed Payments** | Sì | Tariffe Stripe + circa 3,5% [F debole: blog di terzi] | Anteprima pubblica da febbraio 2026; disponibilità per un privato italiano non verificata | Da valutare dopo |
| **Paddle** | Sì | 5% + 0,50 $ [F] | Richiede sito proprio e verifica di più giorni; orientata a SaaS [F: easy.tools] | Seconda scelta, più burocratica |
| **Polar** | Sì | Non verificato | Solo prodotti digitali, non servizi umani [F: docs.polar.sh] | Da verificare |
| Payhip | No: gestisce l'IVA UE/UK solo in parte e il venditore resta il merchant [F: fungies, wearefounders] | — | — | **Esclusa** dal vincolo |
| Etsy | Non verificato | — | — | **Esclusa finché non verificata** |

**Cosa serve da te, e non posso fare io:** aprire l'account a tuo nome (non con la partita IVA), completare la verifica di identità, scegliere il metodo di payout e collegare il conto. Sono atti con implicazioni fiscali e contrattuali, quindi richiedono la tua approvazione e il tuo accesso.

## 3. Il vincolo che il parere introduce

- **[F]** Il lavoro autonomo occasionale richiede assenza di abitualità e professionalità; la soglia di 5.000 € annui riguarda l'obbligo di iscrizione alla Gestione Separata INPS e opera solo se l'attività è già qualificabile come occasionale. [F: pmi.it; fiscozen; circolare INPS 103/2004]
- **[F debole]** Una fonte divulgativa segnala che un catalogo sempre disponibile con ordini ricorrenti può essere considerato abituale anche sotto i 5.000 € annui. [centrofiscale.com]
- **[I]** Un prodotto a catalogo con vendite ripetute somiglia proprio a questo schema. Non è una conclusione legale: è il motivo per cui chiedo al commercialista una conferma scritta delle condizioni in cui il suo parere resta valido.
- **[I, aritmetica]** Con i raddoppi, la casella 12 vale 4.096 € e la casella 13 vale 8.192 €: la soglia di 5.000 € si supera proprio in corrispondenza della casella 13. Il capitale non coincide col reddito annuo, ma l'ordine di grandezza dice che il tema fiscale diventa concreto molto prima della casella 20.
- **[Ipotesi prudente]** Va assunto che i payout siano tracciabili dalle autorità fiscali. Un blog di parte (creem.io) lo collega alla normativa DAC8, ma non ho verificato la norma esatta, quindi non la cito come fondamento.

### Domande da porre per iscritto al commercialista

1. Con quale qualificazione vanno trattati i payout di una piattaforma MoR (lavoro autonomo occasionale, altro) e con quali adempimenti?
2. Oltre quale volume o frequenza il parere decade e serve la partita IVA? Il reddito di riferimento è al lordo o al netto dei costi?
3. L'aliquota di accantonamento da applicare ai payout, per stimare il saldo netto del ledger.
4. L'attività ha implicazioni di compatibilità con il tuo lavoro attuale o con la tua partita IVA esistente?

**Cancello fiscale proposto [O]:** prima di arrivare a circa 4.000 € di incassi annui da queste attività (vicini alla casella 12), si ferma l'espansione e si rivede l'inquadramento col commercialista.

## 4. Confronto delle opzioni di prodotto

| Criterio | A. StudioMargin generico | B. Template tecnico NTC/Eurocodici | C. Parcella DM 17/6/2016 | D. Servizi su richiesta |
|---|---|---|---|---|
| Domanda dimostrata | Debole | Debole | Debole | Non valutata |
| Prezzo di mercato rilevato | Excel generici: mediana 4,70 $ su Etsy (luglio 2026, singolo autore) | Fogli singoli semplici 3–7 CA$, calcolatori e pacchetti 29–68 CA$ su Etsy; 17–29 $ su Selar; prevalentemente per norme USA/UK | Strumento online gratuito già esistente | — |
| Concorrenza | Molta | Offerta gratuita italiana (es. ZNE.IT con 250+ calcolatori) e fogli allegati a libri | Strumento gratuito di professionearchitetto.it; normativa in revisione | — |
| Responsabilità | Bassa | **Alta**: errori di calcolo in un contesto professionale | Media | Media |
| Conflitti | Nessuno noto | Possibile con il tuo ufficio (proprietà intellettuale, tempo, risorse) | Nessuno noto | **Richiede partita IVA**: incompatibile col parere |
| Tempo per l'MVP | Fatto (v0.1) | Settimane, con validazione tecnica | Settimane, con rischio di aggiornamenti | — |
| Verdetto [O] | **Veicolo per le prime caselle** | Rimandare finché non risolti responsabilità e proprietà | Scartare per ora | Escludere |

Le fonti: [Etsy "structural engineering excel sheets"](https://www.etsy.com/it/listing/4572289337/structural-engineering-excel-sheets), [Selar RCC spreadsheets](https://selar.com/33wr82670a), [ZNE.IT](https://pasqualepillitteri.it/news/519/zne-it-tool-calcolo-gratuiti-ingegneri-professionisti), [professionearchitetto.it](https://www.professionearchitetto.it/tools/parametri/), [Ediltecnico sul nuovo decreto](https://ediltecnico.it/calcolo-parcella-servizi-ingegneria-e-architettura/), [CartMango prezzi Etsy](https://cartmango.com/sell-excel-templates/).

**Conclusione [O]:** nessuna opzione ha una domanda dimostrata; la più economica da provare è StudioMargin, già costruito e testato. Non c'è un'evidenza che renda migliore un'altra strada. Cambierei idea se emergessero richieste spontanee di un prodotto tecnico preciso.

## 5. Prezzo e numeri

Ipotesi **[S]**: Gumroad 10% + 0,50 $, più pagamento 2,9% + 0,30 $ come in un'analisi di terzi; cambio dollaro/euro, IVA e imposte non modellati.

| Prezzo | Netto per vendita | Vendite per la casella 1 | casella 4 | casella 7 | casella 10 | casella 12 |
|---|---|---|---|---|---|---|
| 9 € | 7,04 | 1 | 3 | 19 | 146 | 582 |
| 12 € | 9,65 | 1 | 2 | 14 | 106 | 425 |
| 15 € | 12,27 | 1 | 2 | 11 | 84 | 334 |

Le vendite sono cumulate, senza reinvestimento e senza imposte; con le imposte i numeri salgono. **[O]** Un prezzo sotto 10 € lascia troppo ai costi fissi; la fascia 12–15 € è coerente con i prezzi di fogli tecnici, ma non con quelli dei template generici.

## 6. Punti ciechi

- **Pubblico:** non c'è nessun canale che porti persone alla pagina. Senza traffico, il collo di bottiglia è la distribuzione, non il prodotto. Il canale più realistico è la tua rete professionale, usata da te in prima persona e senza invii di massa.
- **Primo incasso:** con Gumroad un payout con carta può richiedere almeno 100 $ e 7 giorni. Per il ledger «verificato» significa che l'incasso si considera tale quando arriva sul conto.
- **Dipendenza dalla piattaforma:** account sospesi o trattenute sono possibili; i fondi stanno presso la piattaforma finché non vengono pagati.
- **Il capitale da 1 €:** con piattaforme senza costi fissi può restare non speso; resta da confermare che sia stato effettivamente accantonato.
- **Qualità dei dati:** i prezzi di mercato citati vengono da singole analisi o inserzioni, non da vendite.

## 7. Prossimi passi

| # | Azione | Chi | Cancello |
|---|---|---|---|
| 1 | Scrivere al commercialista le 4 domande di §3 e ottenere risposta per iscritto | Proprietario | Prima del primo incasso |
| 2 | Aprire account Gumroad a nome personale, verifica identità, scelta payout | Proprietario | Approvazione esplicita |
| 3 | Aprire il file Excel in Microsoft Excel e controllare grafici e stampa | Proprietario | Prima della messa in vendita |
| 4 | Verificare la pagina pubblicata su GitHub Pages | Proprietario | — |
| 5 | Riposizionare StudioMargin per i liberi professionisti tecnici, scheda prodotto, bozza della pagina di vendita, informativa | Claude | Senza pubblicare il link di acquisto |
| 6 | Prodotto gratuito «calcolatore» nel browser come esca di interesse | Claude | Misure solo da richieste spontanee |
| 7 | Attivare il link di acquisto e fissare il prezzo | Proprietario | Dopo 1 e 2 |

## 8. Cosa mi farebbe cambiare conclusione

- Un parere scritto che non consenta nemmeno il primo incasso senza partita IVA: il piano si ferma alla fase gratuita.
- Richieste spontanee di un prodotto tecnico preciso: si apre l'opzione B, risolti prima responsabilità e conflitti.
- Evidenza che un account nuovo italiano non riceva payout su una piattaforma MoR: cambia la scelta della piattaforma.
