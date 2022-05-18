from scrapy import Request, FormRequest
from uuid import uuid4
import csv
import scrapy

class properties_data(scrapy.Spider):
    name="properties_data"

    def start_requests(self):
        yield Request('http://www.onlineumc.org.in:8080/umc/jsp/propertyduessearch.jsp?id=0&lang=1',
            meta={'cookiejar':str(uuid4)},
            callback=self.parse)

    def parse(self,response):
        data=response.xpath('//*[@name="propward"]/option/@value')[1:11].extract()
        
        for property_no in data:
            yield FormRequest('http://www.onlineumc.org.in:8080/umc/jsp/propertyduessearch.jsp',
                formdata = {
                    'txtFName': '',
                    'txtSName':'', 
                    'txtLName':'' ,
                    'oldpropno':'', 
                    'propward': str(property_no),
                    'lang': "1"},
                    meta={'cookiejar':str(uuid4)},
                    callback=self.next_page)

    def next_page(self,response):
        pages = response.xpath('//*[@class="bluetext"]/td[@class="contentmarathi"]/a/@href').extract()
        
        for page in pages:
            
            yield Request('http://www.onlineumc.org.in:8080/umc/jsp/{}'.format(page),
            meta={'cookiejar':str(uuid4)},
            callback=self.pages_data)

    def pages_data(self,response):
        table=response.xpath('//*[@id="cash"]/table/tr')
        
        with open('properties_data.csv','w') as f:
            for td in table.xpath('.//td'):
                
                for a in td.xpath('.//a/font/text()').extract():
                    
                    f.write(a)
                    f.write("\n") 
                        
# # page no seven scrape 