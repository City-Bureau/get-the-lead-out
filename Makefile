tabula = java -jar ./tabula-java/target/tabula-0.9.0-jar-with-dependencies.jar

.PHONY : all
all : clean.csv

tabula-java :
	git clone https://github.com/tabulapdf/tabula-java.git
	cd tabula-java && mvn clean compile assembly:single

.PHONY : pdfs
pdfs :
	-wget -r -N -nd -l1 -H -AInd*.pdf http://www.cps.edu/Pages/LeadTesting.aspx

.PHONY : csvs
csvs : pdfs
	for pdf in *.pdf; \
            do $(tabula) --pages all -g -r $$pdf > $$pdf.csv; \
	done

out.csv : csvs
	csvstack --filenames Indiv*.csv | sed 's/,,\+/,/g' > $@

clean.csv : out.csv
	cat $< | python3 validate.py > $@

.PHONY : clean
clean :
	-rm Ind*.pdf Ind*.csv


hand_scrape.clean.csv : 
	python scripts/clean_hand_scrape.py > $@

tabula.clean.csv : tabula/tabula-cps_lead_results.csv
	perl -p -e 's|,pdf.$$|,filename|; s|http:.*LeadTesting/||' $< > $@.tmp
	echo "\nZapata,1-E-CS02-51,Room 105 - North,6/3/16 6:50 AM,27.6,Individualschool_Zapata_609973.pdf\n\
	Orr,51558-1-HAL-F05,\"Main- Next to Room 118, Fountain\",10/12/16 6:00 AM,530,IndividualSchool_Orr_610389.pdf" >> $@.tmp
	csvsort $@.tmp | python scripts/clean_tabula.py > $@


cps.csv : hand_scrape.clean.csv tabula.clean.csv
	csvstack $< $(word 2,$^) | csvsort | uniq > $@ 

