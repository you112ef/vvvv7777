#!/bin/bash

# Sperm Analyzer AI - Environment Setup Script
# Automated setup for development environment

set -e

echo "🔧 Setting up Sperm Analyzer AI Development Environment"
echo "======================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Detect OS
OS="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    OS="windows"
fi

print_status "Detected OS: $OS"

# Step 1: Install Python dependencies for AI model
print_status "Setting up AI model environment..."

if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    print_error "Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

print_success "Python found: $($PYTHON_CMD --version)"

# Create virtual environment for AI model
cd sperm-analyzer-ai/ai-model

if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    $PYTHON_CMD -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
if [[ "$OS" == "windows" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

print_success "Python dependencies installed"

# Step 2: Create sample dataset structure
print_status "Creating dataset structure..."
mkdir -p dataset/images/train
mkdir -p dataset/images/val
mkdir -p dataset/images/test
mkdir -p dataset/labels/train
mkdir -p dataset/labels/val
mkdir -p dataset/labels/test

print_success "Dataset structure created"

# Step 3: Download YOLOv8 base model
print_status "Downloading YOLOv8 base model..."
$PYTHON_CMD -c "
from ultralytics import YOLO
model = YOLO('yolov8n.pt')
print('YOLOv8 nano model downloaded successfully')
"

print_success "YOLOv8 base model ready"

# Step 4: Setup Android app environment
print_status "Setting up Android app environment..."
cd ../android-app

# Check Node.js
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 16+ first."
    print_status "Visit: https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 16 ]; then
    print_error "Node.js version 16+ is required. Current: $(node --version)"
    exit 1
fi

print_success "Node.js $(node --version) is ready"

# Install Node.js dependencies
print_status "Installing Node.js dependencies..."
if command -v yarn &> /dev/null; then
    yarn install
else
    npm install --legacy-peer-deps
fi

print_success "Node.js dependencies installed"

# Step 5: Android SDK setup check
print_status "Checking Android development environment..."

if [ -z "$ANDROID_HOME" ]; then
    print_warning "ANDROID_HOME is not set"
    print_status "Please install Android Studio and set ANDROID_HOME environment variable"
    print_status "Common locations:"
    print_status "  Linux: ~/Android/Sdk"
    print_status "  macOS: ~/Library/Android/sdk"
    print_status "  Windows: %LOCALAPPDATA%\\Android\\Sdk"
else
    print_success "ANDROID_HOME is set: $ANDROID_HOME"
fi

# Check Java
if command -v java &> /dev/null; then
    print_success "Java is installed: $(java -version 2>&1 | head -n 1)"
else
    print_warning "Java is not installed"
    print_status "Please install JDK 11+ for Android development"
fi

# Step 6: Create development scripts
print_status "Creating development scripts..."

# Create AI model training script
cat > ../ai-model/train_model.sh << 'EOF'
#!/bin/bash
echo "🧠 Starting YOLOv8 training for sperm detection..."
source venv/bin/activate
python train.py
echo "✅ Training completed!"
EOF

chmod +x ../ai-model/train_model.sh

# Create model analysis script
cat > ../ai-model/analyze_sample.sh << 'EOF'
#!/bin/bash
if [ $# -eq 0 ]; then
    echo "Usage: $0 <image_or_video_path>"
    exit 1
fi
echo "🔍 Analyzing media: $1"
source venv/bin/activate
python analyze_media.py "$1"
EOF

chmod +x ../ai-model/analyze_sample.sh

# Create Android development script
cat > start_dev.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting React Native development server..."
npx react-native start
EOF

chmod +x start_dev.sh

# Create Android build script
cat > build_debug.sh << 'EOF'
#!/bin/bash
echo "🔨 Building debug APK..."
cd android
./gradlew assembleDebug
echo "✅ Debug APK built successfully!"
echo "📱 Location: android/app/build/outputs/apk/debug/app-debug.apk"
EOF

chmod +x build_debug.sh

print_success "Development scripts created"

# Step 7: Create project documentation
print_status "Creating project documentation..."

cat > ../DEVELOPMENT_GUIDE.md << 'EOF'
# Sperm Analyzer AI - Development Guide

## Quick Start

### 1. AI Model Development
```bash
cd sperm-analyzer-ai/ai-model
source venv/bin/activate
python train.py                    # Train the model
python analyze_media.py sample.mp4 # Test analysis
```

### 2. Android App Development
```bash
cd sperm-analyzer-ai/android-app
npm start                          # Start Metro bundler
npx react-native run-android       # Run on device/emulator
```

### 3. Build Production APK
```bash
./build_apk.sh                     # Build release APK
```

## Project Structure

```
sperm-analyzer-ai/
├── ai-model/                      # AI training and inference
│   ├── dataset/                   # Training data
│   ├── train.py                   # YOLOv8 training
│   ├── analyze_media.py           # Analysis engine
│   └── utils/casa_metrics.py      # CASA calculations
├── android-app/                   # React Native app
│   ├── src/                       # App source code
│   ├── android/                   # Android native code
│   └── package.json               # Dependencies
└── build_apk.sh                   # APK build script
```

## Development Workflow

1. **Prepare Dataset**: Add sperm images/videos to `ai-model/dataset/`
2. **Train Model**: Run `./train_model.sh` to train YOLOv8
3. **Test Analysis**: Use `./analyze_sample.sh <file>` to test
4. **Develop App**: Modify React Native code in `android-app/src/`
5. **Build APK**: Run `./build_apk.sh` for production build

## Key Features

- **Real AI Models**: YOLOv8 + DeepSORT (no simulation)
- **Offline Processing**: 100% local inference
- **CASA Metrics**: Complete sperm analysis parameters
- **Multi-language**: English and Arabic support
- **Professional UI**: Material Design components

## Requirements

- Python 3.8+ with PyTorch
- Node.js 16+ with React Native
- Android Studio with SDK 33
- JDK 11+ for Android builds

## Troubleshooting

### Model Training Issues
- Ensure dataset is properly formatted
- Check GPU availability for faster training
- Verify CUDA installation if using GPU

### Android Build Issues
- Set ANDROID_HOME environment variable
- Install required SDK platforms and build tools
- Clear cache: `cd android && ./gradlew clean`

### App Runtime Issues
- Grant camera and storage permissions
- Check model files in assets folder
- Enable USB debugging for development

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes and test thoroughly
4. Submit pull request with description

## Support

For issues and questions:
- Email: youssef@spermanalyzer.ai
- GitHub: https://github.com/youssefshtaiwi

Built with ❤️ by Youssef Shtaiwi
EOF

print_success "Development guide created"

# Step 8: Final setup summary
echo ""
echo "🎉 ENVIRONMENT SETUP COMPLETED!"
echo "==============================="
echo ""
echo "📁 Project Structure Created:"
echo "   • AI model environment with Python virtual env"
echo "   • Android app with React Native dependencies"
echo "   • Build scripts and development tools"
echo "   • Documentation and guides"
echo ""
echo "🚀 Next Steps:"
echo "   1. Prepare your sperm dataset in ai-model/dataset/"
echo "   2. Train the AI model: cd ai-model && ./train_model.sh"
echo "   3. Develop the app: cd android-app && npm start"
echo "   4. Build APK: ./build_apk.sh"
echo ""
echo "📚 Documentation:"
echo "   • Development Guide: DEVELOPMENT_GUIDE.md"
echo "   • API Documentation: In source code comments"
echo "   • Build Instructions: build_apk.sh"
echo ""
echo "🔧 Development Commands:"
echo "   • Train AI model: cd ai-model && ./train_model.sh"
echo "   • Test analysis: cd ai-model && ./analyze_sample.sh <file>"
echo "   • Start dev server: cd android-app && ./start_dev.sh"
echo "   • Build debug APK: cd android-app && ./build_debug.sh"
echo "   • Build release APK: ./build_apk.sh"
echo ""
print_success "Ready to build the future of sperm analysis! 🧬"

cd ../..
