"""Genera StudioMargin.xlsx (v0.1). Uso: python tools/build_studiomargin.py [output.xlsx]"""
import sys
from datetime import date
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.utils import get_column_letter as L

OUT = sys.argv[1] if len(sys.argv) > 1 else "StudioMargin.xlsx"
FONT = "Arial"
def F(**k): return Font(name=FONT, size=k.pop("size", 10), **k)
NAVY = "1F3864"
HDR = PatternFill("solid", fgColor=NAVY)
INP = PatternFill("solid", fgColor="FFF2CC")      # celle da compilare
BAN = PatternFill("solid", fgColor="FCE4D6")
thin = Side(style="thin", color="BFBFBF"); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
EUR = '#,##0.00 "€";[Red]-#,##0.00 "€";"-"'
PCT = '0.0%'
BLUE = "0000FF"

wb = Workbook()

def title(ws, text, sub=None):
    ws["A1"] = text; ws["A1"].font = F(bold=True, size=14, color=NAVY)
    if sub: ws["A2"] = sub; ws["A2"].font = F(italic=True, color="595959")

def head(ws, row, labels, col=1):
    for j, t in enumerate(labels):
        c = ws.cell(row, col + j, t); c.font = F(bold=True, color="FFFFFF"); c.fill = HDR
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center"); c.border = BOX

def inp(c, v, fmt=None):
    c.value = v; c.font = F(color=BLUE); c.fill = INP; c.border = BOX
    if fmt: c.number_format = fmt

def cal(c, f, fmt=None, bold=False):
    c.value = f; c.font = F(bold=bold); c.border = BOX
    if fmt: c.number_format = fmt

def printsetup(ws, area, landscape=True):
    ws.print_area = area
    ws.page_setup.orientation = "landscape" if landscape else "portrait"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
    ws.print_options.horizontalCentered = True
    ws.page_margins.left = ws.page_margins.right = 0.5
    ws.oddHeader.center.text = "StudioMargin v0.1 - &A"
    ws.oddFooter.center.text = "Pagina &P di &N"
    ws.oddFooter.right.text = "Stampato il &D"

# ------------------------------------------------------------------ Leggimi
ws = wb.active; ws.title = "Leggimi"
lines = [
 ("StudioMargin v0.1 — tariffa oraria, preventivi, margini e cassa", "t"),
 ("Strumento gestionale per freelance e piccoli studi. Gratuito, senza macro, tutto con formule visibili.", ""),
 ("", ""),
 ("DATI DIMOSTRATIVI", "h"),
 ("Tutti i numeri presenti sono ESEMPI inventati per mostrare il funzionamento. Sostituiscili con i tuoi.", ""),
 ("", ""),
 ("Come si usa", "h"),
 ("1. Tariffa: inserisci obiettivo di compenso, costi, ore fatturabili e margine desiderato (celle gialle con testo blu).", ""),
 ("2. Preventivi: elenca le attività (fino a 12) con ore, spese esterne e maggiorazione per imprevisti. Se hai già concordato un prezzo, scrivilo in «Prezzo concordato».", ""),
 ("3. Cassa 12 mesi: indica mese iniziale, saldo di partenza e gli incassi che prevedi mese per mese (incassi = soldi in conto, non fatture emesse).", ""),
 ("4. Cruscotto: riepilogo, avvisi e due grafici. 5. Documento: preventivo stampabile per il cliente (A4, senza margini interni).", ""),
 ("", ""),
 ("Cosa NON fa (limiti dichiarati)", "h"),
 ("• Non calcola imposte, contributi previdenziali, IVA a debito o insoluti: il compenso obiettivo va inteso al lordo di imposte e contributi.", ""),
 ("• L'IVA sul foglio Documento è solo un'aliquota da te scelta (0% se non applicabile): verifica con il tuo commercialista.", ""),
 ("• Non è una consulenza fiscale o finanziaria. I risultati dipendono dalle ipotesi inserite.", ""),
 ("", ""),
 ("Formule principali", "h"),
 ("Costo pieno/ora = (compenso + costi fissi + altre spese) / ore fatturabili + costi variabili per ora.", ""),
 ("Tariffa suggerita/ora = costo pieno / (1 − margine sul prezzo).  Il margine è calcolato sul prezzo, non sul costo.", ""),
 ("Prezzo calcolato = (ore × tariffa + spese esterne) × (1 + imprevisti).  Margine = prezzo − (ore × costo pieno + spese esterne).", ""),
 ("Saldo cassa del mese = saldo precedente + incassi − uscite fisse − prelievo compenso − altre uscite.", ""),
 ("", ""),
 ("Verifiche: la cartella tests/ del repository contiene una suite che ricalcola il file e lo confronta con un modello indipendente.", ""),
]
for i, (t, k) in enumerate(lines, 1):
    c = ws.cell(i, 1, t); c.alignment = Alignment(wrap_text=True, vertical="top")
    c.font = F(bold=k in ("t", "h"), size=14 if k == "t" else 11 if k == "h" else 10, color=NAVY if k else "000000")
    if t == "DATI DIMOSTRATIVI": c.fill = BAN
