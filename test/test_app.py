# Using py.test framework
from service import Intro, Iris


def test_example_message(client):
    """Example message should be returned"""
    client.app.add_route('/iris', Intro())

    result = client.simulate_get('/iris')
    assert result.json == {
        'message': 'This service verifies a model using the Iris Test data set. '
                   'Invoke using the form /Iris/<index of test sample>. For example, /iris/24'}, \
        "The service test will fail until a trained model has been approved"


def test_classification_request(client):
    """Expected classification for Iris sample should be returned"""
    client.app.add_route('/iris/{index:int(min=0)}', Iris())

    result = client.simulate_get('/iris/1')
    assert result.status == "200 OK", "The service test will fail until a trained model has been approved"
    assert all(k in result.json for k in (
        "index", "predicted_label", "predicted")), "The service test will fail until a trained model has been approved"
