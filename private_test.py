import EmmyAPI as Api

api = Api.EmmyAPI(
	'anton@antonbaumann.com',
	'A8Q6+2])62+9]^2=x$(Z(K948')
api.login()

cars = api.list_cars(lat='48.0894622', lon='11.563034199999999')
res = api.start_reservation(car_id=cars[0].car_id)
res = api.end_reservation(res.reservation_id)
print(res)
