import pytest

from controllers.PlanetController import PlanetController
from DTOs.PlanetsQueryParamsDTO import PlanetsQueryParamsDTO

@pytest.fixture
def mock_planet_service(mocker):
    return mocker.patch('controllers.PlanetController.PlanetService')

def test_get_planets_success(mock_planet_service):
    mock_service_instance = mock_planet_service.return_value
    mock_service_instance.get_planets.return_value = [{"name": "Tatooine"}]
   
    query_params = {"name": "Tatooine"}
    result = PlanetController.get_planets(query_params)

    mock_planet_service.assert_called_once()
    mock_service_instance.get_planets.assert_called_once()
    
    call_args = mock_service_instance.get_planets.call_args[0]

    assert len(call_args) == 1
    filters_dto = call_args[0]
    assert isinstance(filters_dto, PlanetsQueryParamsDTO)
    assert filters_dto.name == "Tatooine"
    assert result == [{"name": "Tatooine"}]

@pytest.mark.parametrize("query_params, error_field", [
    ({"page": "abc"}, "page")
])
def test_get_planets_validation_error(mock_planet_service, query_params, error_field):
    result, status_code = PlanetController.get_planets(query_params)

    assert status_code == 400
    assert result["error"] == "Validation Error"
    assert result["details"][0]["loc"] == (error_field,)

def test_get_planets_internal_server_error(mock_planet_service):
    mock_service_instance = mock_planet_service.return_value
    error_message = "API timeout"
    mock_service_instance.get_planets.side_effect = Exception(error_message)
    
    query_params = {"name": "Tatooine"}
    result, status_code = PlanetController.get_planets(query_params)

    assert status_code == 500
    assert result["error"] == "Internal Server Error"
    assert result["details"] == error_message