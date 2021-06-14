#### Environment:
- Ubuntu 18.04

#### File Structure


#### To Run:
Generate trained models
```
nate/
python -m util.train_page_classifier
```
- To run the app with Docker:
```
nate/
docker-compose up
```
- Go to the link
- Upload files with `rwx` access for the group
- Uploaded files will be under directory `nate/uploads`
- To clear the database of `uploads`, use the endpoint `/refresh`

- To run the network test over Docker:
```
chmod u+x dockertest.sh
./dockertest.sh
```
- To run the app without Docker/and test:
```
nate/app/routes.py, set
line 9: Redis(host="0.0.0.0"

nate/
python -m run
chmod u+x test_app.sh
./test_app.sh
```
>> 
- To run the unit tests: 
```
pytest _path_to_each_test_from_the_current_directory_
```
Caveats:
To host the docker app on Mac, may want to refer to the [github issues](https://github.com/docker/for-mac/issues/2670)