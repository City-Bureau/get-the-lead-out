import sys
import csv
import re
import datetime

def clean(row, patterns):
    for pattern in patterns:
        try:
            return pattern(row)
        except:
            continue
    else:
        pattern(row)

def school_source(group):
    pdf = group.replace('.csv', '')
    school = re.findall(r'Individual.chool_(.*?)_\d\d\d\d', pdf)[0].title()
    if school == 'Lasalle_Ii':
        school = 'LaSalle II'
    source = 'http://www.cps.edu/SiteCollectionDocuments/LeadTesting/' + pdf
    return school, source

def validate(group, sample, location, date, test_result):
    assert re.match(r'^[\w\d/-]+$', sample) is not None
    school, source = school_source(group)
    return (school, sample, location, to_time(date, DATE_FORMATS), to_result(test_result), source)
            
def pattern_1(row):
    group, sample, location, date, test_result, *rest = row
    return validate(group, sample, location, date, test_result)

def pattern_2(row):
    group, sample, location, date, test_result, *rest = row
    test_result = re.sub(r' (ND|BA)$', '', test_result)
    return validate(group, sample, location, date, test_result)    

def pattern_3(row):
    group, sample_location, date, test_result, *rest = row
    sample, location = re.findall(r'^([\w\d]+-[\w\d/-]+)\s(.*)', sample_location)[0]
    return validate(group, sample, location, date, test_result)    

def pattern_4(row):
    group, sample_location, _, date, *mid, test_result, _ = row
    sample, location = re.findall(r'^([\w\d]+-[\w\d/-]+)\s(.*)', sample_location)[0]
    return validate(group, sample, location, date, test_result)    

def pattern_5(row):
    group, _, sample, location, date, test_result, *rest = row
    return validate(group, sample, location, date, test_result)

def pattern_6(row):
    group, sample_location_date, test_result, *rest = row
    sample, location, date = re.findall(r'^([\w\d]+-[\w\d/-]+)\s(.*)\s(\d{1,2}/\d{1,2}/\d{1,4}.*)', sample_location_date)[0]
    return validate(group, sample, location, date, test_result)

def pattern_7(row):
    group, sample, location, _, date, test_result, *rest = row
    return validate(group, sample, location, date, test_result)

def pattern_8(row):
    group, sample_location, date_test_result, *rest = row
    sample, location = re.findall(r'^([\w\d]+-[\w\d/-]+)\s(.*)', sample_location)[0]
    date, test_result = re.findall(r'^(.*?(?:AM|PM))\s(.*)$', date_test_result)[0]
    return validate(group, sample, location, date, test_result)

def pattern_9(row):
    group, _, _, sample, location, _, date, *mid, test_result, _ = row
    return validate(group, sample, location, date, test_result)

def pattern_10(row):
    group, sample, location_date, test_result, *rest = row
    location, date = re.findall(r'^(.*)\s(\d{1,2}/\d{1,2}/\d{1,4}.*)', location_date)[0]
    return validate(group, sample, location, date, test_result)

def pattern_11(row):
    group, sample, location, date_test_result, *rest = row
    date, test_result = re.findall(r'^(.*?(?:AM|PM))\s(.*)$', date_test_result)[0]
    test_result = re.sub(r' (ND|BA|AA)$', '', test_result)
    return validate(group, sample, location, date, test_result)

def pattern_12(row):
    group, sample_date, test_result, *rest = row
    sample, date = re.findall(r'^([\w\d]+-[\w\d/-]+)\s(.*)$', sample_date)[0]
    location = None
    return validate(group, sample, location, date, test_result)

def pattern_13(row):
    group, sample, location_date_test_result, *rest = row
    location, date, test_result = re.findall(r'^(.*)\s(\d{1,2}/\d{1,2}/\d{1,4}.*(?:AM|PM))\s(.*)$', location_date_test_result)[0]
    return validate(group, sample, location, date, test_result)

def pattern_14(row):
    group, sample, location, date_test_result, *rest = row
    date, test_result = re.findall(r'^(.*?\s\d{1,2}/\d{1,2}/\d{1,4})\s(.*)', date_test_result)[0]
    return validate(group, sample, location, date, test_result)

def pattern_15(row):
    group, _, _, sample, location, date, test_result, *rest = row
    return validate(group, sample, location, date, test_result)

