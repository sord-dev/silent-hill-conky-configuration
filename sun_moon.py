#!/usr/bin/env python3
"""
Conky Sun/Moon Times - Clean version with shared config
Provides sunrise, sunset, and moon phase information
"""

import requests
import sys
import json
import os
from datetime import datetime, timedelta

class SunMoonManager:
    def __init__(self, config_path=None):
        """Initialize with configuration"""
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.location = self.config['location']
        self.api_url = self.config['sun_moon']['api_url']
    
    def get_sun_times(self):
        """Fetch sunrise and sunset times"""
        try:
            url = f"{self.api_url}?lat={self.location['latitude']}&lng={self.location['longitude']}&formatted=0"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') != 'OK':
                return "API Error"
            
            # Parse times (they come in UTC)
            sunrise_utc = datetime.fromisoformat(data['results']['sunrise'].replace('Z', '+00:00'))
            sunset_utc = datetime.fromisoformat(data['results']['sunset'].replace('Z', '+00:00'))
            
            # Convert to local time
            local_offset = timedelta(hours=self.location['timezone_offset_hours'])
            
            sunrise_local = sunrise_utc + local_offset
            sunset_local = sunset_utc + local_offset
            
            return {
                'sunrise': sunrise_local.strftime('%H:%M'),
                'sunset': sunset_local.strftime('%H:%M'),
                'day_length': str(sunset_local - sunrise_local).split('.')[0]  # Remove microseconds
            }
        
        except Exception as e:
            return "Network Error"
    
    def get_moon_phase(self):
        """Get current moon phase (simple calculation)"""
        try:
            # Simple moon phase calculation
            now = datetime.now()
            # Known new moon date (update periodically for accuracy)
            known_new_moon = datetime(2024, 1, 11)
            days_since = (now - known_new_moon).days
            lunar_cycle = 29.53059  # Average lunar cycle in days
            
            phase = (days_since % lunar_cycle) / lunar_cycle
            
            if phase < 0.0625:
                return "New Moon"
            elif phase < 0.1875:
                return "Waxing Crescent"
            elif phase < 0.3125:
                return "First Quarter"
            elif phase < 0.4375:
                return "Waxing Gibbous"
            elif phase < 0.5625:
                return "Full Moon"
            elif phase < 0.6875:
                return "Waning Gibbous"
            elif phase < 0.8125:
                return "Third Quarter"
            else:
                return "Waning Crescent"
        except:
            return "Unknown"

def main():
    try:
        manager = SunMoonManager()
        
        if len(sys.argv) < 2:
            print("Usage: sun_moon.py [sunrise|sunset|day_length|moon|all]")
            sys.exit(1)
        
        command = sys.argv[1].lower()
        sun_data = manager.get_sun_times()
        
        if isinstance(sun_data, str):  # Error occurred
            print(sun_data)
            return
        
        if command == 'sunrise':
            print(sun_data['sunrise'])
        elif command == 'sunset':
            print(sun_data['sunset'])
        elif command == 'day_length':
            print(sun_data['day_length'])
        elif command == 'moon':
            print(manager.get_moon_phase())
        elif command == 'all':
            print(f"↑{sun_data['sunrise']} ↓{sun_data['sunset']} ({sun_data['day_length']})")
        else:
            print(f"Unknown command: {command}")
    
    except Exception as e:
        print("Sun/Moon service unavailable")

if __name__ == "__main__":
    main()