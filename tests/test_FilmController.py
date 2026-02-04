import pytest

from controllers.FilmController import FilmController
from DTOs.FilmsQueryParamsDTO import FilmsQueryParamsDTO

@pytest.fixture
def mock_film_service(mocker):
    return mocker.patch('controllers.FilmController.FilmService')

def test_get_films_success(mock_film_service):
    mock_service_instance = mock_film_service.return_value
    mock_service_instance.get_films.return_value = [{"title": "A New Hope"}]

    query_params = {"title": "Hope"}
    result = FilmController.get_films(query_params)

    mock_film_service.assert_called_once()
    mock_service_instance.get_films.assert_called_once()
    
    call_args = mock_service_instance.get_films.call_args[0]

    assert len(call_args) == 1
    filters_dto = call_args[0]
    assert isinstance(filters_dto, FilmsQueryParamsDTO)
    assert filters_dto.title == "Hope"

    assert result == [{"title": "A New Hope"}]

@pytest.mark.parametrize("query_params, error_field", [
    ({"episode_id": "not-a-number"}, "episode_id")
])
def test_get_films_validation_error(mock_film_service, query_params, error_field):
    result, status_code = FilmController.get_films(query_params)

    assert status_code == 400
    assert result["error"] == "Validation Error"
    assert result["details"][0]["loc"] == (error_field,)

def test_get_films_internal_server_error(mock_film_service):
    mock_service_instance = mock_film_service.return_value
    error_message = "DB is down"
    mock_service_instance.get_films.side_effect = Exception(error_message)
    
    query_params = {"title": "Hope"}
    result, status_code = FilmController.get_films(query_params)

    assert status_code == 500
    assert result["error"] == "Internal Server Error"
    assert result["details"] == error_message