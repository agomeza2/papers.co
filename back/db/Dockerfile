FROM mongo:7

COPY ColombiaResearch /dump/ColombiaResearch
COPY init.sh /docker-entrypoint-initdb.d/init.sh
COPY .env   /docker-entrypoint-initdb.d/.env 
RUN chmod +x /docker-entrypoint-initdb.d/init.sh

CMD ["mongod"]
