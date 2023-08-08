import pytest
from _pytest.fixtures import SubRequest


class Bubs:
    DEFAULT_NAME: str = 'lothar'

    def __init__(self, name: str):
        self.name: str = name if name else Bubs.DEFAULT_NAME


class Bubser:
    def __init__(self, bubs: Bubs):
        self.bubs: Bubs = bubs

    def get_bubs_name(self) -> str:
        return self.bubs.name


@pytest.fixture
def params(request: SubRequest) -> str | None:
    return request.param if hasattr(request, 'param') else None


@pytest.fixture
def create_bubs(params, request: SubRequest) -> Bubs:
    name: str = request.param if hasattr(request, 'param') else params
    return Bubs(name=name)


@pytest.fixture
def create_bubser(create_bubs) -> Bubser:
    return Bubser(bubs=create_bubs)


@pytest.mark.parametrize(
    'create_bubs,expected_bubs_name',
    [['ulf', 'ulf']],
    indirect=['create_bubs']
)
def test_bubs_1(create_bubs, expected_bubs_name: str):
    assert create_bubs.name == expected_bubs_name


@pytest.mark.parametrize(
    'params,expected_bubs_name',
    [['ulf', 'ulf']],
    indirect=['params']
)
def test_bubs_2(params, create_bubs, expected_bubs_name: str):
    assert create_bubs.name == expected_bubs_name


def test_bubs_3(create_bubs):
    assert create_bubs.name == Bubs.DEFAULT_NAME


@pytest.mark.parametrize(
    'params,expected_bubs_name',
    [['ulf', 'ulf']],
    indirect=['params']
)
def test_bubser_1(params, create_bubser, expected_bubs_name: str):
    assert create_bubser.get_bubs_name() == expected_bubs_name


def test_bubser_2(create_bubser):
    assert create_bubser.get_bubs_name() == Bubs.DEFAULT_NAME
