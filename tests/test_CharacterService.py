import pytest
from types import SimpleNamespace
from services.CharacterService import CharacterService
from DTOs.CharactersQueryParamsDTO import CharactersQueryParamsDTO

def create_mock_character(name, birth_year="19BBY"):
    return SimpleNamespace(
        url=f"http://test/{name}",
        name=name,
        birth_year=birth_year,
        homeworld="http://test/planet/1",
        height="172",
        mass="77",
        gender="male",
        eye_color="blue",
        hair_color="blond",
        skin_color="fair",
        species=[],
        vehicles=[],
        starships=[],
        films=[]
    )

@pytest.fixture
def mock_swapi_client(mocker):
    return mocker.patch('services.CharacterService.SWAPIClient')

def test_get_characters_success(mock_swapi_client):
    mock_instance = mock_swapi_client.return_value
    mock_instance.get_people.return_value = [create_mock_character("Luke Skywalker")]
    mock_instance.get_data.return_value = [] # Evita erro se tentar buscar dados extras

    service = CharacterService()
    filters = CharactersQueryParamsDTO(name="Luke", fields="name")

    result = service.get_characters(filters)

    assert len(result) == 1
    assert result[0]['name'] == "Luke Skywalker"

def test_get_characters_birth_year_parsing(mock_swapi_client):
    mock_instance = mock_swapi_client.return_value
    mock_instance.get_people.return_value = [create_mock_character("Yoda", "896BBY")]
    mock_instance.get_data.return_value = []

    service = CharacterService()
    filters = CharactersQueryParamsDTO(fields="name,birth_year,period")

    result = service.get_characters(filters)

    assert result[0]['birth_year'] == 896.0
    assert result[0]['period'] == "BBY"