# To start docker container:

`docker run -d -p8081:80 p43:latest`

# Notes
Use of the port publish parameter:
[local bind addr:]local_port:container_port[/protocol]

So to bind port 80 of the container (where nginx is listening) to port 8081 on the local machine,
listening on 0.0.0.0 (all interfaces), use `-p 8081:80/tcp`.

-d detaches the container after run

# Building a new docker container
1. Clone the project repository from GitHub
2. cd to the `docker-dist` directory
3. Prepare to run the `p43-build` script
4. Until the project is made public, an ssh keypair will be required for the automation process (the docker container build script) to clone the repository.
5. Once this project is cloned to a public repository, the keypair will no longer be required; the project can be anonymously cloned.

The expected key is `id_ed25519_docker_github`, and can be generated with the command `ssh-keygen -ted25519`.  Save the generated private key as `~/.ssh/id_ed25519_docker_github` and the paired public key will be named similarly with a `.pub` extension.
The `p43-build` script will pass this key to the container build environment, and the key will be removed from the image layer as it is built.

Once the script completes you should have a new image named `p43`.

```
$ docker image list
REPOSITORY                  TAG       IMAGE ID       CREATED        SIZE
p43                         latest    7c7f29f24cb4   3 weeks ago    1.77GB
```

This image can be copied to another host (for instance, on a host that doesn't have the proper dependencies to build the docker container).

To export the container:
`docker image save -o p43.tar p43`

To import the container on the remote host:
`docker image load -i p43.tar`

If you have a fast network connection, it may be faster to transfer the uncompressed tar archive than it is to compress it on the source, transfer it, and uncompress it on the destination.

## Notes

Conditional build steps are not used in the Dockerfile; they will prevent docker from using cached layers when rebuilding the image.

Currently, two Dockerfiles are maintained; one with the ssh keypair configuration (in the `key-based-build/` directory) and one without in the `public-build/` directory.  We are not using a configuration tool like ansible to reduce the number of requirements.  Once the project has been forked to a public repo, the key-based Dockerfile will no longer need to be maintained.

# gunicorn notes
If you enter the container and obtain a shell, these gunicron commands may be useful:

```
gunicorn --bind=unix:/tmp/gunicorn.sock --workers=2 wsgi:create_app
```

gunicorn logging:

```
gunicorn --bind=unix:/tmp/gunicorn.sock --workers=2 --log-file=/var/log/gune --log-level debug --access-logfile=/var/log/guna wsgi:create_app
```

## nginx

Please use the -h argument to `p43-build` to specify the hostname used by nginx.
Alternately, you can permanently edit the file `support-files/server-hostname`.

## OpenSSL

Please edit the ssl configuration parameters in `support-files/openssl.cnf` for your host prior to
building an image

#### Credits

Project 43 - Web Application for Radio Astronomy Sensitivity
Author: Brian Pape
Revision: 0.1