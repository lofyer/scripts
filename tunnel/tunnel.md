# 1. File Transfer

## server:
    nc -l 5555 < file_to_copy
## client:
    nc server_ip 5555 > new_file

# 2. Chat

## client1:
    nc -l 5555
## client2:
    nc server_ip 5555

# 3. UDP Connection

## server:
    nc -4 -u -l 5555
## clinet:
    nc -4 -u localhost 5555

# 4. TCP relay tunnel

## remote 443 to local 8443:
    ssh -g -L 8443:0.0.0.0:443 -f -N root@remote-server.com

OR

    socat tcp-listen:8443,reuseaddr,fork tcp:remote-server.com:443

## local 443 to remote 8443
    ssh -R 8443:remote-server:443 root@remote-server.com
>If you wanna 0.0.0.0:8443:remote-server:443, please modify /etc/ssh/sshd_config of remote-server.com

    GatewayPorts clientspecified

Localhost Port Forwarding

![sshL](sshL.png)

Remotehost Port Forwarding

![sshR](sshR.png)