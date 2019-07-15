import pytest

__author__ = 'Kien'


@pytest.fixture(autouse=True)
def app(request):
    from ducttapp import app
    from ducttapp.models import db

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()
    # test db initializations go below here
    db.create_all()

    def teardown():
        db.session.remove()
        db.drop_all()
        ctx.pop()
        pass

    request.addfinalizer(teardown)
    return app
