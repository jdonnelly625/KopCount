# KopCount

Analyze the buzz around Liverpool FC players during match days!

## Overview

KopCount is a Python-based tool designed to track mentions of Liverpool FC players in match threads on the r/liverpoolfc subreddit. It provides insights into which players are most talked about during matches, allowing fans to gauge the hot topics of discussion in real-time. It scrapes using reddit's API PRAW to scrape for player mentions and transforms them into real time plots using matplotlib's pyplot. 

## Features

- **Real-time Tracking:** Continuously monitor match threads for player mentions.
- **Visual Analysis:** Plots the mentions over time for each player using pyplot from matplotlib.
- **Expandable Player List:** Easily add or remove players and their potential nicknames/aliases.

## Prerequisites

1. Python 3.x
2. PRAW library for Reddit API integration
3. MatPlotLib

## Setup & Installation

1. Clone the repository:
2. Navigate to the project directory and install the required libraries: pip install -r requirements.txt
3. Set up your Reddit API credentials:
- Go to [Reddit's App Preferences](https://www.reddit.com/prefs/apps).
- Create a new developer application to get your `client_id`, `client_secret`, and `user_agent`.
- Replace the placeholders in the `LFCAnalyzer.py` script with your credentials.

4. Run the script: python LFCAnalyzer.py

## How it Works

Once executed, KopCount will:
1. Access the specified Reddit subreddit.
2. Search for match threads posted within the day.
3. Extract and analyze the comments for mentions of Liverpool FC players, accounting for nicknames.
4. Plot the mentions in real-time, providing a visual representation of player mentions as the match progresses with pyplot from matplotlib.

## Limitations and Considerations

- **Reddit API Rate Limits:** Reddit imposes rate limits on how often you can make requests. This is more of an issue for when the script tries to fetch comments from particularly active threads. The use of the PRAW library helps in respecting these limits by handling potential rate-limit errors and waiting as required.

- **Comment Fetching Limitations:** Due to the nature of the Reddit API and PRAW, there are constraints on the number of comments that can be fetched at once. To mitigate this, KopCount fetches comments in chunks, ensuring that it captures as many relevant comments as possible within the constraints by sorting by timeframe. This might occasionally mean that some comments are missed during peak activity periods, but for most match threads, the data should be representative.

- **Time Sensitivity:** KopCount is designed to analyze match threads in real-time. While it can be used post-match, its primary utility is during live matches where it continually polls for new comments and updates the analysis.

- **Search Precision:** The tool relies on specific search terms (like "Match Thread") to find relevant threads. Variations in naming or case sensitivity can affect the results. However, the script incorporates case-insensitive checks to enhance its search precision.

- **Thread Selection:** The current implementation focuses on threads posted within the day to ensure relevancy. This might mean that very early or late posts around midnight could be missed. Adjusting the `time_filter` parameter in the script can change this behavior if necessary.

- **MoreComments Objects:** Due to the way PRAW structures comment trees, some comments are wrapped in "MoreComments" objects, especially in deeper comment chains. The script has logic to expand these when possible, but there's always a trade-off between completeness and performance.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

