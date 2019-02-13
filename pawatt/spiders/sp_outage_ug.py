import logging
import scrapy 
from scrapy import Spider
from pawatt.items import OutageItemUG


class OutageSpiderUG(Spider):
  name = "sp_outage_ug"
  allowed_domains = ["www.umeme.co.ug"]
  root_url = "https://www.umeme.co.ug/"
  start_urls = [
    "{}planned-outages/".format(root_url)
  ]

  def parse(self, response):
    base_query = "//div[@id='x-root']\
      /div[@id='x-site']\
      /div[@class='x-main full']\
      /article//div[@id='x-section-2']\
      /div[2]/div/a/@href"
    
    outage_url = response.xpath(base_query).extract_first()
    yield scrapy.Request(outage_url, self.save_pdf)
  
  def save_pdf(self, response):
    pdf_name = response.url.split("/")[5]
    pdf_path = "pawatt/data/{}".format(pdf_name)
    logging.info("Saving pdf file '{}' ...".format(pdf_name))
    with open(pdf_path, "wb") as file:
      file.write(response.body)
      logging.info("Saved pdf file '{}'.".format(pdf_name))
      yield OutageItemUG({"data": pdf_name})
