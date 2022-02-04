
class ScrapytestPipeline(object):

    def open_spider(self,spider):
        #Cree el archivo my.txt y establezca el conjunto de caracteres en utf-8
        self.file = open('my.txt', 'w', encoding='utf-8') 
 
    def close_spider(self,spider):
        self.file.close()
 
    def process_item(self, item, spider):
        # Guarde el texto rastreado en my.txt; al escribir un diccionario, enumere la colección en txt, use str ()
        self.file.write(str(item)+'\n')     

