from config import *
from scraper import Scraper

def main():
    scraper = Scraper()
    for i in range(100):
        if scraper.collect_names("12345"):
            break
    scraper.search_contact()
    scraper.quit()


if __name__ == "__main__":
    main()