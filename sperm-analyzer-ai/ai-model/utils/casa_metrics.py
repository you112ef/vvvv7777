"""
CASA (Computer Assisted Sperm Analysis) Metrics Calculator
Real scientific calculations for sperm analysis
"""

import numpy as np
from scipy.spatial.distance import euclidean
from typing import List, Tuple, Dict, Any
import math

class CASAMetrics:
    """Calculate CASA metrics for sperm analysis"""
    
    def __init__(self, pixel_to_micron_ratio: float = 0.5, fps: float = 30.0):
        """
        Initialize CASA calculator
        
        Args:
            pixel_to_micron_ratio: Conversion ratio from pixels to microns
            fps: Frames per second of the video
        """
        self.pixel_to_micron_ratio = pixel_to_micron_ratio
        self.fps = fps
        self.frame_interval = 1.0 / fps  # Time between frames in seconds
    
    def calculate_velocity_metrics(self, positions: List[Tuple[float, float]], 
                                 timestamps: List[float]) -> Dict[str, float]:
        """
        Calculate velocity metrics (VCL, VSL, VAP, LIN, STR, WOB)
        
        Args:
            positions: List of (x, y) positions in pixels
            timestamps: List of timestamps in milliseconds
            
        Returns:
            Dictionary containing velocity metrics
        """
        if len(positions) < 2:
            return self._empty_metrics()
        
        # Convert positions to microns
        positions_microns = [(x * self.pixel_to_micron_ratio, 
                            y * self.pixel_to_micron_ratio) for x, y in positions]
        
        # Convert timestamps to seconds
        timestamps_sec = [t / 1000.0 for t in timestamps]
        
        # Calculate VCL (Curvilinear Velocity)
        vcl = self._calculate_vcl(positions_microns, timestamps_sec)
        
        # Calculate VSL (Straight Line Velocity)
        vsl = self._calculate_vsl(positions_microns, timestamps_sec)
        
        # Calculate VAP (Average Path Velocity)
        vap = self._calculate_vap(positions_microns, timestamps_sec)
        
        # Calculate derived metrics
        lin = (vsl / vcl * 100) if vcl > 0 else 0  # Linearity
        str_metric = (vsl / vap * 100) if vap > 0 else 0  # Straightness
        wob = (vap / vcl * 100) if vcl > 0 else 0  # Wobble
        
        # Calculate ALH (Amplitude of Lateral Head displacement)
        alh = self._calculate_alh(positions_microns)
        
        # Calculate BCF (Beat Cross Frequency)
        bcf = self._calculate_bcf(positions_microns, timestamps_sec)
        
        return {
            'VCL': round(vcl, 2),  # μm/s
            'VSL': round(vsl, 2),  # μm/s
            'VAP': round(vap, 2),  # μm/s
            'LIN': round(lin, 1),  # %
            'STR': round(str_metric, 1),  # %
            'WOB': round(wob, 1),  # %
            'ALH': round(alh, 2),  # μm
            'BCF': round(bcf, 1),  # Hz
            'track_length': len(positions),
            'duration': timestamps_sec[-1] - timestamps_sec[0] if len(timestamps_sec) > 1 else 0
        }
    
    def _calculate_vcl(self, positions: List[Tuple[float, float]], 
                      timestamps: List[float]) -> float:
        """Calculate Curvilinear Velocity (VCL)"""
        if len(positions) < 2:
            return 0.0
        
        total_distance = 0.0
        for i in range(len(positions) - 1):
            distance = euclidean(positions[i], positions[i + 1])
            total_distance += distance
        
        total_time = timestamps[-1] - timestamps[0]
        return total_distance / total_time if total_time > 0 else 0.0
    
    def _calculate_vsl(self, positions: List[Tuple[float, float]], 
                      timestamps: List[float]) -> float:
        """Calculate Straight Line Velocity (VSL)"""
        if len(positions) < 2:
            return 0.0
        
        straight_distance = euclidean(positions[0], positions[-1])
        total_time = timestamps[-1] - timestamps[0]
        return straight_distance / total_time if total_time > 0 else 0.0
    
    def _calculate_vap(self, positions: List[Tuple[float, float]], 
                      timestamps: List[float]) -> float:
        """Calculate Average Path Velocity (VAP)"""
        if len(positions) < 3:
            return self._calculate_vsl(positions, timestamps)
        
        # Smooth the path using a simple moving average
        smoothed_positions = self._smooth_path(positions)
        
        total_distance = 0.0
        for i in range(len(smoothed_positions) - 1):
            distance = euclidean(smoothed_positions[i], smoothed_positions[i + 1])
            total_distance += distance
        
        total_time = timestamps[-1] - timestamps[0]
        return total_distance / total_time if total_time > 0 else 0.0
    
    def _calculate_alh(self, positions: List[Tuple[float, float]]) -> float:
        """Calculate Amplitude of Lateral Head displacement (ALH)"""
        if len(positions) < 3:
            return 0.0
        
        # Calculate the main direction vector
        start_pos = np.array(positions[0])
        end_pos = np.array(positions[-1])
        main_vector = end_pos - start_pos
        
        if np.linalg.norm(main_vector) == 0:
            return 0.0
        
        main_vector_normalized = main_vector / np.linalg.norm(main_vector)
        
        # Calculate lateral displacements
        lateral_displacements = []
        for pos in positions[1:-1]:
            pos_array = np.array(pos)
            vector_to_pos = pos_array - start_pos
            
            # Project onto main direction
            projection_length = np.dot(vector_to_pos, main_vector_normalized)
            projection_point = start_pos + projection_length * main_vector_normalized
            
            # Calculate lateral displacement
            lateral_displacement = np.linalg.norm(pos_array - projection_point)
            lateral_displacements.append(lateral_displacement)
        
        return np.mean(lateral_displacements) if lateral_displacements else 0.0
    
    def _calculate_bcf(self, positions: List[Tuple[float, float]], 
                      timestamps: List[float]) -> float:
        """Calculate Beat Cross Frequency (BCF)"""
        if len(positions) < 5:
            return 0.0
        
        # Calculate lateral displacements from the average path
        smoothed_positions = self._smooth_path(positions)
        
        # Find zero crossings in lateral displacement
        crossings = 0
        prev_side = 0
        
        for i in range(1, len(positions) - 1):
            # Calculate which side of the smoothed path the point is on
            current_side = self._calculate_side(positions[i], smoothed_positions, i)
            
            if prev_side != 0 and current_side != 0 and prev_side != current_side:
                crossings += 1
            
            if current_side != 0:
                prev_side = current_side
        
        # Calculate frequency
        total_time = timestamps[-1] - timestamps[0]
        frequency = (crossings / 2.0) / total_time if total_time > 0 else 0.0
        
        return frequency
    
    def _smooth_path(self, positions: List[Tuple[float, float]], 
                    window_size: int = 3) -> List[Tuple[float, float]]:
        """Smooth the path using moving average"""
        if len(positions) <= window_size:
            return positions
        
        smoothed = []
        half_window = window_size // 2
        
        for i in range(len(positions)):
            start_idx = max(0, i - half_window)
            end_idx = min(len(positions), i + half_window + 1)
            
            x_sum = sum(pos[0] for pos in positions[start_idx:end_idx])
            y_sum = sum(pos[1] for pos in positions[start_idx:end_idx])
            count = end_idx - start_idx
            
            smoothed.append((x_sum / count, y_sum / count))
        
        return smoothed
    
    def _calculate_side(self, point: Tuple[float, float], 
                       smoothed_path: List[Tuple[float, float]], 
                       index: int) -> int:
        """Calculate which side of the smoothed path a point is on"""
        if index >= len(smoothed_path) - 1:
            return 0
        
        # Use cross product to determine side
        p1 = np.array(smoothed_path[index])
        p2 = np.array(smoothed_path[index + 1])
        p = np.array(point)
        
        cross_product = np.cross(p2 - p1, p - p1)
        
        if cross_product > 0:
            return 1
        elif cross_product < 0:
            return -1
        else:
            return 0
    
    def _empty_metrics(self) -> Dict[str, float]:
        """Return empty metrics dictionary"""
        return {
            'VCL': 0.0,
            'VSL': 0.0,
            'VAP': 0.0,
            'LIN': 0.0,
            'STR': 0.0,
            'WOB': 0.0,
            'ALH': 0.0,
            'BCF': 0.0,
            'track_length': 0,
            'duration': 0.0
        }

