"""
Recompute every headline number asserted in manuscript/log.tex directly from the
KnotInfo CSV, and print CLAIMED vs ACTUAL side by side.

Run:  ./venv/bin/python verification/audit_log_claims.py
"""
import pandas as pd, numpy as np, sys

CSV = "data/processed/knotinfo_invariants.csv"
df = pd.read_csv(CSV, low_memory=False)

def num(col):
    return pd.to_numeric(df[col], errors="coerce")

s   = num("rasmussen_invariant")
tau = num("ozsvath_szabo_tau_invariant")
sig = num("signature")
g3  = num("three_genus")
g4  = num("smooth_four_genus")
g4t = num("topological_four_genus")
u   = num("unknotting_number")
gT  = num("turaev_genus")
c   = num("crossing_number")

rows = []
def check(label, claimed, actual, fmt="{:.1f}"):
    ok = "OK   " if abs(actual - claimed) < 0.05 else "WRONG"
    rows.append((ok, label, fmt.format(claimed), fmt.format(actual)))

# --- Log Entry 3 (Approach 1): inequality slack table ----------------------
m = (~sig.isna()) & (~g4.isna())
slack = 2*g4[m] - sig[m].abs()
check("E3 |sigma|<=2g4 : evaluated",        12967, m.sum(),               "{:.0f}")
check("E3 |sigma|<=2g4 : tight %",           74.2, 100*(slack==0).mean())
check("E3 |sigma|<=2g4 : mean slack",       0.628, slack.mean(),          "{:.3f}")
check("E3 |sigma|<=2g4 : max slack",          8.0, slack.max())

m = (~s.isna()) & (~g4.isna())
slack = 2*g4[m] - s[m].abs()
check("E3 |s|<=2g4 : tight %",              100.0, 100*(slack==0).mean())
check("E3 |s|<=2g4 : mean slack",           0.000, slack.mean(),          "{:.3f}")
check("E3 |s|<=2g4 : max slack",              0.0, slack.max())

m = (~tau.isna()) & (~g4.isna())
check("E3 |tau|<=g4 : tight %",              75.3, 100*((g4[m]-tau[m].abs())==0).mean())

m = (~g4.isna()) & (~g3.isna())
check("E3 g4<=g3 : tight %",                  5.9, 100*((g3[m]-g4[m])==0).mean())

# --- Log Entry 4 (Approach 2): subclass exactness --------------------------
fib = df["fibered"].astype(str).str.strip().eq("Y")
m = fib & (~s.isna()) & (~g4.isna())
check("E4 fibered: 2g4=|s| exact %",        100.0, 100*(s[m].abs()==2*g4[m]).mean())
m = fib & (~sig.isna()) & (~tau.isna())
check("E4 fibered: sigma=-2tau exact %",     71.4, 100*(sig[m]==-2*tau[m]).mean())

alt = df["alternating"].astype(str).str.strip().eq("Y")
m = alt & (~s.isna()) & (~g4.isna())
check("E4 alternating: 2g4=|s| exact %",    100.0, 100*(s[m].abs()==2*g4[m]).mean())

# --- Log Entry 9 (Approach 7): conjecture violation counts -----------------
m = (~tau.isna()) & (~g4t.isna())
check("E9 |tau|<=g4_top : violations",          0, (tau[m].abs() > g4t[m]).sum(), "{:.0f}")
m = (~s.isna()) & (~g4t.isna())
check("E9 |s|/2<=g4_top : violations",          0, (s[m].abs()/2 > g4t[m]).sum(), "{:.0f}")
m = (~u.isna()) & (~g4.isna()) & (~gT.isna())
check("E9 u>=g4+gT : violations",              84, (u[m] < g4[m]+gT[m]).sum(),   "{:.0f}")
m = (~g3.isna()) & (~g4.isna()) & (~gT.isna())
check("E9 g3>=g4+gT : violations",             12, (g3[m] < g4[m]+gT[m]).sum(),  "{:.0f}")

# --- Log Entry 10 (Approach 8): pinched g4 --------------------------------
m = (~s.isna())&(~tau.isna())&(~sig.isna())&(~g3.isna())&(~g4.isna())&(~u.isna())
lo = np.maximum.reduce([tau[m].abs(), s[m].abs()/2, sig[m].abs()/2])
hi = np.minimum(g3[m], u[m])
check("E10 g4 pinched exactly %",            74.2, 100*((lo==hi)&(lo==g4[m])).mean())

# --- Log Entry 12: defect knot count --------------------------------------
m = (~s.isna()) & (~sig.isna())
check("E12 defect knots (|s|>|sigma|)",       343, ((s[m].abs()-sig[m].abs())>0).sum(), "{:.0f}")

# --- Log Entry 13 (T3): gT <= braid_index - 1 -----------------------------
bi = num("braid_index")
m = (~gT.isna()) & (~bi.isna())
check("E13 gT<=braid-1 : evaluated",         2953, m.sum(),                       "{:.0f}")
check("E13 gT<=braid-1 : violations",           0, (gT[m] > bi[m]-1).sum(),        "{:.0f}")

w = max(len(r[1]) for r in rows)
print(f"{'':5}  {'CLAIM IN log.tex':<{w}}  {'CLAIMED':>9}  {'ACTUAL':>9}")
print("-"*(w+30))
for ok,label,cl,ac in rows:
    print(f"{ok}  {label:<{w}}  {cl:>9}  {ac:>9}")
bad = sum(1 for r in rows if r[0].strip()=="WRONG")
print("-"*(w+30))
print(f"{bad} of {len(rows)} audited claims do not match the data.")
