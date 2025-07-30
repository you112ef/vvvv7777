"""
YOLOv8 Training Script for Sperm Detection
Real AI model training - no simulation
"""

import os
import torch
from ultralytics import YOLO
import yaml
from pathlib import Path

def setup_training_environment():
    """Setup training environment and check requirements"""
    print("🔧 Setting up training environment...")
    
    # Check if CUDA is available
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"🖥️  Using device: {device}")
    
    # Create necessary directories
    os.makedirs("runs", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)
    
    return device

def train_yolov8_model():
    """Train YOLOv8 model for sperm detection"""
    print("🧠 Starting YOLOv8 training for sperm detection...")
    
    # Initialize YOLOv8 model
    model = YOLO('yolov8n.pt')  # Start with nano model for mobile deployment
    
    # Training configuration
    training_config = {
        'data': 'dataset/data.yaml',
        'epochs': 100,
        'imgsz': 640,
        'batch': 8,
        'name': 'sperm-analyzer-model',
        'patience': 20,
        'save': True,
        'save_period': 10,
        'cache': False,
        'device': 'auto',
        'workers': 4,
        'project': 'runs/detect',
        'exist_ok': True,
        'pretrained': True,
        'optimizer': 'SGD',
        'verbose': True,
        'seed': 42,
        'deterministic': True,
        'single_cls': True,  # Single class detection
        'rect': False,
        'cos_lr': True,
        'close_mosaic': 10,
        'resume': False,
        'amp': True,  # Automatic Mixed Precision
        'fraction': 1.0,
        'profile': False,
        'freeze': None,
        'lr0': 0.01,
        'lrf': 0.01,
        'momentum': 0.937,
        'weight_decay': 0.0005,
        'warmup_epochs': 3.0,
        'warmup_momentum': 0.8,
        'warmup_bias_lr': 0.1,
        'box': 7.5,
        'cls': 0.5,
        'dfl': 1.5,
        'pose': 12.0,
        'kobj': 1.0,
        'label_smoothing': 0.0,
        'nbs': 64,
        'overlap_mask': True,
        'mask_ratio': 4,
        'dropout': 0.0,
        'val': True,
        'plots': True
    }
    
    # Start training
    results = model.train(**training_config)
    
    print("✅ Training completed!")
    return model, results

def export_model_for_mobile(model):
    """Export trained model for mobile deployment"""
    print("📤 Exporting model for mobile deployment...")
    
    # Export to TorchScript (recommended for mobile)
    try:
        model.export(format='torchscript', optimize=True)
        print("✅ TorchScript export successful!")
    except Exception as e:
        print(f"❌ TorchScript export failed: {e}")
    
    # Export to ONNX (alternative format)
    try:
        model.export(format='onnx', optimize=True, simplify=True)
        print("✅ ONNX export successful!")
    except Exception as e:
        print(f"❌ ONNX export failed: {e}")
    
    # Copy models to outputs directory
    model_path = "runs/detect/sperm-analyzer-model/weights/best.pt"
    if os.path.exists(model_path):
        # Load the best model
        best_model = YOLO(model_path)
        
        # Export TorchScript
        try:
            torchscript_path = best_model.export(format='torchscript')
            # Copy to outputs
            import shutil
            shutil.copy(torchscript_path, "outputs/sperm_analyzer.torchscript.pt")
            print("✅ TorchScript model saved to outputs/")
        except Exception as e:
            print(f"❌ Failed to save TorchScript: {e}")
        
        # Export ONNX
        try:
            onnx_path = best_model.export(format='onnx')
            # Copy to outputs
            import shutil
            shutil.copy(onnx_path, "outputs/sperm_analyzer.onnx")
            print("✅ ONNX model saved to outputs/")
        except Exception as e:
            print(f"❌ Failed to save ONNX: {e}")

def validate_model():
    """Validate the trained model"""
    print("🔍 Validating trained model...")
    
    model_path = "runs/detect/sperm-analyzer-model/weights/best.pt"
    if os.path.exists(model_path):
        model = YOLO(model_path)
        
        # Run validation
        results = model.val(data='dataset/data.yaml')
        
        print(f"📊 Validation Results:")
        print(f"   mAP50: {results.box.map50:.4f}")
        print(f"   mAP50-95: {results.box.map:.4f}")
        print(f"   Precision: {results.box.mp:.4f}")
        print(f"   Recall: {results.box.mr:.4f}")
        
        return results
    else:
        print("❌ Model not found for validation")
        return None

def main():
    """Main training pipeline"""
    print("🚀 Starting Sperm Analyzer AI Model Training")
    print("=" * 50)
    
    # Setup environment
    device = setup_training_environment()
    
    # Check if dataset exists
    if not os.path.exists("dataset/data.yaml"):
        print("❌ Dataset not found! Please prepare your dataset first.")
        print("📁 Expected structure:")
        print("   dataset/")
        print("   ├── data.yaml")
        print("   ├── images/")
        print("   │   ├── train/")
        print("   │   ├── val/")
        print("   │   └── test/")
        print("   └── labels/")
        print("       ├── train/")
        print("       ├── val/")
        print("       └── test/")
        return
    
    # Train model
    model, results = train_yolov8_model()
    
    # Validate model
    validation_results = validate_model()
    
    # Export for mobile
    export_model_for_mobile(model)
    
    print("\n🎉 Training pipeline completed!")
    print("📱 Models ready for mobile deployment:")
    print("   - outputs/sperm_analyzer.torchscript.pt")
    print("   - outputs/sperm_analyzer.onnx")
    print("\n🔬 Ready for real sperm analysis!")

if __name__ == "__main__":
    main()
