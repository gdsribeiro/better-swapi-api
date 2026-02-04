import pytest
from types import SimpleNamespace
from services.StarshipService import StarshipService
from DTOs.StarshipsQueryParamsDTO import StarshipsQueryParamsDTO

def create_mock_starship(name, model):
    return SimpleNamespace(
        url=f"http://test/{name}",
        name=name,
        model=model,
        MGLT="10",
        cargo_capacity="100000",
        consumables="2 months",
        cost_in_credits="100000",
        crew="4",
        hyperdrive_rating="0.5",
        length="30",
        manufacturer="Corellian Engineering Corporation",
        max_atmosphering_speed="1050",
        passengers="6",
        starship_class="Freighter",
        pilots=[],
        films=[]
    )

@pytest.fixture
def mock_swapi_client(mocker):
    return mocker.patch('services.StarshipService.SWAPIClient')

def test_get_starships_filtering(mock_swapi_client):
    mock_instance = mock_swapi_client.return_value
    mock_instance.get_starships.return_value = [
        create_mock_starship("Millennium Falcon", "YT-1300 light freighter"),
        create_mock_starship("X-wing", "T-65 X-wing")
    ]
    mock_instance.get_data.return_value = []

    service = StarshipService()
    filters = StarshipsQueryParamsDTO(name="Falcon", fields="name,model")

    result = service.get_starships(filters)

    assert len(result) == 1
    assert result[0]['name'] == "Millennium Falcon"

def test_get_starships_sorting(mock_swapi_client):
    mock_instance = mock_swapi_client.return_value
    mock_instance.get_starships.return_value = [
        create_mock_starship("A-wing", "A"),
        create_mock_starship("B-wing", "B")
    ]
    mock_instance.get_data.return_value = []

    service = StarshipService()
    filters = StarshipsQueryParamsDTO(sort_by="name", order="desc", fields="name")

    result = service.get_starships(filters)

    assert result[0]['name'] == "B-wing"
    assert result[1]['name'] == "A-wing"