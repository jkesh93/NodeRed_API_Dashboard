# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install Node-RED (if not already installed)
npm install -g node-red

# 3. Install Node-RED dependencies
cd ~/.node-red  # or %USERPROFILE%\.node-red on Windows
npm install node-red-dashboard

# 4. Start services
# Terminal 1 - Python Service
python api_manager_service.py

# Terminal 2 - Node-RED
node-red