def calculate_motility_parameters(all_tracks_metrics: List[Dict[str, float]], 
                                total_sperm_count: int) -> Dict[str, Any]:
    """
    Calculate overall motility parameters from all tracks
    
    Args:
        all_tracks_metrics: List of metrics for each track
        total_sperm_count: Total number of sperm detected
        
    Returns:
        Dictionary containing motility parameters
    """
    if not all_tracks_metrics:
        return {
            'total_count': total_sperm_count,
            'motile_count': 0,
            'progressive_count': 0,
            'non_progressive_count': 0,
            'immotile_count': total_sperm_count,
            'motility_percentage': 0.0,
            'progressive_motility_percentage': 0.0,
            'average_vcl': 0.0,
            'average_vsl': 0.0,
            'average_vap': 0.0,
            'average_lin': 0.0,
            'average_alh': 0.0,
            'average_bcf': 0.0
        }
    
    # Classification thresholds (WHO 2010 standards)
    VCL_THRESHOLD = 25.0  # μm/s
    VSL_THRESHOLD = 25.0  # μm/s
    LIN_THRESHOLD = 50.0  # %
    
    motile_tracks = [track for track in all_tracks_metrics if track['VCL'] >= VCL_THRESHOLD]
    progressive_tracks = [track for track in motile_tracks 
                         if track['VSL'] >= VSL_THRESHOLD and track['LIN'] >= LIN_THRESHOLD]
    non_progressive_tracks = [track for track in motile_tracks if track not in progressive_tracks]
    
    motile_count = len(motile_tracks)
    progressive_count = len(progressive_tracks)
    non_progressive_count = len(non_progressive_tracks)
    immotile_count = total_sperm_count - motile_count
    
    # Calculate averages
    def safe_average(values):
        return sum(values) / len(values) if values else 0.0
    
    return {
        'total_count': total_sperm_count,
        'motile_count': motile_count,
        'progressive_count': progressive_count,
        'non_progressive_count': non_progressive_count,
        'immotile_count': immotile_count,
        'motility_percentage': round((motile_count / total_sperm_count * 100) if total_sperm_count > 0 else 0.0, 1),
        'progressive_motility_percentage': round((progressive_count / total_sperm_count * 100) if total_sperm_count > 0 else 0.0, 1),
        'average_vcl': round(safe_average([track['VCL'] for track in all_tracks_metrics]), 2),
        'average_vsl': round(safe_average([track['VSL'] for track in all_tracks_metrics]), 2),
        'average_vap': round(safe_average([track['VAP'] for track in all_tracks_metrics]), 2),
        'average_lin': round(safe_average([track['LIN'] for track in all_tracks_metrics]), 1),
        'average_alh': round(safe_average([track['ALH'] for track in all_tracks_metrics]), 2),
        'average_bcf': round(safe_average([track['BCF'] for track in all_tracks_metrics]), 1)
    }

# Convenience function for backward compatibility
def calculate_velocity(positions: List[Tuple[float, float]], 
                      timestamps: List[float]) -> Tuple[float, float, float]:
    """
    Calculate basic velocity metrics (backward compatibility)
    
    Returns:
        Tuple of (VCL, VSL, LIN)
    """
    casa = CASAMetrics()
    metrics = casa.calculate_velocity_metrics(positions, timestamps)
    return metrics['VCL'], metrics['VSL'], metrics['LIN']
