1. Enable ssl and proxy
a2enmod proxy proxy_http ssl

2. Edit apache conf
cat /etc/apache2/sites-enabled/portal.conf

<VirtualHost *:443>
Servername dingding.zstack.io
ErrorLog /var/log/apache2/portal_error_log
TransferLog /var/log/apache2/portal_access_log
LogLevel warn
SSLEngine on
SSLProxyEngine on
#SSLProtocol all -SSLv2
#SSLCipherSuite ALL:!ADH:!EXPORT:!SSLv2:RC4+RSA:+HIGH:+MEDIUM:+LOW
SSLCACertificateFile /root/zstack-price-calc-for-account/cert/3729215_dingding.zstack.io_chain.crt
SSLCertificateKeyFile /root/zstack-price-calc-for-account/cert/3729215_dingding.zstack.io.key
SSLCertificateFile /root/zstack-price-calc-for-account/cert/3729215_dingding.zstack.io_public.crt
ProxyRequests Off
ProxyPass / http://127.0.0.1:9999/
ProxyPassReverse / http://127.0.0.1:9999/
</VirtualHost>

3. Restart apache2
service apache2 restart
