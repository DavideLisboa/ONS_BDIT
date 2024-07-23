import logging


def logs(dataLogName,logging_Path):
    logpath= str(logging_Path + dataLogName + '.txt')
    f = open(logpath, 'w')
    f.close            
    logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S', filename=logpath, filemode='w')