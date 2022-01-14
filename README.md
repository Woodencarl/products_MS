# Applifting entry task REST API Python

This is simple Django REST API micro service to get job at great Applifting company. Assignment can be found in root dir in **Python_task.pdf**
Microservice is build ob Django REST framework na SQLite DB. Background job for updating offers is solved by thred started by any call

## Installation
You need to instal python >= 3.9.7 and pip >= 21.2.4

Then download source code for local running: `git clone --branch local https://github.com/Woodencarl/products_MS`

Go to `prodcuts_MS` directory


You need to setup and activate virtual enviroment: 

`pip install virtualenv`

`python -m venv env`

`env\Scripts\activate`

Install all dependencies from requirements.txt with command: `pip install -r requirements.txt`

Run tests if everything went okay: `python manage.py test`

If all test passed you can start server locally: `python manage.py runserver`

Now you have running backend with API described below.

Default local URL is `http://127.0.0.1:8000/`


##  REST API description

This catalog micro service is deployed on Heroku, so you can test API from some client like Postman.

`https://applifting-entry.herokuapp.com/api/v1`

After first request the automatic updater will start, updating offer for all products every 60 seconds.


## Get list of Products

Get list of all products in database.
### Request

`GET /products`

### Response

    HTTP/1.1 200 OK
    Body:
    {
      "status":true
      "products": [
          {
            "id": <product id>,
            "create": "<creation timestamp, format example: 2022-01-14T10:55:10.912597Z>", 
            "updated": "<update timestamp, format example: 2022-01-14T10:55:10.912597Z>",
            "name": "<product name from request>",
            "description": "<product description form request>"
          }
        ]
    }



## Create a new Product
Create new product and register it to offers service. Only name of new product is required.

### Request

`POST /products/create`

    Body:{
      "name": "<name of new product>" #required
      "description": "<description of new product>" #optional
    }

### Response

    HTTP/1.1 201 Created
    {
    "status": true,
    "product": {
        "id": <product id>,
        "create": "<creation timestamp, format example: 2022-01-14T10:55:10.912597Z>", 
        "updated": "<update timestamp, format example: 2022-01-14T10:55:10.912597Z>",
        "name": "<product name from request>",
        "description": "<product description form request>"
      },
    "offers": [
        {
            "id": <local id of offer>,
            "offer_id": <id of offer in offer service,
            "price": <price>,
            "items_in_stock": <items in stock>,
            "product_id": <product id>
         }
       ]



     HTTP/1.1 400 Bad request
     {
        "name": [
            "This field is required."
        ]
     }
     

## Get specific Product

Get specific product from database without offers.

### Request

`GET /products/<product id>`

### Response

    HTTP/1.1 200 OK
    Body:
        {
          "id": <product id>,
          "create": "<creation timestamp, format example: 2022-01-14T10:55:10.912597Z>", 
          "updated": "<update timestamp, format example: 2022-01-14T10:55:10.912597Z>",
          "name": "<product name from request>",
          "description": "<product description form request>"
        }

       
## Get specific Product offer

Get offers for specific product.

### Request

`GET /products/<product id>/offers`


### Response

    HTTP/1.1 200 OK
    {
    "status": true,
    "product": {
        "id": <product id>,
        "create": "<creation timestamp, format example: 2022-01-14T10:55:10.912597Z>", 
        "updated": "<update timestamp, format example: 2022-01-14T10:55:10.912597Z>",
        "name": "<product name from request>",
        "description": "<product description form request>"
      },
    "offers": [
        {
            "id": <local id of offer>,
            "offer_id": <id of offer in offer service,
            "price": <price>,
            "items_in_stock": <items in stock>,
            "product_id": <product id>
         }
       ]


     When product id does not exits in database:
     HTTP/1.1 404 Bad request
     {
        "status": false,
        "message:": "Product not found!"
     }
     
## Update specific Product

Update specific product from database without offers.

### Request

`PUT /products/<product id>`
    Body:{
      "name": "<new or same name of new product>" #required
      "description": "<description of new product>" #optional
    }


### Response

    HTTP/1.1 200 OK
    Body:
        {
          "status": true,
          "message": "Product updated!",
          "data":{
              "id": <product id>,
              "create": "<creation timestamp, format example: 2022-01-14T10:55:10.912597Z>", 
              "updated": "<updated timestamp, format example: 2022-01-14T10:55:10.912597Z>",
              "name": "<product name from request>",
              "description": "<product description form request>"
          }
        }



     HTTP/1.1 400 Bad request
       {
          "name": [
              "This field is required."
          ]
       }
       
## Delete specific Product

Delete specific product from database.

### Request

`DELETE /products/<product id>`

### Response

    HTTP/1.1 204 No Content
    Body:
        {
          "status": true,
          "message": "Product deleted!"
        }
        
        
### Known bugs
  * On Heroku Delete request does not return response sometimes but delete is successful
  * When updater updates offers in database, it locks database and when request comes, API returns error due to locked database. Proposition: implement job query for synchronyzing request with updater
  * Update request requires name, which is not necessary to perform update. Proposition: do not use default serializer and write own serializer.

    
![REST is](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmedia.tenor.com%2Fimages%2Fa48bfeb9935100b3850124005294b6de%2Ftenor.gif&f=1&nofb=1)    
