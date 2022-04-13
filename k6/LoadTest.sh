# docker-compose up -d influxdb grafana
echo "   __   ____  ___   ___    ____________________"
echo "  / /  / __ \/ _ | / _ \  /_  __/ __/ __/_  __/"
echo " / /__/ /_/ / __ |/ // /   / / / _/_\ \  / /   "
echo "/____/\____/_/ |_/____/   /_/ /___/___/ /_/    "
echo "................................................"
echo "http://localhost:3000/d/k6/k6-load-testing-results"

k6 run -e FILE=${PWD}/${1} ./K6WorkloadDispatcher.js
