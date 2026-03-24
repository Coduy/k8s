# Minikube Useful Commands

## 1. Start Minikube
To start a local Kubernetes cluster with Minikube:

```bash
minikube start
```

You can specify the Kubernetes version and driver, for example
```bash
minikube start --kubernetes-version=v1.21.0 --driver=docker
```

## 2. Check status
```bash
minikube status
```

## 3. Run minikube Dashboard
To open the Kubernetes Dashboard in your browser:

```bash
minikube dashboard
```

## 4. Gest Cluster Info
To open the Kubernetes Dashboard in your browser:

```bash
kubectl cluster-info
```

## 5. Get minikube nodes
To get detailed information about the Minikube node:

```bash
minikube node list
```

## 7. Deploy a simple pod 

```bash
kubectl apply -f tomcat-deploy.yaml
```


## 8. Expose the Deployment as a Service

```bash
kubectl expose deployment tomcat-deployment --type=NodePort --port=8080
```

##  9: Verify Deployment and Pods

Open a new terminal tab and run:
```bash
kubectl port-forward pod/tomcat-deployment-XXXXX-XXXXX 8080:8080
```

##  10: Verify Deployment and Pods

```bash
kubectl get deployments
kubectl get pods
kubectl get services
```