import sys
from dotenv import load_dotenv
load_dotenv()

from helpers import create_scheduled_query

def main():
    try:
        schedule = sys.argv[1]
        create_scheduled_query(schedule=schedule)
    except IndexError:
        raise Exception("Please specify schedule for the query.")

if __name__ == "__main__":
    main()