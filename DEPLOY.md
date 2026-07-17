#!/bin/bash

echo "🚀 Quick Deployment Guide"
echo "=========================="

echo ""
echo "1️⃣ LOCAL TESTING"
echo "   pip install -r requirements.txt"
echo "   python app.py"
echo "   Visit: http://localhost:5000"

echo ""
echo "2️⃣ DOCKER (Local)"
echo "   docker build -t football-simulator ."
echo "   docker run -p 5000:5000 football-simulator"
echo "   Visit: http://localhost:5000"

echo ""
echo "3️⃣ DOCKER COMPOSE"
echo "   docker-compose up"
echo "   Visit: http://localhost"

echo ""
echo "4️⃣ HEROKU (Paid)"
echo "   heroku login"
echo "   heroku create football-simulator-YOUR-NAME"
echo "   git push heroku main"
echo "   heroku open"

echo ""
echo "5️⃣ AWS EC2 (Ubuntu/Amazon Linux)"
echo "   # SSH into instance first:"
echo "   ssh -i key.pem ec2-user@IP"
echo "   # Then run:"
echo "   curl https://raw.githubusercontent.com/wop27812-creator/Python-/main/deploy-ec2.sh | bash"

echo ""
echo "6️⃣ GOOGLE CLOUD RUN"
echo "   gcloud run deploy football-simulator --source . --region us-central1"

echo ""
echo "7️⃣ AZURE APP SERVICE"
echo "   az webapp up --name football-simulator --runtime python:3.11"

echo ""
echo "8️⃣ GITHUB PAGES (Static Site)"
echo "   Create docs folder with index.html"
echo "   Settings → Pages → Source: main /docs"