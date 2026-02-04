import pytest

from controllers.StarshipController import StarshipController
from DTOs.StarshipsQueryParamsDTO import StarshipsQueryParamsDTO

@pytest.fixture
def mock_starship_service(mocker):
    return mocker.patch('controllers.StarshipController.StarshipService')

def test_get_starships_success(mock_starship_service):
    mock_service_instance = mock_starship_service.return_value
    mock_service_instance.get_starships.return_value = [{"name": "Millennium Falcon"}]

    query_params = {"name": "Falcon"}
    result = StarshipController.get_starships(query_params)

    mock_starship_service.assert_called_once()
    mock_service_instance.get_starships.assert_called_once()
    
    call_args = mock_service_instance.get_starships.call_args[0]

    assert len(call_args) == 1
    filters_dto = call_args[0]
    assert isinstance(filters_dto, StarshipsQueryParamsDTO)
    assert filters_dto.name == "Falcon"
    assert result == [{"name": "Millennium Falcon"}]

@pytest.mark.parametrize("query_params, error_field", [
    ({"page": "xyz"}, "page"),
])
def test_get_starships_validation_error(mock_starship_service, query_params, error_field):
    result, status_code = StarshipController.get_starships(query_params)

    assert status_code == 400
    assert result["error"] == "Validation Error"
    assert result["details"][0]["loc"] == (error_field,)

def test_get_starships_internal_server_error(mock_starship_service):
    mock_service_instance = mock_starship_service.return_value
    error_message = "External service unavailable"
    mock_service_instance.get_starships.side_effect = Exception(error_message)
    
    query_params = {"name": "Falcon"}
    result, status_code = StarshipController.get_starships(query_params)

    assert status_code == 500
    assert result["error"] == "Internal Server Error"
    assert result["details"] == error_message