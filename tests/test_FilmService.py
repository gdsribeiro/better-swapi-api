import pytest
from types import SimpleNamespace
from services.FilmService import FilmService
from DTOs.FilmsQueryParamsDTO import FilmsQueryParamsDTO

def create_mock_film(title, episode_id):
    return SimpleNamespace(
        url=f"http://test/{title}",
        title=title,
        episode_id=episode_id,
        director="George Lucas",
        producer="Gary Kurtz",
        opening_crawl="Long time ago...",
        release_date="1977-05-25",
        characters=[],
        planets=[],
        starships=[],
        vehicles=[],
        species=[]
    )

@pytest.fixture
def mock_swapi_client(mocker):
    return mocker.patch('services.FilmService.SWAPIClient')

def test_get_films_filtering(mock_swapi_client):
    mock_instance = mock_swapi_client.return_value
    mock_instance.get_films.return_value = [
        create_mock_film("A New Hope", 4),
        create_mock_film("The Empire Strikes Back", 5)
    ]
    mock_instance.get_data.return_value = []

    service = FilmService()
    filters = FilmsQueryParamsDTO(title="Hope", fields="title")

    result = service.get_films(filters)

    assert len(result) == 1
    assert result[0]['title'] == "A New Hope"

def test_get_films_sorting(mock_swapi_client):
    mock_instance = mock_swapi_client.return_value
    mock_instance.get_films.return_value = [
        create_mock_film("Episode I", 1),
        create_mock_film("Episode IV", 4)
    ]
    mock_instance.get_data.return_value = []

    service = FilmService()
    filters = FilmsQueryParamsDTO(sort_by="episode_id", order="desc", fields="title,episode_id")

    result = service.get_films(filters)

    assert result[0]['episode_id'] == 4
    assert result[1]['episode_id'] == 1