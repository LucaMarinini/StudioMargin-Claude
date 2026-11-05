"""Suite di test per StudioMargin.xlsx.
Ricalcola copie del file con LibreOffice, confronta con un modello Python indipendente e prova casi limite.
Uso:  python tests/test_studiomargin.py [StudioMargin.xlsx]
Variabile opzionale RECALC_SCRIPT = percorso di uno script che ricalcola il file in place (altrimenti soffice)."""
import os, shutil, subprocess, sys, tempfile, zipfile, math
from datetime import date
from openpyxl import load_workbook

SRC = sys.argv[1] if len(sys.argv) > 1 else "StudioMargin.xlsx"
RESULTS = []

def recalc(path):
    s = os.environ.get("RECALC_SCRIPT")
    if s:
        subprocess.run([sys.executable, s, path, "90"], check=True, capture_output=True)
    else:
        out = tempfile.mkdtemp()
        subprocess.run(["soffice", "--headless", "--convert-to", "xlsx", "--outdir", out, path], check=True, capture_output=True)
        shutil.move(os.path.join(out, os.path.basename(path)), path)

def scenario(mods):
    """mods: {(foglio, cella): valore}. Ritorna workbook ricalcolato (data_only)."""
    d = tempfile.mkdtemp(); f = os.path.join(d, "t.xlsx")
    wb = load_workbook(SRC)
    for (sh, ce), v in mods.items(): wb[sh][ce] = v
    wb.save(f); recalc(f)
    return load_workbook(f, data_only=True)

def close(a, b, tol=1e-6): return a is not None and b is not None and abs(a - b) <= tol * max(1, abs(b))

def check(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail)); print(("PASS " if cond else "FAIL ") + name + (f"  [{detail}]" if detail and not cond else ""))

# ---- modello indipendente
def model(inp, acts, cash):
    ore = inp["ore"]
    ok = ore > 0 and 0 <= inp["marg"] < 1
    costo = (inp["comp"] + inp["fissi"] + inp["altre"]) / ore + inp["var"] if ore > 0 else 0
    tar = costo / (1 - inp["marg"]) if ok else 0
    rows = []
    for a in acts:
        calc = (a["ore"] * tar + a["spese"]) * (1 + a["imp"])
        fin = a["conc"] if a["conc"] is not None else calc
        c = a["ore"] * costo + a["spese"]
        rows.append(dict(calc=calc, fin=fin, costo=c, marg=fin - c, pct=(fin - c) / fin if fin > 0 else 0))
    saldo, saldi = cash["iniz"], []
    for k in range(12):
        saldo = saldo + cash["inc"][k] - (inp["fissi"] + inp["altre"]) / 12 - inp["comp"] / 12 * cash["prel"] - cash["oth"][k]
        saldi.append(saldo)
    return dict(ok=ok, costo=costo, tar=tar, rows=rows, saldi=saldi)

BASE_INP = dict(comp=36000, fissi=4800, altre=1200, ore=1000, var=2, marg=0.15)
BASE_ACTS = [dict(ore=18, spese=0, imp=0, conc=None), dict(ore=32, spese=150, imp=.10, conc=None),
             dict(ore=12, spese=0, imp=.05, conc=None), dict(ore=8, spese=40, imp=0, conc=300)]
BASE_CASH = dict(iniz=1500, prel=1, inc=[3000, 4200, 2500, 3800, 5200, 3000, 2000, 4500, 3800, 4000, 3500, 5000],
                 oth=[0, 0, 600, 0, 0, 0, 0, 0, 0, 0, 0, 0])

