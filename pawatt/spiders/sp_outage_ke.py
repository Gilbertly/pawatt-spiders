import logging
import scrapy
from scrapy import Spider
from pawatt.items import OutageItemKE
from os.path import join, dirname


class OutageSpiderKE(Spider):
  name = "sp_outage_ke"
  allowed_domains = ["kplc.co.ke"]
  root_url = "https://kplc.co.ke/"
  start_urls = [f"{root_url}category/view/50/planned-power-interruptions"]

  def parse(self, response):
    base_query = "//div[@class='items']\
      //div[@class='contentrow']\
      //div//a/@href"

    outage_url = response.xpath(base_query).extract_first()
    yield scrapy.Request(outage_url, self.save_pdf)

  def save_pdf(self, response):
    pdf_name = response.url.split("---")[-1].strip(" ") + ".pdf"
    pdf_path = join(dirname(__file__), f"../data/{pdf_name}")
    file_url = response.url

    data = {
      "pdf_name": pdf_name,
      "file_url": file_url
    }

    try:
      with open(pdf_path, "wb") as file:
        logging.info("Saving pdf file '{}' ...".format(pdf_name))
        file.write(response.body)
        logging.info("Saved pdf file '{}'.".format(pdf_name))
      yield OutageItemKE({"data": data, "io_error": False})
    except IOError as error:
      logging.info("IOError: '{}'".format(error))
      yield OutageItemKE({"data": data, "io_error": True})
