# PostgreSQL Howto(Active Active)

## 1. Single Installation

Ref: https://www.postgresql.org/download/linux/redhat/
Install the repository RPM:

```bash
yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm
yum install -y postgresql96-server
```

Optionally initialize the database and enable automatic start:

```bash
/usr/pgsql-96/bin/postgresql-96-setup initdb
systemctl enable --now postgresql-96
```

## 1.1. Change postgres password

```bash
su - postgres
psql postgres postgres
ALTER USER postgres PASSWORD 'password';
\q
```

Validate

```bash
psql -h localhost postgres postgres
\q
```

## 1.2. Allow any host access

```bash
echo "listen_addresses = '*'" >> /var/lib/pgsql/9.6/data/postgresql.conf
systemctl restart postgresql96
```

## 2. Setup Active Active with Bucardo

Ref: https://developer.ibm.com/tutorials/configure-postgresql-active-active-replication-bucardo/

Following should be executed on `both nodes`.

```bash
yum install bucardo_96 perl-DBIx-Safe postgresql96-plperl
mkdir -p /var/run/bucardo
mkdir -p /var/log/bucardo

# Create database bucardo
su - postgres                                               # change user to *postgres*
psql                                                              # enter the psql shell
create user bucardo with superuser password 'bucardobucardo';
create database bucardo with owner = bucardo;

# allow user bucardo from remote
echo -e "host\tall\t\tpostgres\t0.0.0.0/0\t\ttrust" >> /var/lib/pgsql/9.6/data/pg_hba.conf
echo -e "local\tall\t\tbucardo\t\t\t\t\ttrust" >> /var/lib/pgsql/9.6/data/pg_hba.conf
echo -e "local\tall\t\tbucardo\t\t\t\t\ttrust" >> /var/lib/pgsql/9.6/data/pg_hba.conf
```

Create test database.

```bash
su - postgres                                               # change user to *postgres*
psql
create database mydatabase;
\c mydatabase 
create table table1(id integer PRIMARY KEY, num integer);
create table table2(id integer PRIMARY KEY, num integer);
create table table3(id integer PRIMARY KEY, num integer);
\dt;
```

On `both nodes`:

```
[root@node1]# bucardo install
This will install the bucardo database into an existing Postgres cluster.
Postgres must have been compiled with Perl support,
and you must connect as a superuser

Current connection settings:
1. Host:           <none>
2. Port:           5432
3. User:           bucardo
4. Database:       bucardo
5. PID directory:  /var/run/bucardo
Enter a number to change it, P to proceed, or Q to quit: 1

Change the host to: 172.30.220.203

Changed host to: 172.30.220.203
Current connection settings:
1. Host:           172.30.220.203
2. Port:           5432
3. User:           bucardo
4. Database:       bucardo
5. PID directory:  /var/run/bucardo
Enter a number to change it, P to proceed, or Q to quit: p

Attempting to create and populate the bucardo database and schema
Database creation is complete

Updated configuration setting "piddir"
Installation is now complete.
If you see errors or need help, please email bucardo-general@bucardo.org

You may want to check over the configuration variables next, by running:
bucardo show all
Change any setting by using: bucardo set foo=bar

[root@node2]# bucardo install
This will install the bucardo database into an existing Postgres cluster.
Postgres must have been compiled with Perl support,
and you must connect as a superuser

Current connection settings:
1. Host:           <none>
2. Port:           5432
3. User:           bucardo
4. Database:       bucardo
5. PID directory:  /var/run/bucardo
Enter a number to change it, P to proceed, or Q to quit: 1

Change the host to: 172.30.220.150

Changed host to: 172.30.220.150
Current connection settings:
1. Host:           172.30.220.150
2. Port:           5432
3. User:           bucardo
4. Database:       bucardo
5. PID directory:  /var/run/bucardo
Enter a number to change it, P to proceed, or Q to quit: p

Attempting to create and populate the bucardo database and schema
Database creation is complete

Updated configuration setting "piddir"
Installation is now complete.
If you see errors or need help, please email bucardo-general@bucardo.org

You may want to check over the configuration variables next, by running:
bucardo show all
Change any setting by using: bucardo set foo=bar
```

On `both nodes`:

```
bucardo add database serv1 dbname=mydatabase host=172.30.220.203
bucardo add database serv2 dbname=mydatabase host=172.30.220.150
bucardo add table % db=serv1
bucardo add table % db=serv2
bucardo add all tables --herd=one2two db=serv1
bucardo add all tables --herd=two2one db=serv2
```

On `node1`:

```
bucardo add sync sync_one2two relgroup=one2two db=serv1,serv2
```

On `node2`:

```
bucardo add sync sync_two2one relgroup=two2one db=serv2,serv1
```

On `both nodes`:

```
bucardo start
bucardo list all
bucardo status
```


## (Choice 2)3. Setup Active Active with SymmetricDS

OK