import os
from dotenv import load_dotenv

load_dotenv()

print("MYSQL_HOST:", os.getenv('MYSQL_HOST'))
print("MYSQL_PORT:", os.getenv('MYSQL_PORT'))
print("MYSQL_USER:", os.getenv('MYSQL_USER'))
print("MYSQL_PASSWORD:", os.getenv('MYSQL_PASSWORD'))
print("MYSQL_DATABASE:", os.getenv('MYSQL_DATABASE'))
