FROM python:3.11-buster

ENV TZ=Asia/Tehran
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
WORKDIR /app

RUN apt-get update && apt-get -y install cron nginx pigz duc default-mysql-client supervisor unar nano vim htop net-tools zip unzip iputils-ping

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . /app/

COPY cron-jobs /etc/cron.d/cron-jobs
RUN chmod 0644 /etc/cron.d/cron-jobs
RUN crontab /etc/cron.d/cron-jobs

ADD start.sh /
RUN chmod +x /start.sh
EXPOSE 80

CMD ["/start.sh"]
