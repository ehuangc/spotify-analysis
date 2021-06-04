This program uses the Spotify API to analyze a user's listening habits over 3 periods of time (the last month, the last 6 months, and over all-time). A Spotify account and some version of Python 3 are required to run the program. To run the program, first enter "pip install -r requirements.txt" into the terminal to install the necessary dependencies. Then, just enter "python3 spotify.py" into the terminal and authenticate with Spotify when prompted. NOTE: The program may take a few seconds to fetch your Spotify data, so please be patient!

Our program runs as a terminal app using the Spotipy module, a Python wrapper for the Spotify API. First, it prompts the user to authenticate with Spotify using their authorization code flow. Then, we pull the user's listening data over 3 periods of time and input the data into a pandas DataFrame. The data we pull are audio features about tracks provided by Spotify. We print out the data in tabular form using the tabulate module, and then visualize the data using histograms created by the seaborn module. Specifically, we use seaborn's subplots function to create multiple historgrams in one window, allowing the user to easily compare their listening data over different periods of time.

Mainatainer Info: Edward Huang (ehuangc@stanford.edu)

Credits: The CS41 teaching team, numerous Spotipy tutorials on the internet