def compare(wb, m, tag):
    t, p, c = wb["Tariffa"], wb["Preventivi"], wb["Cassa12m"]
    check(f"{tag}: costo pieno/ora", close(t["B13"].value, m["costo"]), f'{t["B13"].value} vs {m["costo"]}')
    check(f"{tag}: tariffa suggerita", close(t["B14"].value, m["tar"]), f'{t["B14"].value} vs {m["tar"]}')
    for i, r in enumerate(m["rows"]):
        row = 5 + i
        ok = all(close(p.cell(row, col).value, v) for col, v in ((6, r["calc"]), (7, r["fin"]), (8, r["costo"]), (9, r["marg"]), (10, r["pct"])))
        check(f"{tag}: preventivo riga {i+1}", ok, str([p.cell(row, k).value for k in range(6, 11)]))
    tot = sum(r["fin"] for r in m["rows"])
    check(f"{tag}: totale ricavi", close(p["G17"].value, tot), f'{p["G17"].value} vs {tot}')
    check(f"{tag}: saldi cassa 12 mesi", all(close(c.cell(12, 2 + k).value, m["saldi"][k]) for k in range(12)))
    check(f"{tag}: saldo minimo", close(c["B15"].value, min(m["saldi"])))
    check(f"{tag}: mesi negativi", c["B17"].value == sum(1 for s in m["saldi"] if s < 0))

# ---- 1. scenario base
wb = scenario({})
compare(wb, model(BASE_INP, BASE_ACTS, BASE_CASH), "base")
check("base: controllo input = OK", wb["Tariffa"]["B12"].value == "OK")
check("base: attività 'Revisione D' segnalata IN PERDITA", wb["Preventivi"]["K8"].value == "IN PERDITA")
check("base: attività A–C 'OK'", [wb["Preventivi"][f"K{r}"].value for r in (5, 6, 7)] == ["OK"] * 3)
check("base: cruscotto conta 1 attività critica", wb["Cruscotto"]["B12"].value == 1)

# ---- 2. errori di input
w = scenario({("Tariffa", "B8"): 0})
check("ore=0: messaggio di errore", str(w["Tariffa"]["B12"].value).startswith("ERRORE"))
check("ore=0: tariffa e costo = 0 (niente #DIV/0)", w["Tariffa"]["B13"].value == 0 and w["Tariffa"]["B14"].value == 0)
w = scenario({("Tariffa", "B10"): 1})
check("margine=100%: errore segnalato e tariffa 0", str(w["Tariffa"]["B12"].value).startswith("ERRORE") and w["Tariffa"]["B14"].value == 0)
w = scenario({("Tariffa", "B10"): 0})
check("margine=0: tariffa = costo pieno", close(w["Tariffa"]["B14"].value, w["Tariffa"]["B13"].value))

# ---- 3. parametri alterati vs modello
inp2 = dict(BASE_INP, comp=60000, fissi=9000, altre=0, ore=1200, var=5, marg=0.30)
w = scenario({("Tariffa", "B5"): 60000, ("Tariffa", "B6"): 9000, ("Tariffa", "B7"): 0, ("Tariffa", "B8"): 1200, ("Tariffa", "B9"): 5, ("Tariffa", "B10"): 0.30})
compare(w, model(inp2, BASE_ACTS, BASE_CASH), "parametri alterati")

# ---- 4. prezzo concordato e spese
acts3 = [dict(ore=10, spese=500, imp=0.2, conc=None), dict(ore=0, spese=100, imp=0, conc=250)]
w = scenario({("Preventivi", "A5"): "X", ("Preventivi", "B5"): 10, ("Preventivi", "C5"): 500, ("Preventivi", "D5"): 0.2, ("Preventivi", "E5"): None,
              ("Preventivi", "A6"): "Y", ("Preventivi", "B6"): 0, ("Preventivi", "C6"): 100, ("Preventivi", "D6"): 0, ("Preventivi", "E6"): 250,
              ("Preventivi", "A7"): None, ("Preventivi", "A8"): None})
m3 = model(BASE_INP, acts3, BASE_CASH)
check("spese+imprevisti: riga 1", close(w["Preventivi"]["G5"].value, m3["rows"][0]["fin"]))
check("prezzo concordato con 0 ore", close(w["Preventivi"]["G6"].value, 250) and close(w["Preventivi"]["I6"].value, 150))
check("totale = somma finali", close(w["Preventivi"]["G17"].value, m3["rows"][0]["fin"] + 250))

# ---- 5. nessuna attività
w = scenario({("Preventivi", f"A{r}"): None for r in range(5, 17)})
pv = w["Preventivi"]
check("0 attività: totali 0 e margine % 0 (niente #DIV/0)", pv["G17"].value == 0 and pv["J17"].value == 0)
check("0 attività: cruscotto senza errori", all(not str(w["Cruscotto"].cell(r, 2).value).startswith("#") for r in range(5, 16)))

