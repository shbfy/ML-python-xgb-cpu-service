# Import your handlers here
from service import Iris, Intro


# Configuration for web API implementation
def config(api):

    # Instantiate handlers and map routes
    api.add_route('/iris', Intro())
    api.add_route('/iris/{index:int(min=0)}', Iris())
