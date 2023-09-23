import praw
import schedule
import time
from matplotlib import pyplot as plt

class LFCAnalyzer:
    """Analyze and visualize mentions of LFC players in match threads."""

    def __init__(self):
        self.reddit = self.initialize_reddit()
        self.comment_counter = 0
        self.comments_seen = set()
        self.time_stamps = []
        self.last_checked_timestamp = None

        # Predefined player data
        players = {
            "Alisson": {
                "nicknames": ["ali", "alison", "alisson", "becker", "becks"],
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
                "nicknames": ["joe", "gomez"],
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
                "nicknames": ["darwin", "nunez", "darwizzy"],
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
                "nicknames": ["alexis", "mac allister", "macca", "big mac", "mac"],
                "count": 0,
                "plot": []
            },
            "Szoboszlai": {
                "nicknames": ["dom", "big dom", "szobo", "schlobbers", "szoboszlai", "szob"],
                "count": 0,
                "plot": []
            },
            "Gravenberch": {
                "nicknames": ["ryan", "gravenberch", "grav", "ry", "gravy"],
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
                "nicknames": ["jarrel", "jarel", "jarell", "quans", "jar", "quansah"],
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
                client_id="YOUR_CLIENT_ID",
                client_secret="YOUR_SECRET",
                user_agent="<console:LFC:1.0>"

        )

    def check_for_players(self, comment):
        """Check a comment for mentions of player names. If player found in comment update count"""
        for player, names in self.playerNames.items():
            if any(name in comment.body.lower() for name in names):
                self.playerCounts[player] += 1

    def update_plot(self):
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
        lfc = self.reddit.subreddit("liverpoolfc")
        for post in lfc.search("Match Thread", time_filter="day"):
            #confirm it is a match thread, not related thread or similar
            if "match thread" in post.title.lower():
                # Replace "MoreComments" objects with actual comments.
                post.comments.replace_more(limit=None)
                all_comments = post.comments.list()
    
                # Sort comments by their creation timestamp
                all_comments.sort(key=lambda x: x.created_utc, reverse=True)
                
                # If this is the first run, just set the latest comment's timestamp.
                if self.last_checked_timestamp is None:
                    # Set to a very old timestamp to ensure all comments are processed the first time.
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

        # Update time and counts
        self.comment_counter += 1
        self.time_stamps.append(self.comment_counter)
        for player in self.playerNames.keys():
            self.playerPlots[player].append(self.playerCounts[player])

    def run(self):
        """Execute analyzer at regular intervals."""
        print("Running")
        schedule.every(1).minute.do(self.process_comments)
        schedule.every(1).minute.do(self.update_plot)
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    analyzer = LFCAnalyzer()
    analyzer.run()