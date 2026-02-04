import pytest
from types import SimpleNamespace
from services.PlanetService import PlanetService
from DTOs.PlanetsQueryParamsDTO import PlanetsQueryParamsDTO

def create_mock_planet(name):
    return SimpleNamespace(
        url=f"http://test/{name}",
        name=name,
        climate="arid",
        diameter="10465",
        gravity="1 standard",
        orbital_period="304",
        population="200000",
        rotation_period="23",
        surface_water="1",
        terrain="desert",
        residents=[],
        films=[]
    )

@pytest.fixture
def mock_swapi_client(mocker):
    return mocker.patch('services.PlanetService.SWAPIClient')

def test_get_planets_pagination(mock_swapi_client):
    mock_instance = mock_swapi_client.return_value
    all_planets = [create_mock_planet(f"Planet {i:02d}") for i in range(1, 16)]
    mock_instance.get_planets.return_value = all_planets
    mock_instance.get_data.return_value = []

    service = PlanetService()
    filters = PlanetsQueryParamsDTO(page=2, limit=10, fields="name")

    result = service.get_planets(filters)

    assert len(result) == 5
    assert result[0]['name'] == "Planet 11"

def test_get_planets_success(mock_swapi_client):
    mock_instance = mock_swapi_client.return_value
    mock_instance.get_planets.return_value = [create_mock_planet("Tatooine")]
    mock_instance.get_data.return_value = []

    service = PlanetService()
    filters = PlanetsQueryParamsDTO(name="Tatooine", fields="name")
    result = service.get_planets(filters)

    assert result[0]['name'] == "Tatooine"