# -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"


if __name__ == "__main__":
    import sharedtools.log as log
    log.createLogger("Deploy")

    import argparse
    from updatemode import UPDATE_MODE
    from config import Config
    from directoryprocessor import DirectoryProcessor

    parser = argparse.ArgumentParser(description='Deploy python project.')
    parser.add_argument("--inputDir", type=str, help="Input directory with source project.", default="C:/ms4w/Apache/htdocs/Generalizace/m3")
    parser.add_argument("--outputDir", type=str, help="Output directory.", default="c:/temp/built")
    args = parser.parse_args()

    log.logger.info("Python Deploy Builder")
    processor = DirectoryProcessor(args.inputDir, args.outputDir, Config())
    processor.mode = UPDATE_MODE.OVERWRITE
    processor.deploy()
    processor.printStatistics()