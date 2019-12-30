from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://geoknow-server.imis.athena-innovation.gr:11480/sparql")
query = """
PREFIX slipo: <http://slipo.eu/def#> 
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
SELECT ?name ?phone_number ?fWKT ?distance_km
WHERE { 
	?uri slipo:name ?fName . 
        ?fName slipo:nameValue ?name . 
        ?uri slipo:category ?fCategory .
	?fCategory slipo:value "RESTAURANT" .
        OPTIONAL { ?uri slipo:phone ?phone .
		   ?phone slipo:contactValue ?phone_number .  }
	?uri geo:hasGeometry ?fGeometry .
        ?fGeometry geo:asWKT ?fWKT .
        BIND (bif:st_distance(bif:st_point(23.735933, 37.975598), ?fWKT ) AS ?distance_km) .
        FILTER (?distance_km < 1)
    }
ORDER BY ?distance_km		
			
"""
sparql.setQuery(query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
results