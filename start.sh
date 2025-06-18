#!/bin/bash
echo "* Starting the cron jobs"
cron

if [ -d /app/supervisor_conf ]; then
  echo "> Copy Supervisor Configuration Directory ..."
  cp -rf /app/supervisor_conf/* /etc/supervisor/conf.d/
  echo "> Starting Supervisor ..."
  for i in {1..5}; do {
    service supervisor stop
    service supervisor start
    supervisorctl reread
    supervisorctl update
    supervisorctl start all
  } && break || sleep 5; done
else
  if [ -f /app/supervisor.conf ]; then
    echo "> Copy Supervisor Configuration ..."
    cp -rf /app/supervisor.conf /etc/supervisor/conf.d/supervisor.conf
    echo "> Starting Supervisor ..."
    for i in {1..5}; do {
      service supervisor stop
      service supervisor start
      supervisorctl reread
      supervisorctl update
      supervisorctl start all
    } && break || sleep 5; done
  fi
fi

echo "do nginx works ..."
if [ -f /app/nginx.conf ]; then
  rm -rf /etc/nginx/sites-available/default
  rm -rf /etc/nginx/sites-enabled/default
  cp -rf /app/nginx.conf /etc/nginx/sites-available/default
  ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default
  service nginx start
fi

echo "docker login ..."
docker login registry.chabokan.net -u chabokan_re_system -p pRE98xC5ece

echo "python quarter_hourly ..."
python manage.py runjobs quarter_hourly

echo "Run Gunicorn Server"
gunicorn core.wsgi -b 0.0.0.0:3000  --workers 2 --threads 2 --timeout 60
