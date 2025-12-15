# 🐳 Docker Quick Start - NestWorth

## ⚡ Fastest Way to Run NestWorth

Just **one command** to start everything:

```bash
docker-compose up --build
```

That's it! 🎉

---

## 📍 What Just Happened?

1. ✅ Built NestWorth API Docker image (~500 MB)
2. ✅ Started PostgreSQL database
3. ✅ Initialized database tables automatically
4. ✅ Started API server on http://localhost:8000

---

## 🌐 Access the Application

Open in your browser:

- **Interactive API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Root Info**: http://localhost:8000/

---

## 🎮 Try It Out

### Using the Browser (Easiest)

1. Go to http://localhost:8000/docs
2. Click on `POST /blueprint`
3. Click **"Try it out"**
4. Click **"Execute"**
5. See your baby budget blueprint! 📊

### Using curl

```bash
curl -X POST "http://localhost:8000/blueprint" \
  -H "Content-Type: application/json" \
  -d '{
    "partner_1_monthly_income": 6000,
    "partner_2_monthly_income": 5000,
    "current_savings": 15000,
    "monthly_housing_cost": 2500,
    "zip": 94107,
    "due_date": "2025-08-01",
    "childcare_preference": "center",
    "partner_1_leave_duration_weeks": 12,
    "partner_1_leave_percent_paid": 100,
    "partner_2_leave_duration_weeks": 8,
    "partner_2_leave_percent_paid": 80
  }' | python -m json.tool
```

---

## 🛠️ Common Commands

### Stop the Application
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f
```

### Restart Everything
```bash
docker-compose restart
```

### Start Fresh (Delete All Data)
```bash
docker-compose down -v
docker-compose up --build
```

### Run Tests
```bash
docker-compose exec nestworth-api pytest -v
```

### Open Shell in Container
```bash
docker-compose exec nestworth-api bash
```

---

## 🚀 Using Make Commands (Even Easier!)

If you have `make` installed:

```bash
# Show all available commands
make help

# Start everything
make up

# View logs
make logs

# Run tests
make test

# Stop everything
make down

# Fresh start
make rebuild
```

---

## 📦 What's Running?

Check container status:
```bash
docker-compose ps
```

You should see:
- `nestworth-api` - The API server
- `nestworth-postgres` - PostgreSQL database

---

## 🐛 Troubleshooting

### Port 8000 Already in Use?

**Option 1**: Stop what's using it
```bash
lsof -i :8000
kill <PID>
```

**Option 2**: Change the port in `docker-compose.yml`
```yaml
ports:
  - "8001:8000"  # Change 8001 to any free port
```

### Container Won't Start?

View the logs:
```bash
docker-compose logs nestworth-api
```

### Database Connection Issues?

Check PostgreSQL:
```bash
docker-compose logs postgres
docker-compose ps postgres
```

### Start Completely Fresh

```bash
# Remove everything
docker-compose down -v
docker system prune -f

# Rebuild
docker-compose up --build
```

---

## 📊 What You Can Do Now

✅ Generate personalized baby budget blueprints
✅ Test different financial scenarios
✅ Explore 3 childcare options (center/home/stay-at-home)
✅ Get smart financial warnings
✅ See 5-year cashflow projections
✅ API is production-ready!

---

## 🎯 Next Steps

1. **Try different scenarios** - Change income, ZIP codes, childcare options
2. **Check the PDFs** - Generated PDFs are in `./pdfs/` folder
3. **Run tests** - `docker-compose exec nestworth-api pytest`
4. **Deploy to cloud** - Use the Docker image on AWS/GCP/Azure
5. **Build a frontend** - Use the API to create a web UI

---

**Need more details?** See `DOCKER.md` for the complete guide.

**Happy budget planning! 🏡👶**
