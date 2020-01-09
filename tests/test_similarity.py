import pytest

from travelrec.similarity import ActvitySimilarity, ClimateSimilarity, GeoFeaturesSimilarity
from travelrec.processed_statement import ProcessedStatement

@pytest.mark.parametrize("test_input, expected", [
    (['mild'], ['mild']),
    (['warm'], ['warm']),
    (['warm', 'mild'], ['warm', 'mild']),
    # TODO: Wordnet - issue #3
    # (['medium'], ['mild']),
    # (['hot'], ['warm'])
    ])
def test_climate_similarity(test_input, expected):
    climateSim = ClimateSimilarity()

    filters = climateSim.construct_filters(test_input)

    assert len(expected) == len(filters)

    for synonym, filter, word in zip(expected, filters, test_input):
        assert climateSim._mapping[synonym] == filter

@pytest.mark.parametrize("test_input, expected", [
    ('swimming in Cracow', []),
    ('mountains near Statue of Liberty', ["T.MT", "T.MTS"]),
    ('lakes in Mazury', ["H.LK", "H.LKS"]),
    ('mountains and lakes in Poland', ["T.MT", "T.MTS", "H.LK", "H.LKS"]),
    ])
def test_geo_features_similarity(test_input, expected):
    geoFeaturesSim = GeoFeaturesSimilarity()

    processed_statement = ProcessedStatement(test_input)
    nouns = processed_statement.nouns()

    similarities = geoFeaturesSim.construct_filters(nouns)

    assert sorted(similarities) == sorted(expected)

@pytest.mark.parametrize("test_input, expected", [
    ('mountains near Statue of Liberty', []),
    ('basketball in Cracow', ['BASKETBALL']),
    ('a ZOO and gym near Statue of Liberty', ['ZOO', 'GYM']),
    ('cinemas in Mazury', ['CINEMA']),
    ('swimming in Poland', ['SWIMMING']),
    ])
def test_actvity_similarity(test_input, expected):
    activitySim = ActvitySimilarity()

    processed_statement = ProcessedStatement(test_input)
    nouns = processed_statement.nouns()

    similarities = activitySim.construct_filters(nouns)

    assert sorted(similarities) == sorted(expected)
