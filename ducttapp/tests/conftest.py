import pytest


@pytest.fixture
def app_class(request, app):
    if request.cls is not None:
        request.cls.app = app
