# 💰 Wini Flousic – Personal Finance Manager with AI Predictions

**Wini Flousic** (Tunisian dialect for *"Where's your money"*) is a full‑stack personal finance web application. It helps users track transactions, visualise spending habits, set financial goals, and get AI‑powered forecasts and insights using machine learning (linear regression).

---

## ✨ Features

- 🔐 **Authentication** – JWT‑based login & registration (Django REST + SimpleJWT)
- 💸 **Transaction Management** – Add, filter, search, and export (CSV) income/expense records
- 📊 **Interactive Dashboard** – Real‑time charts (income vs expenses, spending by category, monthly trends)
- 🎯 **Financial Goals** – Set savings targets with automatic progress tracking
- 🤖 **AI Predictions & Insights**:
  - Next month expense/income forecast (linear regression)
  - Risk score & spending anomaly detection
  - Category trends, recurring expenses detection
  - Overspending alerts & budget recommendations
- 📈 **Advanced Analytics** – Financial health score, spending heatmap, cashflow analysis, month‑over‑month comparisons
- 🎨 **Modern UI** – Dark/light theme, responsive design, smooth animations (Framer Motion, Recharts)

---

## 🛠️ Tech Stack

### Backend
- Django 5.2 + Django REST Framework
- SQLite (development) / PostgreSQL (production ready)
- Simple JWT for authentication
- scikit‑learn & numpy for ML predictions
- django‑filters, django‑cors‑headers

### Frontend
- React 19 + Vite
- Tailwind CSS (custom dark theme)
- Recharts, React Calendar Heatmap
- Framer Motion (animations)
- Axios (API client)
- React Router DOM

---

## 📁 Project Structure

```
wini-flousic/
├── backend/                  # Django project root
├── core/                 # Custom User model
├── transactions/         # Transaction CRUD + dashboard API
├── predictions/          # ML forecasts, goals, AI insights
├── financial_analytics/  # Health score, heatmap, trends
├── backend/              # Settings, URLs  
├── frontend/                 # React + Vite frontend
│   ├── src/
│   │   ├── components/       # Reusable UI parts
│   │   ├── pages/            # Dashboard, Transactions, Analytics, Predictions, Goals
│   │   ├── contexts/         # Auth & Theme providers
│   │   ├── services/         # API client
│   │   └── hooks/            # Custom hooks (pagination, toast, etc.)
│   ├── package.json
│   └── vite.config.js
├── .gitignore
├── README.md
└── start.bat                 # Windows launcher (optional)
└── manage.py
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10+ with pip
- Node.js 18+ and npm
- Git

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/wini-flousic.git
cd wini-flousic
```

### 2. Backend setup

Create and activate a virtual environment:

```bash
# Windows
python -m venv backend-env
backend-env\Scripts\activate

# macOS/Linux
python3 -m venv backend-env
source backend-env/bin/activate
```

Install dependencies:

```bash
pip install django djangorestframework django-cors-headers djangorestframework-simplejwt django-filter scikit-learn numpy python-dotenv
```

Run migrations and create superuser:

```bash
cd backend
python manage.py migrate
python manage.py createsuperuser
```

Start the Django development server:

```bash
python manage.py runserver
```

### 3. Frontend setup

Open a new terminal, navigate to the frontend folder:

```bash
cd frontend
npm install
npm run dev
```

The app will open at `http://localhost:5173` (backend runs on `http://localhost:8000`).

### 4. Environment variables (optional)

Create a `.env` file inside `backend/backend/`:

```ini
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## 📡 API Endpoints (selected)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register/` | POST | User registration |
| `/api/auth/token/` | POST | Obtain JWT tokens |
| `/api/transactions/` | GET/POST | List / create transactions |
| `/api/transactions/dashboard/` | GET | Dashboard stats (period filter) |
| `/api/transactions/export/` | GET | Export CSV |
| `/api/predictions/expense-forecast/` | GET | ML forecast + risk score |
| `/api/predictions/ai-insights/` | GET | Category trends, alerts, budget |
| `/api/predictions/goals/` | CRUD | Manage financial goals |
| `/api/analytics/health/` | GET | Financial health score |
| `/api/analytics/heatmap/` | GET | Spending heatmap data |
| `/api/analytics/forecast/` | GET | Multi‑month forecast |

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first. Please follow existing code style (PEP8 for Python, ESLint for React).

---

## 🙏 Acknowledgements

- Built as a capstone project for personal finance management
- Icons from Heroicons, charts from Recharts
- Inspired by Tunisian youth financial challenges
