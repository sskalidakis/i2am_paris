FROM jwilder/nginx-proxy:0.9
COPY nginx/vhost.d/default /etc/nginx/vhost.d/default
COPY nginx/custom.conf /etc/nginx/conf.d/custom.conf

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d