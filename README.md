# UdaConnect

## Overview
The application is just a learning experience.

### Goal 
- Refactor a monolithic Moduler app into microservices. 

- deploying the all the new microservices to a kubernetes cluster.

- implementing Restful apis, grpc and kafka 

- PS.I kept my implementations focused to deliver these goals in the minmum frame of the technical and business requirements defined in this project.

### Technologies 
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - API webserver
* [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
* [PostgreSQL](https://www.postgresql.org/) - Relational database
* [PostGIS](https://postgis.net/) - Spatial plug-in for PostgreSQL enabling geographic queries]
* [Vagrant](https://www.vagrantup.com/) - Tool for managing virtual deployed environments
* [VirtualBox](https://www.virtualbox.org/) - Hypervisor allowing you to run multiple operating systems
* [K3s](https://k3s.io/) - Lightweight distribution of K8s to easily develop against a local cluster
* [Apatche-Kafka](https://kafka.apache.org/) - Apache Kafka is an open-source distributed event streaming platform used by thousands of companies for high-performance data pipelines, streaming analytics, data integration, and mission-critical applications.
* [grpc](https://grpc.io/) - 

### Environment Setup
To run the application, you will need a K8s cluster running locally and to interface with it via `kubectl`. We will be using Vagrant with VirtualBox to run K3s.

#### Initialize K3s
In this project's root, run `vagrant up`. 
```bash
$ vagrant up
```
The command will take a while and will leverage VirtualBox.

#### Set up `kubectl`
After `vagrant up` is done, you will SSH into the Vagrant environment and retrieve the Kubernetes config file used by `kubectl`. We want to copy the contents of this file into our local environment so that `kubectl` knows how to communicate with the K3s cluster.
```bash
$ vagrant ssh
```
You will now be connected inside of the virtual OS. Run `sudo cat /etc/rancher/k3s/k3s.yaml` to print out the contents of the file. You should see output similar to the one that I've shown below. Note that the output below is just for your reference: every configuration is unique and you should _NOT_ copy the output I have below.

Copy the contents from the output issued from your own command into your clipboard -- we will be pasting it somewhere soon!
```bash
$ sudo cat /etc/rancher/k3s/k3s.yaml

apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUJWekNCL3FBREFnRUNBZ0VBTUFvR0NDcUdTTTQ5QkFNQ01DTXhJVEFmQmdOVkJBTU1HR3N6Y3kxelpYSjIKWlhJdFkyRkFNVFU1T1RrNE9EYzFNekFlRncweU1EQTVNVE13T1RFNU1UTmFGdzB6TURBNU1URXdPVEU1TVROYQpNQ014SVRBZkJnTlZCQU1NR0dzemN5MXpaWEoyWlhJdFkyRkFNVFU1T1RrNE9EYzFNekJaTUJNR0J5cUdTTTQ5CkFnRUdDQ3FHU000OUF3RUhBMElBQk9rc2IvV1FEVVVXczJacUlJWlF4alN2MHFseE9rZXdvRWdBMGtSN2gzZHEKUzFhRjN3L3pnZ0FNNEZNOU1jbFBSMW1sNXZINUVsZUFOV0VTQWRZUnhJeWpJekFoTUE0R0ExVWREd0VCL3dRRQpBd0lDcERBUEJnTlZIUk1CQWY4RUJUQURBUUgvTUFvR0NDcUdTTTQ5QkFNQ0EwZ0FNRVVDSVFERjczbWZ4YXBwCmZNS2RnMTF1dCswd3BXcWQvMk5pWE9HL0RvZUo0SnpOYlFJZ1JPcnlvRXMrMnFKUkZ5WC8xQmIydnoyZXpwOHkKZ1dKMkxNYUxrMGJzNXcwPQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg==
    server: https://127.0.0.1:6443
  name: default
contexts:
- context:
    cluster: default
    user: default
  name: default
current-context: default
kind: Config
preferences: {}
users:
- name: default
  user:
    password: 485084ed2cc05d84494d5893160836c9
    username: admin
```
Type `exit` to exit the virtual OS and you will find yourself back in your computer's session. Create the file (or replace if it already exists) `~/.kube/config` and paste the contents of the `k3s.yaml` output here.

Afterwards, you can test that `kubectl` works by running a command like `kubectl describe services`. It should not return any errors.


### Run these commands to Deploy the apps to Kubernetes:

1. `kubectl apply -f deployment/db-configmap.yaml` - Set up environment variables for the pods
2. `kubectl apply -f deployment/db-secret.yaml` - Set up secrets for the pods
3. `kubectl apply -f deployment/postgres.yaml` - Set up a Postgres database running PostGIS
4. `kubectl apply -f deployment/udaconnect-api-connections.yaml` - Set up the service and deployment for the connections app API
5. `kubectl apply -f deployment/udaconnect-api-locations.yaml` - Set up the service and deployment for the locations app API
6. `kubectl apply -f deployment/udaconnect-api-persons.yaml` - Set up the service and deployment for the persons app API
7. `kubectl apply -f deployment/udaconnect-api-grpc-persons.yaml` - Set up the service and deployment for the persons grpc 
8. `kubectl apply -f deployment/udaconnect-app.yaml` - Set up 
the service and deployment for the web app
9. `kubectl apply -f deployment/kafka.yaml` - Set up the service and deployment for kafka and zookeeper
10. `sh scripts/run_db_command.sh <POD_NAME>` - Seed your database against the `postgres` pod. (`kubectl get pods` will give you the `POD_NAME`)

Note: Manually applying each of the individual `yaml` files is cumbersome but going through each step provides some context on the content of the project. In practice, we would have reduced the number of steps by running the command against a directory to apply of the contents: `kubectl apply -f deployment/`.

Note: The first time you run this project, you will need to seed the database with dummy data. Use the command `sh scripts/run_db_command.sh <POD_NAME>` against the `postgres` pod. (`kubectl get pods` will give you the `POD_NAME`). Subsequent runs of `kubectl apply` for making changes to deployments or services shouldn't require you to seed the database again!

### Verifying it Works
Once the project is up and running, you should be able to see deployments and  services in Kubernetes:
`kubectl get pods` and `kubectl get services` - should both return `udaconnect-app`, `udaconnect-api-persons`, `udaconnect-api-locations` , `udaconnect-grpc-persons`, `udaconnect-api-persons`, `kafka-0` , `kafka-zookeeper` and `postgres`

This page will load on the frontend app your web browser in which will call all persons end point from the api-persons app and the connection endpoint from api-connection app:

* `http://localhost:30000/` - Frontend ReactJS Application

### Project directories 
1. udaconnect/db - Database 
2. udaconnect/deployment - All deployment yaml files
3. udaconnect/docs - All screenshots, required text files for design decisions and yaml files for manually written OpenAPI spec 
4. udaconnect/modules - individual apps that were deployed to kubernetes.
5. udaconnect/scripts - Useful scripts to fill the database with dummy data. 


### Steps to test  Kafka Broker to consume from items topic

- a producer was implemented in the code of the locations api to produce and save  messages in the Kafka broker whenever you make an api endpoint call `/locations`. 
- a consumer was also implemented to consume data from kafka and save it to location db, hint, Errors could happed due to dummy data primary key, keep on requesting till you pass to the right auto generated location_id primary key.
- first you need to run kafka-zookeeper `kubectl port-forward kafka-zookeeper-0 2181:2181` Start port-forwarding kafka-zookeeper first and run kafka by port-forwarding `kubectl port-forward kafka-0 9092:9092`