import configparser

config = configparser.RawConfigParser()
config.read("configurations\config.ini")

class Read_Config:
    @staticmethod
    def get_amazon_url():
        url = config.get('amazon url','amazon_url')
        return url