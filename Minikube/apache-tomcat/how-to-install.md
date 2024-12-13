# Create a simple WAR based Tomcat App

This guide will help you install Minikube on Docker Desktop for Windows and set up a local Kubernetes cluster.


## Step 1: Creat a simple deployment file


```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tomcat-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: tomcat
  template:
    metadata:
      labels:
        app: tomcat
    spec:
      containers:
      - name: tomcat
        image: tomcat:9.0
        ports:
        - containerPort: 8080


```
## Step 2: Download a sample 

On Windows, via curl:

```bash
curl -o sample.war https://tomcat.apache.org/tomcat-9.0-doc/appdev/sample/sample.war
```

## Step 3: Add mounting to the deployment file:


```bash
        volumeMounts:
        - name: tomcat-root
          mountPath: /usr/local/tomcat/webapps/ROOT.war
          subPath: sample.war
      volumes:
      - name: tomcat-root
        configMap:
          name: tomcat-root
```

The full deployment file: 

```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tomcat-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: tomcat
  template:
    metadata:
      labels:
        app: tomcat
    spec:
      containers:
      - name: tomcat
        image: tomcat:9.0
        ports:
        - containerPort: 8080
        volumeMounts:
        - name: tomcat-root
          mountPath: /usr/local/tomcat/webapps/ROOT.war
          subPath: sample.war
      volumes:
      - name: tomcat-root
        configMap:
          name: tomcat-root
```

## Step 4: Redeploy the deployment file:

On Windows, via curl:

```bash
kubectl apply -f tomcat-deploy.yaml
```

## Step 5: Create a port forward using a new pod name

On Windows, via curl:

```bash
kubectl get pods
kubectl port-forward pod/tomcat-deployment-XXXXX-XXXXX 8080:8080
```


## Step 6: Test it out in a browser
```bash
localhost:8080
```