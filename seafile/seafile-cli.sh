#!/bin/bash
seaf-cli init -d seafile-client

seaf-cli start

seaf-cli list-remote -s http://192.168.0.40:8000 -u admin@example.com -p admin

seaf-cli sync -s http://192.168.0.40:8000 -u admin@example.com -p admin -l d86ab503-df0e-4fa0-bf5b-37003ca692a6 -d ./test-dir/

