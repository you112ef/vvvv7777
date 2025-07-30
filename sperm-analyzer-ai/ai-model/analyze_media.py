"""
Media Analysis Module for Sperm Detection and Tracking
Real AI processing with YOLOv8 + DeepSORT
"""

import cv2
import numpy as np
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
from utils.casa_metrics import CASAMetrics, calculate_motility_parameters
from typing import Dict, List, Tuple, Any, Optional
import os
import json
from pathlib import Path
import time

class SpermAnalyzer:
    """Real sperm analyzer using YOLOv8 + DeepSORT"""
    
    def __init__(self, model_path: str = "outputs/sperm_analyzer.torchscript.pt"):
        """
        Initialize the sperm analyzer
        
        Args:
            model_path: Path to the trained model
        """
        self.model_path = model_path
        self.model = None
        self.tracker = None
        self.casa_calculator = CASAMetrics()
        self.load_model()
        self.setup_tracker()
    
    def load_model(self):
        """Load the trained YOLOv8 model"""
        try:
            if os.path.exists(self.model_path):
                print(f"🧠 Loading model from {self.model_path}")
                self.model = YOLO(self.model_path)
                print("✅ Model loaded successfully!")
            else:
                # Fallback to default YOLOv8 if custom model not found
                print("⚠️  Custom model not found, using default YOLOv8n")
                self.model = YOLO('yolov8n.pt')
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            print("🔄 Using default YOLOv8n model")
            self.model = YOLO('yolov8n.pt')
    
    def setup_tracker(self):
        """Setup DeepSORT tracker"""
        try:
            self.tracker = DeepSort(
                max_age=30,
                n_init=3,
                nms_max_overlap=1.0,
                max_cosine_distance=0.2,
                nn_budget=None,
                override_track_class=None,
                embedder="mobilenet",
                half=True,
                bgr=True,
                embedder_gpu=True,
                embedder_model_name=None,
                embedder_wts=None,
                polygon=False,
                today=None
            )
            print("✅ DeepSORT tracker initialized!")
        except Exception as e:
            print(f"❌ Error initializing tracker: {e}")
            self.tracker = DeepSort()
    
    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """
        Analyze a single image for sperm detection
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Analysis results dictionary
        """
        print(f"📸 Analyzing image: {image_path}")
        
        if not os.path.exists(image_path):
            return {"error": "Image file not found"}
        
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                return {"error": "Could not load image"}
            
            # Run detection
            results = self.model(image, verbose=False)[0]
            
            # Extract detections
            detections = []
            if results.boxes is not None:
                for box in results.boxes:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    conf = float(box.conf[0].cpu().numpy())
                    
                    # Filter by confidence
                    if conf > 0.3:
                        detections.append({
                            'bbox': [int(x1), int(y1), int(x2), int(y2)],
                            'confidence': round(conf, 3),
                            'center': [int((x1 + x2) / 2), int((y1 + y2) / 2)]
                        })
            
            # Calculate basic statistics
            sperm_count = len(detections)
            image_area = image.shape[0] * image.shape[1]
            density = sperm_count / (image_area / 1000000) if image_area > 0 else 0  # per mm²
            
            result = {
                'type': 'image',
                'file_path': image_path,
                'sperm_count': sperm_count,
                'density_per_mm2': round(density, 2),
                'detections': detections,
                'image_dimensions': {
                    'width': image.shape[1],
                    'height': image.shape[0]
                },
                'analysis_timestamp': time.time()
            }
            
            print(f"🧬 Sperm Count: {sperm_count}")
            print(f"📊 Density: {density:.2f} per mm²")
            
            return result
            
        except Exception as e:
            print(f"❌ Error analyzing image: {e}")
            return {"error": str(e)}
    
    def analyze_video(self, video_path: str, 
                     max_frames: Optional[int] = None,
                     progress_callback: Optional[callable] = None) -> Dict[str, Any]:
        """
        Analyze a video for sperm detection and tracking
        
        Args:
            video_path: Path to the video file
            max_frames: Maximum number of frames to process (None for all)
            progress_callback: Callback function for progress updates
            
        Returns:
            Analysis results dictionary
        """
        print(f"📹 Analyzing video: {video_path}")
        
        if not os.path.exists(video_path):
            return {"error": "Video file not found"}
        
        try:
            # Open video
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return {"error": "Could not open video file"}
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = total_frames / fps if fps > 0 else 0
            
            print(f"📊 Video info: {width}x{height}, {fps:.1f} FPS, {duration:.1f}s")
            
            # Update CASA calculator with video FPS
            self.casa_calculator.fps = fps
            
            # Process frames
            tracks_data = {}
            frame_detections = []
            frame_count = 0
            processed_frames = 0
            
            frames_to_process = min(max_frames, total_frames) if max_frames else total_frames
            
            while cap.isOpened() and (max_frames is None or processed_frames < max_frames):
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                
                # Skip frames for performance if needed
                if frame_count % 1 == 0:  # Process every frame
                    processed_frames += 1
                    
                    # Run detection
                    results = self.model(frame, verbose=False)[0]
                    
                    # Prepare detections for DeepSORT
                    detections = []
                    if results.boxes is not None:
                        for box in results.boxes:
                            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                            conf = float(box.conf[0].cpu().numpy())
                            
                            if conf > 0.3:  # Confidence threshold
                                w = x2 - x1
                                h = y2 - y1
                                detections.append([
                                    [int(x1), int(y1), int(w), int(h)],
                                    conf,
                                    'sperm'
                                ])
                    
                    # Update tracker
                    tracks = self.tracker.update_tracks(detections, frame=frame)
                    
                    # Get current timestamp
                    timestamp_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
                    
                    # Store tracking data
                    frame_detection_data = {
                        'frame_number': frame_count,
                        'timestamp_ms': timestamp_ms,
                        'detections': len(detections),
                        'tracks': []
                    }
                    
                    for track in tracks:
                        if not track.is_confirmed():
                            continue
                        
                        track_id = track.track_id
                        x1, y1, x2, y2 = map(int, track.to_ltrb())
                        center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2
                        
                        # Store track data
                        if track_id not in tracks_data:
                            tracks_data[track_id] = []
                        
                        tracks_data[track_id].append({
                            'timestamp': timestamp_ms,
                            'position': (center_x, center_y),
                            'bbox': [x1, y1, x2, y2]
                        })
                        
                        frame_detection_data['tracks'].append({
                            'id': track_id,
                            'bbox': [x1, y1, x2, y2],
                            'center': [center_x, center_y]
                        })
                    
                    frame_detections.append(frame_detection_data)
                    
                    # Progress callback
                    if progress_callback:
                        progress = processed_frames / frames_to_process
                        progress_callback(progress)
            
            cap.release()
            
            # Calculate CASA metrics for each track
            track_metrics = []
            for track_id, track_data in tracks_data.items():
                if len(track_data) >= 3:  # Need at least 3 points for meaningful analysis
                    positions = [point['position'] for point in track_data]
                    timestamps = [point['timestamp'] for point in track_data]
                    
                    metrics = self.casa_calculator.calculate_velocity_metrics(positions, timestamps)
                    metrics['track_id'] = track_id
                    track_metrics.append(metrics)
            
            # Calculate overall motility parameters
            total_sperm_count = len(tracks_data)
            motility_params = calculate_motility_parameters(track_metrics, total_sperm_count)
            
            # Prepare final results
            result = {
                'type': 'video',
                'file_path': video_path,
                'video_info': {
                    'width': width,
                    'height': height,
                    'fps': fps,
                    'total_frames': total_frames,
                    'processed_frames': processed_frames,
                    'duration_seconds': duration
                },
                'sperm_analysis': {
                    'total_tracks': len(tracks_data),
                    'analyzed_tracks': len(track_metrics),
                    'motility_parameters': motility_params
                },
                'casa_metrics': track_metrics,
                'frame_by_frame': frame_detections,
                'analysis_timestamp': time.time()
            }
            
            print(f"🧬 Analysis complete!")
            print(f"   Total tracks: {len(tracks_data)}")
            print(f"   Motile sperm: {motility_params['motile_count']}")
            print(f"   Progressive: {motility_params['progressive_count']}")
            print(f"   Motility: {motility_params['motility_percentage']:.1f}%")
            
            return result
            
        except Exception as e:
            print(f"❌ Error analyzing video: {e}")
            return {"error": str(e)}
    
    def save_results(self, results: Dict[str, Any], output_path: str):
        """Save analysis results to JSON file"""
        try:
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"💾 Results saved to {output_path}")
        except Exception as e:
            print(f"❌ Error saving results: {e}")

# Convenience functions for backward compatibility
def analyze_image(image_path: str) -> Dict[str, Any]:
    """Analyze a single image"""
    analyzer = SpermAnalyzer()
    return analyzer.analyze_image(image_path)

def analyze_video(video_path: str) -> Dict[str, Any]:
    """Analyze a video file"""
    analyzer = SpermAnalyzer()
    return analyzer.analyze_video(video_path)

# Main execution for testing
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python analyze_media.py <image_or_video_path>")
        sys.exit(1)
    
    media_path = sys.argv[1]
    
    # Initialize analyzer
    analyzer = SpermAnalyzer()
    
    # Determine file type and analyze
    file_ext = Path(media_path).suffix.lower()
    
    if file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
        print("🔍 Detected image file")
        results = analyzer.analyze_image(media_path)
    elif file_ext in ['.mp4', '.avi', '.mov', '.mkv', '.wmv']:
        print("🔍 Detected video file")
        results = analyzer.analyze_video(media_path)
    else:
        print(f"❌ Unsupported file format: {file_ext}")
        sys.exit(1)
    
    # Save results
    output_path = f"analysis_results_{int(time.time())}.json"
    analyzer.save_results(results, output_path)
    
    print("\n🎉 Analysis complete!")
