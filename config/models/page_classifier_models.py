import os
from definition import Config

page_classifier_model = {
    'models': {
        'NAME': 'SGD', # also available LinearSVM, RFC, SGD  (RFC does not have decision_function feature)
        'LOAD_SAVED_MODEL': False,
        'SAVED_MODEL_DIRECTORY': './',
        'TRAIN_ON_TEST_SET': False,
        'CLASS_NUMBER_FROM_NAME': {'out_of_stock': 0,
                                   'popup': 1,
                                   'product_landing_page': 2,
                                   'product_listing': 3,
                                   'site_error': 4,
                                   'bot': 5
                                   },
        'TRAIN_DATASET_DIR': Config.DATA_STORE_DIR + '/train',
        'TEST_DATASET_DIR':Config.DATA_STORE_DIR + '/test',
        'CLASSES_TO_TRAIN': ['out_of_stock', 'popup', 'product_landing_page', 'product_listing', 'site_error', 'bot'],
        'CLASSES_TO_TEST': ['out_of_stock', 'popup', 'product_landing_page', 'product_listing', 'site_error'],
        'MAX_ITEMS_PER_CLASS': None,
        'SAVE_MODEL_AFTER_TEST': True,
        'OUTPUT_DIRECTORY': './saved_predictor_temp',
        'OUTPUT1': 'clf.pickle',
        'OUTPUT2': 'vectorizer.pickle',
    }
}
