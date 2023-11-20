# 2-Tier Web Application in Managed K8s Cluster with Amazon EKS

2-tier web app by configuring dynamic background image locations through a ConfigMap linked to private S3 buckets. Integrated with Kubernetes, the solution involved passing MySQL DB credentials as secrets and adding a custom header via Environment variable using Flask. Dockerized and locally tested in Cloud9, the app is stored on GitHub with GitHub Actions automating builds and publishing to Amazon ECR upon successful tests and establishing an Amazon EKS cluster, deploying Kubernetes resources like ConfigMap, Secret, PersistentVolumeClaim, ServiceAccount, K8s role, MySQL DB, Flask app, and services.

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
