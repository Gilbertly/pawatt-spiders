import scrapy 
from scrapy import Item, Field


class OutageItemUG(Item):
	data = Field()
	def __str__(self):
		return ""


class OutageItemKE(Item):
	data = Field()
	def __str__(self):
		return ""
