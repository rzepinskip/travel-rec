from SPARQLWrapper import SPARQLWrapper, JSON
from travelrec.constants import get_slipo_codes
from manual_tests.coordinates_to_file import coordinates_to_file

sparql = SPARQLWrapper(
    "http://geoknow-server.imis.athena-innovation.gr:11480/sparql"
)
all_activities = [get_slipo_codes()[k] for k in get_slipo_codes().keys()]
# all_activities = ['ZOO']
actitivies_quoted = [f'"{x}"' for x in all_activities]
query = f"""
PREFIX slipo: <http://slipo.eu/def#> 
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
SELECT ?name ?fWKT
WHERE {{ 
    ?uri slipo:name ?fName . 
        ?fName slipo:nameValue ?name . 
        ?uri slipo:category ?fCategory .
    ?fCategory slipo:value ?fCategory_Val .
    ?uri geo:hasGeometry ?fGeometry .
        ?fGeometry geo:asWKT ?fWKT .
        FILTER (?fCategory_Val IN ({", ".join(actitivies_quoted)}))
    }}
"""
sparql.setQuery(query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

coordinates_to_file(results, 'manual_tests/points.txt')

# then project it in http://dwtkns.com/pointplotter/
