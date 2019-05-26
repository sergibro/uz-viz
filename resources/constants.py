DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"

BASE_URL = 'https://booking.uz.gov.ua/'
BASE_EN_URL = f'{BASE_URL}en/'
BASE_UA_URL = f'{BASE_URL}ua/'
BASE_RU_URL = f'{BASE_URL}ru/'

TRAIN_SEARCH_EN_URL = f'{BASE_EN_URL}train_search/'
TRAIN_SEARCH_UA_URL = f'{BASE_UA_URL}train_search/'
TRAIN_SEARCH_RU_URL = f'{BASE_RU_URL}train_search/'
ROUTE_EN_URL = f'{BASE_EN_URL}route/'
ROUTE_UA_URL = f'{BASE_UA_URL}route/'
ROUTE_RU_URL = f'{BASE_RU_URL}route/'
TRAIN_WAGONS_EN_URL = f'{BASE_EN_URL}train_wagons/'
TRAIN_WAGONS_UA_URL = f'{BASE_UA_URL}train_wagons/'
TRAIN_WAGONS_RU_URL = f'{BASE_RU_URL}train_wagons/'
TRAIN_WAGON_EN_URL = f'{BASE_EN_URL}train_wagon/'
TRAIN_WAGON_UA_URL = f'{BASE_UA_URL}train_wagon/'
TRAIN_WAGON_RU_URL = f'{BASE_RU_URL}train_wagon/'
WAGONS_EN_URL = f'{TRAIN_WAGONS_EN_URL}wagons/'
WAGONS_UA_URL = f'{TRAIN_WAGONS_UA_URL}wagons/'
WAGONS_RU_URL = f'{TRAIN_WAGONS_RU_URL}wagons/'
STATION_SEARCH_EN_URL = f'{TRAIN_SEARCH_EN_URL}/station/?term='
STATION_SEARCH_UA_URL = f'{TRAIN_SEARCH_UA_URL}/station/?term='
STATION_SEARCH_RU_URL = f'{TRAIN_SEARCH_RU_URL}/station/?term='

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'

SOCKS = []  # maybe some socks to use if bad IP

MONGO_URL = 'mongodb://USERNAME:PASSWORD@IP_HOST'  # to save data
