# Conky Trading Dashboard# Enhanced Conky Configuration with Trading212 Integration



A comprehensive conky configuration for trading, news, weather, and system monitoring with clean, portable setup.This enhanced Conky configuration displays your Trading212 portfolio data alongside comprehensive system monitoring, weather information, and market data.



## Features## Features



✅ **Trading 212 Portfolio**### Trading212 Portfolio Display

- Live portfolio value, P&L, cash balance- **Total Portfolio Value** - Your complete portfolio worth

- Position count and pending orders- **Profit & Loss (P&L)** - Current gains/losses with percentage

- **Free Cash** - Available cash balance

✅ **Scrolling News Headlines**  - **Invested Amount** - Total amount invested

- Vertical scrolling through multiple headlines- **Position Count** - Number of open positions

- Horizontal scrolling for long titles- **Pending Orders** - Number of pending trades

- Multiple sources: BBC, Guardian, Sky News, Hacker News, TechCrunch- **Top Position** - Your largest holding by value

- **API Status** - Connection status indicator

✅ **Weather & Astronomy**

- Current weather for your location### Enhanced System Monitoring

- Sunrise/sunset times and day length- **Performance Metrics** - CPU usage, RAM, disk I/O, temperatures

- Moon phase information- **Network Information** - Speed graphs, IP addresses, data usage

- **Process Monitoring** - Top CPU-consuming processes

✅ **System Monitoring**- **Hardware Info** - CPU frequency, GPU temperature (NVIDIA)

- CPU, RAM, disk usage

- Network speeds and IP address### Market & Weather Data

- System uptime and load- **London Weather** - Current conditions, humidity, wind

- **Market Indices** - FTSE 100, GBP/USD, Bitcoin prices

✅ **Market Data**- **Real-time Updates** - Automatic refresh intervals

- GBP/USD exchange rate

- Extensible for more currency pairs## Setup Instructions



## Quick Setup### 1. Install Dependencies



1. **Copy the entire conky folder** to `~/.config/conky/`First, install the required Python package for API requests:

2. **Run setup script**: `cd ~/.config/conky && ./setup.sh`

3. **Configure Trading212** (optional): Edit `trading212_config.json` with your API key```bash

4. **Adjust location** (optional): Edit `config.json` for your locationpip3 install requests

5. **Start conky**: `conky -c ~/.config/conky/conky.conf````



## File Structure### 2. Configure Trading212 API Access



```#### Get Your API Credentials

~/.config/conky/1. Open the **Trading212 mobile app**

├── config.json              # 🔧 Main configuration (location, news sources, etc.)2. Go to **Settings** → **API**

├── conky.conf               # 🖥️  Conky display configuration  3. Generate your **API Key** and **API Secret**

├── trading212_config.json   # 💰 Trading212 API credentials4. **Important**: Store these securely - they provide full account access

├── requirements.txt         # 📦 Python dependencies

├── setup.sh                 # 🚀 Automated setup scriptFor detailed instructions, visit: [Trading212 API Key Guide](https://helpcentre.trading212.com/hc/en-us/articles/14584770928157-Trading-212-API-key)

├── news_simple.py           # 📰 Simple news headlines fetcher

├── sun_moon.py              # 🌅 Sunrise/sunset/moon phases#### Configure the API Keys

├── trading212_api.py        # 💹 Trading212 API integration1. Edit the configuration file:

└── README.md               # 📖 This file   ```bash

```   nano ~/.config/conky/trading212_config.json

   ```

## Configuration

2. Replace the placeholder values:

### Location Settings   ```json

Edit `config.json` to change location (affects weather, sunrise/sunset):   {

```json     "api_key": "YOUR_ACTUAL_API_KEY_HERE",

"location": {     "api_secret": "YOUR_ACTUAL_API_SECRET_HERE",

  "name": "London",     "update_interval": 300,

  "latitude": 51.5074,     "cache_duration": 60,

  "longitude": -0.1278,     "preferences": {

  "timezone_offset_hours": 1       "currency_symbol": "£",

}       "show_percentages": true,

```       "show_ticker_suffixes": false,

       "max_positions_display": 5

### News Sources     }

Add/remove news sources in `config.json`:   }

```json   ```

