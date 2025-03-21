from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
import requests
from dotenv import load_dotenv; load_dotenv()
import os


app = FastAPI()


DOMAIN = os.getenv('DOMAIN')
table_original_short = {}
table_short_original = {}


serial = 0
def generate_short_url():
    global serial
    serial += 1
    return f'{serial}'


@app.get('/urls')
def root(short_url):
    try:
        original_url = table_short_original[f'{short_url}']
        return JSONResponse(
            content={
                'data': {'original_url': f'{original_url}'},
                'errors': []
            },
            status_code=status.HTTP_200_OK
        )
    except:
        return JSONResponse(
            content={
                'message': '',
                'errors': [{'UrlNotFound': 'This URL does not exist'}]
            },
            status_code=status.HTTP_404_NOT_FOUND
        )

@app.post('/shorten')
def shorten(original_url):
    if original_url in table_original_short.keys():
        return JSONResponse(
            content={
                'data':{
                    'message': f'URL already exists. Shortened version: {DOMAIN}?url={table_original_short[original_url]}'
                },
                'errors': []
            },
            status_code=status.HTTP_208_ALREADY_REPORTED
        )
    else:
        short_url = generate_short_url()

        try:
            requests.get(f'{original_url}')
        except:
            return JSONResponse(
                content={
                    'message': '',
                    'errors': [
                        {'UrlNotReachable': 'This URL can not be reached'}
                    ]
                },
                status_code=status.HTTP_400_BAD_REQUEST
            )

        table_original_short.update(
            {original_url: short_url}
        )
        table_short_original.update(
            {short_url: original_url}
        )

        return JSONResponse(
            content={
                'data': {
                    'new_url': f'{DOMAIN}/urls?short_url={table_original_short[original_url]}'
                }
            },
            status_code=status.HTTP_201_CREATED
        )
        