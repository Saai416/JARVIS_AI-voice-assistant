"""
JARVIS Custom UI Widgets
Custom widgets for the Iron Man-style interface
"""

import customtkinter as ctk
from tkinter import Canvas
import math
from ui.animations import AnimationEngine, WaveformGenerator
from config import Config


class ArcReactorWidget(Canvas):
    """Animated Arc Reactor widget - the centerpiece of JARVIS UI"""
    
    def __init__(self, parent, size=200):
        super().__init__(
            parent,
            width=size,
            height=size,
            bg=Config.COLOR_BACKGROUND,
            highlightthickness=0
        )
        self.size = size
        self.center = size // 2
        self.animation = AnimationEngine()
        self.is_active = False
        self.angle = 0
        
        self.draw_arc_reactor()
        self.animate()
    
    def draw_arc_reactor(self):
        """Draw the arc reactor with multiple rings"""
        self.delete("all")
        
        # Get pulse intensity
        intensity = self.animation.get_pulse_intensity(Config.PULSE_SPEED)
        
        # Glow color based on intensity
        glow_color = self.animation.get_glow_color(Config.COLOR_GLOW, intensity)
        
        # Draw multiple concentric rings
        num_rings = Config.ARC_REACTOR_RINGS
        for i in range(num_rings, 0, -1):
            radius = (self.size // 2 - 20) * (i / num_rings)
            
            # Outer glow
            self.create_oval(
                self.center - radius - 5,
                self.center - radius - 5,
                self.center + radius + 5,
                self.center + radius + 5,
                outline=glow_color,
                width=8,
                tags="glow"
            )
            
            # Main ring
            self.create_oval(
                self.center - radius,
                self.center - radius,
                self.center + radius,
                self.center + radius,
                outline=Config.COLOR_PRIMARY,
                width=3,
                tags="ring"
            )
        
        # Draw rotating arcs for active state
        if self.is_active:
            self._draw_rotating_arcs()
        
        # Center dot
        center_radius = 10
        self.create_oval(
            self.center - center_radius,
            self.center - center_radius,
            self.center + center_radius,
            self.center + center_radius,
            fill=Config.COLOR_PRIMARY,
            outline=glow_color,
            width=2,
            tags="center"
        )
    
    def _draw_rotating_arcs(self):
        """Draw rotating arcs around the reactor"""
        radius = self.size // 2 - 30
        
        for i in range(3):
            start_angle = self.angle + (i * 120)
            end_angle = start_angle + 80
            
            # Convert to radians
            start_rad = math.radians(start_angle)
            end_rad = math.radians(end_angle)
            
            # Draw arc
            self.create_arc(
                self.center - radius,
                self.center - radius,
                self.center + radius,
                self.center + radius,
                start=start_angle,
                extent=80,
                outline=Config.COLOR_SECONDARY,
                width=2,
                style="arc",
                tags="rotating"
            )
    
    def animate(self):
        """Animation loop"""
        self.angle = self.animation.update_arc_reactor()
        self.draw_arc_reactor()
        self.after(50, self.animate)  # 20 FPS
    
    def set_active(self, active=True):
        """Set active state (shows rotating arcs)"""
        self.is_active = active


class WaveformWidget(Canvas):
    """Animated waveform visualization for voice"""
    
    def __init__(self, parent, width=400, height=80, num_bars=30):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=Config.COLOR_BACKGROUND,
            highlightthickness=0
        )
        self.width = width
        self.height = height
        self.num_bars = num_bars
        self.waveform = WaveformGenerator(num_bars)
        self.is_active = False
        
        self.draw_waveform()
        self.animate()
    
    def draw_waveform(self):
        """Draw animated waveform bars"""
        self.delete("all")
        
        bar_heights = self.waveform.update(self.is_active)
        bar_width = self.width / self.num_bars - 2
        
        for i, height in enumerate(bar_heights):
            x = i * (self.width / self.num_bars)
            bar_height = height * (self.height - 10)
            y = (self.height - bar_height) / 2
            
            # Get color based on height
            color = self.waveform.get_bar_color(height)
            
            # Draw bar
            self.create_rectangle(
                x,
                y,
                x + bar_width,
                y + bar_height,
                fill=color,
                outline="",
                tags=f"bar_{i}"
            )
    
    def animate(self):
        """Animation loop"""
        self.draw_waveform()
        self.after(50, self.animate)  # 20 FPS
    
    def set_active(self, active=True):
        """Set active state (animates waveform)"""
        self.is_active = active


class GlassPanel(ctk.CTkFrame):
    """Glassmorphic panel with semi-transparency"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color=(Config.COLOR_PANEL, Config.COLOR_PANEL),
            corner_radius=15,
            border_width=1,
            border_color=(Config.COLOR_PRIMARY, Config.COLOR_PRIMARY),
            **kwargs
        )


class StatusLabel(ctk.CTkLabel):
    """Glowing status text label"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            text_color=Config.COLOR_PRIMARY,
            font=("Segoe UI", 18, "bold"),
            **kwargs
        )
    
    def set_status(self, text, color=None):
        """Update status text and color"""
        self.configure(text=text)
        if color:
            self.configure(text_color=color)


class ConversationText(ctk.CTkTextbox):
    """Scrollable conversation display"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color=Config.COLOR_BACKGROUND,
            text_color=Config.COLOR_TEXT,
            font=("Consolas", 12),
            corner_radius=10,
            border_width=1,
            border_color=Config.COLOR_PRIMARY,
            **kwargs
        )
        self.configure(state="disabled")
    
    def add_message(self, speaker, text, color=None):
        """Add a message to the conversation"""
        self.configure(state="normal")
        
        # Format message
        if color is None:
            color = Config.COLOR_PRIMARY if speaker == "JARVIS" else Config.COLOR_TEXT
        
        message = f"\n{speaker}: {text}\n"
        
        self.insert("end", message)
        self.see("end")
        self.configure(state="disabled")
    
    def clear(self):
        """Clear all messages"""
        self.configure(state="normal")
        self.delete("1.0", "end")
        self.configure(state="disabled")
