FROM python:3.11.4-slim-bullseye as web

ADD . /opt/MedItCRM
WORKDIR /opt/MedItCRM/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && \
    apt upgrade -y && \
    apt install -y --no-install-recommends curl gcc gnupg netcat cron build-essential libsasl2-dev python3-dev \
    libldap2-dev && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt update && ACCEPT_EULA=Y apt install -y --no-install-recommends msodbcsql18 unixodbc-dev && \
    pip install --upgrade pip && \
    pip install -r ./requirements.txt && \
    sed -i "s/\(CipherString *= *\).*/\1DEFAULT@SECLEVEL=1 /" "/etc/ssl/openssl.cnf" && \
    sed -i 's/\r$//g' ./entrypoint.sh && chmod +x ./entrypoint.sh && \
    apt purge -y curl gcc && rm -rf /var/cache/apt/* && \
    chmod ugo+x cronmail.sh && touch /var/log/cronmail.log && \
    echo "#!/bin/sh\n* * * * * /bin/bash /opt/MedItCRM/cronmail.sh\n" > /tmp/tmpcron && crontab /tmp/tmpcron &&  \
    rm /tmp/tmpcron && service cron restart


#CMD cron && tail -f /var/log/cron.log

    # postgresql-dev #python3-dev musl-devc

# run entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]