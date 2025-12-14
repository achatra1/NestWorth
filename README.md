# 🏡 NestWorth

**A calm, trustworthy financial clarity tool for families**

NestWorth is an AI-powered baby budget planner that generates personalized 5-year financial plans ("Baby Budget Blueprint") for new parents. Get clarity on baby-related costs with empathetic, data-driven insights—without the financial jargon.

---

## 🌟 Features

- **📊 5-Year Financial Projections**: Month-by-month cashflow simulations for the first 5 years
- **👶 Personalized Baby Budgets**: Tailored to your income, location, and childcare preferences
- **⚠️ Smart Warnings**: Proactive alerts for potential financial challenges
- **📄 Beautiful PDF Reports**: Professional, empathetic reports you can share with your partner
- **🔒 Privacy-First**: Your financial data stays secure and private
- **🧮 Deterministic Calculators**: Pure Python calculations with versioned assumptions
- **🌐 REST API**: FastAPI-powered backend with OpenAPI documentation

---

## 🏗️ Architecture

NestWorth follows a clean, modular architecture:

```
NestWorth/
├── apps/api/              # FastAPI server
│   └── main.py           # API endpoints
├── packages/
│   ├── domain/           # Data models (Pydantic + SQLAlchemy)
│   │   ├── models.py     # Pydantic schemas
│   │   └── db.py         # Database models
│   ├── calculators/      # Business logic
│   │   ├── assumptions_loader.py
│   │   ├── baby_plan.py
│   │   ├── budget_split.py
│   │   └── generator.py
│   ├── assumptions/      # Versioned cost data (JSON)
│   │   ├── center_assumptions_v1.json
│   │   ├── home_assumptions_v1.json
│   │   └── stay_home_assumptions_v1.json
│   ├── pdf/              # PDF generation
│   │   ├── report_generator.py
│   │   └── templates/
│   │       └── blueprint_report.html
│   └── tests/            # Pytest tests
│       ├── test_calculators_unit.py
│       └── test_blueprint_against_example.py
├── pdfs/                 # Generated PDF reports
├── requirements.txt      # Python dependencies
├── docker-compose.yml    # PostgreSQL setup
└── init_db.py           # Database initialization
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL 15+ (or use Docker Compose)
- (Optional) Docker & Docker Compose

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd NestWorth

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start PostgreSQL

**Option A: Using Docker Compose (Recommended)**

```bash
docker-compose up -d
```

**Option B: Use your own PostgreSQL**

Create a database named `nestworth` and update `.env` with your credentials.

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env if needed (default settings work with docker-compose)
```

### 4. Initialize Database

```bash
python init_db.py
```

### 5. Start the API Server

```bash
uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Test the API

Visit:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Demo Blueprint**: http://localhost:8000/blueprint/demo

---

## 📖 API Usage

### Generate a Blueprint

**POST** `/blueprint`

```bash
curl -X POST "http://localhost:8000/blueprint" \
  -H "Content-Type: application/json" \
  -d '{
    "partner_1_monthly_income": 5000,
    "partner_2_monthly_income": 4500,
    "current_savings": 10000,
    "monthly_housing_cost": 2000,
    "zip": 94107,
    "due_date": "2025-06-01",
    "childcare_preference": "center",
    "partner_1_leave_duration_weeks": 12,
    "partner_1_leave_percent_paid": 80,
    "partner_2_leave_duration_weeks": 6,
    "partner_2_leave_percent_paid": 100
  }'
```

**Response:**
```json
{
  "profile": {...},
  "assumptions_version": "v1.0",
  "calculator_version": "v1.0",
  "five_year_projection": [...],
  "cashflow_projection": [...],
  "budget_split": {
    "housing_percent": 21.1,
    "childcare_percent": 25.3,
    "baby_needs_percent": 3.1,
    "remaining_percent": 50.5,
    "monthly_baby_cost": 2690,
    "total_five_year_baby_cost": 147890
  },
  "warnings": ["CHILDCARE_HIGH"],
  "report_sections": [...],
  "pdf_url": "/path/to/generated.pdf"
}
```

### Childcare Preferences

- **`center`**: Daycare centers (higher cost, varies by region)
- **`home`**: In-home nanny or family care (moderate cost)
- **`stay_home`**: One parent stays home (zero childcare cost, one income)

### Warning Codes

- `HOUSING_HIGH`: Housing costs >30% of income
- `CHILDCARE_HIGH`: Childcare costs >30% of income
- `CHILDCARE_UNSUSTAINABLE`: Childcare costs >80% of income
- `NEGATIVE_CASHFLOW`: Some months have expenses > income
- `LOW_SAVINGS`: Current savings may be exhausted

---

## 🧪 Testing

### Run All Tests

```bash
pytest
```

### Run Specific Tests

```bash
# Unit tests only
pytest packages/tests/test_calculators_unit.py -v

