# Twitter scrapper


## Dockerr

- docker build -t scrap_test .
- docker docker run -t -p 8000:8000 scrap_test:latest


## APi

- curl -X POST -H 'Content-Type: application/json' http://0.0.0.0:8000/scrap -d'{"words": ["btc","bitcoin"],"start_date": "2021-06-24","max_date": "2021-06-25"}'

### it return a json file with result of scrapping like this:
![Screenshot](curl_result.png)


