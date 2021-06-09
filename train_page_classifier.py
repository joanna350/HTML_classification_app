from sklearn.metrics import confusion_matrix

from config.models.page_classifier_models import page_classifier_model
from data.dataset import Dataset
from configclass import ConfigClass
import logging
from sklearn import metrics

from logger import initialise_logger
from page_classifier import PageClassifier


module_logger = logging.getLogger('main_app.train_page_classifier')


def main_train_page_classifier():
    config = ConfigClass.config

    # load train dataset
    dc_train = Dataset(config['models']['TRAIN_DATASET_DIR'],
                       training_set=True)
    dc_train.load_from_class_names(config['models']['CLASSES_TO_TRAIN'], multiple_resolution_dataset=True)

    # load test dataset
    dc_test = Dataset(config['models']['TEST_DATASET_DIR'])
    dc_test.load_from_class_names(config['models']['CLASSES_TO_TEST'], multiple_resolution_dataset=False)

    # combine dataset
    if config['models']['TRAIN_ON_TEST_SET']:
        dc_train.combine_datasets(dc_test)

    # Create Model
    config = page_classifier_model
    model = PageClassifier(config)
    #Train Model
    model.train(dc_train)

    # Evaluation
    pred = model.predict(dc_test)[0]
    score = metrics.accuracy_score(dc_test.list_of_class_values, pred)
    cm = confusion_matrix(dc_test.list_of_class_values, pred)
    module_logger.info("The final accuracy is %f" % score)

    # Save model
    if config['models']['SAVE_MODEL_AFTER_TEST']:
        model.save(config['models']['OUTPUT_DIRECTORY'])


if __name__ == '__main__':
    root_logger_ = initialise_logger()
    ConfigClass.set_configuration(config=page_classifier_model, config_seed=42)
    main_train_page_classifier()
