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
    upload_filepath = f"raw/{upload_folder_year}/{file_name}"

    if item["io_error"]:
      file_url = item["data"]["file_url"]
      self.stream_to_s3(upload_filepath, file_url)
      self.new_items += 1
    else:
      file_path = f"{self.pdf_path}{file_name}"
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
        upload_filepath
      )
      self.new_items += 1
      logging.info(f"Uploaded pdf '{file_name}' to S3.")

    return item

  def stream_to_s3(self, upload_filepath, file_url):
    logging.info(f"Streaming '{upload_filepath}' into S3 ...")
    resp = call(f"wget -qO- '{file_url}' | AWS_ACCESS_KEY_ID={self.access_key} AWS_SECRET_ACCESS_KEY={self.secret_key} aws s3 cp - s3://{self.s3_bucket}/{upload_filepath}", shell=True)
    if not resp:
      logging.info(f"Successfully streamed '{upload_filepath}' into S3!")
    else:
      logging.info(f"Error streaming into S3 file path!")

  def close_spider(self, spider):
    logging.info(f"Items New: '{self.new_items}'")
