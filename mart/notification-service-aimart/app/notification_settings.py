#NOTIFICATION-svc-db SETTINGS.py
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

KAFKA_CONSUMER_GROUP_ID_FOR_NOTIFICATION = config("KAFKA_CONSUMER_GROUP_ID_FOR_NOTIFICATION", cast=str)
# topic for Notification
#KAFKA_Notification_TOPIC = config("KAFKA_NOTIFICATION_TOPIC", cast=str)
KAFKA_CREATE_NOTIFICATION_TOPIC = config("KAFKA_CREATE_NOTIFICATION_TOPIC", cast=str)
KAFKA_UPDATE_NOTIFICATION_TOPIC = config("KAFKA_UPDATE_NOTIFICATION_TOPIC", cast=str)
KAFKA_DELETE_NOTIFICATION_TOPIC = config("KAFKA_DELETE_NOTIFICATION_TOPIC", cast=str)
KAFKA_SEND_NOTIFICATION_TOPIC   = config("KAFKA_SEND_NOTIFICATION_TOPIC",   cast=str)
# kafka group and topic of order processing for notifications
KAFKA_CONSUMER_GROUP_ID_FOR_ORDER = config("KAFKA_CONSUMER_GROUP_ID_FOR_ORDER", cast=str)
KAFKA_CREATE_ORDER_TOPIC = config("KAFKA_CREATE_ORDER_TOPIC" , cast = str)
KAFKA_UPDATE_ORDER_TOPIC = config("KAFKA_UPDATE_ORDER_TOPIC" , cast = str)
KAFKA_DELETE_ORDER_TOPIC = config("KAFKA_DELETE_ORDER_TOPIC" , cast = str)

#KAFKA_PRODUCT_TOPIC=Product-events-topic
KAFKA_CREATE_PRODUCT_TOPIC= config("KAFKA_CREATE_PRODUCT_TOPIC", cast = str)
KAFKA_UPDATE_PRODUCT_TOPIC= config("KAFKA_UPDATE_PRODUCT_TOPIC", cast = str)
KAFKA_DELETE_PRODUCT_TOPIC= config("KAFKA_DELETE_PRODUCT_TOPIC", cast = str)
#CONSIUMER GRPOUP For Product
KAFKA_CONSUMER_GROUP_ID_FOR_PRODUCT= config("KAFKA_CONSUMER_GROUP_ID_FOR_PRODUCT", cast = str)


#Gmail SMTP setup
SMTP_SERVER =   config("SMTP_SERVER", cast = str)
SMTP_PORT=      config("SMTP_PORT", cast = int)
SMTP_USERNAME=  config("SMTP_USERNAME", cast = str)
SMTP_PASSWORD=  config("SMTP_PASSWORD", cast = Secret)