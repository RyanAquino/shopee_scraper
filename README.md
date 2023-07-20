# Shopee Products Scraper
Scrapes shopee.com products per category and saves it to a Postgres database

### Requirements
* Python 3
* Google Chrome
* Selenium Chrome Driver compatible with installed Google Chrome version. Download [here](https://chromedriver.chromium.org/downloads)

### Technology
* Python 3
* Selenium
* Multiprocessing
* Docker
* PostgreSQL

### Setup
##### Create virtual environment
```
python3 -m venv venv
```
##### Install depedencies
```
pip install -r requirements.txt
```
##### Setup PostgreSQL database configuration and adapt to your needs `.env`
```
cp .env.example .env
```
##### Run the application
```
python main.py
```

#### Setup with dockerize PostgreSQL database (Alternative)
```
docker-compose up -d
```
##### Run the application
```
python main.py
```