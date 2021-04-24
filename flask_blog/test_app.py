from hello import app

# function to test app
def test_app():
    # get main page
    response = app.test_client().get('/')

# test if status code 200 is returned
    assert response.status_code == 200
    # test if we get "Hello World!"
    assert response.data == b'Hello, World!'