ws.column_dimensions["A"].width = 120
printsetup(ws, f"A1:A{len(lines)}", landscape=False)

# ------------------------------------------------------------------ Tariffa
t = wb.create_sheet("Tariffa")
title(t, "Tariffa oraria sostenibile", "DATI DIMOSTRATIVI — sostituisci le celle gialle con i tuoi dati")
t["A2"].fill = BAN
head(t, 4, ["Voce", "Valore", "Note"])
rows = [
 ("Compenso annuo obiettivo (€)", 36000, EUR, "Quanto vuoi guadagnare in un anno, al lordo di imposte e contributi"),
 ("Costi fissi annui (€)", 4800, EUR, "Software, assicurazioni, commercialista, cassa previdenziale minima, ecc."),
 ("Altre spese annue (€)", 1200, EUR, "Formazione, attrezzature, trasferte non addebitabili"),
 ("Ore annue fatturabili", 1000, '#,##0', "Ore vendibili, non ore lavorate complessive (tipico: 50–70% del tempo)"),
 ("Costi variabili per ora (€)", 2, EUR, "Costi che crescono con le ore lavorate"),
 ("Margine desiderato sul prezzo (%)", 0.15, PCT, "Quota del prezzo che resta dopo tutti i costi (0–95%)"),
]
for i, (lab, v, fmt, note) in enumerate(rows):
    r = 5 + i
    t.cell(r, 1, lab).font = F(); t.cell(r, 1).border = BOX
    inp(t.cell(r, 2), v, fmt); t.cell(r, 3, note).font = F(italic=True, color="595959")
t["A12"] = "Controllo input"; t["A12"].font = F(bold=True)
cal(t["B12"], '=IF(B8<=0,"ERRORE: le ore fatturabili devono essere > 0",IF(OR(B10<0,B10>=1),"ERRORE: il margine deve essere tra 0% e 95%","OK"))', bold=True)
t["A13"] = "Costo pieno / ora (€)"; t["A13"].font = F(bold=True)
cal(t["B13"], "=IF(B8>0,(B5+B6+B7)/B8+B9,0)", EUR, bold=True)
t["A14"] = "Tariffa suggerita / ora (€)"; t["A14"].font = F(bold=True)
cal(t["B14"], "=IF(AND(B8>0,B10>=0,B10<1),B13/(1-B10),0)", EUR, bold=True)
t["C13"] = "Formula: (compenso + costi fissi + altre spese) / ore + costi variabili"; t["C14"] = "Formula: costo pieno / (1 − margine)"
for a in ("C13", "C14"): t[a].font = F(italic=True, color="595959")
dv = DataValidation(type="decimal", operator="greaterThan", formula1="0", showErrorMessage=True, errorTitle="Valore non valido", error="Inserisci un numero maggiore di 0")
t.add_data_validation(dv); dv.add("B8")
dv2 = DataValidation(type="decimal", operator="between", formula1="0", formula2="0.95", showErrorMessage=True, errorTitle="Margine non valido", error="Inserisci un valore tra 0% e 95%")
t.add_data_validation(dv2); dv2.add("B10")
dv3 = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", showErrorMessage=True, error="Inserisci un valore >= 0")
t.add_data_validation(dv3); dv3.add("B5:B7"); dv3.add("B9")
t.conditional_formatting.add("B12", FormulaRule(formula=['LEFT($B$12,6)="ERRORE"'], font=Font(name=FONT, bold=True, color="C00000"), fill=PatternFill("solid", bgColor="F8CBAD")))
t.column_dimensions["A"].width = 38; t.column_dimensions["B"].width = 22; t.column_dimensions["C"].width = 75
printsetup(t, "A1:C14")

