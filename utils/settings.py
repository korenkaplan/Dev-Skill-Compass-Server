# max number of workers to perform the multiprocessing web scraping
MAX_NUMBER_OF_WORKERS = 3

# max amount of tries to scrape listings for role if failed
MAX_NUMBER_OF_RETRIES_SCARPING = 10

# number of categories to show beside all categories
NUMBER_OF_CATEGORIES = 4

# limit of items per category list in the website
NUMBER_OF_ITEMS_PER_CATEGORY = 10

# limit of items per category list in the website
NUMBER_OF_ITEMS_ALL_CATEGORIES = 20

# cache ttl 24 hours
CACHE_TTL: int = 60 * 60 * 24

# number of months to aggregate backwards
NUMBER_OF_MONTHS_TO_AGGREGATE = 4

# ============= Google Jobs ========================
SHOW_FULL_DESCRIPTION_BUTTON_XPATH_GOOGLE_JOBS = "/html/body/div[2]/div/div[2]/div[1]/div/div/div[3]/div[2]/div/div[1]/div/div/div[4]/g-expandable-container/div/div/div/div/div/div/g-expandable-content/span/div/g-inline-expansion-bar/div[1]/div"
EXPANDABLE_JOB_DESCRIPTION_TEXT_XPATH_GOOGLE_JOBS = "/html/body/div[2]/div/div[2]/div[1]/div/div/div[3]/div[2]/div/div[1]/div/div/div[4]/g-expandable-container/div/div/div/span"
NOT_EXPANDABLE_JOB_DESCRIPTION_TEXT_XPATH_GOOGLE_JOBS = "/html/body/div[2]/div/div[2]/div[1]/div/div/div[3]/div[2]/div/div[1]/div/div/div[4]/g-expandable-container/div/div/span"
