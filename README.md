# Emmy-Api
## usage:
```
api = EmmyAPI(username='user', password='pass')
api.login()

cars = api.list_cars(lat='48.1366', lon='11.5765')
reservation = api.start_reservation(car_id=cars[0].car_id)
...
```