# ------------------------------------------------------------------ Preventivi
p = wb.create_sheet("Preventivi")
title(p, "Preventivi e margini per attività", "DATI DIMOSTRATIVI — fino a 12 attività. «Prezzo concordato» è facoltativo e sostituisce il prezzo calcolato")
p["A2"].fill = BAN
head(p, 4, ["Attività", "Ore", "Spese esterne (€)", "Imprevisti (% sul prezzo)", "Prezzo concordato (€, facoltativo)",
            "Prezzo calcolato (€)", "Prezzo finale (€)", "Costo pieno (€)", "Margine (€)", "Margine (%)", "Stato"])
p.row_dimensions[4].height = 44
demo = [("Consulenza A", 18, 0, 0, None), ("Progetto B", 32, 150, 0.10, None), ("Analisi C", 12, 0, 0.05, None), ("Revisione D", 8, 40, 0, 300)]
R0, R1 = 5, 16
for r in range(R0, R1 + 1):
    d = demo[r - R0] if r - R0 < len(demo) else (None, None, None, None, None)
    inp(p.cell(r, 1), d[0]); inp(p.cell(r, 2), d[1], '#,##0.0'); inp(p.cell(r, 3), d[2], EUR)
    inp(p.cell(r, 4), d[3], PCT); inp(p.cell(r, 5), d[4], EUR)
    cal(p.cell(r, 6), f'=IF($A{r}="","",($B{r}*Tariffa!$B$14+$C{r})*(1+$D{r}))', EUR)
    cal(p.cell(r, 7), f'=IF($A{r}="","",IF($E{r}<>"",$E{r},$F{r}))', EUR)
    cal(p.cell(r, 8), f'=IF($A{r}="","",$B{r}*Tariffa!$B$13+$C{r})', EUR)
    cal(p.cell(r, 9), f'=IF($A{r}="","",$G{r}-$H{r})', EUR)
    cal(p.cell(r, 10), f'=IF($A{r}="","",IF($G{r}>0,$I{r}/$G{r},0))', PCT)
    cal(p.cell(r, 11), f'=IF($A{r}="","",IF($I{r}<0,"IN PERDITA",IF($J{r}<Tariffa!$B$10,"Sotto margine obiettivo","OK")))')
T = R1 + 1  # riga totali
p.cell(T, 1, "TOTALE").font = F(bold=True)
for col in (2, 3, 6, 7, 8, 9):
    cal(p.cell(T, col), f"=SUM({L(col)}{R0}:{L(col)}{R1})", EUR if col != 2 else '#,##0.0', bold=True)
cal(p.cell(T, 10), f"=IF(G{T}>0,I{T}/G{T},0)", PCT, bold=True)
dvp = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", showErrorMessage=True, error="Inserisci un valore >= 0")
p.add_data_validation(dvp); dvp.add(f"B{R0}:C{R1}"); dvp.add(f"E{R0}:E{R1}")
dvp2 = DataValidation(type="decimal", operator="between", formula1="0", formula2="1", showErrorMessage=True, error="Inserisci una percentuale tra 0% e 100%")
p.add_data_validation(dvp2); dvp2.add(f"D{R0}:D{R1}")
red = PatternFill("solid", bgColor="F8CBAD"); amb = PatternFill("solid", bgColor="FFE699"); grn = PatternFill("solid", bgColor="C6E0B4")
p.conditional_formatting.add(f"K{R0}:K{R1}", FormulaRule(formula=[f'$K{R0}="IN PERDITA"'], fill=red))
p.conditional_formatting.add(f"K{R0}:K{R1}", FormulaRule(formula=[f'$K{R0}="Sotto margine obiettivo"'], fill=amb))
p.conditional_formatting.add(f"K{R0}:K{R1}", FormulaRule(formula=[f'$K{R0}="OK"'], fill=grn))
for col, w in zip("ABCDEFGHIJK", [28, 9, 16, 16, 20, 17, 17, 16, 15, 12, 26]): p.column_dimensions[col].width = w
p.freeze_panes = "B5"
printsetup(p, f"A1:K{T}")

# ------------------------------------------------------------------ Cassa 12 mesi
c = wb.create_sheet("Cassa12m")
title(c, "Previsione di cassa a 12 mesi", "DATI DIMOSTRATIVI — gli incassi sono entrate effettive in conto, non fatture emesse")
c["A2"].fill = BAN
c["A3"] = "Mese iniziale"; inp(c["B3"], date(2026, 12, 1), "mmm yyyy")
c["A4"] = "Saldo iniziale in conto (€)"; inp(c["B4"], 1500, EUR)
c["A5"] = "Includi prelievo compenso (1 = sì, 0 = no)"; inp(c["B5"], 1, "0")
for a in ("A3", "A4", "A5"): c[a].font = F(bold=True)
head(c, 7, ["Voce"] + [None] * 12 + ["Totale"])
for k in range(12):
    cell = c.cell(7, 2 + k, f"=DATE(YEAR($B$3),MONTH($B$3)+{k},1)"); cell.number_format = "mmm yy"
    cell.font = F(bold=True, color="FFFFFF"); cell.fill = HDR; cell.alignment = Alignment(horizontal="center"); cell.border = BOX
