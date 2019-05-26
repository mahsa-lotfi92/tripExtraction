from datetime import datetime
from typing import NamedTuple

from config.static_values import IGNORE_DISTANCE
from log_book.util.haversine import distance as haversine_distance


class WayPoint(NamedTuple):
    timestamp: datetime
    lat: float
    lng: float

    @staticmethod
    def create_from_dict(obj):
        if not isinstance(obj, dict):
            return None

        lat = obj['lat']
        lng = obj['lng']
        timestamp = datetime.strptime(obj['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
        return WayPoint(timestamp=timestamp, lat=lat, lng=lng)

    def __eq__(self, waypoint2) -> bool:
        assert isinstance(waypoint2, WayPoint)
        return haversine_distance(self, waypoint2) <= IGNORE_DISTANCE

    def __repr__(self):
        return '(lat:{}, lng:{}, time:{})'.format(self.lat, self.lng, self.timestamp)

    def to_dict(self):
        return {'timestamp': self.timestamp,
                'lat': self.lat,
                'lng': self.lng}


class Trip(NamedTuple):
    distance: int
    start: WayPoint
    end: WayPoint

    def to_dict(self):
        return {'distance': self.distance,
                'start': self.start.to_dict(),
                'end': self.end.to_dict()}


class TripEntity:
    def __init__(self, start=None, end=None, distance=0):
        self.start = start
        self.end = end
        self.distance = distance

    def __repr__(self):
        return 'Start: {}, End:{}, Distance:{}'.format(self.start, self.end, self.distance)
