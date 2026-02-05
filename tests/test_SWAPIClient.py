import pytest
import requests
from clients.SWAPIClient import SWAPIClient

@pytest.fixture
def client():
    return SWAPIClient()

@pytest.fixture
def mock_requests_get(mocker):
    return mocker.patch('requests.get')

def test_get_data_single_page(client, mock_requests_get, mocker):
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "results": [{"name": "Item 1"}],
        "next": None
    }
    mock_requests_get.return_value = mock_response

    result = client.get_data("test")

    assert len(result) == 1
    assert result[0]["name"] == "Item 1"
    mock_requests_get.assert_called_once_with("https://swapi.dev/api/test")

def test_get_data_pagination(client, mock_requests_get, mocker):
    response_page_1 = mocker.MagicMock()
    response_page_1.status_code = 200
    response_page_1.json.return_value = {
        "results": [{"name": "Item 1"}],
        "next": "https://swapi.dev/api/test?page=2"
    }

    response_page_2 = mocker.MagicMock()
    response_page_2.status_code = 200
    response_page_2.json.return_value = {
        "results": [{"name": "Item 2"}],
        "next": None
    }

    mock_requests_get.side_effect = [response_page_1, response_page_2]

    result = client.get_data("test")

    assert len(result) == 2
    assert result[0]["name"] == "Item 1"
    assert result[1]["name"] == "Item 2"
    assert mock_requests_get.call_count == 2

def test_get_data_404(client, mock_requests_get, mocker):
    mock_response = mocker.MagicMock()
    mock_response.status_code = 404
    
    error = requests.HTTPError(response=mock_response)
    mock_response.raise_for_status.side_effect = error
    mock_requests_get.return_value = mock_response

    result = client.get_data("unknown")

    assert result == []

def test_get_data_server_error(client, mock_requests_get, mocker):
    mock_response = mocker.MagicMock()
    mock_response.status_code = 500
    
    error = requests.HTTPError(response=mock_response)
    mock_response.raise_for_status.side_effect = error
    mock_requests_get.return_value = mock_response

    with pytest.raises(requests.HTTPError):
        client.get_data("test")

def test_get_people_success(client, mocker):
    mock_get_data = mocker.patch.object(client, 'get_data')
    mock_get_data.return_value = [{
        "name": "Luke Skywalker",
        "height": "172",
        "mass": "77",
        "hair_color": "blond",
        "skin_color": "fair",
        "eye_color": "blue",
        "birth_year": "19BBY",
        "gender": "male",
        "homeworld": "https://swapi.dev/api/planets/1/",
        "films": [],
        "species": [],
        "vehicles": [],
        "starships": [],
        "created": "2014-12-09T13:50:51.644000Z",
        "edited": "2014-12-20T21:17:56.891000Z",
        "url": "https://swapi.dev/api/people/1/"
    }]

    result = client.get_people()

    assert len(result) == 1
    assert result[0].name == "Luke Skywalker"
    assert hasattr(result[0], 'birth_year')

def test_get_films_success(client, mocker):
    mock_get_data = mocker.patch.object(client, 'get_data')
    mock_get_data.return_value = [{
        "title": "A New Hope",
        "episode_id": 4,
        "opening_crawl": "Crawl",
        "director": "Lucas",
        "producer": "Kurtz",
        "release_date": "1977-05-25",
        "characters": [], "planets": [], "starships": [], "vehicles": [], "species": [],
        "created": "2014-12-10T14:23:31.880000Z", "edited": "2014-12-20T19:49:45.256000Z",
        "url": "https://swapi.dev/api/films/1/"
    }]

    result = client.get_films()

    assert len(result) == 1
    assert result[0].title == "A New Hope"
    assert result[0].episode_id == 4

def test_get_people_validation_error(client, mocker):
    mock_get_data = mocker.patch.object(client, 'get_data')
    # Missing required fields
    mock_get_data.return_value = [{'invalid': 'data'}]

    with pytest.raises(ValueError, match='Erro de integração: Dados da API inválidos'):
        client.get_people()