FROM python:3.12-alpine AS builder

WORKDIR /build
COPY generate_data.py .
RUN python generate_data.py

FROM nginx:alpine

COPY index.html  /usr/share/nginx/html/index.html
COPY --from=builder /build/pages /usr/share/nginx/html/pages

EXPOSE 80
