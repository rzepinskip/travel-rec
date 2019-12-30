from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://factforge.net/repositories/ff-news")
query = """
# F02: Big Cities in Eastern Europe

PREFIX onto: <http://www.ontotext.com/>
PREFIX gn: <http://www.geonames.org/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT * FROM onto:disable-sameAs
WHERE {
    SERVICE <http://factforge.net/repositories/ff-news>{
    ?loc gn:parentFeature dbr:Eastern_Europe ; 
         gn:featureClass  gn:P;
         gn:featureCode gn:A.ADM2.
    ?loc dbo:populationTotal ?population ; dbo:country ?country .
    ?country a dbo:Country .
    }
    FILTER(?population > 300000 )
    ?country skos:prefLabel ?country_name . 

} ORDER BY ?country_name DESC(?population)

"""
sparql.setQuery(query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
results