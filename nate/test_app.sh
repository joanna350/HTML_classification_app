# runs the endpoint 'refresh', then check whether the directory is empty

if [ -d "uploads" ]; then
  echo "Directory 'uploads' exists."
  curl --silent --output /dev/null http://0.0.0.0:5000/refresh
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