# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database
MONGOALCHEMY_DATABASE = 'baper-sis'

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
WTF_CSRF_ENABLED = False

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "rahasia"

# Secret key for signing cookies
SECRET_KEY = "rahasia"

# Elastic server
ELASTICSEARCH_SERVER = 'http://localhost:9200'
ELASTICSEARCH_SERVER_USERNAME = "admin"
ELASTICSEARCH_SERVER_PASSWORD = "admin"

MONGOALCHEMY_SERVER = 'localhost'
