# Get the Lead Out

Scripts for extracting measurements from Chicago Public School lead reports.

## Assumes

* posix environment (linux, mac, that sort of thing)
* already installed: python3, maven, git, csvkit, wget

## Install

We are using https://github.com/tabulapdf/tabula-java for extracting the tables from a whole mess of pdfs.

To install tabula-java, run `make tabula-java`

## Run

run `make clean.csv` This will make a spreadsheet `clean.csv` with the
school name, sample id, sample time, sample level, and url of the
source file. It will also make a spreadsheet called `err.csv` with the
rows that it as not able to extract cleanly. You'll need to deal with
those by hand.

In the making of these two spreadsheets, we will download all the pdf
reports from the Chicago Public Schools website and extract a bunch of
messy spreadsheets from those pdfs using tabula. It could take a few hours all told. 
