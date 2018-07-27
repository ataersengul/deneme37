import logging
# import  logging.config
# import deneme37.Logging.logger-demo-conf as conf


# demo = LoggerDemoConf()

#filename="test.log",
logging.basicConfig(format="%(asctime)s: %(levelname)s: %(message)s",
                    datefmt="%m%d%Y %H:%M:%S %p",
                    level=logging.DEBUG)

logging.warning("warning test")
logging.info("info test")
logging.error("error test")