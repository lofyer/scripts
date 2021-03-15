#!/bin/bash
docker commit --change 'ENV ["CATTLE_UI_PL"="Zaku"]' --change 'Entrypoint ["entrypoint.sh"]' 31 zaku:v2.4.13-ent2
