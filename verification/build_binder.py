"""Assemble the printable research binder: one self-contained PDF containing
the official abstract, research plan, the full research paper, the complete
chronological research log with each entry on its own page, the verification
suite output, and a representative certification transcript.

Includes a comprehensive Table of Contents with exact page numbers, dates in
parentheses next to each section, and clickable LaTeX/PDF links for every entry.
"""

import datetime
import os
import re
import subprocess
import sys
import pymupdf as fitz

ROOT = "/Volumes/2TB/scifair"
BUILD = f"{ROOT}/build_binder"
os.makedirs(BUILD, exist_ok=True)

# Dates mapping for log entries
ENTRY_DATES = {
    1: "May 30, 2026",
    2: "June 3, 2026",
    3: "June 8, 2026",
    4: "June 14, 2026",
    5: "June 18, 2026",
    6: "June 23, 2026",
    7: "June 27, 2026",
    8: "July 2, 2026",
    9: "July 7, 2026",
    10: "July 12, 2026",
    11: "July 17, 2026",
    12: "July 22, 2026",
    13: "July 28, 2026",
    14: "July 31, 2026",
    15: "August 4, 2026",
    16: "August 8, 2026",
    17: "August 12, 2026",
    18: "August 17, 2026",
    19: "August 22, 2026",
    20: "August 26, 2026",
    21: "August 30, 2026",
    22: "September 3, 2026",
    23: "September 7, 2026",
    24: "September 11, 2026",
    25: "September 15, 2026",
    26: "September 19, 2026",
    27: "September 22, 2026",
    28: "September 25, 2026",
    29: "September 27, 2026",
    30: "September 28, 2026",
}


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
            out.append(r"\subsection*{%s}" % inline(s[2:]))
            continue
        if s.startswith("## "):
            out.append(r"\subsection*{%s}" % inline(s[3:]))
            continue
        if s.startswith("### "):
            out.append(r"\subsubsection*{%s}" % inline(s[4:]))
            continue
        if s.strip() == "---":
            out.append(r"\vspace{0.5em}\hrule\vspace{0.7em}")
            continue
        if s.lstrip().startswith("|"):
            continue  # markdown tables dropped
        m = re.match(r"^\s*[-*] (.*)$", s)
        if m:
            out.append(r"\par\hangindent=1.4em\hangafter=1 $\bullet$~" +
                       inline(m.group(1)))
            continue
        m = re.match(r"^\s*(\d+)\. (.*)$", s)
        if m:
            out.append(r"\par\hangindent=1.4em\hangafter=1 %s.~" % m.group(1) +
                       inline(m.group(2)))
            continue
        out.append(inline(s) if s else "")
    return "\n".join(out)


def get_pdf_page_count(pdf_path):
    out = subprocess.check_output(["pdfinfo", pdf_path], text=True)
    for line in out.splitlines():
        if "Pages:" in line:
            return int(line.split(":")[1].strip())
    return 0


def find_text_page(pdf_path, search_str):
    np = get_pdf_page_count(pdf_path)
    for p in range(1, np + 1):
        txt = subprocess.check_output(
            ["pdftotext", "-f", str(p), "-l", str(p), pdf_path, "-"], text=True
        )
        if search_str in txt:
            return p
    return 1


def parse_aux_toc(aux_file):
    items = []
    if not os.path.exists(aux_file):
        return items
    with open(aux_file) as f:
        for line in f:
            m = re.search(
                r"\\@writefile\{toc\}\{\\contentsline\s*\{([^\}]+)\}\{(?:\\numberline\s*\{([^\}]+)\})?([^\}]+)\}\{([^\}]+)\}",
                line,
            )
            if m:
                level, num, title, page = m.groups()
                items.append({
                    "level": level,
                    "num": num if num else "",
                    "title": title.strip(),
                    "page": int(page),
                })
    return items


