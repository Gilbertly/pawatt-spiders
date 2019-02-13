import logging
import boto3
from boto3.s3.transfer import S3Transfer
from scrapy.exceptions import DropItem


class S3Pipeline(object):
  @classmethod
  def from_crawler(cls, crawler):
    return cls(crawler.settings)
  
  def __init__(self, settings):
    self.settings = settings
    self.new_items = 0
    self.access_key = settings.get("AWS_ACCESS_KEY_ID")
    self.secret_key = settings.get("AWS_SECRET_ACCESS_KEY")
    self.s3_bucket = settings.get("S3_BUCKET")
    self.pdf_path = settings.get("PDF_PATH")

  def process_item(self, item, spider):
    file_name = item["data"]
    file_path = "{}{}".format(self.pdf_path, file_name)

    client = boto3.client(
      "s3",
      aws_access_key_id=self.access_key, 
      aws_secret_access_key=self.secret_key
    )
    transfer = S3Transfer(client)
    logging.info("Uploading pdf to S3 ...")
    transfer.upload_file(
      file_path,
      self.s3_bucket,
      "outages-ug/"+file_name
    )
    self.new_items += 1
    logging.info("Uploaded pdf '{}' to S3.".format(file_path))
  
  def close_spider(self, spider):
    logging.info("Items New: '{}'".format(
      self.new_items
    ))
