# nate.blackbox.page.classifier
Landing Page Classifier

## Setup virtualenv 

Run the `./setup_env.sh` script

## Training and predicting 
The first step to training the page classifier is to load in a dataset of the various types of pages.

```python
    from data.dataset import Dataset

    dc_train = Dataset(dataset_dir='./data_store/train',
                       training_set=True)
    dc_train.load_from_class_names(class_names=['out_of_stock', 'popup', 'product_landing_page', 'product_listing', 'site_error', 'bot'],
                                   multiple_resolution_dataset=True)

```

To train the page classifier you simply call its `train` method with a loaded dataset:

```python
    from config.configclass import ConfigClass
    from util.page_classifier import PageClassifier
    from config.models.page_classifier_models import page_classifier_model

    # initialise configuration
    config = page_classifier_model
    # Create Model
    model = PageClassifier(config)
    #Train Model
    model.train(dc_train)
``` 
 
For prediction similarly just use the predict method, which also takes in a dataset.

```python
    from data.functions_for_dataset_creator import inverse_map_dict
    predictions = model.predict(dc_train)

    predicted_classes = predictions[0]
    confidence_arrays = predictions[1]
    for predicted_class, confidence_array in zip(predicted_classes, confidence_arrays):
        results_dict = {
            'pageClass': inverse_map_dict(config['models']['CLASS_NUMBER_FROM_NAME'])[predicted_class],
            'confidence': confidence_array[predicted_class]
        }
        print(results_dict)


```    

This will output an tuple, the first dimension is a list of predicted page types 
for each document in the dataset (as integers). The enumeration is found in config/models/page_classifier_models.py[CLASS_NUMBER_FROM_NAME]
The second dimension is a list of arrays giving the confidence in each class.  

Separate training script is in `train_page_classifier.py`
and a sample evaluation from html string inside `page_classifier.py`