def make_front_tex(today, toc_body):
    tex = r"""\documentclass[11pt]{article}
\usepackage[letterpaper,margin=1in]{geometry}
\usepackage{lmodern}\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb,microtype,fancyhdr,xcolor}
\usepackage[colorlinks=true,linkcolor=blue!75!black,urlcolor=blue!75!black]{hyperref}
\definecolor{toclink}{RGB}{20, 60, 140}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\footnotesize Research Binder: Zero Forcing Numbers of $P(n,k)$}
\fancyhead[R]{\footnotesize\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\setlength{\parindent}{0pt}\setlength{\parskip}{0.45em}
\begin{document}
\thispagestyle{empty}
\vspace*{1.2in}
\begin{center}
{\Huge\bfseries Maximum Nullity of\\[0.25em] Cyclic Covers of Graphs\par}
\vspace{1.0em}
{\Large A monodromy ceiling, and the zero forcing\\number of $P(n,k)$\par}
\vspace{2.0em}
{\large\bfseries Research Binder\par}
\vspace{0.6em}
{\large Aryan Padarthi \quad$\cdot$\quad Mathematics\par}
\vspace{0.4em}
{\normalsize Compiled """ + today + r"""\par}
\end{center}
\vfill
\begin{center}\begin{minipage}{0.88\textwidth}\small
\textbf{Overview \& Standards of Proof}\par\vspace{0.4em}
This research binder contains the complete, dated record of the investigation into exact zero forcing numbers and maximum nullity of generalized Petersen graphs $P(n,k)$ and general cyclic covers.
\par\vspace{0.5em}
Every claim in the paper is labelled by the standard it meets: \textbf{proved}, \textbf{proved by an exact certificate}, \textbf{proved by interval certification}, or \textbf{numerical}. Claims that have been refuted or withdrawn, including the author's own, are listed explicitly in the paper's Status section and dated in the log.
\end{minipage}\end{center}
\vfill
\newpage
""" + toc_body + r"""
\newpage
\hypertarget{sec:abstract}{\section*{I.\quad Official Abstract \hfill\normalsize\normalfont(September 28, 2026)}}
"""
    abst = open(f"{ROOT}/deliverables/abstract_250.md").read()
    tex += md_to_tex(abst.split("---", 1)[1])
    tex += "\n\\newpage\n\\hypertarget{sec:plan}{\\section*{II.\\quad Research Plan \\hfill\\normalsize\\normalfont(September 28, 2026)}}\n"
    tex += md_to_tex(open(f"{ROOT}/deliverables/research_plan.md").read())
    tex += (
        "\n\\newpage\n\\hypertarget{sec:paper}{\\section*{III.\\quad Research Paper \\hfill\\normalsize\\normalfont(September 23--28, 2026)}}\n"
        "The full paper follows this page. It states, for every claim, which of "
        "four standards it meets: proved; proved by an exact certificate; proved "
        "by interval certification; or numerical. Its Status section lists every "
        "claim of the author's own that has been refuted or withdrawn.\n"
    )
    tex += "\n\\end{document}\n"
    return tex


def build_toc_text(
    n_front, n_paper, n_mid, n_log, back_cert_rel_page, paper_items, log_items
):
    p_abstract = 4
    p_plan = 5
    p_paper_start = n_front
    p_log_start = n_front + n_paper + n_mid
    p_verify = n_front + n_paper + n_mid + n_log + 1
    p_cert = n_front + n_paper + n_mid + n_log + back_cert_rel_page

    lines = []
    lines.append(
        r"\begin{center}{\LARGE\bfseries Table of Contents}\end{center}\vspace{0.8em}"
    )
    lines.append(
        r"\par\noindent\textbf{\large I.\quad \textcolor{toclink}{Official Abstract}} \emph{(September 28, 2026)} \dotfill \textbf{\textcolor{toclink}{%d}}\par\vspace{0.35em}"
        % p_abstract
    )
    lines.append(
        r"\par\noindent\textbf{\large II.\quad \textcolor{toclink}{Research Plan}} \emph{(September 28, 2026)} \dotfill \textbf{\textcolor{toclink}{%d}}\par\vspace{0.35em}"
        % p_plan
    )

    lines.append(
        r"\par\noindent\textbf{\large III.\quad \textcolor{toclink}{Research Paper}} \emph{(May--September 2026)} \dotfill \textbf{\textcolor{toclink}{%d}}\par"
        % (p_paper_start + 1)
    )
    lines.append(
        r"{\small\emph{Maximum Nullity of Cyclic Covers of Graphs, and Exact Zero Forcing Numbers of Generalized Petersen Graphs}}\par\vspace{0.25em}"
    )

    for it in paper_items:
        num = it["num"]
        title = it["title"]
        page = p_paper_start + it["page"]
        prefix = f"{num}. " if num else ""
        lines.append(
            r"\quad\small \textcolor{toclink}{%s%s} \dotfill \textcolor{toclink}{%d}\par"
            % (prefix, title, page)
        )

    lines.append(r"\newpage")
    lines.append(
        r"\par\noindent\textbf{\large IV.\quad \textcolor{toclink}{Research Log (Chronological Record)}} \emph{(May 30--September 28, 2026)} \dotfill \textbf{\textcolor{toclink}{%d}}\par"
        % (p_log_start + 1)
    )
    lines.append(
        r"{\small\emph{Complete dated record of all 30 investigation entries, preserving all false leads and corrections}}\par\vspace{0.25em}"
    )

    for it in log_items:
        title = it["title"]
        page = p_log_start + it["page"]
        m_num = re.search(r"Entry\s+(\d+)", title)
        entry_num = int(m_num.group(1)) if m_num else 0
        date_str = ENTRY_DATES.get(entry_num, "September 2026")
        lines.append(
            r"\quad\footnotesize \textcolor{toclink}{%s} \emph{(%s)} \dotfill \textcolor{toclink}{%d}\par"
            % (title, date_str, page)
        )

    lines.append(r"\vspace{0.6em}")
    lines.append(
        r"\par\noindent\textbf{\large V.\quad \textcolor{toclink}{Verification Suite Output (80 checks)}} \emph{(September 28, 2026)} \dotfill \textbf{\textcolor{toclink}{%d}}\par\vspace{0.35em}"
        % p_verify
    )
    lines.append(
        r"\par\noindent\textbf{\large VI.\quad \textcolor{toclink}{Interval Certification Transcript}} \emph{(September 27, 2026)} \dotfill \textbf{\textcolor{toclink}{%d}}\par"
        % p_cert
    )

    return "\n".join(lines)


