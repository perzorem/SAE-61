#!/bin/bash

docker run --rm -d \
		-p 3306:3306 \
		-v vol-sql-demo:/var/lib/mysql \
		--name serveur-mysql \
		--env MYSQL_ROOT_PASSWORD=root \
		--env MYSQL_USER=user \
		--env MYSQL_PASSWORD=user \
		--env MYSQL_DATABASE=sae61 \
		--network net-sae61 \
		mysql

sleep 10

mysql -u root -p'root' -h 127.0.0.1 --port=3306 sae61 < "sql/db-sae61.sql" 2> /dev/null