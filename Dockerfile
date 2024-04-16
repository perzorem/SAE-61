FROM python:3.6

EXPOSE 5000

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY app.py /app
CMD python app.py
FROM mysql

# Environment variables
ENV MYSQL_ROOT_PASSWORD secretadmin

# Allows you to change the value of "max_allowed_packet"
ADD ["mysqlconf/gatewaymy.cnf", "/etc/mysql/conf.d/conf_mysql.cnf"]

# Create Database
RUN	mkdir /usr/sql
RUN	chmod 644 /usr/sql

ADD ["sql/sources.sql", "/usr/sql/sources.sql"]

RUN /etc/init.d/mysql start && \
        mysql -u root -p${MYSQL_ROOT_PASSWORD} -e "CREATE DATABASE lba" && \
    	mysql -u root -p${MYSQL_ROOT_PASSWORD} -D lba < /usr/sql/sources.sql && \
    	rm -rd /usr/sql && \
