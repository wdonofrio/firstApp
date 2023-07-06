import logging

# Configure the root logger to output to the console and a file called Game.log
logging.basicConfig(
    filename="Game.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S%p",
)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(levelname)s: %(message)s")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)

# Create a logger
logger = logging.getLogger("Game")
