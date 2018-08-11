import codecs
import os

from requests_html import HTMLSession

session = HTMLSession()

# Replace the default behavior of decode to replace unkown characters
codecs.register_error('strict', codecs.replace_errors)

BASE_PATH = (
    "http://www.visajourney.com/timeline/k1list.php?cfl=0&op1=&op2=&op3=1"
    "&op4={page}&op5=5,6,8,10,11,13,14,15,16,17,18,20,21,22,25,26,27,28,108"
    ",110,111,208,210,211&op6=All&op66=All&op7={country}&dfile=No&adv=1"
)

def login(username, password):
    data = {
        "auth": username,
        "password": password,
        "remember_me": 1,
        "_processLogin": "usernamepassword"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    return session.post(
        "http://www.visajourney.com/login",
        headers=headers, data=data)


def timeline(page, country):
    # path = (
    #     "http://www.visajourney.com/timeline/k1list.php?cfl=0&op1=q&op2=a"
    #     "&op3=&op4={page}&op5=5,6,8,10,11,13,14,15,16,17,18,20,21,22,25,26"
    #     ",27,28,108,110,111,208,210,211&op6=All&op66=All&op7={country}"
    #     "&dfile=No&adv=1").format(page=page, country=country)
    path = BASE_PATH.format(page=page, country=country)
    return session.get(path)


def timeline_table(page=1, country="Brazil"):
    table_selector = "#ipsLayout_mainArea .pme-main"
    
    t = timeline(page, country)
    table = t.html.find(table_selector, first=True)
    
    return table

def table_top(table):
    top = table.find("tr")[0]

    columns = top.find("th")
    top_headers = []
    for column in columns:
        top_headers.append(_format_text(' '.join(column.text.split())))

    return top_headers


def table_body(table):
    rows = table.find("tr")

    body_rows = []
    for row in rows[1:]:
        columns = row.find("td")
        row_elements = []
        for column in columns:
            row_elements.append(_format_text(column.text))

        body_rows.append(row_elements)
    
    return body_rows


def append_rows_to_csv(csv_path, *rows):
    with open(csv_path, "a") as csv_file:
        for row in rows:
            csv_file.write(','.join(row) + '\n')


def _format_text(text):
    text = text if text else ""

    no_quotes = text.replace('"', "'")
    quote_delimited = '"{}"'.format(no_quotes)

    return quote_delimited


username = os.environ.get("VISAJOURNEY_USERNAME")
password = os.environ.get("VISAJOURNEY_PASSWORD")
csv_path = "all_countries_k1_timelines.csv"
country = "All"
start_page = 1
stop_page = 10000

if __name__ == "__main__":
    if os.path.exists(csv_path):
        print("Path {} already exists.".format(csv_path))
        exit(1)
    
    if not username or not password:
        print(
            "Export the Environment Variables VISAJOURNEY_USERNAME "
            "and VISAJOURNEY_PASSWORD with your VisaJourney Credentials.")
        exit(1)
    
    login(username, password)
    
    table = timeline_table(page=1, country=country)
    top = table_top(table)
    append_rows_to_csv(csv_path, top)
    
    print("Processed pages: ", end=" ", flush=True)
    for page in range(start_page, stop_page + 1):
        table = timeline_table(page=page, country=country)
        if not table:
            print("\nAll pages with information processed.")
            exit(1)
        body = table_body(table)
        append_rows_to_csv(csv_path, *body)
        print(page, end=" ", flush=True)

    print("\nPages from {} to {} processed and saved to {}.".format(
        start_page, stop_page, csv_path))