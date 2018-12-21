import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

BOT_NAME = 'pawatt'
SPIDER_MODULES = ['pawatt.spiders']
NEWSPIDER_MODULE = 'pawatt.spiders'
LOG_LEVEL = 'INFO'
USER_AGENT = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
# Obey robots.txt rules
ROBOTSTXT_OBEY = True
HTTPERROR_ALLOW_ALL = True
FEED_EXPORT_ENCODING = 'utf-8'
REDIRECT_ENABLED = False

# Configure item pipelines
ITEM_PIPELINES = {
	'pawatt.pipelines.S3Pipeline': 300
}

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
S3_BUCKET = os.environ.get("S3_BUCKET")
PDF_PATH = join(dirname(__file__), "./data/")
