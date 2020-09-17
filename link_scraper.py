from selenium import webdriver

from selenium.webdriver.firefox.options import Options

# hiding browser
options = webdriver.FirefoxOptions()
options.add_argument('-headless')

# driver and url loading
geckodriver = 'D:\Python\geckodriver.exe'
driver = webdriver.Firefox(executable_path=geckodriver, options=options)
links = []
urls = ['https://www.betexplorer.com/next/soccer/', 'https://www.betexplorer.com/next/hockey/']
for url in urls:
    driver.get(url)
    # scraping match links from url
    elements = driver.find_elements_by_class_name("table-main__tt [href]")
    links_subpage = [link.get_attribute('href') for link in elements]
    for link in links_subpage:
        links.append(link)


print("links scrapped")
driver.quit()


"""
def execute(links):
    for link in links:
        driver = load_driver(link)
        match = get_match(driver)
        date = get_date(driver)
        if not odds_exist_check(driver)
            continue
        rows = get_rows(driver)
        cells = get_cells(driver)
        rows = row_truncate(rows)
        cells = fix_cell_list(cells)
        odds_objects = store_in_class(rows, cells, dictionary_home, dictionary_draw, dictionary_away)
        sort_by_odds(dictionary)
        get_best_odd(dictionary)
        Mecz = BestBet(match, date, get_best_odd(dictionary_home), ...)
        save_results(file, Mecz)
         
        
"""