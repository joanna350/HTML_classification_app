#### Environment:
- Ubuntu 18.04

#### File Structure
```
├── nate
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

#### To Run:

Run the app with Docker:
```
nate/
docker-compose up
```
- Click on the url

- Upload files with `rwx` access for the group

- To clear the database of `nate/uploads`, add `/refresh` to the url and enter

Run the network test over Docker:
```
chmod u+x dockertest.sh
./dockertest.sh
```

Run the app without Docker/and test:

```
nate/app/routes.py
line 9: Redis(host="0.0.0.0"
```

```
nate/
python -m run
chmod u+x test_app.sh
./test_app.sh
```

Run the unit tests:
```
Nate/
chmod u+x nate/run_tests.sh
./nate/run_tests.sh
```

Generate trained models

* current unit tests are set to pre-made models, test cases must be updated with new generation
```
nate/
python -m util.train_page_classifier
```

Caveats:
To host the docker app on Mac, may want to refer to the [github issues](https://github.com/docker/for-mac/issues/2670)