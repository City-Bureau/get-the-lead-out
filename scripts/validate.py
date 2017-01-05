import sys
import csv
import re
import datetime

from config import (SCHOOLS_WITH_RESULTS_OVER_400, 
                    SCHOOLS_WITH_KNOWN_SCRAPE_ERRORS)

def clean(row, patterns, force=False):
    if not force:
        for pattern in patterns:
            try:
                return pattern(row)
            except:
                continue
        else:
            pattern(row)
    else:
        for pattern in patterns:
            try:
                return pattern(row, force=True)
            except:
                continue
        else:
            pattern(row)

def school_source(group):
    pdf = group.replace('.csv', '')
    school = re.findall(r'.ndividual.chools*_(.*?)_\d\d\d\d', pdf)[0].title()
    if school == 'Lasalle_Ii':
        school = 'LaSalle II'
    source = 'http://www.cps.edu/SiteCollectionDocuments/LeadTesting/' + pdf
    return school, source

def validate(group, sample, location, date, test_result, force=False):
    assert re.match(r'^[\w\d/-]+$', sample) is not None
    school, source = school_source(group)

    if not force:
        return (school, sample, location, to_time(date, DATE_FORMATS), to_result(test_result), source)
    else:
        return (school, sample, location, to_time(date, DATE_FORMATS), to_result(test_result, force=True), source)      

def pattern_1(row, force=False):
    group, sample, location, date, test_result, *rest = row
    if not force:
        return validate(group, sample, location, date, test_result)
    else:
        return validate(group, sample, location, date, test_result, force=True)

def pattern_2(row, force=False):
    group, sample, location, _, date, *mid, test_result, _ = row
    if not force:
        return validate(group, sample, location, date, test_result)  
    else:
        return validate(group, sample, location, date, test_result, force=True)  

def pattern_3(row, force=False):
    group, sample, location, _, date, test_result, *rest = row
    if not force:
        return validate(group, sample, location, date, test_result)
    else:
        return validate(group, sample, location, date, test_result, force=True)

def pattern_4(row, force=False):
    group, _, _, sample, location, _, date, *mid, test_result, _ = row
    if not force:
        return validate(group, sample, location, date, test_result)
    else:
        return validate(group, sample, location, date, test_result, force=True)

def pattern_5(row, force=False):
    group, sample, location_date, test_result, *rest = row
    location, date = re.findall(r'^(.*)((?:1|2|3|4|5|6|7|8|9|10|11|12)/\d{1,2}/\d{1,4}.*)', location_date)[0]
    if not force:
        return validate(group, sample, location, date, test_result)
    else:
        return validate(group, sample, location, date, test_result, force=True)

def pattern_6(row, force=False):
    group, facility_id, sample, location, date, test_result, test_result_2 = row
    if not force:
        return validate(group, sample, location, date, test_result)
    else:
        return validate(group, sample, location, date, test_result, force=True)

def pattern_7(row, force=False):
    group, short_school, facility_id, sample, location, date, test_result, *rest = row
    if not force:
        return validate(group, sample, location, date, test_result)
    else:
        return validate(group, sample, location, date, test_result, force=True)

def pattern_8(row, force=False):
    group, sample, location, date, test_result, test_result_2 = row
    if not force:
        return validate(group, sample, location, date, test_result)
    else:
        return validate(group, sample, location, date, test_result, force=True)

def pattern_9(row, force=False):
    group, sample, location, date, time_in_pipe, test_result, test_result_2 = row
    if not force:
        return validate(group, sample, location, date, test_result)
    else:
        return validate(group, sample, location, date, test_result, force=True)

def pattern_10(row, force=False):
    group, short_school, facility_id, sample, location, date, time, test_result, *rest = row
    if not force:
        return validate(group, sample, location, date, test_result)
    else:
        return validate(group, sample, location, date, test_result, force=True)

def pattern_11(row, force=False):
    group, sample, location, collector_name, fixture_manufacturer, test_result, *rest = row
    date = 'kOqgIOP4XiZZu5CMqq0o'
    if not force:
        return validate(group, sample, location, date, test_result)
    else:
        return validate(group, sample, location, date, test_result, force=True)

