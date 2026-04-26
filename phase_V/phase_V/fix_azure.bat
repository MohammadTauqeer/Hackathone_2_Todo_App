@echo off
setlocal

REM Set KUBECONFIG to azure-config.yaml
set KUBECONFIG=%CD%\azure-config.yaml

echo Using KUBECONFIG: %KUBECONFIG%

echo Deleting dockerhub-secret in todo-app namespace
kubectl delete secret dockerhub-secret -n todo-app --ignore-not-found=true

REM Create Docker config with proper base64 encoding
set USERNAME=mohammadtouqeer
set TOKEN=dckr_pat_0MuA

REM For Windows, we need to handle base64 encoding differently
powershell -Command "$encoded = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes('%USERNAME%:%TOKEN%')); Write-Output $encoded" > temp_encoded.txt
set /p ENCODED_AUTH=<temp_encoded.txt

REM Create JSON with properly encoded auth
echo {"auths": {"https://index.docker.io/v1/": {"auth": "%ENCODED_AUTH%"}}} > temp_config.json

kubectl create secret dockerconfigjson dockerhub-secret ^
  --from-file=config.json=temp_config.json ^
  --namespace=todo-app

REM Clean up temp file
del temp_config.json
del temp_encoded.txt

echo Patching backend deployment with v2 image and runAsUser: 0
kubectl patch deployment backend-deployment -n todo-app -p "{\"spec\":{\"template\":{\"spec\":{\"containers\":[{\"name\":\"backend\",\"image\":\"mohammadtouqeer/todo-backend:v2\"}], \"securityContext\":{\"runAsNonRoot\": false, \"runAsUser\": 0, \"fsGroup\": 0}}}}}"

echo Patching frontend deployment with v2 image
kubectl patch deployment frontend-deployment -n todo-app -p "{\"spec\":{\"template\":{\"spec\":{\"containers\":[{\"name\":\"frontend\",\"image\":\"mohammadtouqeer/todo-frontend:v2\"}]}}}}"

echo Restarting all pods in todo-app namespace
kubectl rollout restart deployment backend-deployment -n todo-app
kubectl rollout restart deployment frontend-deployment -n todo-app

echo Waiting for deployments to be ready...
kubectl rollout status deployment/backend-deployment -n todo-app
kubectl rollout status deployment/frontend-deployment -n todo-app

echo All operations completed successfully!
pause