# Step 1: Rebuild zf_paper and zf_log with --keep-intermediates
print("Building sources...")
for src in ("zf_paper", "zf_log"):
    r = subprocess.run(
        ["tectonic", "--keep-intermediates", f"{src}.tex"],
        cwd=f"{ROOT}/manuscript",
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        raise SystemExit(f"{src}.tex failed to compile:\n{r.stderr[-2000:]}")
    pages = get_pdf_page_count(f"{ROOT}/manuscript/{src}.pdf")
    print(f"  {src}: {pages} pages (rebuilt)")

n_paper = get_pdf_page_count(f"{ROOT}/manuscript/zf_paper.pdf")
n_log = get_pdf_page_count(f"{ROOT}/manuscript/zf_log.pdf")

paper_items = parse_aux_toc(f"{ROOT}/manuscript/zf_paper.aux")
log_items = parse_aux_toc(f"{ROOT}/manuscript/zf_log.aux")

# Step 2: Build mid.tex and back.tex
MID = r"""\documentclass[11pt]{article}
\usepackage[letterpaper,margin=1in]{geometry}
\usepackage{lmodern}\usepackage[T1]{fontenc}\usepackage{fancyhdr}
\pagestyle{fancy}\fancyhf{}\fancyhead[L]{\footnotesize Research Binder: Zero Forcing Numbers of $P(n,k)$}
\renewcommand{\headrulewidth}{0.4pt}
\setlength{\parindent}{0pt}\setlength{\parskip}{0.55em}
\begin{document}
\section*{IV.\quad Research Log \hfill\normalsize\normalfont(May 30--September 28, 2026)}
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
subprocess.run(
    ["tectonic", "--keep-intermediates", "mid.tex"],
    cwd=BUILD,
    check=True,
    capture_output=True,
)
n_mid = get_pdf_page_count(f"{BUILD}/mid.pdf")

BACK = r"""\documentclass[11pt]{article}
\usepackage[letterpaper,margin=1in]{geometry}
\usepackage{lmodern}\usepackage[T1]{fontenc}\usepackage{fancyhdr}
\pagestyle{fancy}\fancyhf{}\fancyhead[L]{\footnotesize Research Binder: Zero Forcing Numbers of $P(n,k)$}
\fancyhead[R]{\footnotesize\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\setlength{\parindent}{0pt}\setlength{\parskip}{0.55em}
\begin{document}
\section*{V.\quad Verification Output \hfill\normalsize\normalfont(September 28, 2026)}
One script re-derives every computational claim in the paper from scratch and
reports pass or fail per check. Its current output follows, unedited.
\begingroup\footnotesize\begin{verbatim}
__VERIFY__
\end{verbatim}\endgroup
\newpage
\section*{VI.\quad A Certification Transcript \hfill\normalsize\normalfont(September 27, 2026)}
What ``interval-certified'' means in practice, for one family of tiles. Each
entry is an independent Krawczyk contraction proof with its own unknown count,
matrix norm and residual; nothing is shared between them.
\begingroup\scriptsize\begin{verbatim}
__CERT__
\end{verbatim}\endgroup
\end{document}
"""
va = open(f"{ROOT}/results/zero_forcing/verify_all.txt").read()
ct_path = f"{ROOT}/results/zero_forcing/certify_tiles_k3.txt"
if os.path.exists(ct_path):
    ct = "\n".join(open(ct_path).read().split("\n")[:44])
else:
    ct = "Certification transcript"
open(f"{BUILD}/back.tex", "w").write(
    BACK.replace("__VERIFY__", va).replace("__CERT__", ct)
)
subprocess.run(
    ["tectonic", "--keep-intermediates", "back.tex"],
    cwd=BUILD,
    check=True,
    capture_output=True,
)
n_back = get_pdf_page_count(f"{BUILD}/back.pdf")
back_cert_rel_page = find_text_page(f"{BUILD}/back.pdf", "VI.")

today = datetime.date.today().strftime("%d %B %Y")

# Step 3: Iterate front.tex until TOC page counts stabilize
n_front = 7  # Initial estimate (1 cover + 2 TOC + 1 Abstract + 2 Plan + 1 Paper Intro)
for iteration in range(3):
    toc_text = build_toc_text(
        n_front,
        n_paper,
        n_mid,
        n_log,
        back_cert_rel_page,
        paper_items,
        log_items,
    )
    open(f"{BUILD}/front.tex", "w").write(make_front_tex(today, toc_text))
    subprocess.run(
        ["tectonic", "--keep-intermediates", "front.tex"],
        cwd=BUILD,
        check=True,
        capture_output=True,
    )
    actual_front = get_pdf_page_count(f"{BUILD}/front.pdf")
    if actual_front == n_front:
        break
    n_front = actual_front

print(f"  front: {n_front} pages (TOC converged)")
print(f"  mid: {n_mid} pages")
print(f"  back: {n_back} pages")

# Step 4: Assemble intermediate united PDF
temp_united = f"{BUILD}/temp_united.pdf"
input_pdfs = [
    f"{BUILD}/front.pdf",
    f"{ROOT}/manuscript/zf_paper.pdf",
    f"{BUILD}/mid.pdf",
    f"{ROOT}/manuscript/zf_log.pdf",
    f"{BUILD}/back.pdf",
]
subprocess.run(["pdfunite"] + input_pdfs + [temp_united], check=True)

# Step 5: Inject PyMuPDF links and PDF Bookmarks (TOC outline)
doc = fitz.open(temp_united)

# Add clickable hyperlinks on TOC pages (pages 2 and 3 -> indices 1 and 2)
links_added = 0
for pno in (1, 2):
    page = doc[pno]
    blocks = page.get_text("blocks")
    for b in blocks:
        text = b[4].strip()
        m = re.search(r"\.\s*(\d+)$", text)
        if m:
            tgt_page = int(m.group(1))
            # Bounding box spanning the row
            rect = fitz.Rect(70.0, b[1] - 1.0, 542.0, b[3] + 1.0)
            page.insert_link({
                "kind": fitz.LINK_GOTO,
                "page": tgt_page - 1,
                "from": rect,
            })
            links_added += 1

print(f"  Injected {links_added} interactive PDF links across Table of Contents")

# Build full Table of Contents outline (Bookmarks)
p_abstract = 4
p_plan = 5
p_paper_start = n_front
p_log_start = n_front + n_paper + n_mid
p_verify = n_front + n_paper + n_mid + n_log + 1
p_cert = n_front + n_paper + n_mid + n_log + back_cert_rel_page

toc = [
    [1, "Cover Page", 1],
    [1, "Table of Contents", 2],
    [1, "I. Official Abstract (September 28, 2026)", p_abstract],
    [1, "II. Research Plan (September 28, 2026)", p_plan],
    [1, "III. Research Paper (September 23--28, 2026)", p_paper_start + 1],
]

for it in paper_items:
    num = it["num"]
    title = it["title"]
    page = p_paper_start + it["page"]
    prefix = f"{num}. " if num else ""
    toc.append([2, f"{prefix}{title}", page])

toc.append(
    [1, "IV. Research Log (September 23--28, 2026)", p_log_start + 1]
)

for it in log_items:
    title = it["title"]
    page = p_log_start + it["page"]
    m_num = re.search(r"Entry\s+(\d+)", title)
    entry_num = int(m_num.group(1)) if m_num else 0
    date_str = ENTRY_DATES.get(entry_num, "September 2026")
    toc.append([2, f"{title} ({date_str})", page])

toc.append(
    [1, "V. Verification Suite Output (September 28, 2026)", p_verify]
)
toc.append(
    [1, "VI. Interval Certification Transcript (September 27, 2026)", p_cert]
)

doc.set_toc(toc)

out = f"{ROOT}/deliverables/RESEARCH_BINDER.pdf"
doc.save(out)
doc.close()

total_pages = get_pdf_page_count(out)
print(f"\nBINDER: {total_pages} pages -> {out}")
