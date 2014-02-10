#!/bin/bash
echo "*****Generating your KEY*****"
openssl genrsa -camellia256 -out server.key 1024 
cp server.key server.key.org 
openssl rsa -in server.key.org -out server.key 
echo "*****Generating your csr*****"
openssl req -new -key server.key -out server.csr
echo "*****Generating your root crt*****"
openssl x509 -req -days 3650 -in server.csr -signkey server.key -out server.crt
echo "*****Generating your site crt*****"
openssl req -new -key server.key -out server.csr
openssl x509 -sha1 -days 1825 -req -CA server.crt -CAkey server.key -CAcreateserial -CAserial ca.srl -in server.csr -out server-site.crt
echo "*****Generating your self crt*****"
openssl req -new -x509 -days 3650 -key server.key -out server-self.crt

cat server.crt server.key > certificate.pem
