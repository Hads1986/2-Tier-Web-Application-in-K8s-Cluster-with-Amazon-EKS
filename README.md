# 2-Tier Web Application in Managed K8s Cluster with Amazon EKS

This project deploys a 2-tiered web application in a managed Kubernetes cluster using Amazon EKS. The deployment involves utilizing secrets, config maps, and PVC for MySQL and the web application.

## Steps to Perform

1. Create the Kubernetes namespace:

    ```bash
    kubectl create ns final
    ```

2. Apply the PersistentVolumeClaim (PVC) for MySQL:

    ```bash
    kubectl apply -f mysql-pvc.yaml
    ```

3. Apply the secret for MySQL credentials:

    ```bash
    kubectl apply -f mysql-secret.yaml
    ```

4. Deploy MySQL:

    ```bash
    kubectl apply -f mysql-deployment.yaml
    ```

5. Create the MySQL service:

    ```bash
    kubectl apply -f mysql-service.yaml
    ```

6. Apply the ConfigMap for the web application:

    ```bash
    kubectl apply -f webapp-configmap.yaml
    ```

7. Deploy the web application:

    ```bash
    kubectl apply -f webapp-deployment.yaml
    ```

8. Create the service for the web application:

    ```bash
    kubectl apply -f webapp-service.yaml
    ```

## Notes

- Container images are hosted on Amazon ECR.
- Images displayed on the web portal are stored on Amazon S3.
