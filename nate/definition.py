"""
Definition file to maintain some original Config definitiions from config.py at the top level
"""
import os


class Config:

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_STORE_DIR = ROOT_DIR + "/data_store"
    CONFIG_DIR = ROOT_DIR + "/config"
