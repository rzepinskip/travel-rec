from geomet import wkt

def coordinates_to_file(sparql_res, filename):
    points = [wkt.loads(el['fWKT']['value'])['coordinates'] for el in sparql_res['results']['bindings']]

    with open(filename, 'w') as f:
        for point in points:
            f.write(f'{point[0]}\t{point[1]}\n')