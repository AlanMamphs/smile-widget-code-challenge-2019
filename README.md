# smile-widget-code-challenge

The Smile Widget Company currently sells two types of smile widgets: a Big Widget and a Small Widget.  We'd like to add more flexibility to our product pricing.

## Setup with Docker
1. Install Docker (https://docs.docker.com/install/)
2. Fork this repository.
3. `>>> docker-compose up --build`

## Setup without Docker
1. Install Python (>3.4)
2. Install postgres.  By default the Django app will connect to the database named 'postgres'.  See `settings.DATABASES`.
3. Fork this repository, then clone your repository locally.
4. Install requirements.
  * `>>> pip install -r requirements.txt`
5. Run migrations.
  * `>>> python manage.py migrate`
6. Load data from fixtures:
  * `>>> python manage.py loaddata 0001_fixtures.json`

### Usage
* Send Get Request to /api/get-price with the below parameter names
    * `"productCode"`
    * `"date"`
    * `"giftCardCode"`(Optional)



## Get Product Price [/api/get-price?productCode=big_widget&date=2019-01-01&giftCardCode=10OFF]
### Product list with date specific prices [GET]


+ Response 200 (application/json)
    
      
    + Body

               [
                    {
                        "price": 119000,
                        "id": 1,
                        "name": "Big Widget"
                    },
                    {
                        "price": 10000,
                        "id": 3,
                        "name": "Big Widget"
                    }
                ]         
        
               
+ Response 400 (application/json)

    - No productCode and date get params
    
    + Body

                {
                    "date": [
                        "Date has wrong format. Use one of these formats instead: YYYY-MM-DD."
                    ],
                    "code": [
                        "Please include productCode in get parameters"
                    ]
                }


