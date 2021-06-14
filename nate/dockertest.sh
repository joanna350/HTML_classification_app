WEB_APP_IP=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' nate_web_1)

if curl http://${WEB_APP_IP}:5000 | grep -q '<b>Visits:</b>'; then
  echo "------------Tests passed------------"
  exit 1
else:
  echo "------------Tests failed------------"
  exit 0
fi