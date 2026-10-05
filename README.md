# Build & Deploy Python App with CI/CD Pipeline

🐍 Python Flask + 🐳 Docker + ⚙️ GitHub Actions + ☁️ AWS EC2

## What This Does

```
Push Code → Build Docker Image → Deploy to EC2
```

Automatic deployment. No manual SSH. No manual Docker commands.

---

## Project Structure

```
flask-cicd/
├── app/
│   └── main.py              # Flask app (10 lines)
├── .github/workflows/
│   └── ci-cd.yml            # CI/CD pipeline
├── Dockerfile               # Container config
├── requirements.txt         # Dependencies
└── README.md
```

---

## Run Locally

```bash
pip install -r requirements.txt
python app/main.py

# Open http://localhost:5000
```

---

## Run with Docker

```bash
docker build -t flask-app .
docker run -p 5000:5000 flask-app

# Open http://localhost:5000
```

---

## CI/CD Setup

### Step 1: Create EC2 Instance

- AMI: Ubuntu
- Type: t2.micro
- Security Group: Allow SSH (22) + HTTP (80)

### Step 2: Install Docker on EC2

```bash
ssh -i your-key.pem ec2-user@your-ec2-ip

sudo apt update -y
sudo curl https://get.docker.com | bash
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user
exit
```

### Step 3: Add GitHub Secrets

Go to: Repository → Settings → Secrets → Actions

| Secret | Value |
|--------|-------|
| `DOCKER_USERNAME` | Your Docker Hub username |
| `DOCKER_PASSWORD` | Your Docker Hub token |
| `EC2_HOST` | Your EC2 public IP |
| `EC2_USERNAME` | ubuntu |
| `EC2_SSH_KEY` | Contents of your .pem file |

### Step 4: Push and Deploy

```bash
git add .
git commit -m "Deploy"
git push origin main
```

🚀 Pipeline runs automatically. App goes live.

---

## Links

- [GitHub Actions Docs](https://docs.github.com/en/actions)