def to_time(date_string, date_formats):
    date_string = date_string.replace(' -\xad‐ ', ' ')
    date_string = date_string.replace(' - ', ' ')
    date_string = date_string.replace(']', '')
    for date_format in date_formats:
        try:
            return datetime.datetime.strptime(date_string, date_format)
        except ValueError:
            continue
    else:
        return datetime.datetime.strptime(date_string, date_format)            

def to_result(test_result, force=False):
    if test_result in {'ND', 'None Detected', 'None Detecetd', 'NT'}:
        return 'None Detected'
    elif test_result.startswith('<'):
        return test_result
    elif test_result in {'', 'Sample Not\nSubmitted'}:
        return None

    if force:
        return float(test_result)
    else:
        if float(test_result) > 400:
            raise ValueError
        else:
            return float(test_result)

def clean_sample_id(sample_id) :
    sample_id = sample_id.replace('-­‐', '-')
    sample_id = sample_id.replace('I -', 'I-')
    sample_id = sample_id.replace('51212- B- ', '51212-B-')
    sample_id = sample_id.replace('B -N', 'B-N')
    sample_id = sample_id.replace('- F', '-F')
    sample_id = sample_id.replace('- S', '-S')
    sample_id = sample_id.replace('- N-', '-N-')
    sample_id = sample_id.replace(' S-', '-S-')
    return sample_id

HEADER_FIELDS = {'Sample Collection', 'Time & Date', 'Test Results (ppb)',
                 '(Hours)', 'Length of time water', 'chool Short Name',
                 'Sample ID #', 'Sample Collection Time & Sample ID # Sample Location',
                 'School Name', 'Date', '& Date','Test Results',
                 'Name of CCA or GSG Sample ID # Sample Location',
                 'Sample ID # Sample Location Sample Collection Time & Date',
                 'remained in pipes Sample ID # Sample Collection Time & Test ResultsDate', 'ppb LevelTime & DateTest Results (ppb)'}

CSV_HEADER = ['school', 'sample', 'location', 'date', 'result', 'pdf']

DATE_FORMATS =  ('%m/%d/%y %I:%M %p',
                 '%m/%d/%Y %I:%M %p',
                 '%m/%d/%y %I:%M%p',
                 '%m/%d/%Y %I:%M%p',
                 '%m/%d/%y %I:%M',
                 '%m/%d/%Y %I%p',
                 '%m/%d %I:%M',
                 '%m/%d/%y',
                 '%I:%M%p',
                 '%I:%M%p',
                 '%I:%M %p %m/%d/%y',
                 '%I:%M%p %m/%d/%y',
                 '%I:%M%p %m/%d//%y',
                 'kOqgIOP4XiZZu5CMqq0o')

PATTERNS = (pattern_1, pattern_2,
            pattern_3, pattern_4,
            pattern_5, pattern_6,
            pattern_7, pattern_8,
            pattern_9, pattern_10,
            pattern_11)

reader = csv.reader(sys.stdin)
next(reader)

out_writer = csv.writer(sys.stdout)
out_writer.writerow(CSV_HEADER)

with open('err.csv', 'w') as err_file:
    err_writer = csv.writer(err_file)

    for row in reader:
        if HEADER_FIELDS & set(row):
            continue
        row[1] = clean_sample_id(row[1])
        try:
            out_writer.writerow(clean(row, PATTERNS))
        except:
            if row[0] in SCHOOLS_WITH_RESULTS_OVER_400:
                try:
                    out_writer.writerow(clean(row, PATTERNS, force=True))
                except:
                    if (len(row) < 5
                        or re.match(r'^[\w\d/-]+$', row[1]) is None
                        or row[0] in SCHOOLS_WITH_KNOWN_SCRAPE_ERRORS):
                        school, source = school_source(row[0])
                        row[0] = school
                        row.append(source)
                        err_writer.writerow(row)
            elif (len(row) < 5
                or re.match(r'^[\w\d/-]+$', row[1]) is None
                or row[0] in SCHOOLS_WITH_KNOWN_SCRAPE_ERRORS):
                school, source = school_source(row[0])
                row[0] = school
                row.append(source)
                err_writer.writerow(row)
            else:
                print(row, file=sys.stderr)
                raise

