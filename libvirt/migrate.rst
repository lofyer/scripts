python-libvirt 迁移测试
========================

迁移条件
--------

- 虚拟机在运行

- 迁移所需网络及端口开放

迁移方式
--------

- p2p

- tunnelled

- direct

迁移可选项
----------

- 离线（关机）

- 在线（保持开机）

- 暂停（迁移后暂停）

- 压缩数据

- 拷贝完整磁盘存储（用于非共享存储）

测试流程
--------

1. 配置libvirt使用tcp监听。迁移网络可以使用加密（tls，参考 http://libvirt.org/remote.html ），或者非加密链接（tcp），可选认证为CA，SASL等。

    修改配置文件/etc/libvirt/libvirtd.conf，添加如下选项
    
    .. code::
    
        listen_tls = 0
        listen_tcp = 1
        auth_tcp = "none"

    修改配置文件/etc/sysconfig/libvirtd，打开libvirtd的监听端口以方便迁移测试
    
    .. code::
    
        LIBVIRTD_ARGS="--listen"
        
    
2. 设置主机名

    在两个主机的/etc/hosts文件中添加
    
    .. code ::
    
        192.168.2.110   libvirt1.example.com
        192.168.2.111   libvirt2.example.com
    
    执行命令，形如：
   
    .. code::
    
        # hostname libvirt1.example.com

3. 修改 migrate.py 中的 `DEST_URI` 后执行迁移。如果目标主机中没有虚拟机的磁盘等相关文件，可以添加 `VIR_MIGRATE_NON_SHARED_DISK` 或者 `VIR_MIGRATE_NON_SHARED_INC` 参数拷贝磁盘或其增量。
