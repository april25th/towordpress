#/usr/local/bin/python3.3
# coding=utf-8
import logging

class logconfig():
    def __init__(self):
        logger = logging.getLogger("ap")  
        logger.setLevel(logging.DEBUG)  
        # create file handler which logs even debug messages  
        fh = logging.FileHandler("ap.log")  
        fh.setLevel(logging.DEBUG)  
        # create console handler with a higher log level  
        ch = logging.StreamHandler()  
        ch.setLevel(logging.DEBUG)  
        # create formatter and add it to the handlers  
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")  
        ch.setFormatter(formatter)  
        fh.setFormatter(formatter)  
        # add the handlers to logger  
        logger.addHandler(ch)  
        logger.addHandler(fh)  
        # "application" code  
##        logger.debug("debug message")  
##        logger.info("info message")  
##        logger.warn("warn message")  
##        logger.error("error message")  
##        logger.critical("critical message") 
