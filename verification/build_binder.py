"""Assemble the printable research binder: front matter + paper + log + appendices."""
import datetime
import os
import re
import subprocess

ROOT = "/Volumes/2TB/scifair"
BUILD = f"{ROOT}/build_binder"
os.makedirs(BUILD, exist_ok=True)


def esc(t):
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                 ("$", r"\$"), ("#", r"\#"), ("_", r"\_"), ("{", r"\{"),
                 ("}", r"\}"), ("~", r"\textasciitilde{}"),
                 ("^", r"\textasciicircum{}")]:
        t = t.replace(a, b)
    return t


def inline(t):
    t = esc(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", t)
    t = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"\\emph{\1}", t)
    t = re.sub(r"`(.+?)`", r"\\texttt{\1}", t)
    return t


def md_to_tex(md, drop_first_heading=True):
    out, seen_h1 = [], False
    for line in md.split("\n"):
        s = line.rstrip()
        if s.startswith("# "):
            if drop_first_heading and not seen_h1:
                seen_h1 = True
                continue
            out.append(r"\subsection*{%s}" % inline(s[2:])); continue
        if s.startswith("## "):
            out.append(r"\subsection*{%s}" % inline(s[3:])); continue
        if s.startswith("### "):
            out.append(r"\subsubsection*{%s}" % inline(s[4:])); continue
        if s.strip() == "---":
            out.append(r"\vspace{0.5em}\hrule\vspace{0.7em}"); continue
        if s.lstrip().startswith("|"):
            continue                                    # markdown tables dropped
        m = re.match(r"^\s*[-*] (.*)$", s)
        if m:
            out.append(r"\par\hangindent=1.4em\hangafter=1 $\bullet$~" +
                       inline(m.group(1))); continue
        m = re.match(r"^\s*(\d+)\. (.*)$", s)
        if m:
            out.append(r"\par\hangindent=1.4em\hangafter=1 %s.~" % m.group(1) +
                       inline(m.group(2))); continue
        out.append(inline(s) if s else "")
    return "\n".join(out)


def verbatim_section(title, path, maxlines=None):
    lines = open(path).read().split("\n")
    if maxlines:
        lines = lines[:maxlines]
    body = "\n".join(lines)
    return (r"\newpage\section*{%s}" % title +
            "\n\\begingroup\\footnotesize\\begin{verbatim}\n" + body +
            "\n\\end{verbatim}\\endgroup\n")


today = datetime.date.today().strftime("%d %B %Y")
tex = r"""\documentclass[11pt]{article}
\usepackage[letterpaper,margin=1in]{geometry}
\usepackage{lmodern}\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb,microtype,fancyhdr}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\footnotesize Research Binder}
\fancyhead[R]{\footnotesize\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\setlength{\parindent}{0pt}\setlength{\parskip}{0.55em}
\begin{document}
\thispagestyle{empty}
\vspace*{1.9in}
\begin{center}
{\Huge\bfseries Maximum Nullity of\\[0.25em] Cyclic Covers of Graphs\par}
\vspace{1.1em}
{\Large A monodromy ceiling, and the zero forcing\\number of $P(n,k)$\par}
\vspace{2.2em}
{\large\bfseries Research Binder\par}
\vspace{0.7em}
{\large Aryan Padarthi \quad$\cdot$\quad Mathematics\par}
\vspace{0.5em}
{\normalsize Compiled """ + today + r"""\par}
\end{center}
\vfill
\begin{center}\begin{minipage}{0.86\textwidth}\small
\textbf{Contents}\par\vspace{0.4em}
\begin{tabular}{@{}rl@{}}
I.   & Official Abstract\\
II.  & Research Plan\\
III. & Research Paper\\
IV.  & Research Log, dated, including every dead end\\
V.   & Verification Output, 69 checks\\
VI.  & A Certification Transcript\\
\end{tabular}
\par\vspace{0.9em}
Every claim in the paper is labelled by the standard it meets: proved, proved by
an exact certificate, proved by interval certification, or numerical. Claims that
have been refuted or withdrawn, including the author's own, are listed explicitly
in the paper's Status section and dated in the log.
\end{minipage}\end{center}
\vfill
\newpage
\section*{I.\quad Official Abstract}
"""
abst = open(f"{ROOT}/deliverables/abstract_250.md").read()
tex += md_to_tex(abst.split("---", 1)[1])
tex += "\n\\newpage\n\\section*{II.\\quad Research Plan}\n"
tex += md_to_tex(open(f"{ROOT}/deliverables/research_plan.md").read())
tex += ("\n\\newpage\n\\section*{III.\\quad Research Paper}\n"
        "The full paper follows this page. It states, for every claim, which of "
        "four standards it meets: proved; proved by an exact certificate; proved "
        "by interval certification; or numerical. Its Status section lists every "
        "claim of the author's own that has been refuted or withdrawn.\n")
