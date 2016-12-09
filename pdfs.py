import csv
import requests

with open('CPSLeadTestingMap.csv') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        filename = row[6]
        url = 'http://cps.edu/SiteCollectionDocuments/LeadTesting/' + filename
        response = requests.get(url)
        with open(filename, 'wb') as outfile:
            outfile.write(response.content)
        print(filename)
        
        

