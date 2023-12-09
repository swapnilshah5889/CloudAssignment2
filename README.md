# Docker Image for Cloud Assignment 2 - Wine Prediction System

[![Docker Hub](https://img.shields.io/docker/pulls/swapnilshah5889/cloud-assignment-2.svg)](https://hub.docker.com/repository/docker/swapnilshah5889/cloud-assignment-2)

This repository contains the Docker image for Cloud Assignment 2. You can pull the image from Docker Hub using the following command:

# Table of Contents

- [Setup AWS Cluster for Training the Model](#setup-aws-cluster-for-training-the-model)
  - [Setup of EMR on AWS](#setup-of-emr-on-aws)
    - [1. Go to EC2 -> Create Cluster](#1-go-to-ec2---create-cluster)
    - [2. Give cluster name](#2-give-cluster-name)
    - [3. Select Amazon EMR release -> emr-6.15.0](#3-select-amazon-emr-release---emr-6150)
    - [4. Click Cluster Configuration -> Add an instance group to add one more instance to create a 4 cluster group](#4-click-cluster-configuration---add-an-instance-group-to-add-one-more-instance-to-create-a-4-cluster-group)
    - [5. Security configuration and EC2 key pair -> Add Amazon EC2 key pair for SSH to the cluster](#5-security-configuration-and-ec2-key-pair---add-amazon-ec2-key-pair-for-ssh-to-the-cluster)
    - [6. Select Role](#6-select-role)
    - [7. Create Cluster](#7-create-cluster)
  - [Connect to EMR Instance](#connect-to-emr-instance)
    - [1. Connect to SSH Server](#1-connect-to-ssh-server)
    - [2. Installing Apache Spark on Ubuntu](#2-installing-apache-spark-on-ubuntu)
    - [3. Installing AWS CLI on Ubuntu](#3-installing-aws-cli-on-ubuntu)
- [Setup of Prediction Application on EC2 Instance on AWS](#setup-of-prediction-application-on-ec2-instance-on-aws)
  - [1. Go to EC2](#1-go-to-ec2)
  - [2. Click on Launch Instance](#2-click-on-launch-instance)
  - [3. Use the steps provided below the image](#3-use-the-steps-provided-below-the-image)
  - [4. Once done, you can now connect with the SSH command](#4-once-done-you-can-now-connect-with-the-ssh-command)
    - [SSH Command](#ssh-command)
    - [Install Java](#install-java)
    - [Install AWS-CLI](#install-aws-cli)
    - [Configure AWS CLI](#configure-aws-cli)
    - [Install Hadoop](#install-hadoop)
    - [Install Spark](#install-spark)
    - [Setup Python in AWS EC2](#setup-python-in-aws-ec2)
- [Docker Image for Cloud Assignment 2](#docker-image-for-cloud-assignment-2-1)
  - [Build Docker Image](#build-docker-image)
  - [Run Docker Container](#run-docker-container)
  - [Build Docker Image](#build-docker-image-1)
  - [Login to Docker Hub](#login-to-docker-hub)
  - [Tag the Image](#tag-the-image)
  - [Push the Image](#push-the-image)


# Setup AWS Cluster for training the model

## Setup of EMR on AWS

### 1. Go to EC2 -> Create Cluster

### 2. Give cluster name

### 3. Select Amazon EMR release -> emr-6.15.0

### 4. Click Cluster Configuration -> Add an instance group to add one more instance to create a 4 cluster group

### 5. Security configuration and EC2 key pair -> Add Amazon EC2 key pair for SSH to the cluster

### 6. Select Role
   - Amazon EMR service role: EMR_DefaultRole
   - EC2 instance profile for Amazon EMR: EMR_DefaultRole

### 7. Create Cluster

Once the cluster is created, go to the security of EC2 instances and open port 22 and custom IP Address.

## Connect to EMR Instance

### 1. Connect to SSH Server

```bash
ssh -i "CS643-Cloud.pem" hadoop@ec2-3-92-224-244.compute-1.amazonaws.com
```

### 2. Installing Apache Spark on Ubuntu

#### Overview
This guide will walk you through the steps to install Apache Spark on Ubuntu using the standard package manager `apt`.

#### Prerequisites
- Ubuntu operating system
- sudo privileges

#### Installation Steps

#### 2.1: Update Package List
Ensure that your package list is up-to-date:
```bash
sudo apt update
```

#### 2.2: Install Java Development Kit (JDK)
Apache Spark requires Java. Install OpenJDK 8 or later:
```bash
sudo apt install openjdk-8-jdk
```

#### 2.3: Download Apache Spark
Visit the Apache Spark Downloads page and copy the link to the latest pre-built version. Replace <version> with the actual version number.
```bash
wget https://archive.apache.org/dist/spark/spark-<version>/spark-<version>-bin-hadoop2.7.tgz
```

#### 2.4: Extract Spark Archive
Extract the downloaded archive:
```bash
tar -xvzf spark-<version>-bin-hadoop2.7.tgz
```

#### 2.5: Move Spark to /opt
Move the extracted Spark directory to the /opt directory (you may need sudo):
```bash
sudo mv spark-<version>-bin-hadoop2.7 /opt/spark
```

#### 2.6: Configure Environment Variables
Add Spark's binaries to the PATH and set the SPARK_HOME variable. Open your shell configuration file (e.g., ~/.bashrc or ~/.zshrc) and add the following lines:
```bash
export SPARK_HOME=/opt/spark
export PATH=$PATH:$SPARK_HOME/bin
export PYSPARK_PYTHON=python3
```
Source the updated configuration:
```bash
source ~/.bashrc
```

#### 2.7: Verify Installation
Run the following command to check if Spark is installed successfully:
```bash
spark-shell
```
#### 2.8 Set Environment Variables

To properly configure your environment for Apache Spark and Hadoop, add the following lines to your shell configuration file. Depending on your shell, this file may be `.bash_profile`, `.zshrc`, or another relevant file. Open the file in a text editor and add the following lines:

```bash
export SPARK_HOME=/usr/local/opt/apache-spark/libexec
export HADOOP_HOME=/usr/local/opt/hadoop
```

### 3. Installing AWS CLI on Ubuntu

#### 3.1. Overview
This guide will walk you through the steps to install the AWS Command Line Interface (AWS CLI) on Ubuntu.

#### 3.2. Prerequisites
- Ubuntu operating system
- sudo privileges
- 
#### 3.3: Update Package List
Ensure that your package list is up-to-date:

```bash
sudo apt update
```
#### 3.4: Install AWS CLI
Install the AWS CLI using the package manager:
```bash
sudo apt install awscli
```

#### 3.5: Verify Installation
After the installation is complete, you can verify it by checking the AWS CLI version:
```bash
aws --version
```

#### 3.6: Configure AWS CLI
To use AWS CLI, you need to configure it with your AWS credentials. Run the following command and follow the prompts:
```bash
aws configure
```

### 4. Copy the file from local to EMR Instance
Exit from the EMR instance and use the below command:
```bash
scp -i CS643-Cloud.pem ~/Desktop/ProgrammingAssignment2-main/training.py ubuntu@ec2-34-207-132-95.compute-1.amazonaws.com:~/trainingModel
```
Reconnect to the server using the SSH command.

### 5. Create a Virtual Environment
Navigate to your project folder and create a virtual environment (replace "venv" with your preferred name):
```bash
python -m venv venv
```

### 6. Activate the Virtual Environment
```bash
source venv/bin/activate
```

### 7. Install Project Dependencies
```bash
pip install -r requirements.txt
```

### 8. Execute the command
```bash
spark-submit --packages org.apache.hadoop:hadoop-aws:3.2.2 training.py
```

# Setup of Prediction Application on EC2 Instance on AWS

1. Go to EC2
2. Click on Launch Instance
3. Use the steps provided below the image

Once done, you can now connect with the SSH command:

### SSH Command
```bash
ssh -i your-key.pem ec2-user@your-instance-ip
```

### Install Java

### Install AWS-CLI

### Configure AWS CLI

### Install Hadoop

### Install Spark

### Setup Python in AWS EC2

Python Environment Setup
This document provides instructions on setting up the Python environment for this project.

Install Python
Download and install the latest version of Python from python.org.

Install virtualenv
If you don't have virtualenv installed, run the following command:

```bash
pip install virtualenv
```

Create a Virtual Environment
Navigate to your project folder and create a virtual environment (replace "venv" with your preferred name):
```bash
python -m venv venv
```

Activate the Virtual Environment
```bash
source venv/bin/activate
```

Install Project Dependencies
```bash
source venv/bin/activate
```

Execute the command
```bash
spark-submit --packages org.apache.hadoop:hadoop-aws:3.2.2 predict.py
```

# Docker Image for Cloud Assignment 2

This Dockerfile sets up an environment for Cloud Assignment 2, including Python, Java, Spark, and Hadoop.

## Build Docker Image

To build the Docker image, navigate to the directory containing the Dockerfile and run:

```bash
docker build -t cloud-assignment-2 .
```

### Run Docker Container
After building the image, you can run a Docker container with the following command:
```bash
docker run -it cloud-assignment-2
```

### Build Docker Image
To build the Docker image, use the following command in the directory containing your Dockerfile:

```bash
docker build -t your-dockerhub-username/cloud-assignment-2:latest .
```

### Login to Docker Hub
```bash
Login to Docker Hub
```

### Tag the Image
```bash
docker tag your-dockerhub-username/cloud-assignment-2:latest your-dockerhub-username/cloud-assignment-2:version-tag
```
Replace version-tag with the desired version or tag for your Docker image.

### Push the Image
```bash
docker push your-dockerhub-username/cloud-assignment-2:version-tag
```

