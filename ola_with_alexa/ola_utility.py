from config import Config
import requests


class BaseCoordinator(object):

    def __init__(self):
        self.base_url = Config.OLA_BASE_URL

    def path_with_slash(self, path):
        return path if path.startswith('/') else '/' + path

    def action(self, path):
        return self.base_url + self.path_with_slash(path)

    def get(self, path, payload, headers):
        url = self.action(path)
        response = requests.get(url, params=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return dict()

    def post(self, path, payload, headers):
        url = self.action(path)
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return dict()


class OlaUtility(object):

    def __init__(self):
        self.coordinator = BaseCoordinator()

    def get_category_data(self, categories):
        category_details = dict()
        for data in categories:
            category_details.update({
                'type': data.get('display_name'),
                'eta': data.get('eta'),
                'distance': data.get('distance'),

            })
        return category_details

    def get_fare_details(self, ride_estimates):
        for fare in ride_estimates:
            for fare_info in fare.get('fares'):
                return fare_info.get('cost')

    def fetch_important_details(self, cab_info):
        important_cab_details = dict()
        categories = cab_info.get('categories')
        ride_estimate = cab_info.get('ride_estimate')
        important_cab_details.update(self.get_category_data(categories))
        important_cab_details['price'] = self.get_fare_details(ride_estimate)
        return important_cab_details

    def get_cabs_details(self):
        url = '/v1/products'
        payload = {
            'pickup_lat': Config.HOME_LOCATION.get('latitude'),
            'pickup_lng': Config.HOME_LOCATION.get('longitude'),
            'drop_lat': Config.WORK_LOCATION.get('latitude'),
            'drop_lng': Config.WORK_LOCATION.get('longitude'),
            'category': 'share'
        }
        headers = {
            'X-APP-TOKEN': Config.X_APP_TOKEN,
            'Authorization': Config.Authorization
        }
        result = self.coordinator.get(url, payload, headers=headers)
        cab_info = self.fetch_important_details(result)
        return cab_info

    def get_booked_cab_details(self, data):
        return {
            'car_model': data.get('car_model'),
            'car_color': data.get('car_color'),
            'driver_name': data.get('driver_name'),
            'eta': data.get('eta'),
            'cab_number': data.get('cab_number'),
            'otp': data.get('otp', {}).get('start_trip', {}).get('value')
        }

    def book_cab(self):
        url = '/v1/bookings/create'
        payload = {
            "pickup_lat": "12.9490936",
            "pickup_lng": "77.6443056",
            "drop_lat": "12.972934",
            "drop_lng": "77.722302",
            "pickup_mode": "NOW",
            "category": "prime"
        }
        headers = {
            'X-APP-TOKEN': Config.X_APP_TOKEN,
            'Authorization': 'Bearer ' + Config.Authorization,
            "Content-Type": "application/json"
        }
        result = self.coordinator.post(url, payload, headers)
        return self.get_booked_cab_details(result)

# class_obj = OlaUtility()
# class_obj.book_cab()
