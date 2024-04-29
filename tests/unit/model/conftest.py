import pytest

from src.archive.domains.document import SearchData


@pytest.fixture
def init_search_data():
    return SearchData(
        cypher="cypher",
        fund="fund",
        inventory="inventory",
        case="case",
        leaf="leaf",
        authenticity="authenticity",
        lang="lang",
        playback_method="playback method"
    )

@pytest.fixture
def upload_search_data():
    return SearchData(
        id=1,
        cypher="cypher",
        fund="fund",
        inventory="inventory",
        case="case",
        leaf="leaf",
        authenticity="authenticity",
        lang="lang",
        playback_method="playback method",
        other="other"
    )