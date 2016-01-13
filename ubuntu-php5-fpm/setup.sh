#!/bin/bash
apt-get update
apt-get install libapache2-mod-fastcgi php5-fpm

echo '
<IfModule mod_fastcgi.c>
AddHandler php5-fcgi .php
Action php5-fcgi /php5-fcgi
Alias /php5-fcgi /usr/lib/cgi-bin/php5-fcgi
FastCgiExternalServer /usr/lib/cgi-bin/php5-fcgi -socket /var/run/php5-fpm.sock -pass-header Authorization

<Directory /usr/lib/cgi-bin>
    Require all granted
    </Directory>

    </IfModule>
' > /etc/apache2/conf-available/php5-fpm.conf
a2enmod actions fastcgi alias
a2enconf php5-fpm
