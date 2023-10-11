import praw
import schedule
import time
from matplotlib import pyplot as plt
from datetime import datetime
from praw.exceptions import APIException
import re

class LFCAnalyzer:
    """Analyze and visualize mentions of LFC players in match threads."""

    def __init__(self):
        self.reddit = self.initialize_reddit()
        self.comment_counter = 0
        self.comments_seen = set()
        self.time_stamps = []
        self.last_checked_timestamp = None
        self.current_match_thread = None

        # Predefined player data
        players = {
            "Alisson": {
                "nicknames": [" ali", "alison", "alisson", "becker", "becks", "ali ", "alii"],
                "count": 0,
                "plot": []
            },
            "Adrian": {
                "nicknames": ["adrian"],
                "count": 0,
                "plot": []
            },
            "Van Dijk": {
                "nicknames": ["van dijk", "virg", "virgil", "dijk"],
                "count": 0,
                "plot": []
            },
            "Konate": {
                "nicknames": ["konate", "ibou", "ibra"],
                "count": 0,
                "plot": []
            },
            "Gomez": {
                "nicknames": ["joe", "gomez", "joey"],
                "count": 0,
                "plot": []
            },
            "Tsimikas": {
                "nicknames": ["tsimikas", "tsimi", "greek scouser", "greek", "kostas"],
                "count": 0,
                "plot": []
            },
            "Diaz": {
                "nicknames": ["luis", "diaz", "lucho"],
                "count": 0,
                "plot": []
            },
            "Nunez": {
                "nicknames": ["darwin", "nunez", "darwizzy", "chaos man", "chaos agent", "agent of chaos"],
                "count": 0,
                "plot": []
            },
            "Robertson": {
                "nicknames": ["andy", "andrew", "robertson", "robbo", "robo"],
                "count": 0,
                "plot": []
            },
            "Matip": {
                "nicknames": ["giraffe", "matip", "joel"],
                "count": 0,
                "plot": []
            },
            "Arnold": {
                "nicknames": ["taa", "trent", "arnold", "alexander arnold", "alexander-arnold"],
                "count": 0,
                "plot": []
            },
            "Thiago": {
                "nicknames": ["thiago", "alcantara"],
                "count": 0,
                "plot": []
            },
            "Jones": {
                "nicknames": ["curt", "jones", "curtis"],
                "count": 0,
                "plot": []
            },
            "Elliot": {
                "nicknames": ["elliot", "harv", "harvey", "harvs"],
                "count": 0,
                "plot": []
            },
            "Salah": {
                "nicknames": [" mo ", " mo.", "mooo", "mo!", "salah", "egyptian king", "sand messi"],
                "count": 0,
                "plot": []
            },
            "Jota": {
                "nicknames": ["jota", "diogo"],
                "count": 0,
                "plot": []
            },
            "Mac Allister": {
                "nicknames": ["alexis", "mac allister", "macca", "big mac", " mac", "mac "],
                "count": 0,
                "plot": []
            },
            "Szoboszlai": {
                "nicknames": ["dom ", "big dom", "szobo", "schlobbers", "szoboszlai", "szob", "sobossla", "dommy", " dom"],
                "count": 0,
                "plot": []
            },
            "Gravenberch": {
                "nicknames": ["ryan", "gravenberch", "grav", "gravy"],
                "count": 0,
                "plot": []
            },
            "Endo": {
                "nicknames": ["wataru", "endo", "legendo", "samurai"],
                "count": 0,
                "plot": []
            },
            "Bajcetic": {
                "nicknames": ["stefan", "baj", "bajcetic", "stef"],
                "count": 0,
                "plot": []
            },
            "Gakpo": {
                "nicknames": ["gakpo", "cody"],
                "count": 0,
                "plot": []
            },
            "Quansah": {
                "nicknames": ["jarrel", "jarel", "jarell", "quans", "quansah"],
                "count": 0,
                "plot": []
            },
            "Doak": {
                "nicknames": ["doak", "ben doak", "doaky"],
                "count": 0,
                "plot": []
            }

        }

        # Splitting the player data for easy access and modification
        self.playerNames = {name: data["nicknames"] for name, data in players.items()}
        self.playerCounts = {name: data["count"] for name, data in players.items()}
        self.playerPlots = {name: data["plot"] for name, data in players.items()}
    

    def initialize_reddit(self):
        """Initialize PRAW instance for Reddit access."""
        return praw.Reddit(
                client_id="YOUR_ID",
                client_secret="YOUR_SECRET",
                user_agent="<console:LFC:1.0>"

        )
    @staticmethod
    def convert_timestamp(unix_timestamp):
        return datetime.utcfromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')

    def write_comment_to_file(self, comment, player):
        """Writes a comment, its timestamp, and the associated player to test.txt."""
        
            
        # print(f"Timestamp: {self.convert_timestamp(comment.created_utc)}, Player: {player}, Comment: {comment.body}\n")
        
    def find_match_thread(self):
        lfc = self.reddit.subreddit("liverpoolfc")
        for post in lfc.search("Match Thread", time_filter="day"):
            if "match thread" in post.title.lower():
                self.current_match_thread = post
                break
            
    def check_for_players(self, comment):
        print("CHECKING FOR PLAYERS")
        """Check a comment for mentions of player names."""
        for player, names in self.playerNames.items():
            if any(name in comment.body.lower() for name in names):
                self.playerCounts[player] += 1
                self.write_comment_to_file(comment, player)
                
    


    def update_plot(self):
        print("UPDATING PLOT")
        """Visualize player mention data."""
        plt.clf()
    
        # Plot each player from playerPlots over time
        for player, plot_data in self.playerPlots.items():
            plt.plot(self.time_stamps, plot_data, linewidth=0.7)
    
        # Annotate the last point for each player with the players name
        for player, plot_data in self.playerPlots.items():
            if self.time_stamps and plot_data:  # ensure there's data to annotate
                plt.annotate(player, (self.time_stamps[-1], plot_data[-1]), fontsize=5)
    
        plt.xlabel("Time")
        plt.ylabel("Number of Mentions")
        plt.title("LFC Match Thread Hot Topic")
        plt.pause(0.05)
        plt.show()




    def process_comments(self):
        """Fetch and process comments from LFC match threads."""
        try:
            print("PROCESSING COMMENTS")
            
            if self.current_match_thread is None:
                self.find_match_thread()
    
            # Check if match thread was found
            if self.current_match_thread is None:
                print("No match thread found for today.")
                return
            post = self.current_match_thread
            
            # Fetch the newest 100 comments
            post.comment_sort = 'new'
            post.comment_limit = 100
            
            # Create an empty list to store the final top-level comments
            all_comments = []
    
            # Iterating over top-level items (comments + MoreComments objects aka "load more comments")
            for item in post.comments:
                if isinstance(item, praw.models.MoreComments):
                    # Load the additional top-level comments represented by this MoreComments object
                    more_comments = item.comments()
                    all_comments.extend(more_comments)
                else:
                    all_comments.append(item)
            
            
            # If this is the first run, just set the latest comment's timestamp to 0
            if self.last_checked_timestamp is None:
                self.last_checked_timestamp = 0
    
            # Process comments newer than the last checked timestamp.
            for comment in all_comments:
                if comment.created_utc <= self.last_checked_timestamp:
                    break
                    
                if hasattr(comment, "body") and comment.id not in self.comments_seen:
                    self.check_for_players(comment)
                    self.comments_seen.add(comment.id)
    
            # Update the last checked timestamp.
            self.last_checked_timestamp = all_comments[0].created_utc
    
            # Update time and counts, to add another minute to the plot axis
            self.comment_counter += 1
            self.time_stamps.append(self.comment_counter)
            
            # add the new counts for y axis
            for player in self.playerNames.keys():
                self.playerPlots[player].append(self.playerCounts[player])
                
            # Checking and printing rate limit status
            limits = self.reddit.auth.limits
            print(f"Remaining requests: {limits['remaining']}")
            print(f"Rate limit will reset at: {limits['reset_timestamp']}")
            
            #Update the plot
            self.update_plot
        except APIException as e:
            if e.error_type == "RATELIMIT":
                # Extract the delay from e.message. 
                # The message typically looks like: "You are doing that too much. Try again in X minutes."
                delay = int(re.search(r"(\d+)", e.message).group(1)) * 60  # Convert minutes to seconds
                print(f"Rate Limit Exceeded! Waiting for {delay} seconds.")
                time.sleep(delay)
                
            else:
                print(f"APIException: {e}")

       

    def run(self):
        
        """Execute analyzer at regular intervals."""
        print("RUNNING")
        #process comments every minute
        schedule.every(1).minute.do(self.process_comments)
        
        #Run until manually cancelled
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    print("Starting program")
    analyzer = LFCAnalyzer()
    print("Analyzer initialized")
    analyzer.run()