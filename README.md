CLO835NBB Final Assignment
Group 7
Deployment of 2-tiered web application to managed K8s cluster on Amazon EKS

Steps to perform:

kubectl create ns finall
kubectl apply -f mysql-pvc.yaml
kubectl apply -f mysql-secret.yaml
kubectl apply -f mysql-deployment.yaml
kubectl apply -f mysql-service.yaml
kubectl apply -f webapp-configmap.yaml
kubectl apply -f webapp-deployment.yaml
kubectl apply -f webapp-service.yaml