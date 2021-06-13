####Environment:
- Ubuntu 18.04

####To Run:
- To run the app with Docker:
```
docker-compose up
```
- To run the connection test over docker:
```
chmod u+x dockertest.sh
./dockertest.sh
```
- To run the app without Docker:
 ```
Nate/nate/app/routes.py, modify as
... Redis(host="0.0.0.0" ...
Nate/ 
python run.py
```
- To run the unit tests: 
```
pytest _path_to_each_test_
```

```
Caveats:
Host configuration on Mac entails a few more steps not considered atm
```