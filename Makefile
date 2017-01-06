SHELL=bash

tabula = java -jar ./tabula-java/target/tabula-0.9.1-jar-with-dependencies.jar
pdf-pages = `pdfinfo "$$pdf" | grep Pages | perl -p -e 's/[^[0-9]*//'`

.PHONY : all
all : cps.csv

tabula-java :
	git clone https://github.com/tabulapdf/tabula-java.git
	cd tabula-java && \
        git checkout a1775ecb744abf06f6d6d7d024b561d13bb01f7d && \
        mvn clean compile assembly:single

.PHONY : pdfs
pdf-archive : 
	python3 scripts/retrieve_pdfs.py

.PHONY : csvs
csvs :
	for pdf in pdf-archive/*.pdf; \
            do if [[ $(pdf-pages) > 2 ]]; then \
                   $(tabula) --pages 3- -g -r "$$pdf" > $$pdf.csv; \
                else \
                   $(tabula) --pages 1- -g -r "$$pdf" > $$pdf.csv; \
               fi \
        done

stacked.csv : #csvs
	csvstack --filenames pdf-archive/*.csv | perl -p -e 's/,,+/,/g' > $@

cps.csv : stacked.csv
	cat $< | python scripts/validate.py > $@
