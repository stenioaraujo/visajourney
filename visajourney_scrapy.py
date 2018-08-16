import requests_html
import scrapy


class VisaJourneyK1Spider(scrapy.Spider):
    name = "k1_timelines"
    base_url = (
        "http://www.visajourney.com/timeline/k1list.php?cfl=0&op1=&op2=&op3=1"
        "&op4={page}&op5=5,6,8,10,11,13,14,15,16,17,18,20,21,22,25,26,27,28,108,"
        "110,111,208,210,211&op6=All&op66=All&op7={country}&dfile=No&adv=1"
    )
    column_names = [
        "Names", "Country", "Service Center", "Xfer?", "Consulate",
        "I-129F Sent", "I-129F NOA1", "I-129F RFE(s) Received",
        "I-129F RFE(s) Sent", "I-129F NOA2", "NVC Received", "NVC Left",
        "Consulate Received", "Packet 3 Received", "Packet 3 Sent",
        "Packet 4 Received", "Interview", "Visa Received", "US Entry",
        "Marriage", "Total Days File ➙ Int.", "I-129F Mail to 1st NOA",
        "I-129F NOA1 to NOA2", "I-129F NOA2 to Interview",
        "Comments. List anything unique to your case.", "Updated Last"
    ]
    custom_settings = {
        "CONCURRENT_REQUESTS": 500
    }
    country = "Brazil"
    start_page = 1
    end_page = 200

    def __init__(self, *args, **kwargs):
        self.start_urls = []
        for i in range(self.start_page, self.end_page):
            self.start_urls.append(self._page(i))

        scrapy.Spider.__init__(self, *args, **kwargs)

    def parse(self, response):
        body = requests_html.HTML(html=response.css("body").extract_first())
        current_page = body.find(".pagecurrent", first=True)
        if current_page is None:
            return None

        for row in body.find('table.pme-main tr'):
            columns = row.find("td")

            timeline = {}
            for i, column in enumerate(columns):
                timeline[self.column_names[i]] = self._text(column)
            
            if timeline:
                yield timeline
    
    def _page(self, page=1):
        return self.base_url.format(page=page, country=self.country)

    def _text(self, column):
        if column:
            text = column.text.strip().replace('"', "'")
            words = text.split()
            formated_text = ' '.join(words)
            return formated_text
