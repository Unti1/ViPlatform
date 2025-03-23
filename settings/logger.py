import logging 

database_logger = logging.getLogger('sqlalchemy')
database_logger.setLevel(logging.INFO)
database_logger_file_handler = logging.FileHandler('logs/sqlalchemy.log')
database_logger_file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
database_logger.addHandler(database_logger_file_handler)

