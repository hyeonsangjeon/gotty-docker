Gotty Docker
===

This example can be used to share the terminal using gotty[1] in the docker container.
This gotty based on ubuntu Linux.
, having:

- gotty
- docker
- ubuntu terminal

 
To try the example, you need to have a docker installed on your OS. And needed sudoers account permission[1]


After docker installation, execute this command to bake a docker image in a terminal:

```console
docker build -t modenaf360/gotty:latest .
```

Let's run gotty docker
```console
docker run -p 8989:8080 -d --name gotty -it  modenaf360/gotty:latest
```

You can use docker-compose templete
```console
docker-compose up
```

or
```console
docker-compose -f ./docker-compose.yml
```

Check rest index call :

```console
http://localhost:8989
```


# docker options are as follows,

|Variables      |Description                                                   |
|---------------|--------------------------------------------------------------|
|'run'          |run                                                           |  
|'-d'           |background run                                                | 
|'-p'           |expose port conainer core-os port to your os (port fowarding) |
|'--name'       |container nickname                                            |
|'-i'           |enable bash standard input (stdin)                            |
|'-t'           |using bash TTY mode (pseudo-TTY)                              |


# Reference

[1]. https://github.com/yudai/gotty
[2]. https://docs.docker.com/engine/installation/

