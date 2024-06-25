import pytest


from tests.helpers import get_sql_fixtures

from titan import resources as res
from titan.resources import Resource

SQL_FIXTURES = list(get_sql_fixtures())


@pytest.fixture(
    params=SQL_FIXTURES,
    ids=[f"{resource_cls.__name__}({idx})" for resource_cls, _, idx in SQL_FIXTURES],
    scope="function",
)
def sql_fixture(request):
    resource_cls, data, idx = request.param
    yield resource_cls, data


@pytest.mark.skip(reason="Stub in test for now")
def test_init_from_sql(sql_fixture):
    resource_cls, data = sql_fixture
    try:
        if resource_cls in (res.Column,):
            pytest.skip("Column is not a valid resource type")
        Resource.from_sql(data)
    except Exception:
        pytest.fail(f"Failed to construct {resource_cls.__name__} from SQL fixture")
