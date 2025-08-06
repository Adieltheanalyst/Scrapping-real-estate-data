import scrapy
class project_37(scrapy.Spider):
    name="property_urls"
    start_urls=[
        "https://www.buyrentkenya.com/property-for-sale/nairobi"
    ]
    def parse(self,response):
        for property_link in response.css('a[data-cy="listing-information-link"]::attr(href)').getall():
            full_url=response.urljoin(property_link)
            yield {"url": full_url}
        for i in range(1,274):
            next_page=(f"https://www.buyrentkenya.com/property-for-sale/nairobi?page={i}")
            if next_page:
                yield response.follow(next_page, self.parse)

