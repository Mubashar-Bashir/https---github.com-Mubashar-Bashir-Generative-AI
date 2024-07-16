from starlette.config import Config  # Import Config class to manage environment variables
from starlette.datastructures import Secret  # Import Secret class to handle sensitive data securely

try:
    # Attempt to create a Config object that reads from a .env file
    config = Config(".env")
except FileNotFoundError:
    # If the .env file is not found, create a Config object that relies on system environment variables
    config = Config()

# Load the DATABASE_URL environment variable and cast it to a Secret for secure handling
DATABASE_URL = config("DATABASE_URL", cast=Secret)

# Load the TEST_DATABASE_URL environment variable and cast it to a Secret for secure handling
TEST_DATABASE_URL = config("TEST_DATABASE_URL", cast=Secret)



BOOTSTRAP_SERVER = config("BOOTSTRAP_SERVER", cast=str)

KAFKA_CONSUMER_GROUP_ID_FOR_PRODUCT = config("KAFKA_CONSUMER_GROUP_ID_FOR_PRODUCT", cast=str)
# topic for products
KAFKA_PRODUCT_TOPIC = config("KAFKA_PRODUCT_TOPIC", cast=str)
KAFKA_CREATE_PRODUCT_TOPIC = config("KAFKA_CREATE_PRODUCT_TOPIC", cast=str)
KAFKA_UPDATE_PRODUCT_TOPIC = config("KAFKA_UPDATE_PRODUCT_TOPIC", cast=str)
KAFKA_DELETE_PRODUCT_TOPIC = config("KAFKA_DELETE_PRODUCT_TOPIC", cast=str)