import csv
import requests

with open('raw/CPSLeadTestingMap.csv') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        filename = row[6]
        url = 'http://cps.edu/SiteCollectionDocuments/LeadTesting/' + filename
        response = requests.get(url)
        if response.ok:
           with open(filename, 'wb') as outfile:
               outfile.write(response.content)
            print('%s downloaded' % filename)
        else:
            print('%s not found' % filename)
        
        

