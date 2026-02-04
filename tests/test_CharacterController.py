import pytest

from controllers.CharacterController import CharacterController
from DTOs.CharactersQueryParamsDTO import CharactersQueryParamsDTO

@pytest.fixture
def mock_character_service(mocker):
    return mocker.patch('controllers.CharacterController.CharacterService')

def test_get_characters_success(mock_character_service):
    mock_service_instance = mock_character_service.return_value
    mock_service_instance.get_characters.return_value = [{"name": "Luke Skywalker"}]

    query_params = {"name": "Luke"}
    result = CharacterController.get_characters(query_params)

    mock_character_service.assert_called_once()
    mock_service_instance.get_characters.assert_called_once()
    
    call_args = mock_service_instance.get_characters.call_args[0]
    assert len(call_args) == 1
    filters_dto = call_args[0]
    assert isinstance(filters_dto, CharactersQueryParamsDTO)
    assert filters_dto.name == "Luke"

    assert result == [{"name": "Luke Skywalker"}]

@pytest.mark.parametrize("query_params, error_field", [
    ({"page": "not-a-number"}, "page")
])
def test_get_characters_validation_error(mock_character_service, query_params, error_field):
    result, status_code = CharacterController.get_characters(query_params)

    assert status_code == 400
    assert result["error"] == "Validation Error"
    assert result["details"][0]["loc"] == (error_field,)

def test_get_characters_internal_server_error(mock_character_service):
    mock_service_instance = mock_character_service.return_value
    error_message = "Something went wrong in the service"
    mock_service_instance.get_characters.side_effect = Exception(error_message)
    
    query_params = {"name": "Luke"}
    result, status_code = CharacterController.get_characters(query_params)

    assert status_code == 500
    assert result["error"] == "Internal Server Error"
    assert result["details"] == error_message