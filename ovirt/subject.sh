#!/bin/bash
openssl x509 -noout -text -in server-cert.pem | grep Subject: | cut -f 10- -d " "
