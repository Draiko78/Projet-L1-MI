"""
sound_sensor.py
Grove Sound Sensor (101020023)
Returns the MAX sound intensity over a 1-second window
"""

import time
from grove.adc import ADC

__all__ = ['soundSensor', 'fearLevel']


# ────────────────────────────────────────────────
# INTERNAL STATE
# ────────────────────────────────────────────────
_adc = None
_smoothed = None
_baseline = None

_last_sample_time = 0.0
_window_start_time = 0.0
_window_max = 0

# Parameters
_SAMPLE_INTERVAL = 0.02      # 50 Hz
_WINDOW_DURATION = 1.0       # seconds
_SMOOTH = 0.2
_BASELINE_ADAPT = 0.001
_MAX_INTENSITY = 1000


def soundSensor(channel=6):
    """
    Call this function whenever you want.
    It returns the MAX intensity of the *previous* 1-second window.
    """

    global _adc, _smoothed, _baseline
    global _last_sample_time, _window_start_time, _window_max

    now = time.monotonic()

    # ── Lazy initialization ─────────────────────
    if _adc is None:
        _adc = ADC()
        first = _adc.read(channel)
        _smoothed = first
        _baseline = first
        _last_sample_time = now
        _window_start_time = now
        _window_max = 0
        return 0

    # ── Sampling rate control ───────────────────
    if now - _last_sample_time < _SAMPLE_INTERVAL:
        return _window_max

    _last_sample_time = now

    raw = _adc.read(channel)

    # ── Smoothing ───────────────────────────────
    _smoothed = _smoothed * (1 - _SMOOTH) + raw * _SMOOTH

    # ── Baseline adaptation ─────────────────────
    if raw < _baseline + 10:
        _baseline = _baseline * (1 - _BASELINE_ADAPT) + raw * _BASELINE_ADAPT

    # ── Intensity computation ───────────────────
    intensity = raw - _baseline
    if intensity < 0:
        intensity = 0

	# Normalize for gameplay
    RAW_MAX_DETECTED = 470
    intensity = intensity * (1000 / RAW_MAX_DETECTED)
    if intensity > 1000:
        intensity = 1000

    # ── Track max in current window ─────────────
    if intensity > _window_max:
        _window_max = intensity

    # ── Window finished? ────────────────────────
    if now - _window_start_time >= _WINDOW_DURATION:
        result = _window_max
        _window_max = 0
        _window_start_time = now
        return int(result)

    return int(_window_max)
