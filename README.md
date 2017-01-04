# Get the Lead Out

Scripts for extracting measurements from Chicago Public School lead reports.

## Requirements

* posix environment (linux or mac OS)
* python 3 
* [maven](https://maven.apache.org/install.html) (mac users can also use homebrew: `brew install maven`) 
* [git](https://git-scm.com/book/en/v1/Getting-Started-Installing-Git)  
* [csvkit](https://csvkit.readthedocs.io/en/0.9.1/install.html)
* pdfinfo (available as part of [Xpdf](http://www.foolabs.com/xpdf/download.html) - mac users can also use the [Poppler](https://poppler.freedesktop.org/) fork via homebrew: `brew install poppler`)

## Installation

Start by cloning this repo:

```bash
git clone git@github.com:City-Bureau/get-the-lead-out.git  # assumes SSH
```

If you prefer using git over HTTPS, you can run a variation of the clone command:

```bash
git clone https://github.com/City-Bureau/get-the-lead-out.git  # assumes HTTPS
```

We use [tabula-java](https://github.com/tabulapdf/tabula-java) to extract tables from PDFs. You don't have to have tabula-java installed - we have a rule that handles the installation in our Makefile. Once you've cloned this repo, run the following commands to install it:

```bash
cd get-the-lead-out
make tabula-java
```

After Make finishes, tabula-java will be installed in the `tabula-java` directory inside this repo.  

(Note for Mac users: tabula-java has been known to open and close Java as part of every command. This can result in annoying behavior, where the scraper renders your machine unusuable for the duration of tabula processing. Make sure to set aside 10-20 minutes while the scraper runs, or to configure Java to run as a background process.)

## Running the scripts

### 1. Make the spreadsheets

To produce the final spreadsheet, run the command `make clean.csv`. This will make two spreadsheets: `clean.csv` and `err.csv`. The spreadsheet `clean.csv` contains the school name, sample id, sample time, sample level, and URL of the
source file for every row that tabula successfully processed. Any row that produced a scraping error will be output to `err.csv`.

In making these two spreadsheets, we download all the PDF reports from the Chicago Public Schools website and extract a bunch of messy spreadsheets from those PDFs. There are a lot of reports (over 500), so set aside a nice chunk of time - 30 minutes to an hour is a safe bet - for the script to run. 

If you'd like to run the Makefile on our archive of reports from Summer 2016, run the make command with the optional variable `source` like so:

```
make clean.csv source=pdf-archive
```

This command will instruct Make to ignore the scraping step, and use the files in the `pdf-archive/` repo to complete the cleaning process.

### 2. Clean up errors

Since errors are output on the level of rows, and not files, `err.csv` may contain anywhere from a few rows to entire reports for schools where the tabula couldn't read the PDF. Once the spreadsheets have been produced, take some time to carefully look over `err.csv` and see what was missed. 

In cases where tabula messed up individual rows, you'll have to check the original PDFs and add these rows to `clean.csv` by hand. If tabula missed entire pages or reports, however, you may want to go back and scrape the PDFs by hand using [tabula's GUI](http://tabula.technology/). Errors on the level of pages are often caused by strange PDF layouts, and it can be easier to deal with them in the GUI.

### 3. Confirm that you caught every school

## Using this code in the future

This code is optimized for the lead reports produced by CPS during Summer 2016. If you're running this code in the future on a different set of reports, you'll have to tweak some portions of the validation script `scripts/validate.py` to adapt to a new set of reports.

### New patterns

Since there is no standard schema for CPS's lead reports, `validate.py` matches table columns against a few different common patterns to try to identify the correct columns for each report. These patterns are defined in lines 41-110, under the method name `pattern_<number>`.

If CPS introduces new table schemas in the future and `validate.py` can't understand them, it will print an error to your shell and include the row that it couldn't parse. Confirm that the issue was a schema error by checking that the previous traceback was to the `pattern_10` method (or whatever `pattern` method is the last pattern in your script); once you've identfied the issue, you can define a new `pattern` method to handle the new schema. Append your new method to the list of patterns in the `clean` function call that starts in line 225 and `validate.py` will match future rows against it. 

### Samples testing above 400 ppb

Time columns that were incorrectly labelled as sample results formed a persistent error in the Summer 2016 reports. After processing, military time units (e.g. `0600`) were sometimes functionally indistinguishable from sample units by the machine, resulting in erroneously high sample results for some schools. 

To handle this error, we included a threshold on line 134 in the `to_result` method that would flag any sample column with a reading higher than 400 ppb, stopping the script and printing the row to the shell. After confirming that the column was indeed a sample result and not an incorrectly-labeled time, we added the school name to a list of schools that tested above the threshold in the exception handling on line 212.

In the future, this list of schools will most likely not be the same. When running the code on a new set of data, empty the list between lines 212-222, and rerun the script to confirm new high-testing schools by hand.

It may seem tedious to confirm each high-testing school by hand, but it can also help you generate ideas for reporting. 400 ppb is significantly higher than the federal action level for lead tests (15 ppb), so you might want your reporters to look into schools with fixtures that persistently test higher than 400 ppb. 
