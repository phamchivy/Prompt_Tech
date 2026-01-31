
source .venv/bin/activate  # Linux/Mac

# 3. Setup env
cp .env.example .env
# Edit .env: PROMETHEUS_URL=http://your-prometheus:9090

set -a && source .env && set +a

# 4. Run local
python main.py