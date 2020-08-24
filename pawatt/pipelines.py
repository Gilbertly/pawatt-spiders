import logging
import boto3
from boto3.s3.transfer import S3Transfer
from scrapy.exceptions import DropItem
from subprocess import call


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
    file_name = item["data"]["pdf_name"]
    upload_folder_year = file_name.split(".")[-2]

    if item["io_error"]:
      file_url = item["data"]["file_url"]
      self.stream_to_s3(file_name, file_url)
      self.new_items += 1
    else:
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
        f"raw/{upload_folder_year}/"+file_name
      )
      self.new_items += 1
      logging.info("Uploaded pdf '{}' to S3.".format(file_path))

    return item

  def stream_to_s3(self, file_name, file_url):
    logging.info("Streaming '{}' into S3 ...".format(file_name))
    resp = call(
      "wget -qO- '{}' | AWS_ACCESS_KEY_ID={} AWS_SECRET_ACCESS_KEY={} aws s3 cp - s3://{}/outages-ug/{}".format(
        file_url, self.access_key, self.secret_key, self.s3_bucket, file_name
      ), shell=True)
    if not resp:
      logging.info("Successfully streamed '{}' into S3!".format(file_name))
    else:
      logging.info("Error streaming '{}' into S3!".format(file_name))

  def close_spider(self, spider):
    logging.info("Items New: '{}'".format(
      self.new_items
    ))
