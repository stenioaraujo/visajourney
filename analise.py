import csv
from datetime import datetime


brazil = []
with open("brazil_k1.csv") as brazil_data:
    data = csv.DictReader(brazil_data)
    fieldnames = data.fieldnames
    fieldnames.insert(-2, "Interview to Visa")
    for row in data:
        brazil.append(row)

interview_to_visa = []
for case in brazil:
    if (case["NVC Received"] != '' and
            "2018" in case["NVC Received"] and
            case["Interview"] != "" and
            case["Visa Received"] != ""):
        interview_to_visa.append(case)

with open("brazil_with_visa.csv", "w") as out:
    result = csv.DictWriter(out, fieldnames=fieldnames)

    result.writeheader()
    for case in interview_to_visa:
        interview = datetime.strptime(case["Interview"], '%Y-%m-%d')
        visa = datetime.strptime(case["Visa Received"], '%Y-%m-%d')
        case["Interview to Visa"] = (visa - interview).days

        result.writerow(case)