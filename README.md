# Pricing API

This is a simple demonstration of a pricing API implemented with DRF (Django REST Framework). This code was developed to demonstrate my Django and REST Framework skills.

## Getting Started

Please clone the project to your local machine and follow this README.

### Prerequisites

First create a virtual environment. Active it.

```
python3 -m venv pricing-venv
```

```
source pricing-venv/bin/activate
```

### Installing Requirements

Make sure you are in the main directory. Install the requirements.txt using pip install.

```
pip install -r requirements.txt
```

### The Products (Database)
For your convenience and to get you started quickly pretty fast, sqlite database with some products have been included (normally wouldn't) in this repo.

### Create a superuser

You will need a superuser account if you'd want to add new products and edit things in admin.

```
python manage.py createsuperuser
```

### Run the server & login

First run the server.
```
python manage.py runserver
```



## Simple Use Case (GBP)

Go to the router page in the following URL. (Assuming you started your server with port 8000)
```
http://127.0.0.1:8000/api/orders/
```
Below the page, you will see a form. Click on the "Raw Data" tab. Paste your input JSON there.
Sample input have been created for you at [sample input data](./sample_input.json)

This will create an order. ```order_total``` and ```vat_total``` will be calculated. Also, VAT for each item in the order will be displayed too.

## International Use Case (With Currency Conversion)
All prices are in GBP. If we'd like to see the prices in different currency, we have to follow the steps below.

I have implemented this in two different ways:
A) Simple Approach
B) Detailed Approach

#### A) Simple Way
Just pass the 3 letter currency code (ie. ISO 4217 code) with your request. See [sample input with currency data](./sample_input_currency.json) to get you started.

You will see that ```order_total``` and ```vat_total``` will be calculated in the foreign currency. (Not the product prices and VAT)

#### A) Detailed Way
If you'd like to see the original prices alongside the currency converted you can go with this approach. This is also handy in case you don't want to record the currency in the database (like lookup uses for several different currencies) (or if you really really want to experiment with cross-currency parity of the conversion API :)

For this use case, you will need to make the request from the shell.
First run:
```
python manage.py shell
```

After the shell loads, we will need to input an order ID and user's native currency (3 letter code, ie: ISO 4217 code) in the payload to make this API work.

```
import requests
import json
headers = {'content-type': 'application/json'}
payload = {"id":3, "user_currency": "USD"}

url = "http://127.0.0.1:8000/api/orders/calculate_currency_price/"
r = requests.get(url, data=json.dumps(payload), headers=headers)
r.json()

```



## References (Built With)

* [Django](https://www.djangoproject.com) - The framework



## Acknowledgments

* I'm aware there are tons of improvements that can be made. It's a matter of time/energy and resources. Looking forward to discussing these with you. I've briefly talked about those in the next section. Here are my answers to few critical questions.

## Critical Questions to Answer
#### If you had more time, what improvements would you make if any?
If this was going to be something more complex (or potential to grow in complexity) and would be used in production for many products and orders, perhaps I might include GraphQL on top of REST. This way GraphQL server can act as a sort of data proxy. With GraphQL, when complexity is high, we can overcome bottlenecks in REST API.

Nevertheless, to architect for a systematic growth, I could have looked at versioning of the API.

On more practical side of things, I could have implemented exception handling. For example orders without any items etc.

Last but not, if this was a bigger project, I could have made a better documentation than this README.


#### What bits did you find the toughest? What bit are you most proud of? In both cases, why?
I struggled bit on serializing M2M filed with a though table since I hadn't done this before. Good to be learning new things. I found the testing part to be different. I hadn't done API testing extensively before. Besides, I'm proud many bits: the project setup, use of Django REST Framework etc.

#### What one thing could we do to improve this test?
You might ask the user to implement (or just ask to propose to implement) an unspecified, creative feature that they think might would make sense. In this case, I would have suggested that: for example API authentication might a such a feature.

## Author

* **Ahter** - (https://github.com/ahter)
