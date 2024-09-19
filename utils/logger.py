import logging


from logging.handlers import RotatingFileHandler

def get_logger(name:str) :
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    #Gestionnaire de rotation de fichier
    file_handler =RotatingFileHandler(f'{name}.log',maxBytes=5*1024*1024,backupCount=5)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    #Ajout du gestionnaire de fichier au logger
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    #Ajout du gestionnaire de console au logger

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
