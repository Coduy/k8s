# Minikube Installation on Docker Desktop for Windows

This guide will help you install Minikube on Docker Desktop for Windows and set up a local Kubernetes cluster.

## Step 1: Install Docker Desktop

Before installing Minikube, ensure Docker Desktop is installed and running on your Windows machine.

1. **Download Docker Desktop**:
   - Go to the [Docker Desktop download page](https://www.docker.com/products/docker-desktop).
   - Download the Windows version.

2. **Install Docker Desktop**:
   - Run the installer and follow the installation steps.
   - During installation, make sure **WSL 2** (Windows Subsystem for Linux 2) is enabled (Docker uses this backend for Windows).

3. **Start Docker Desktop**:
   - After installation, launch Docker Desktop and make sure it's running.

## Step 2: Install Minikub Manually

1. **Download Minikube**:
   - Go to the (https://minikube.sigs.k8s.io/docs/start/?arch=%2Fwindows%2Fx86-64%2Fstable%2F.exe+download) or search Minikube Windows Download on Google.
   - Download the **Windows** version of Minikube (e.g., `minikube-installer.exe`).

2. **Install Minikube**:
   - Run the downloaded installer and follow the instructions.

## Step 3: Start Minikube with Docker as the Driver

Now, let’s start Minikube using Docker as the driver. Minikube can be run on different driveres, in our case we use  Docker Desktop on Windows (10/11)

1. **Start Minikube**:
   - Open **Command Prompt** or **PowerShell** and run the following command:
     ```bash
     minikube start --driver=docker
     ```
   - Minikube will download the necessary Kubernetes images and start the cluster using Docker.

2. **Verify Minikube is Running**:
   - Check the status of your Minikube cluster:
     ```bash
     minikube status
     ```
   - It should show that the Minikube cluster is running.

## Step 4: Install kubectl (Kubernetes CLI)

Minikube automatically configures **kubectl**, the Kubernetes CLI tool. If you don’t have it installed yet, install it by searching it on Google. 
