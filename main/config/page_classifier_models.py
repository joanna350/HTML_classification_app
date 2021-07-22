import inspect
import os
import sys
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from definition import Config

page_classifier_model = {
    "models": {
        "NAME": "SGD",  # RFC does not have decision_function feature
        "LOAD_SAVED_MODEL": False,
        "SAVED_MODEL_DIRECTORY": "./",
        "TRAIN_ON_TEST_SET": False,
        "CLASS_NUMBER_FROM_NAME": {

        },
        "TRAIN_DATASET_DIR": Config.DATA_STORE_DIR + "/train",
        "TEST_DATASET_DIR": Config.DATA_STORE_DIR + "/test",
        "CLASSES_TO_TRAIN": [

        ],
        "CLASSES_TO_TEST": [

        ],
        "MAX_ITEMS_PER_CLASS": None,
        "SAVE_MODEL_AFTER_TEST": True,
        "OUTPUT_DIRECTORY": "./saved_predictor_temp",
        "OUTPUT1": "clf.pickle",
        "OUTPUT2": "vectorizer.pickle",
    }
}
