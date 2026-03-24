# Helm installation on Windows

## Step 1: Download Helm binaries from [text](../how-to-install.md)

1. Copy the folder path where the helm.exe file is located and add it to the SYSTEM $PATH env var on Windows. 
2. Restart terminal and run helm command to confirm it's working fine.  

## Step 1: Create a new Helm skeleton 

```bash
helm create nginx. 
```

## Step 2: Edit values.yaml 

Edit values as you wish. 



## To remove a release:

```bash
helm list
helm uninstall <release-name>
```

## To reinstall a helm release:

```bash
helm list

helm upgrade <release-name> <chart-name> -n <namespace> -f values.yaml
```
