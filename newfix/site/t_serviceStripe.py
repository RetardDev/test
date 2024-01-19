import stripe

stripe.api_key = 'sk_test_51OTMQlBTJjXpaW8bRJHuGZaHG58CKsNMEdkEOy24J6G8Wd5A1hvzG07fBxhWC4tpy7YiwWpDS7f9HDk5vD34HYPt00KMXlgdoZ'

service_data = [
    {
    'name': 'Bad Boy cleaners',
    'price': '8500'
    },
      {
    'name': 'Ena Malta - Power line repair',
    'price': '12000'
    },
      {
    'name': 'fxp hair styling',
    'price': '4000'
    },
      {
    'name': 'Red Crimson Training',
    'price': '18000'
    },
      {
    'name': 'Jeff The Criminal Lawyer',
    'price': '450000'
    },
      {
    'name': 'ServerFX - Server Maintenaces',
    'price': '250000'
    },
    
]

for service_info in service_data:
    product = stripe.Product.create(
        name=service_info['name'],
        type='service'
    )

    price = stripe.Price.create(
        product = product.id,
        unit_amount = service_info['price'],
        currency='eur',
    )