import math

import requests


class Map(object):
    def __init__(self):
        self.url = 'https://api-adresse.data.gouv.fr/search/'
        self.radius = 6371  # km

    def distance(self, departure, arrival):
        try:
            departure_latitude, departure_longitude = float(departure['latitude']), float(departure['longitude'])
            arrival_latitude, arrival_longitude = float(arrival['latitude']), float(arrival['longitude'])
        except ValueError:
            return None
        latitude_distance = math.radians(arrival_latitude - departure_latitude)
        longitude_distance = math.radians(arrival_longitude - departure_longitude)
        a = (math.sin(latitude_distance / 2) * math.sin(latitude_distance / 2) +
             math.cos(math.radians(arrival_longitude)) * math.cos(math.radians(arrival_latitude)) *
             math.sin(longitude_distance / 2) * math.sin(longitude_distance / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = self.radius * c

        return d

    def point(self, location):
        # TODO: fallback to the name of the hotel and other complementary operations if we don't have the
        #       address
        if not location.get('address'):
            return None
        geographic_information = self.get(location)
        geographic_information_features = geographic_information['features']
        if not geographic_information_features:
            return None
        best_score_geophic_information = sorted(
            geographic_information_features,
            key=lambda k: k['properties']['score']
        )[0]
        latitude, longitude = best_score_geophic_information['geometry']['coordinates']
        return {'latitude': latitude, 'longitude': longitude}

    def get(self, parameters):
        payload = {'q': parameters.get('address'), 'postcode': parameters.get('postcode')}
        request = requests.get(self.url, params=payload)
        request.raise_for_status()

        response = request.json()

        return response


if __name__ == '__main__':
    map = Map()

    address1 = {'address': 'Avenue Winston Churchill', 'postcode': 27000}
    address2 = {'address': 'Rue Gay Lussac', 'postcode': 60000}

    point1 = map.point(address1)
    point2 = map.point(address2)

    distance = map.distance(point1, point2)

    print('{} kms'.format(distance))
