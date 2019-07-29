import pytest
import config

__author__ = 'Kien'

admin = {
    'username': 'anhducc13',
    'email': 'trantienduc10@gmail.com',
    'password': 'Anhducc13',
    'is_admin': True
}

user_not_verify = {
    'username': 'ductt97',
    'email': 'trantienduc1001@gmail.com',
    'password': 'Anhducc13',
    'user_token_confirm': config.JWT_TEST
}


@pytest.fixture(autouse=True)
def app(request):
    from ducttapp import app
    from ducttapp.models import db, User, Signup_Request

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()
    # test db initializations go below here
    db.create_all()
    db.session.add(User(**admin))
    db.session.add(Signup_Request(**user_not_verify))
    db.session.commit()

    def teardown():
        db.session.remove()
        db.drop_all()
        ctx.pop()
        pass

    request.addfinalizer(teardown)
    return app
