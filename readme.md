# Escape Room Scraper

This project is a web scraper designed to collect information about escape rooms from Google Maps across multiple cities in the United States.

## Description

The Escape Room Scraper uses Selenium WebDriver to automate Google Maps searches for escape rooms in specified cities. It collects detailed information about each escape room, including name, address, phone number, website URL, hours of operation, reviews, and social media links.

## Project Structure

The project consists of the following files:

1. `escape_room_scraper_100.py`: The main Python script that performs the web scraping.
2. `requirements.txt`: A file listing all the Python dependencies required for this project.
3. `README.md`: This file, providing information about the project and how to use it.
4. `escape_rooms_data_100.json`: The output file where scraped data is stored (generated after running the script).

## Requirements

- Python 3.7+
- Selenium WebDriver
- Chrome browser
- ChromeDriver (automatically managed by webdriver_manager)

## Installation

1. Clone this repository:
git clone https://github.com/Pratyush-12345/breakout.git


2. Install the required Python packages:
pip install -r requirements.txt


## Usage

1. Run the scraper:

python app.py


2. The script will start scraping data from Google Maps for escape rooms in various cities.

3. Once complete, the data will be saved to `escape_rooms_data_100.json` in the same directory.

## File Descriptions

### escape_room_scraper_100.py

This is the main Python script that performs the web scraping. It includes functions for:
- Setting up the Selenium WebDriver
- Searching for escape rooms on Google Maps
- Scraping individual escape room profiles
- Managing multi-threaded scraping across multiple cities

### requirements.txt

This file lists all the Python packages required to run the scraper. It includes:


### README.md

This file, which provides documentation for the project.

### escape_rooms_data_100.json

This is the output file generated after running the scraper. It contains the scraped data in JSON format, including information about approximately 100 escape rooms across multiple cities.

## Features

- Multi-threaded scraping for improved speed
- Automatic handling of ChromeDriver installation
- Error handling and logging
- Random delays to avoid detection
- Scrolling to load more results

## Customization

You can modify the list of cities or the number of results by editing the `cities` list and the `total_results` parameter in the `escape_room_scraper_100.py` file.

## Disclaimer

Web scraping may be against the terms of service of some websites. Use this script responsibly and ensure you have the right to scrape the data you're collecting.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/yourusername/escape-room-scraper/issues) if you want to contribute.

## License

[MIT](https://choosealicense.com/licenses/mit/)

