FROM python:3.9.2

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV access_token=1372051636772741120-YrW3XljpG3s20IsvBf6ubdsQGciKBk
ENV access_token_secret=FPC8Tfdkccah3fR7X9MfCyPyU5prOHCVMtBxwAMZHOdN3
ENV agent_id=1a881bd1-4321-4bc0-9266-25e52450506817fb583a205358
ENV API_KEY_mebo=2f187337-6c08-4430-b013-0aa31533e94e17fba0db70d13c
ENV bearer_token=AAAAAAAAAAAAAAAAAAAAABEvUgEAAAAArv%2BcT6IdpXbJn22xebUWiDsLjvw%3DoQBL8VDdb7qyKp7Y3qdzQxgrb5iocRuRuf5OG8iKHnen9ES3nT
ENV consumer_key=BBYsKlf3hijpExb75R5EYvGd2
ENV consumer_secret=hxvhAWsJ3dPSQrwsxaCPTmIW5FlHy9WsZFRx3g8BZ3INH2uOCI

COPY . .

CMD [ "python", "./main.py" ]