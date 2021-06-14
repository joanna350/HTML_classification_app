# runs the endpoint 'refresh', then check whether the directory is empty
WEB_APP_IP=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' nate_web_1)

if [ -d "uploads" ]; then
  echo "Directory 'uploads' exists."
  curl --silent --output /dev/null http://${WEB_APP_IP}:5000/refresh
  echo "Refreshed."
  if [ -z "$(ls -A uploads)" ]; then
    echo "------------Tests passed------------"
    exit 1
  else: # not empty
    echo "------------Tests failed------------"
    exit 0
  fi
else:
 echo "Retry from the path ~/Nate/nate/"
fi