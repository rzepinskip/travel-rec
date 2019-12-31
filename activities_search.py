from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://geoknow-server.imis.athena-innovation.gr:11480/sparql")
query = """
PREFIX slipo: <http://slipo.eu/def#> 
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
SELECT ?name ?fWKT ?distance_km
WHERE { 
	?uri slipo:name ?fName . 
        ?fName slipo:nameValue ?name . 
        ?uri slipo:category ?fCategory .
	?fCategory slipo:value ?fCategory_Val .
	?uri geo:hasGeometry ?fGeometry .
        ?fGeometry geo:asWKT ?fWKT .
        BIND (bif:st_distance(bif:st_point(51.50853, -0.12574), ?fWKT ) AS ?distance_km) .
        FILTER (?distance_km < 4700 && ?fCategory_Val IN ("FOOTBALL", "TENNIS"))
    }
ORDER BY ?distance_km		
			
"""
sparql.setQuery(query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
results