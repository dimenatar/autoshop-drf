from decouple import config

class SimulationConfig:
    MIN_MAX_CAR_RANDOM_USER_INCOME = config("MIN_MAX_CAR_RANDOM_USER_INCOME", cast=(float, float))
    MAX_ACTIVE_ENTITIES_PER_MODEL = config("MAX_ACTIVE_ENTITIES_PER_MODEL", cast=int, default=50)
    MIN_MAX_CAR_RANDOM_PRICE = config("MIN_MAX_CAR_RANDOM_PRICE", cast=(float, float))