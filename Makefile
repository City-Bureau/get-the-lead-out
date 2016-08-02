tabula = java -jar ./tabula-java/target/tabula-0.9.0-jar-with-dependencies.jar

clean.csv : out.csv
	cat $< | python3 validate.py > $@


.PHONY : pdfs
pdfs :
	-wget -r -N -nd -l1 -H -AInd*.pdf http://www.cps.edu/Pages/LeadTesting.aspx

.PHONY : csvs
csvs : pdfs
	for pdf in *.pdf; \
            do $(tabula) --pages all -g $$pdf > $$pdf.csv; \
	done

out.csv : csvs
	csvstack --filenames Indiv*.csv | sed 's/,,\+/,/g' > $@

tabula-java :
	git clone https://github.com/tabulapdf/tabula-java.git
	cd tabula-java && mvn clean compile assembly:single