# Golden tests (requires Example.xlsx)
pytest packages/tests/test_blueprint_against_example.py -v
```

### Test Coverage

```bash
pytest --cov=packages --cov-report=html
```

---

## 🎨 How It Works

### 1. **Deterministic Calculators**

All calculations are pure Python (no NumPy) and deterministic:
- Month-by-month income and expense simulation
- Parental leave income reductions
- Childcare cost schedules (starting after leave period)
- One-time costs (baby gear, medical)
- Recurring costs (diapers, formula, etc.)
- Inflation adjustments by year

### 2. **Versioned Assumptions**

Cost data is stored in JSON files by childcare preference:
- `center_assumptions_v1.json`: Daycare center costs
- `home_assumptions_v1.json`: In-home care costs
- `stay_home_assumptions_v1.json`: Stay-at-home parent

Each file includes:
- One-time costs (crib, stroller, car seat, etc.)
- Monthly recurring costs (diapers, formula, wipes)
- Regional childcare costs (Low/Medium/High bands)
- Cost adjustment factors by year
- Version tracking for reproducibility

### 3. **Regional Cost Bands**

ZIP codes are mapped to cost bands:
- **High**: San Francisco (94107), Boston (02101), NYC (10001), etc.
- **Medium**: Atlanta (30301), Dallas (75201), Denver (80201), etc.
- **Low**: Rural areas (36052, 68001, etc.)

### 4. **PDF Report Generation**

- **Jinja2 templates** render HTML from blueprint data
- **WeasyPrint** converts HTML to professional PDFs
- Empathetic, non-advisory tone
- Includes all sections: Overview, Arrival Costs, Year-by-Year, Warnings, Assumptions

---

## 🗄️ Database Schema

### `blueprints` Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `user_profile` | JSONB | Input profile data |
| `blueprint_json` | JSONB | Full blueprint output |
| `assumptions_version` | TEXT | Version of assumptions used |
| `calculator_version` | TEXT | Version of calculator logic |
| `created_at` | TIMESTAMP | Creation timestamp |
| `warnings` | TEXT[] | List of warning codes |
| `pdf_url` | TEXT | Path to generated PDF |

---

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql+psycopg2://...` | PostgreSQL connection string |
| `API_HOST` | `0.0.0.0` | API server host |
| `API_PORT` | `8000` | API server port |
| `ENVIRONMENT` | `development` | Environment name |

---

## 📊 Example Scenarios

### Scenario 1: High-Income, Urban Family
- Combined income: $15,000/month
- San Francisco ZIP (94107)
- Center-based childcare: $2,400/month
- **Result**: CHILDCARE_HIGH warning, but sustainable
- **5-year baby cost**: ~$180,000

### Scenario 2: Moderate-Income, Stay-at-Home Parent
- Combined income: $8,000/month → $5,000/month (one parent stays home)
- Medium-cost area
- Zero childcare cost
- **Result**: No major warnings if savings adequate
- **5-year baby cost**: ~$35,000 (baby needs only)

### Scenario 3: Tight Budget, High Housing
- Combined income: $5,000/month
- Housing: $2,000/month (40% of income)
- Low-cost area, center care: $800/month
- **Result**: HOUSING_HIGH warning
- **5-year baby cost**: ~$80,000

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Run tests (`pytest`)
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

---

## 🔒 Privacy & Security

- **No external API calls**: All calculations run locally
- **Data stays in your database**: No third-party data sharing
- **HTTPS recommended** for production deployments
- **Input validation**: Pydantic ensures data integrity

---

## 📝 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

Built with:
- **FastAPI** - Modern Python web framework
- **Pydantic v2** - Data validation
- **SQLAlchemy** - Database ORM
- **WeasyPrint** - PDF generation
- **Jinja2** - Template engine

---

## 📞 Support

- **Documentation**: http://localhost:8000/docs (when running)
- **Issues**: Create an issue on GitHub
- **Email**: support@nestworth.example

---

## 🗺️ Roadmap

- [ ] Frontend web app (React/Next.js)
- [ ] More regional cost data
- [ ] Tax deduction estimator
- [ ] College savings projections
- [ ] Multi-child support
- [ ] Export to CSV/Excel
- [ ] Mobile app

---

**Built with ❤️ for new parents everywhere**
