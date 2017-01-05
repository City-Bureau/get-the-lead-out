# our validating scrape treats results over 400 ppb as read errors,
# but lead was found in exceptional amounts in some schools. this
# is a list of the csv files corresponding to those schools, which
# will be excepted from the 400 ppb rule.

SCHOOLS_WITH_RESULTS_OVER_400 = [
    'IndividualSchool_Wells_610110.pdf.csv',
    'Individualschool_Beasley_610246.pdf.csv',
    'IndividualSchool_Hamline_609964.pdf.csv',
    'IndividualSchool_Kershaw_610019.pdf.csv',
    'Individualschool_Blair_610087.pdf.csv',
    'Individualschool_Bouchet_609815.pdf.csv',
    'Individualschool_Mireles_610171.pdf.csv',
    'Individualschool_Onahan_610104.pdf.csv',
    'Individualschool_Sherman_610172.pdf.csv',
    'IndividualSchool_Pullman_610139.pdf.csv',
    'IndividualSchool_Orr_610389.pdf.csv'
]

# tabula-java is wonderful but imperfect. add filenames for schools
# where the majority of results are misread during the scraping
# process to omit them from automatic validation, and deal with
# them by hand.

SCHOOLS_WITH_KNOWN_SCRAPE_ERRORS = [
    'IndividualSchool_Libby_610037.pdf.csv',
    'Individualschool_Ravenswood_610141.pdf.csv'
]