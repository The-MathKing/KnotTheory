# Builds the current documents and FAILS on a silent layout overflow.
#
# The board has twice been shipped with content pushed off the bottom of a
# column: tectonic reports that as one warning among dozens and still exits 0,
# and the PDF looks correct unless you render the bottom strip and look.  On a
# fixed-size board an Overfull \vbox means content the reader never sees, so it
# is an error here, not a warning.  Overfull \hbox is left as a warning: a few
# points of horizontal spill is a typesetting nuisance, not lost content.

TEX     := tectonic -X compile
DOCS    := zf_paper zf_poster zf_presentation zf_log zf_guide
STRICT  := zf_poster zf_presentation

all: $(DOCS)

$(DOCS): %: %.tex
	@echo "==> $@"
	@if ! $(TEX) $< > /tmp/build_$@.log 2>&1; then \
	  echo "BUILD FAILED: $@ did not compile."; \
	  grep -Ei 'error' /tmp/build_$@.log | head -20; \
	  exit 1; \
	fi
	@grep -Ei 'overfull' /tmp/build_$@.log | sort -u | head -10 || true
	@if echo " $(STRICT) " | grep -q " $@ "; then \
	  if grep -q 'Overfull .vbox' /tmp/build_$@.log; then \
	    echo ""; \
	    echo "BUILD FAILED: $@ has an Overfull \\vbox --- content is off the page."; \
	    grep 'Overfull .vbox' /tmp/build_$@.log | sort -u; \
	    exit 1; \
	  fi; \
	fi
	@if grep -q 'AUTHOR: insert' $<; then \
	  echo ""; \
	  echo "NOT PRINTABLE: $@ still contains the provenance placeholder."; \
	  echo "  Complete the assistance/independence statement before printing."; \
	  echo "  (The PDF was still produced, so you can keep working.)"; \
	fi
	@echo "    $@.pdf ok"

# The figures the board and the paper depend on, regenerated from the
# verification code rather than kept as loose binaries.
figures:
	cd .. && python3 verification/make_corner_figures.py
	cd .. && python3 verification/make_ramanujan_figures.py

# zf_numbers.tex and ram_table.tex are GENERATED.  Never edit them by hand;
# this is the only thing that should write them.
numbers:
	cd .. && python3 verification/verify_all.py

clean:
	rm -f *.aux *.log *.out *.toc *.bbl *.blg *.nav *.snm *.vrb

.PHONY: all figures numbers clean $(DOCS)
