"""
FPS counter and frame drop warning system.
Displays current FPS on screen and logs warnings when frames are dropped.
"""

from collections import deque

import pygame


class FPSCounter:
    """Tracks and displays FPS with frame drop warnings."""

    TARGET_FPS = 60
    FRAME_TIME_MS = 1000 / TARGET_FPS  # ~16.67ms per frame
    WARNING_THRESHOLD_MS = FRAME_TIME_MS * 1.5  # Warn if frame takes 50% longer

    def __init__(self, font: pygame.font.Font = None, sample_size: int = 60):
        """
        Initialize FPS counter.

        Args:
            font: Font to use for rendering. If None, uses default.
            sample_size: Number of frames to average for FPS calculation.
        """
        self.font = font or pygame.font.Font(None, 24)
        self.frame_times = deque(maxlen=sample_size)
        self.current_fps = 0.0
        self.dropped_frames = 0
        self.total_frames = 0
        self.show_warning = False
        self.warning_timer = 0
        self.warning_display_ms = 1000  # Show warning for 1 second

    def update(self, dt_ms: float):
        """
        Update FPS tracking with the current frame's delta time.

        Args:
            dt_ms: Time since last frame in milliseconds.
        """
        self.total_frames += 1
        self.frame_times.append(dt_ms)

        # Calculate average FPS from sample
        if len(self.frame_times) > 0:
            avg_frame_time = sum(self.frame_times) / len(self.frame_times)
            self.current_fps = 1000 / avg_frame_time if avg_frame_time > 0 else 0

        # Check for dropped frames
        if dt_ms > self.WARNING_THRESHOLD_MS:
            self.dropped_frames += 1
            self.show_warning = True
            self.warning_timer = self.warning_display_ms
            frames_lost = int(dt_ms / self.FRAME_TIME_MS) - 1
            print(f"[FPS WARNING] Frame drop detected! dt={dt_ms:.1f}ms (~{frames_lost} frames lost). Total drops: {self.dropped_frames}")

        # Update warning display timer
        if self.warning_timer > 0:
            self.warning_timer -= dt_ms
            if self.warning_timer <= 0:
                self.show_warning = False

    def draw(self, screen: pygame.Surface, x: int = 10, y: int = 10):
        """
        Draw FPS counter on screen.

        Args:
            screen: Surface to draw on.
            x: X position of the counter.
            y: Y position of the counter.
        """
        # Determine color based on FPS
        if self.current_fps >= 55:
            color = (0, 255, 0)  # Green - good
        elif self.current_fps >= 45:
            color = (255, 255, 0)  # Yellow - acceptable
        else:
            color = (255, 0, 0)  # Red - poor

        # Render FPS text
        fps_text = f"FPS: {self.current_fps:.1f}"
        fps_surface = self.font.render(fps_text, True, color)

        # Draw background for readability
        padding = 4
        bg_rect = fps_surface.get_rect(topleft=(x - padding, y - padding))
        bg_rect.inflate_ip(padding * 2, padding * 2)
        pygame.draw.rect(screen, (0, 0, 0, 180), bg_rect)

        screen.blit(fps_surface, (x, y))

        # Draw warning if active
        if self.show_warning:
            warning_text = f"! FRAME DROP ({self.dropped_frames} total)"
            warning_surface = self.font.render(warning_text, True, (255, 100, 100))
            screen.blit(warning_surface, (x, y + fps_surface.get_height() + 4))
