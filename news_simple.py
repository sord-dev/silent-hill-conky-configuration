#!/usr/bin/env python3
"""
Simple News Headlines for Conky
No caching, no click functionality - just clean news display
"""

import feedparser
import sys
import json
import os

class SimpleNewsManager:
    def __init__(self, config_path=None):
        """Initialize with configuration"""
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        
        with open(config_path, 'r') as f:
            self.config = json.load(f)
    
    def fetch_headlines_from_source(self, source_name, max_headlines=2):
        """Fetch headlines from a specific RSS source"""
        try:
            sources = self.config['news']['sources']
            if source_name not in sources:
                return []
            
            headers = {'User-Agent': self.config['general']['user_agent']}
            feed = feedparser.parse(sources[source_name])
            
            if not feed.entries:
                return []
            
            headlines = []
            for entry in feed.entries[:max_headlines]:
                title = entry.title.strip()
                title = title.replace('\n', ' ').replace('\r', ' ')
                title = ' '.join(title.split())  # Clean whitespace
                
                headlines.append({
                    'source': source_name.upper(),
                    'title': title
                })
            
            return headlines
        except:
            return []
    
    def get_all_headlines(self):
        """Get headlines from all sources - fresh each time"""
        all_headlines = []
        sources = ['bbc', 'guardian', 'sky', 'hackernews']
        
        for source in sources:
            if source in self.config['news']['sources']:
                headlines = self.fetch_headlines_from_source(source, 2)
                all_headlines.extend(headlines)
                
                if len(all_headlines) >= 8:
                    break
        
        # Fallback if no headlines
        if len(all_headlines) < 2:
            all_headlines = [
                {'source': 'INFO', 'title': 'Check internet connection'},
                {'source': 'INFO', 'title': 'News feeds temporarily unavailable'}
            ]
        
        return all_headlines
    
    def format_headline(self, headline, max_width=45, truncate=True):
        """Format a single headline for display"""
        full_text = f"{headline['source']}: {headline['title']}"
        
        # Only truncate if requested (for list mode)
        if truncate and len(full_text) > max_width:
            return full_text[:max_width-3] + "..."
        return full_text
    
    def get_headlines_for_display(self, num_lines=4):
        """Get formatted headlines for display"""
        headlines = self.get_all_headlines()
        
        # Just return the first few headlines, formatted
        display_lines = []
        for i in range(min(num_lines, len(headlines))):
            formatted = self.format_headline(headlines[i])
            display_lines.append(formatted)
        
        # Pad with empty lines if needed
        while len(display_lines) < num_lines:
            display_lines.append("")
        
        return display_lines
    
    def get_single_headline(self, index=0):
        """Get a single headline by index - full length for conky scrolling"""
        headlines = self.get_all_headlines()
        if index < len(headlines):
            return self.format_headline(headlines[index], truncate=False)
        return "No headlines available"

def main():
    try:
        news_manager = SimpleNewsManager()
        
        if len(sys.argv) < 2:
            # Default: return multiple headlines
            headlines = news_manager.get_headlines_for_display(4)
            for headline in headlines:
                print(headline)
            return
        
        command = sys.argv[1].lower()
        
        if command == 'list':
            # Show multiple headlines
            num_lines = int(sys.argv[2]) if len(sys.argv) > 2 else 4
            headlines = news_manager.get_headlines_for_display(num_lines)
            for headline in headlines:
                print(headline)
        
        elif command == 'single':
            # Show single headline by index
            index = int(sys.argv[2]) if len(sys.argv) > 2 else 0
            headline = news_manager.get_single_headline(index)
            print(headline)
        
        elif command == 'count':
            # Get total number of headlines available
            headlines = news_manager.get_all_headlines()
            print(len(headlines))
        
        else:
            print(f"Usage: {sys.argv[0]} [list|single|count] [number]")
    
    except Exception as e:
        print("News service temporarily unavailable")

if __name__ == "__main__":
    main()