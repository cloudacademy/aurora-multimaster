# Amazon Aurora Multi-Master

```
sudo apt-get install mysql-client
```

```
HOST=
MYSQL_PWD=cloudacademy mysql -h $HOST -u admin demo
```

```
select @@hostname;
```

```
CREATE DATABASE demo;
```

```
CREATE TABLE course (
    title VARCHAR(40), 
    instructor VARCHAR(40),
    duration INT, 
    created DATE, 
    url VARCHAR(256)
);
```

```
INSERT INTO course (title, instructor, duration, created, url) VALUES ('Course1', 'Jeremy Cook', 100, '1999-03-30', 'http://here.com');
```

```
NODE1=<aurora endpoint 1 here>
NODE2=<aurora endpoint 2 here>

watch -n1 "MYSQL_PWD=cloudacademy mysql -h $NODE1 -u admin demo -e 'select count(*) from course'"
```

```
NODE1=<aurora endpoint 1 here>
NODE2=<aurora endpoint 2 here>

MYSQL_PWD=cloudacademy mysql -h $NODE1 -u admin -e 'ALTER SYSTEM CRASH'
```
