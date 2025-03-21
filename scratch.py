from dotenv import load_dotenv; load_dotenv()
import os


d = {
    'a': '1',
    'b': '2'
}

print('a' in d.keys(), 'c' in d.keys())

DOMAIN = os.getenv('DOMAIN')
print(DOMAIN); exit()