"news": {

  "sources": {### 3. Make Scripts Executable

    "bbc": "http://feeds.bbci.co.uk/news/rss.xml",

    "guardian": "https://www.theguardian.com/uk/rss"```bash

  }chmod +x ~/.config/conky/trading212_api.py

}```

```

### 4. Test the Setup

### Trading212 Setup

Create `trading212_config.json`:Test the API connection:

```json```bash

{cd ~/.config/conky/

  "api_key": "your_api_key_here",python3 trading212_api.py status

  "demo": false```

}

```Test individual data points:

```bash

## Backup & Restorepython3 trading212_api.py total_value

python3 trading212_api.py total_ppl

To backup your setup:python3 trading212_api.py free_cash

```bash```

tar -czf conky-dashboard-backup.tar.gz ~/.config/conky/

```### 5. Start Conky



To restore on a new system:```bash

```bashconky -c ~/.config/conky/conky.conf

tar -xzf conky-dashboard-backup.tar.gz -C ~/```

cd ~/.config/conky && ./setup.sh

```Or add to your startup applications.



## Troubleshooting## Configuration Options



- **News not loading**: Check internet connection, RSS feeds may be temporarily down### Update Intervals

- **Trading212 errors**: Verify API key in `trading212_config.json`- **Trading212 Data**: 300 seconds (5 minutes)

- **Location issues**: Update coordinates in `config.json`- **System Stats**: 2 seconds

- **Python errors**: Run `./setup.sh` to reinstall dependencies- **Weather**: 1800 seconds (30 minutes)  

- **Market Data**: 600 seconds (10 minutes)

## Manual Commands- **API Status**: 60 seconds



Test individual components:### Customization

```bash

# Test news#### Color Scheme

# Test news
~/.config/.venv/bin/python ~/.config/conky/news_simple.py listThe Silent Hill aesthetic uses:

- `color1` (aa4444) - Rust red headers

# Test sun/moon- `color2` (888888) - Fog grey secondary text

~/.config/.venv/bin/python ~/.config/conky/sun_moon.py all- `color3` (666666) - Dark grey lines

- `color4` (cccccc) - Light grey labels

# Test trading212- `color5` (44aa44) - Profit green

~/.config/.venv/bin/python ~/.config/conky/trading212_api.py total_value- `color6` (dd4444) - Loss red

```
#### Display Preferences
Edit `trading212_config.json` to customize:
- **currency_symbol**: Change display currency (£, $, €)
- **show_percentages**: Enable/disable percentage displays
- **max_positions_display**: Limit number of positions shown

### Available Data Points

The `trading212_api.py` script supports these arguments:
- `total_value` - Complete portfolio value
- `total_ppl` - Profit/loss with percentage and color coding
- `free_cash` - Available cash balance
- `invested` - Total invested amount
- `positions_count` - Number of open positions
- `pending_orders` - Number of pending orders
- `top_position` - Largest position by value
- `status` - API connection status

## Troubleshooting

### Common Issues

1. **"API Error" or "N/A" displayed**
   - Check your API credentials in `trading212_config.json`
   - Verify internet connection
   - Ensure Trading212 API is accessible

2. **Permission errors**
   - Make sure the script is executable: `chmod +x trading212_api.py`
   - Check file permissions on config file

3. **Python import errors**
   - Install requests: `pip3 install requests`
   - Use correct Python version: `python3` not `python`

4. **Network/GPU temperature not showing**
   - Install appropriate drivers and monitoring tools
   - Adjust hardware monitoring commands for your system

### Rate Limiting
Trading212 API has rate limits:
- Portfolio data: 1 request per 5 seconds
- Account info: 1 request per 30 seconds
- Orders: 1 request per 5 seconds

The configuration respects these limits with appropriate update intervals.

### Security Notes
- **Never share your API credentials**
- **Use IP restrictions** in Trading212 settings if possible
- **Monitor API usage** through Trading212 dashboard
- **Revoke keys immediately** if compromised

## Support

For issues:
1. Check Trading212 API documentation: https://t212public-api-docs.redoc.ly/
2. Verify Conky configuration syntax
3. Test API script independently
4. Check system logs for errors

## API Limits & Beta Notes

- Trading212 API is currently in beta
- Live trading supports only Market Orders via API
- Rate limits are per-account regardless of API key used
- Some features may change during beta period

The configuration automatically handles API errors and displays fallback information when services are unavailable.