from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://factforge.net/repositories/ff-news")
query = """
# GraphDB’s geo-spatial plug-in allows efficient evaluation of near-by
# RDFRank ranks entities based on their popularity(links to other entities)

PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX geo-pos: <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX gdb-geo: <http://www.ontotext.com/owlim/geo#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rank: <http://www.ontotext.com/owlim/RDFRank#>
PREFIX gn: <http://www.geonames.org/ontology#>

SELECT DISTINCT ?object ?featureCode ?rrank ?london_lat ?lond_nlong ?lat ?long ?dist
WHERE {
   { SELECT * { dbr:London geo-pos:lat ?london_lat ; geo-pos:long ?lond_nlong . } LIMIT 1 }
   ?object gdb-geo:nearby(?london_lat ?lond_nlong "15mi");
       gn:featureCode ?featureCode;
       rank:hasRDFRank3 ?rrank;
		geo-pos:lat ?lat;
		geo-pos:lat ?long .
    BIND (gdb-geo:distance(?lat, ?long, ?london_lat, ?lond_nlong) AS ?dist)
    FILTER(?featureCode IN (gn:S.BANK, gn:S.CSTL))
} 
ORDER BY DESC(?rrank)

"""
sparql.setQuery(query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
results