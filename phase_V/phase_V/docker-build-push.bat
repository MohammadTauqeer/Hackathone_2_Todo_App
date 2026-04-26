@echo off
setlocal enabledelayedexpansion

REM Docker build and push script for Windows
REM Replace 'yourusername' with your actual Docker Hub username

set "DOCKER_USERNAME=yourusername"

REM Check if Docker username is provided as an argument
if not "%1"=="" (
    set "DOCKER_USERNAME=%1"
)

REM Check if Docker username is still default
if "%DOCKER_USERNAME%"=="yourusername" (
    echo ERROR: Please replace 'yourusername' with your actual Docker Hub username.
    echo Usage: docker-build-push.bat ^[your-docker-username^]
    echo Or edit this script to set the DOCKER_USERNAME variable.
    exit /b 1
)

echo Using Docker Hub username: %DOCKER_USERNAME%

REM Backend image details
set "BACKEND_IMAGE_NAME=%DOCKER_USERNAME%/phasev-backend"
set "BACKEND_TAG=latest"

REM Frontend image details
set "FRONTEND_IMAGE_NAME=%DOCKER_USERNAME%/phasev-frontend"
set "FRONTEND_TAG=latest"

REM Build backend image
echo Building backend image...
cd backend
docker build -t !BACKEND_IMAGE_NAME!:!BACKEND_TAG! .
if !errorlevel! neq 0 (
    echo Error building backend image
    exit /b 1
)
echo Backend image built successfully

REM Return to root directory
cd ..

REM Build frontend image
echo Building frontend image...
cd frontend
docker build -t !FRONTEND_IMAGE_NAME!:!FRONTEND_TAG! .
if !errorlevel! neq 0 (
    echo Error building frontend image
    exit /b 1
)
echo Frontend image built successfully

REM Return to root directory
cd ..

REM Log in to Docker Hub
echo Logging in to Docker Hub...
docker login
if !errorlevel! neq 0 (
    echo Error logging in to Docker Hub
    exit /b 1
)

REM Push backend image
echo Pushing backend image...
docker push !BACKEND_IMAGE_NAME!:!BACKEND_TAG!
if !errorlevel! neq 0 (
    echo Error pushing backend image
    exit /b 1
)
echo Backend image pushed successfully

REM Push frontend image
echo Pushing frontend image...
docker push !FRONTEND_IMAGE_NAME!:!FRONTEND_TAG!
if !errorlevel! neq 0 (
    echo Error pushing frontend image
    exit /b 1
)
echo Frontend image pushed successfully

echo All images built and pushed successfully!
echo Backend image: !BACKEND_IMAGE_NAME!:!BACKEND_TAG!
echo Frontend image: !FRONTEND_IMAGE_NAME!:!FRONTEND_TAG!

endlocal