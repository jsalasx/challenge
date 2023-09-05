# Desafío de ingeniero de software (ML y LLM)

## Descripción general

Bienvenidos al despliego del predictor de retraso en vuelos

## Requerimientos 
    1. Python 3.9
    2. Docker
    3. Kubernetes

## Pasos para el despliegue
### Todo ejecutar en la carpeta o directorio raiz del proyecto

1. Crear la imagen de docker del proyecto, si adiciona alguna libreria incluirla en requirement.txt


    ```docker build -t fastapi .```

2. Crear un Cluster de Kubernetes en Google Cloud GKE. puede guiarse en este tutorial
    [Guia GKE](https://cloud.google.com/kubernetes-engine/docs/how-to/creating-a-regional-cluster?hl=es-419)

3. Crear un contenedor de imagenes ('Artifact Registry')
    [Guia Artifact Registry](https://cloud.google.com/artifact-registry?hl=es-419)

4. Autenticarse en Google Console.

5. Tagear la imagen de docker.
    '''
    docker tag fastapi us-east1-docker.pkg.dev/clusterla/latamimages/fastapi:latest
    '''

6. Subirla al Artifact Registry
    '''
    docker tag fastapi us-east1-docker.pkg.dev/clusterla/latamimages/fastapi:latest
    '''

7. Crear el namespace en Kubernetes
    kubectl apply -f namespace.yml
8. Crear el deployment en Kubernetes
    kubectl apply -f deployment.yml

9. Crear el service en Kubernetes
    kubectl apply -f service.yml

10. Verificar la ip publica que tiene el servicio.  (EXTERNAL-IP)
    kubectñ get services mi-aplicacion-servicio -n latamairlines






