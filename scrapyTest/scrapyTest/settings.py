BOT_NAME = 'scrapyTest'

SPIDER_MODULES = ['scrapyTest.spiders']
NEWSPIDER_MODULE = 'scrapyTest.spiders'

ROBOTSTXT_OBEY = False

# El código clave, sin esta sección, es imposible guardar
ITEM_PIPELINES = {
   'scrapyTest.pipelines.ScrapytestPipeline': 300,
}
