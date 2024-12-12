kubectl get pods --no-headers | ForEach-Object { 
    if ($_.StartsWith("dag")) { 
        $podName = $_.Split(" ")[0]
        kubectl delete pod $podName 
    } 
}