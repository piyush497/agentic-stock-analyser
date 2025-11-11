# How to deploy locally on Windows 11

That's a frustrating error! The message: "The specified executable is not a valid application for this OS platform" usually means one of two things happened during the manual download:
    1. The download file was corrupted (incomplete).
    2. The file being downloaded was the 32-bit version, but your Windows 11 installation is 64-bit (which is standard).
Let's try a different, more robust approach using a Windows-native tool that often handles Minikube installations flawlessly: Chocolatey (choco).
If you don't have Chocolatey installed, the first step will guide you through it. If you do, skip to Step 2.

🛠️ Revised Installation Steps for Windows 11
## Step 1: Install Chocolatey (if needed)
Chocolatey is a decentralized package manager for Windows that handles installation, PATH setup, and dependency checks automatically.
    1. Open PowerShell as Administrator. (Right-click the Start button, select "Terminal (Admin)" or "Windows PowerShell (Admin)").
    2. Execute the following command to install Chocolatey. This command is safe and recommended by the Chocolatey maintainers:
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```
    
    3. Verify the installation: Close and reopen the PowerShell window (as a standard user, not Admin) and type:
```powershell
choco
```

You should see the version information.
## Step 2: Install Minikube and kubectl using Chocolatey
Now, let Chocolatey handle the installation of both tools, ensuring they are placed correctly on your PATH.
    1. In a standard (non-Admin) PowerShell window, run these two commands:
```powershell
choco install minikube -y
choco install kubernetes-cli -y
```
## Step 3: Start Minikube cluster
Once Chocolatey finishes (which may take a few minutes), your executable files will be valid and on the PATH. You can now start the cluster.
Start Docker Desktop, then run:
```powershell
minikube start --driver=docker
```

This should now successfully start a Minikube instance inside Docker Desktop.

## Step 4: Configure the Docker environment (the Minikube link)
This is the required step to allow your local docker build commands to run inside the Minikube cluster, so Kubernetes can find your local/ images.
Run this command in your PowerShell terminal:
```powershell
& minikube -p minikube docker-env | Invoke-Expression
```



## Step 5: Build and tag application images (using the Minikube Docker daemon)
Before this step, you had to run the command above to switch your shell to Minikube's Docker.

- Build Java Stock API image (from the `java-stock-api` folder):
```powershell
docker build -t local/java-stock-api:latest .
```
- Build Python Agent image (from the `pythen-agent-client` folder):
```powershell
docker build -t local/python-agent-client:latest .
```

## Step 6: Prepare the Kubernetes secret
Your Python application needs an OpenAI API Key to function. Kubernetes uses Secrets to securely store sensitive information like API keys, making sure they aren't exposed in your YAML files or logs.
Create the namespace and secret (replace with your actual key):
```powershell
kubectl apply -f k8s/namespace.yaml
kubectl create secret generic openai-secret --namespace=stock-analyser \
  --from-literal=OPENAI_API_KEY='<YOUR_OPENAI_API_KEY>'
```

    • What it does:
        ○ kubectl create secret generic: Tells Kubernetes to create a standard secret.
        ○ openai-secret: This is the name the Python Deployment YAML (python-agent-client-deployment.yaml) uses to look up the key.
        ○ --namespace=stock-analyser: Ensures the Secret is created in the correct isolated environment (Namespace).

## Step 7: Deploy Kubernetes manifests
Manifests are just your YAML configuration files. This is where you tell Kubernetes exactly what applications to run, how many copies, and how to make them talk to each other.
You must apply these in a logical order: Namespace first, then Services and Deployments.
```powershell
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/java-stock-api-service.yaml
kubectl apply -f k8s/python-agent-client-service.yaml
kubectl apply -f k8s/java-stock-api-deployment.yaml
kubectl apply -f k8s/python-agent-client-deployment.yaml
```
    • What it does:
        ○ kubectl apply -f: Reads the YAML file and sends the instructions to the Minikube control plane.
        ○ Namespace (stock-analyser): Creates the dedicated environment.
        ○ Services: Creates the internal network routes (java-stock-api and python-agent-client) that allow the two applications to communicate using easy-to-read hostnames.
        ○ Deployments: Creates the Pods (the running container instances) for your Java and Python applications, pulling the images built in Step 1.

## Step 8: Verification and access
The final steps are simply checking that everything started correctly and creating an external access point so you can use the application in your web browser.
A. Monitor status
Wait until the containers are running and healthy.
```powershell
kubectl get pods -n stock-analyser
```
You should see output indicating all your Pods (e.g., java-stock-api-... and python-agent-client-...) are in the Running state.
B. Access the app (port forwarding)
Since your Python service is defined as a ClusterIP (internal only), you need to "tunnel" traffic from your local Windows machine into the Minikube cluster using kubectl port-forward.
Important: Open a new, separate PowerShell window for this command and leave it running.
```powershell
kubectl port-forward svc/python-agent-client 8080:8000 -n stock-analyser
```
    • What it does: This command takes traffic from your Windows machine's Port 8080 and sends it to the Minikube cluster's python-agent-client service on its internal Port 8000.
C. Open the UI
Finally, open your web browser and navigate to the address:
http://localhost:8080
