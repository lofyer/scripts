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

# 4. ssh proxy

## socksv5 proxy
ssh -ND 7070 root@remotehost

# 5. TCP relay tunnel

## remote/remote-lan host 443 to local 8443:

    ssh -g -L 0.0.0.0:8443:remote-lan-server:443 -f -N root@remote-ssh-server

OR

    socat tcp-listen:8443,reuseaddr,fork tcp:remote-server:443

## local/local-lan host 443 to remote 8443

    ssh -R 0.0.0.0:8443:lan-server:443 root@remote-server

>If you wanna 0.0.0.0:8443:remote-server:443 rather than 127.0.0.1:8443:remote-server:443, please modify /etc/ssh/sshd_config of remote-server

    GatewayPorts clientspecified

>Close sshd CLOSED_WAIT connections

    StreamLocalBindUnlink yes

Local Port Forwarding

![sshL](sshL.png)

Remote Port Forwarding

![sshR](sshR.png)

# 6. Change from ssh to autossh

    # Auto connect when closed
    autossh -f -M 20000 -R 0.0.0.0:8443:lan-server:443 root@remote-server

    # Clean CLOSE_WAIT process
    netstat -anp | grep ':8889 ' | grep CLOSE_WAIT | awk '{print $7}' | cut -d \/ -f1 | grep -oE "[[:digit:]]{1,}" | xargs kill -9