def to_time(date_string, date_formats):
    date_string = date_string.replace(' -\xad‐ ', ' ')
    for date_format in date_formats:
        try:
            return datetime.datetime.strptime(date_string, date_format)
        except ValueError:
            continue
    else:
        return datetime.datetime.strptime(date_string, date_format)            

def to_result(test_result):
    if test_result in {'ND', 'None Detected', 'None Detecetd'}:
        return 'None Detected'
    elif test_result.startswith('<'):
        return test_result
    elif test_result == '':
        return None
    return float(test_result)

def clean_sample_id(sample_id) :
    sample_id = sample_id.replace('-­‐', '-')
    sample_id = sample_id.replace('I -', 'I-')
    sample_id = sample_id.replace('51212- B- ', '51212-B-')
    sample_id = sample_id.replace('B -N', 'B-N')
    sample_id = sample_id.replace('- F', '-F')
    sample_id = sample_id.replace('- S', '-S')
    return sample_id

HEADER_FIELDS = {'Sample Collection', 'Time & Date', 'Test Results (ppb)',
                 '(Hours)', 'Length of time water', 'chool Short Name',
                 'Sample ID #', 'Sample Collection Time & Sample ID # Sample Location',
                 'School Name',
                 'Name of CCA or GSG Sample ID # Sample Location',
                 'Sample ID # Sample Location Sample Collection Time & Date',
                 'remained in pipes Sample ID # Sample Collection Time & Test ResultsDate', 'ppb LevelTime & DateTest Results (ppb)'}

DATE_FORMATS =  ('%m/%d/%y %I:%M %p',
                 '%m/%d/%Y %I:%M %p',
                 '%m/%d/%y %I:%M%p',
                 '%m/%d/%Y %I:%M%p',
                 '%m/%d/%y %I:%M',
                 '%m/%d/%Y %I%p',
                 '%m/%d %I:%M',
                 '%I:%M %p %m/%d/%y',
                 '%I:%M%p %m/%d/%y')

reader = csv.reader(sys.stdin)
next(reader)

out_writer = csv.writer(sys.stdout)

with open('err.csv', 'w') as err_file:
    err_writer = csv.writer(err_file)

    for row in reader:
        if HEADER_FIELDS & set(row):
            continue
        row[1] = clean_sample_id(row[1])
        try:
            out_writer.writerow(clean(row, (pattern_1,
                                            pattern_2,
                                            pattern_3,
                                            pattern_4,
                                            pattern_5,
                                            pattern_6,
                                            pattern_7,
                                            pattern_8,
                                            pattern_9,
                                            pattern_10,
                                            pattern_11,
                                            pattern_12,
                                            pattern_13,
                                            pattern_14,
                                            pattern_15)))
        except:
            if row[0] in {'Individualschool_Beidler_609797.pdf.csv',
                          'Individualschool_Blair_610087.pdf.csv',
                          'Individualschool_Budlong_609817.pdf.csv',
                          'Individualschool_Burroughs_609829.pdf.csv',
                          'Individualschool_Camras_610539.pdf.csv',
                          'Individualschool_Dawes_609879.pdf.csv',
                          'Individualschool_Fulton_609929.pdf.csv',
                          'Individualschool_Goethe_609942.pdf.csv',
                          'Individualschool_Haugan_609972.pdf.csv',
                          'Individualschool_Nightingale_610096.pdf.csv',
                          'Individualschool_Peirce_610122.pdf.csv',
                          'Individualschool_Ravenswood_610141.pdf.csv',
                          'Individualschool_Ray_610142.pdf.csv',
                          'Individualschool_Reilly_610144.pdf.csv',
                          'Individualschool_Rogers_610147.pdf.csv',
                          'Individualschool_Saucedo_610017.pdf.csv',
                          'Individualschool_Tanner_610279.pdf.csv',
                          'Individualschool_Vick_609871.pdf.csv',
                          'Individualschool_VonLinne_610039.pdf.csv',
                          'Individualschool_Washington_610124.pdf.csv',
                          'Individualschool_Wentworth_610223.pdf.csv',
                          'Individualschool_Whitney_610227.pdf.csv',
                          'Individualschool_whittier_610228.pdf.csv'}:
                school, source = school_source(row[0])
                row[0] = school
                row.append(source)
                err_writer.writerow(row)
