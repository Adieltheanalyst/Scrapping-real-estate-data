import scrapy
import os
import json

class PropertyDetailsSpider(scrapy.Spider):
    name = "property_details"
    def start_requests(self):
        with open(r"C:\Users\gacha\PycharmProjects\kenyan realestate\realestate\urls.json","r") as f:
            data=json.load(f)
            urls=[entry["url"] for entry in data]
            for url in urls:
                yield scrapy.Request(url=url,callback=self.parse)


    def parse(self,response):
        # price_cleaned=response.css(r".md\:font-extrabold::text").get()
        price_cleaned = response.css(".md\\:font-extrabold::text").get()
        if price_cleaned:
            price = price_cleaned.replace("KSh ", "").replace(",", "").strip()
        else:
            self.logger.warning(f"Missing price on page: {response.url}")
            price = None
        location_raw = response.css(r".text-gray-500.md\:hidden::text").get()
        location = location_raw.strip() if location_raw else None
        internal_features_raw=response.css(r".w-full:nth-child(1) .even\:bg-gray-50:nth-child(1) .text-base::text").getall()
        internal_features = ",".join(u.strip() for u in internal_features_raw if u.strip())
        title = response.xpath('//h1[@data-cy="listing-heading"]/text()').get()
        title = title.strip() if title else None
        date_posted_raw=response.xpath(r'//div[@class="flex w-full justify-between py-2"]/span/text()').get().strip()
        date_posted = date_posted_raw.replace("Created At: ","")
        external_features_raw = response.css(r'.even\:bg-gray-50+ .even\:bg-gray-50 .text-base::text').getall()
        external_features=",".join(u.strip() for u in external_features_raw if u.strip())
        nearby_raw = response.css(r'.flex-col+ .flex-col .text-base.text-grey-550::text').getall()
        nearby = ",".join(u.strip() for u in nearby_raw if u.strip())
        size = response.css(".md\:gap-x-8+ .md\:gap-x-8 .md\:justify-end::text").get()
        school_divs = response.css(".md\:border:nth-child(1) .md\:py-4 .w-full")  # Select all school blocks

        nearby_schools = []
        for school in school_divs :
            name = school.css(".md\:text-base::text").get()
            distance_raw = school.css(".text-gray-500 span+ span::text").re_first(r'approx\.\s*([\d,\.]+)\s*(m|km)')

            nearby_schools.append({
                "name": name.strip(),
                "approximate_distance(m)": distance_raw
            })
        recreation_divs = response.css(".md\:border+ .md\:border .md\:py-4 .w-full")  # Select all school blocks

        nearby_recreation = []
        for recreation in recreation_divs:
            name = recreation.css(".md\:text-base::text").get()
            distance_raw = recreation.css(".text-gray-500 span+ span::text").re_first(r'approx\.\s*([\d,\.]+)\s*(m|km)')
            nearby_recreation.append({
                "name": name.strip(),
                "approximate_distance(m)": distance_raw
            })

        yield {
            "title": title,
            "price_ksh": price,
            "location": location,
            "date_posted": date_posted,
            "size": size.strip() if size else None,
            "internal_features": internal_features,
            "external_features": external_features,
            "nearby_amenities": nearby,
            "nearby_schools": nearby_schools,
            "nearby_recreation": nearby_recreation,
        }