labels = ["Incassi previsti (€)", "Uscite fisse (costi fissi + altre spese, €)", "Prelievo compenso (€)", "Altre uscite (€)", "Saldo di fine mese (€)", "Mese in negativo"]
for i, lab in enumerate(labels):
    c.cell(8 + i, 1, lab).font = F(bold=(i == 4)); c.cell(8 + i, 1).border = BOX
incassi = [3000, 4200, 2500, 3800, 5200, 3000, 2000, 4500, 3800, 4000, 3500, 5000]
altre = [0, 0, 600, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for k in range(12):
    col = 2 + k; X = L(col)
    inp(c.cell(8, col), incassi[k], EUR)
    cal(c.cell(9, col), "=(Tariffa!$B$6+Tariffa!$B$7)/12", EUR)
    cal(c.cell(10, col), "=Tariffa!$B$5/12*$B$5", EUR)
    inp(c.cell(11, col), altre[k], EUR)
    prev = "$B$4" if k == 0 else f"{L(col-1)}12"
    cal(c.cell(12, col), f"={prev}+{X}8-{X}9-{X}10-{X}11", EUR, bold=True)
    cal(c.cell(13, col), f'=IF({X}12<0,{X}7,"")', "mmm yy")
for r in (8, 9, 10, 11):
    cal(c.cell(r, 14), f"=SUM(B{r}:M{r})", EUR, bold=True)
c["A15"] = "Saldo minimo (€)"; cal(c["B15"], "=MIN(B12:M12)", EUR, bold=True)
c["A16"] = "Mese del saldo minimo"; cal(c["B16"], "=INDEX(B7:M7,MATCH(B15,B12:M12,0))", "mmm yy", bold=True)
c["A17"] = "Mesi con saldo negativo"; cal(c["B17"], '=COUNTIF(B12:M12,"<0")', "0", bold=True)
c["A18"] = "Primo mese in negativo"; cal(c["B18"], '=IF(COUNT(B13:M13)=0,"nessuno",MIN(B13:M13))', "mmm yy", bold=True)
for a in ("A15", "A16", "A17", "A18"): c[a].font = F(bold=True)
c.conditional_formatting.add("B12:M12", FormulaRule(formula=["B12<0"], fill=red, font=Font(name=FONT, bold=True, color="C00000")))
c.column_dimensions["A"].width = 44
for k in range(2, 15): c.column_dimensions[L(k)].width = 11.5
c.column_dimensions["N"].width = 14
c.freeze_panes = "B8"
printsetup(c, "A1:N18")

# ------------------------------------------------------------------ Cruscotto
d = wb.create_sheet("Cruscotto", 1)
title(d, "Cruscotto", "DATI DIMOSTRATIVI — i valori seguono quanto inserito negli altri fogli")
d["A2"].fill = BAN
kp = [
 ("Controllo input tariffa", "=Tariffa!B12", None),
 ("Costo pieno / ora", "=Tariffa!B13", EUR),
 ("Tariffa suggerita / ora", "=Tariffa!B14", EUR),
 ("Ricavi preventivati", f"=Preventivi!G{T}", EUR),
 ("Costo pieno preventivato", f"=Preventivi!H{T}", EUR),
 ("Margine preventivato", f"=Preventivi!I{T}", EUR),
 ("Margine sul prezzo", f"=Preventivi!J{T}", PCT),
 ("Attività sotto il margine obiettivo o in perdita", f'=COUNTIF(Preventivi!K{R0}:K{R1},"IN PERDITA")+COUNTIF(Preventivi!K{R0}:K{R1},"Sotto margine obiettivo")', "0"),
 ("Saldo minimo di cassa", "=Cassa12m!B15", EUR),
 ("Mese del saldo minimo", "=Cassa12m!B16", "mmm yy"),
 ("Mesi con saldo negativo", "=Cassa12m!B17", "0"),
]
head(d, 4, ["Indicatore", "Valore"])
for i, (lab, f, fmt) in enumerate(kp):
    r = 5 + i
    d.cell(r, 1, lab).font = F(); d.cell(r, 1).border = BOX
    cal(d.cell(r, 2), f, fmt, bold=True); d.cell(r, 2).alignment = Alignment(horizontal="right")
d.conditional_formatting.add("B5", FormulaRule(formula=['LEFT($B$5,6)="ERRORE"'], font=Font(name=FONT, bold=True, color="C00000")))
d.conditional_formatting.add("B12", FormulaRule(formula=["$B$12>0"], fill=amb))
d.conditional_formatting.add("B13:B15", FormulaRule(formula=["$B$13<0"], fill=red))
d.conditional_formatting.add("B15", FormulaRule(formula=["$B$15>0"], fill=red))
ch = BarChart(); ch.type = "col"; ch.title = "Margine per attività (€)"; ch.style = 10
ch.add_data(Reference(p, min_col=9, min_row=4, max_row=R1), titles_from_data=True)
ch.set_categories(Reference(p, min_col=1, min_row=R0, max_row=R1))
ch.y_axis.title = "€"; ch.x_axis.title = "Attività"; ch.legend = None
ch.x_axis.delete = False; ch.y_axis.delete = False; ch.height = 8; ch.width = 15
ch.x_axis.tickLblPos = "low"; ch.y_axis.number_format = "#,##0"
d.add_chart(ch, "D4")
lc = LineChart(); lc.title = "Saldo di cassa a fine mese (€)"; lc.style = 12
lc.add_data(Reference(c, min_col=1, max_col=13, min_row=12), titles_from_data=True, from_rows=True)
lc.set_categories(Reference(c, min_col=2, max_col=13, min_row=7))
lc.y_axis.title = "€"; lc.x_axis.title = "Mese"; lc.legend = None; lc.x_axis.number_format = "mmm yy"
lc.x_axis.delete = False; lc.y_axis.delete = False; lc.height = 8; lc.width = 15
lc.y_axis.number_format = "#,##0"; lc.x_axis.tickLblPos = "low"
for sr in lc.series: sr.smooth = False
d.add_chart(lc, "D21")
d["A18"] = "Nota: strumento gestionale, non include imposte, contributi, IVA a debito o insoluti."; d["A18"].font = F(italic=True, color="595959")
d.column_dimensions["A"].width = 46; d.column_dimensions["B"].width = 22
printsetup(d, "A1:M38")

# ------------------------------------------------------------------ Documento (preventivo stampabile)
q = wb.create_sheet("Documento")
q["A1"] = "PREVENTIVO"; q["A1"].font = F(bold=True, size=18, color=NAVY)
fields = [("Mittente", "Il tuo nome o studio", None), ("Preventivo n.", "2026-001", None), ("Data", date(2026, 12, 1), "dd/mm/yyyy"),
          ("Cliente", "Nome del cliente", None), ("Oggetto", "Descrizione sintetica del lavoro", None),
          ("Validità (giorni)", 30, "0"), ("Aliquota IVA (%) — 0 se non applicabile", 0.22, PCT)]
for i, (lab, v, fmt) in enumerate(fields):
    r = 3 + i
    q.cell(r, 1, lab).font = F(bold=True); inp(q.cell(r, 2), v, fmt)
    q.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
head(q, 11, ["Descrizione", "Ore", "Importo (€)"], col=1)
for k in range(12):
    r = 12 + k; s = R0 + k
    cal(q.cell(r, 1), f'=IF(Preventivi!A{s}="","",Preventivi!A{s})')
    cal(q.cell(r, 2), f'=IF(Preventivi!A{s}="","",Preventivi!B{s})', '#,##0.0')
    cal(q.cell(r, 3), f'=IF(Preventivi!A{s}="","",Preventivi!G{s})', EUR)
q["A25"] = "Imponibile"; cal(q["C25"], "=SUM(C12:C23)", EUR, bold=True)
q["A26"] = "IVA"; cal(q["C26"], "=C25*B9", EUR)
q["A27"] = "Totale"; cal(q["C27"], "=C25+C26", EUR, bold=True)
for a in ("A25", "A26", "A27"): q[a].font = F(bold=True)
q["A29"] = "Gli importi includono eventuali spese esterne. Preventivo non vincolante oltre la validità indicata. Condizioni di pagamento da definire con il cliente."
q["A29"].font = F(italic=True, size=9, color="595959"); q["A29"].alignment = Alignment(wrap_text=True, vertical="top")
q.merge_cells("A29:C30")
q.column_dimensions["A"].width = 48; q.column_dimensions["B"].width = 12; q.column_dimensions["C"].width = 20; q.column_dimensions["D"].width = 18
printsetup(q, "A1:C30", landscape=False)

wb.save(OUT)
print("salvato", OUT)