tex += "\n\\end{document}\n"
open(f"{BUILD}/front.tex", "w").write(tex)

MID = r"""\documentclass[11pt]{article}
\usepackage[letterpaper,margin=1in]{geometry}
\usepackage{lmodern}\usepackage[T1]{fontenc}\usepackage{fancyhdr}
\pagestyle{fancy}\fancyhf{}\fancyhead[L]{\footnotesize Research Binder}
\renewcommand{\headrulewidth}{0.4pt}
\setlength{\parindent}{0pt}\setlength{\parskip}{0.55em}
\begin{document}
\section*{IV.\quad Research Log}
The dated research log follows this page. It records the work in the order it
happened rather than as a finished account, and it deliberately preserves what
went wrong: conjectures that were tested and died, claims of the author's own
that were later refuted, and software bugs that produced confident wrong answers
before being caught.

It is included because a reader is entitled to see which conclusions were
reached first and revised later, and because the superseded versions have been
left in place rather than edited away.
\end{document}
"""
open(f"{BUILD}/mid.tex", "w").write(MID)

BACK = r"""\documentclass[11pt]{article}
\usepackage[letterpaper,margin=1in]{geometry}
\usepackage{lmodern}\usepackage[T1]{fontenc}\usepackage{fancyhdr}
\pagestyle{fancy}\fancyhf{}\fancyhead[L]{\footnotesize Research Binder}
\fancyhead[R]{\footnotesize\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\setlength{\parindent}{0pt}\setlength{\parskip}{0.55em}
\begin{document}
\section*{V.\quad Verification Output}
One script re-derives every computational claim in the paper from scratch and
reports pass or fail per check. Its current output follows, unedited.
\begingroup\footnotesize\begin{verbatim}
__VERIFY__
\end{verbatim}\endgroup
\newpage
\section*{VI.\quad A Certification Transcript}
What ``interval-certified'' means in practice, for one family of tiles. Each
entry is an independent Krawczyk contraction proof with its own unknown count,
matrix norm and residual; nothing is shared between them.
\begingroup\scriptsize\begin{verbatim}
__CERT__
\end{verbatim}\endgroup
\end{document}
"""
va = open(f"{ROOT}/results/zero_forcing/verify_all.txt").read()
ct = "\n".join(open(f"{ROOT}/results/zero_forcing/certify_tiles_k3.txt")
               .read().split("\n")[:44])
open(f"{BUILD}/back.tex", "w").write(
    BACK.replace("__VERIFY__", va).replace("__CERT__", ct))

for name in ("front", "mid", "back"):
    subprocess.run(["tectonic", "-X", "compile", f"{name}.tex"], cwd=BUILD,
                   capture_output=True)
    n = subprocess.run(["pdfinfo", f"{BUILD}/{name}.pdf"], capture_output=True,
                       text=True).stdout
    print(f"  {name}: {n.split('Pages:')[1].split()[0]} pages")

parts = [f"{BUILD}/front.pdf", f"{ROOT}/manuscript/zf_paper.pdf",
         f"{BUILD}/mid.pdf", f"{ROOT}/manuscript/zf_log.pdf",
         f"{BUILD}/back.pdf"]
out = f"{ROOT}/deliverables/RESEARCH_BINDER.pdf"
subprocess.run(["pdfunite"] + parts + [out], check=True)
info = subprocess.run(["pdfinfo", out], capture_output=True, text=True).stdout
print("\nBINDER:", info.split("Pages:")[1].split()[0], "pages ->", out)
