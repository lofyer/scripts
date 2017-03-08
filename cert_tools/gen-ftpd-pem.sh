#!/bin/bash
openssl req -x509 -nodes -days 7300 -newkey rsa:2048 -keyout ftpd-ssl.pem -out ftpd-ssl.pem
