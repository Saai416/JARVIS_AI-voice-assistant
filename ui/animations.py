"""
JARVIS UI Animations
Handles all visual effects and animations for the Iron Man-style interface
"""

import math
import time
from typing import List, Tuple

class AnimationEngine:
    """Manages animation states and calculations"""
    
    def __init__(self):
        self.start_time = time.time()
        self.arc_reactor_angle = 0
        self.pulse_phase = 0
    
    def get_elapsed_time(self):
        """Get elapsed time since animation start"""
        return time.time() - self.start_time
    
    def update_arc_reactor(self):
        """Update arc reactor rotation angle"""
        self.arc_reactor_angle = (self.arc_reactor_angle + 2) % 360
        return self.arc_reactor_angle
    
    def get_pulse_intensity(self, speed=2.0):
        """
        Get pulsing intensity (0.0 to 1.0) based on sine wave
        
        Args:
            speed: Pulse speed in seconds per cycle
        
        Returns:
            float: Intensity value between 0.0 and 1.0
        """
        elapsed = self.get_elapsed_time()
        phase = (elapsed / speed) * 2 * math.pi
        # Scale from [-1, 1] to [0.5, 1.0] for better visibility
        intensity = 0.5 + 0.5 * math.sin(phase)
        return intensity
    
    def get_glow_color(self, base_color, intensity):
        """
        Calculate glowing color based on intensity
        
        Args:
            base_color: Base color in hex format (e.g., "#00d4ff")
            intensity: Intensity value (0.0 to 1.0)
        
        Returns:
            str: Color in hex format
        """
        # Parse hex color
        base_color = base_color.lstrip('#')
        r = int(base_color[0:2], 16)
        g = int(base_color[2:4], 16)
        b = int(base_color[4:6], 16)
        
        # Apply intensity
        r = int(r * intensity)
        g = int(g * intensity)
        b = int(b * intensity)
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def generate_circle_points(self, center_x, center_y, radius, num_points=100):
        """
        Generate points for a circle
        
        Args:
            center_x: X coordinate of center
            center_y: Y coordinate of center
            radius: Circle radius
            num_points: Number of points to generate
        
        Returns:
            List of (x, y) tuples
        """
        points = []
        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))
        return points
    
    def generate_arc_points(self, center_x, center_y, radius, start_angle, end_angle, num_points=50):
        """
        Generate points for an arc (partial circle)
        
        Args:
            center_x: X coordinate of center
            center_y: Y coordinate of center
            radius: Arc radius
            start_angle: Start angle in degrees
            end_angle: End angle in degrees
            num_points: Number of points to generate
        
        Returns:
            List of (x, y) tuples
        """
        points = []
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        for i in range(num_points):
            angle = start_rad + (i / num_points) * (end_rad - start_rad)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))
        return points


class WaveformGenerator:
    """Generates animated waveforms for voice visualization"""
    
    def __init__(self, num_bars=20):
        self.num_bars = num_bars
        self.bar_heights = [0.0] * num_bars
        self.time_offset = 0
    
    def update(self, is_active=False):
        """
        Update waveform animation
        
        Args:
            is_active: Whether voice is active (listening/speaking)
        
        Returns:
            List of bar heights (0.0 to 1.0)
        """
        self.time_offset += 0.1
        
        for i in range(self.num_bars):
            if is_active:
                # Generate animated sine wave
                phase = (i / self.num_bars) * 2 * math.pi + self.time_offset
                height = 0.3 + 0.7 * abs(math.sin(phase + i * 0.5))
            else:
                # Decay to baseline
                self.bar_heights[i] *= 0.9
                height = max(0.1, self.bar_heights[i])
            
            self.bar_heights[i] = height
        
        return self.bar_heights
    
    def get_bar_color(self, height, base_color="#00d4ff"):
        """Get color for bar based on height"""
        # Brighter at higher amplitudes
        intensity = 0.4 + 0.6 * height
        base_color = base_color.lstrip('#')
        r = int(base_color[0:2], 16)
        g = int(base_color[2:4], 16)
        b = int(base_color[4:6], 16)
        
        r = int(r * intensity)
        g = int(g * intensity)
        b = int(b * intensity)
        
        return f"#{r:02x}{g:02x}{b:02x}"


class FadeAnimation:
    """Handles fade in/out animations"""
    
    def __init__(self, duration=0.3):
        """
        Args:
            duration: Animation duration in seconds
        """
        self.duration = duration
        self.start_time = None
        self.is_fading_in = False
        self.is_fading_out = False
    
    def start_fade_in(self):
        """Start fade in animation"""
        self.start_time = time.time()
        self.is_fading_in = True
        self.is_fading_out = False
    
    def start_fade_out(self):
        """Start fade out animation"""
        self.start_time = time.time()
        self.is_fading_out = True
        self.is_fading_in = False
    
    def get_alpha(self):
        """
        Get current alpha value (0.0 to 1.0)
        
        Returns:
            float: Alpha value, or None if animation is complete
        """
        if not (self.is_fading_in or self.is_fading_out):
            return None
        
        elapsed = time.time() - self.start_time
        progress = min(1.0, elapsed / self.duration)
        
        if self.is_fading_in:
            alpha = progress
            if progress >= 1.0:
                self.is_fading_in = False
        else:  # Fading out
            alpha = 1.0 - progress
            if progress >= 1.0:
                self.is_fading_out = False
        
        return alpha
    
    def is_complete(self):
        """Check if animation is complete"""
        return not (self.is_fading_in or self.is_fading_out)
