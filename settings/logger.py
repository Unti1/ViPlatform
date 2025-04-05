import logging



database_logger = logging.getLogger("sqlalchemy")
database_logger.setLevel(logging.WARNING)
database_logger_file_handler = logging.FileHandler("logs/sqlalchemy.log")
database_logger_file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
database_logger.addHandler(database_logger_file_handler)


fastapi_logger = logging.getLogger("fastapi")
fastapi_logger.setLevel(logging.WARNING)
fastapi_logger_file_handler = logging.FileHandler("logs/fastapi.log")
fastapi_logger_file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
fastapi_logger.addHandler(fastapi_logger_file_handler)