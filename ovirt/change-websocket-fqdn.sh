mv /etc/pki/ovirt-engine/certs/websocket-proxy.cer /root/websocket-proxy.cer.orig
cp /etc/pki/ovirt-engine/keys/websocket-proxy.key.nopass /root/websocket-proxy.key.nopass.orig

# Regenerate websocket-proxy certificate:
/usr/share/ovirt-engine/bin/pki-enroll-pkcs12.sh --name=websocket-proxy --password=mypass --subject="/CN=MYSERVER" --keep-key
# Note: Replace MYSERVER with correct domain name.

# Regenerate key:
openssl pkcs12 -in /etc/pki/ovirt-engine/keys/websocket-proxy.p12 -passin "pass:mypass" -nocerts -nodes > /etc/pki/ovirt-engine/keys/websocket-proxy.key.nopass 
