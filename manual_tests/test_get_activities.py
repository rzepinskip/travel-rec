from travelrec.sparql import ( get_activities, get_location )
from manual_tests.coordinates_to_file import coordinates_to_file

latitude, longitude = get_location('Berlin')

res = get_activities(latitude, longitude, 100, ['ZOO'])

coordinates_to_file(res, 'manual_tests/zoos_Berlin_100.txt')