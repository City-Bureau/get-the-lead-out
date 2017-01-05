tabula = java -jar ./tabula-java/target/tabula-0.9.1-jar-with-dependencies.jar
tabula-process-skip-letter = $(tabula) --pages 3-$$pages -g -r "$$pdf" > $$pdf.csv
tabula-process = $(tabula) --pages 1-$$pages -g -r $$pdf > $$pdf.csv
source = "${source:-scraped}"

.PHONY : all
all : clean.csv

tabula-java :
	git clone https://github.com/tabulapdf/tabula-java.git
	cd tabula-java && git checkout -b 931b9ee8e449bb4bf6d534df4ea6ac0453a59d81 && mvn clean compile assembly:single

.PHONY : pdfs
pdfs :
ifeq ($(source),pdf-archive)
	:
else
	python3 scripts/retrieve_pdfs.py
endif

.PHONY : csvs
csvs : pdfs
ifeq ($(source),pdf-archive)
	find pdf-archive/*.pdf -print0 | \
	while read -d $$'\0' pdf; do \
		pages=`pdfinfo "$$pdf" | grep Pages | perl -p -e 's/[^[0-9]*//'`; \
		if [ $$pages -gt 2 ]; then $(tabula-process-skip-letter); else $(tabula-process); fi; \
	done
else
	find *.pdf -print0 | \
	while read -d $$'\0' pdf; do \
		pages=`pdfinfo "$$pdf" | grep Pages | perl -p -e 's/[^[0-9]*//'`; \
		if [ $$pages -gt 2 ]; then $(tabula-process-skip-letter); else $(tabula-process); fi; \
	done
endif

out.csv : #csvs
ifeq ($(source),pdf-archive)
	csvstack --filenames pdf-archive/*.csv | perl -p -e 's/,,+/,/g' > $@
else
	csvstack --filenames *.csv | perl -p -e 's/,,+/,/g' > $@
endif

clean.csv : out.csv
	cat $< | python scripts/validate.py > $@