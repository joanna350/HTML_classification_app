## Project Scope
- Flask Web Service that returns classification result based on received .html file
- Model trained will be saved in serialised pickle format
- TDD approach with Docker containerisation

## Environment:
- Ubuntu 18.04

## File Structure
```
├── main
│   ├── app
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── routes.py
│   │   └── templates
│   │       └── upload.html
│   ├── config
│   │   ├── __init__.py
│   │   ├── configclass.py
│   │   ├── page_classifier_models.py
│   │   └── singleton.py
│   ├── data
│   │   ├── dataset.py
│   │   └── functions_for_dataset_creator.py
│   ├── data_store
│   │   ├── examples
│   │   ├── test
│   │   │   └──  5 classes of html
│   │   └── train
│   │   │   └──  5 classes of html
│   ├── definition.py
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── dockertest.sh
│   ├── __init__.py
│   ├── README.md
│   ├── requirements.txt
│   ├── run.py
│   ├── saved_predictor_temp
│   │   ├── clf.pickle
│   │   └── vectorizer.pickle
│   ├── setup_env.sh
│   ├── test_app.sh
│   ├── uploads
│   └── util
│       ├── __init__.py
│       ├── io_funcs.py
│       ├── page_classifier.py
│       └── train_page_classifier.py
├── Readme.md
└── tests
    ├── data
    │   ├── __init__.py
    │   └── test_functions_for_dataset_creator.py
    ├── __init__.py
    └── util
        ├── test_io_funcs.py
        └── test_page_classifier.py
```

## How to Run 

#### The app (with Docker):
```
main/app/routes.py
line 9: Redis(host="redis"
```
```
main/
docker-compose up
```
- Click on the url

- Upload files with `rwx` access for the group

- To clear the database of `main/uploads`, add `/refresh` to the url and enter

#### Network test:
```
chmod u+x dockertest.sh
./dockertest.sh
```

#### The app locally:

```
main/app/routes.py
line 9: Redis(host="0.0.0.0"
```

#### Curl test

```
main/
python -m run
chmod u+x test_app.sh
./test_app.sh
```

#### Run the unit tests:
```
root
chmod u+x main/run_tests.sh
./main/run_tests.sh
```

#### Generate trained models

* current unit tests are set to pre-made models, test cases must be updated with new generation
```
main/
python -m util.train_page_classifier
```

Caveats:
To host the docker app on Mac, may want to refer to the [github issues](https://github.com/docker/for-mac/issues/2670)