'''To create pydantic model for credentials'''
from pydantic_settings import BaseSettings
from requests_oauthlib import OAuth1

class Settings(BaseSettings):
    '''class for tumbler credentials'''

    CONSUMER_KEY:str
    CONSUMER_SECRET:str
    TOKEN:str
    TOKEN_SECRET:str
    BLOG_IDENTIFIER:str
    DATABASE_URL:str
    class Config:
        '''to config with .env file'''
        env_file=".env"
        env_file_encoding = 'utf-8'

settings=Settings()
auth = OAuth1(settings.CONSUMER_KEY,settings.CONSUMER_SECRET,settings.TOKEN,settings.TOKEN_SECRET)
