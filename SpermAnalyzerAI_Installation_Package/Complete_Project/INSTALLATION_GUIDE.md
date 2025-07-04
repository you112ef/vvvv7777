# 🚀 Installation Guide - Sperm Analyzer AI

## 📋 Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **Node.js**: 16 or higher (for mobile development)
- **Android Studio**: For mobile app building
- **Docker**: For containerized deployment (optional)

### Hardware Requirements
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 5GB free space
- **GPU**: NVIDIA GPU recommended for AI processing
- **Camera**: For mobile testing

## ⚡ Quick Installation

### 1. Backend Setup
```bash
# Clone or extract project
cd SpermAnalyzerAI_Complete_Download

# Install Python dependencies
pip install -r requirements.txt

# Start the backend server
python backend/main.py

# Verify installation
curl http://localhost:8000/ping
```

### 2. Mobile App Setup
```bash
# Navigate to mobile directory
cd mobile/

# Install Node.js dependencies
npm install

# For Android development
npx react-native run-android
```

### 3. Docker Deployment (Recommended)
```bash
# Build and start all services
docker-compose up -d

# Check services
docker-compose ps

# View logs
docker-compose logs backend
```

## 🔧 Configuration

### Backend Configuration
Edit `backend/config.py` or create `.env` file:
```
HOST=0.0.0.0
PORT=8000
DEBUG=True
DATABASE_URL=sqlite:///./sperm_analyzer.db
```

### Mobile App Configuration
Edit `mobile/src/services/BackendService.ts`:
```typescript
const BASE_URL = 'http://your-server:8000';
```

## 🧪 Testing Installation

### Backend Tests
```bash
# Test API endpoints
curl -X POST http://localhost:8000/analyze \
  -F "file=@sample_video.mp4"

# Check system status
curl http://localhost:8000/status
```

### Mobile App Tests
```bash
# Run React Native tests
cd mobile/
npm test

# Build Android APK
npx react-native build-android
```

## 🚨 Troubleshooting

### Common Issues

**Python Dependencies Error**
```bash
# Update pip and reinstall
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**Mobile Build Error**
```bash
# Clean React Native cache
npx react-native start --reset-cache

# Clean Android build
cd mobile/android/
./gradlew clean
```

**Docker Issues**
```bash
# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## ✅ Verification Steps

1. **Backend Running**: Visit http://localhost:8000/docs
2. **API Working**: Upload test video via API
3. **Mobile App**: Successfully launches and connects
4. **Analysis**: Completes sample analysis
5. **Results**: Displays graphs and metrics

## 📞 Support

For installation issues:
- Check README.md for detailed documentation
- Review error logs in backend/logs/
- Verify all dependencies are installed
- Contact: youssef@spermanalyzer.ai

**Installation Complete! 🎉**
