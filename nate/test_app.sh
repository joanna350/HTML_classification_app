WEB_APP_IP='0.0.0.0'

if curl http://${WEB_APP_IP}:5000 | grep -q '<b>Visits:</b>'; then
  echo "------------Test passed------------"

  if [ -d "uploads" ]; then
    echo "Directory 'uploads' exists."

    curl --silent --output /dev/null http://${WEB_APP_IP}:5000/refresh
    echo "Refreshed."

    if [ -z "$(ls -A uploads)" ]; then
      echo "------------Test passed------------"
      exit 0
    else: # not empty
      echo "------------Test failed------------"
      exit 1
    fi
  else: # directory does not exist
   echo "Retry from the path ~/Nate/nate/"
  fi
  exit 1

else:
  echo "------------Test failed------------"
  exit 1
fi