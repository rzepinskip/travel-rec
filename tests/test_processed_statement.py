import pytest

import en_core_web_sm
from travelrec.processed_statement import ProcessedStatement

@pytest.mark.parametrize("test_input, expected", [
    ("hot place in Paris", ["Paris"]),
    ("sightseeing in Cracow", ["Cracow"]),
    ("swimming near Eiffel Tower", ["Eiffel Tower"]),
    ("swimming near Statue of Liberty", ["Statue of Liberty"]),
    ("warm place in the Tatra Mountains", ["the Tatra Mountains"]),
    ])
def test_location_entities(test_input, expected):
    processed_statement = ProcessedStatement(test_input)
    location_entities = processed_statement.location_entities()

    assert [entity.string for entity in location_entities] == expected

@pytest.mark.parametrize("test_input, expected", [
    ("sightseeing in Cracow", "sightseeing"),
    ("mountains near Statue of Liberty", "mountain"),
    ("lakes in Mazury", "lake"),
    ("swimming in Poland", "swimming"),
    ])
def test_nouns(test_input, expected):
    processed_statement = ProcessedStatement(test_input)
    nouns = processed_statement.nouns()

    assert expected in nouns

@pytest.mark.parametrize("test_input, expected", [
    ("warm places", ["warm"]),
    ("snowy resort in Alps", ["snowy"]),
    ("city in Poland with mild temperature", ["mild"]),
    ])
def test_climate_terms(test_input, expected):
    processed_statement = ProcessedStatement(test_input)
    climate_terms = processed_statement.climate_terms()

    assert climate_terms == expected
