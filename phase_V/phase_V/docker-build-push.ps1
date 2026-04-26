# PowerShell script for Docker build and push
# Replace 'yourusername' with your actual Docker Hub username

param(
    [string]$DockerUsername = "yourusername"
)

# Check if Docker username is still default
if ($DockerUsername -eq "yourusername") {
    Write-Host "ERROR: Please provide your Docker Hub username as a parameter." -ForegroundColor Red
    Write-Host "Usage: .\docker-build-push.ps1 -DockerUsername `"your-docker-username`"" -ForegroundColor Yellow
    exit 1
}

Write-Host "Using Docker Hub username: $DockerUsername" -ForegroundColor Green

# Backend image details
$BackendImageName = "${DockerUsername}/phasev-backend"
$BackendTag = "latest"

# Frontend image details
$FrontendImageName = "${DockerUsername}/phasev-frontend"
$FrontendTag = "latest"

# Build backend image
Write-Host "Building backend image..." -ForegroundColor Cyan
Set-Location backend
docker build -t "${BackendImageName}:${BackendTag}" .
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error building backend image" -ForegroundColor Red
    exit 1
}
Write-Host "Backend image built successfully" -ForegroundColor Green

# Return to root directory
Set-Location ..

# Build frontend image
Write-Host "Building frontend image..." -ForegroundColor Cyan
Set-Location frontend
docker build -t "${FrontendImageName}:${FrontendTag}" .
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error building frontend image" -ForegroundColor Red
    exit 1
}
Write-Host "Frontend image built successfully" -ForegroundColor Green

# Return to root directory
Set-Location ..

# Log in to Docker Hub
Write-Host "Logging in to Docker Hub..." -ForegroundColor Cyan
docker login
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error logging in to Docker Hub" -ForegroundColor Red
    exit 1
}

# Push backend image
Write-Host "Pushing backend image..." -ForegroundColor Cyan
docker push "${BackendImageName}:${BackendTag}"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error pushing backend image" -ForegroundColor Red
    exit 1
}
Write-Host "Backend image pushed successfully" -ForegroundColor Green

# Push frontend image
Write-Host "Pushing frontend image..." -ForegroundColor Cyan
docker push "${FrontendImageName}:${FrontendTag}"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error pushing frontend image" -ForegroundColor Red
    exit 1
}
Write-Host "Frontend image pushed successfully" -ForegroundColor Green

Write-Host "All images built and pushed successfully!" -ForegroundColor Green
Write-Host "Backend image: ${BackendImageName}:${BackendTag}" -ForegroundColor Yellow
Write-Host "Frontend image: ${FrontendImageName}:${FrontendTag}" -ForegroundColor Yellow