# ---- 6. cassa negativa
w = scenario({("Cassa12m", "B4"): 0, **{("Cassa12m", f"{c}8"): 0 for c in "BCDEFGHIJKLM"}})
cs = w["Cassa12m"]
check("incassi 0: 12 mesi in negativo", cs["B17"].value == 12)
check("incassi 0: primo mese negativo = mese iniziale", cs["B18"].value == date(2026, 12, 1) or str(cs["B18"].value).startswith("2026-12-01"))
w = scenario({("Cassa12m", "B5"): 0})
mc = model(BASE_INP, BASE_ACTS, dict(BASE_CASH, prel=0))
check("senza prelievo compenso: saldi", all(close(w["Cassa12m"].cell(12, 2 + k).value, mc["saldi"][k]) for k in range(12)))
check("calendario: 12 mesi consecutivi da dic 2026", str(wb["Cassa12m"]["M7"].value).startswith("2027-11-01") and str(wb["Cassa12m"]["C7"].value).startswith("2027-01-01"))

# ---- 7. documento stampabile
dc = wb["Documento"]
check("documento: righe coerenti con preventivi", close(dc["C12"].value, wb["Preventivi"]["G5"].value) and dc["A12"].value == "Consulenza A")
imp = sum(dc.cell(r, 3).value for r in range(12, 24) if isinstance(dc.cell(r, 3).value, (int, float)))
check("documento: imponibile = ricavi totali", close(dc["C25"].value, wb["Preventivi"]["G17"].value) and close(dc["C25"].value, imp))
check("documento: IVA 22% e totale", close(dc["C26"].value, imp * .22) and close(dc["C27"].value, imp * 1.22))
check("documento: nessun margine interno esposto", not any(k in str(dc.cell(r, c).value) for r in range(1, 31) for c in range(1, 5) for k in ("Margine", "Costo pieno")))

# ---- 8. struttura del file
f = load_workbook(SRC)
check("nessun errore # in nessun foglio (valori in cache)", all(not (isinstance(c.value, str) and c.value.startswith("#")) for ws in wb.worksheets for row in ws.iter_rows() for c in row))
check("stampa: area impostata su tutti i fogli", all(ws.print_area for ws in f.worksheets), str([ws.title for ws in f.worksheets if not ws.print_area]))
check("stampa: A4 e adattamento alla larghezza", all(ws.page_setup.fitToWidth == 1 and ws.sheet_properties.pageSetUpPr.fitToPage for ws in f.worksheets))
check("Documento in verticale, gli altri orizzontali tranne Leggimi", f["Documento"].page_setup.orientation == "portrait" and f["Cruscotto"].page_setup.orientation == "landscape")
fonts = {c.font.name for ws in f.worksheets for row in ws.iter_rows() for c in row if c.value is not None}
check("font unico Arial", fonts == {"Arial"}, str(fonts))
z = zipfile.ZipFile(SRC); names = z.namelist()
check("2 grafici presenti nel file", len([n for n in names if n.startswith("xl/charts/chart")]) == 2)
check("nessun collegamento esterno", not any(n.startswith("xl/externalLinks") for n in names))
check("nessuna macro", not any("vba" in n.lower() for n in names))
check("validazioni dati presenti", sum(len(ws.data_validations.dataValidation) for ws in f.worksheets) >= 5)

ko = [r for r in RESULTS if not r[1]]
print(f"\nTOTALE: {len(RESULTS)-len(ko)}/{len(RESULTS)} superati")
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "RISULTATI.txt"), "w", encoding="utf-8") as fh:
    fh.write(f"File: {SRC}\n")
    for n, ok, d in RESULTS: fh.write(("PASS " if ok else "FAIL ") + n + ("" if ok or not d else f"  [{d}]") + "\n")
    fh.write(f"\nTOTALE: {len(RESULTS)-len(ko)}/{len(RESULTS)} superati\n")
sys.exit(1 if ko else 0)
