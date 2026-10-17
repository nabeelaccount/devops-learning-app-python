FROM        dhi.io/nginx:1-alpine

WORKDIR     /app

COPY        ./config/loadbalance.conf /etc/nginx/conf.d/default.conf

COPY        ./static/index.html /usr/share/nginx/html/