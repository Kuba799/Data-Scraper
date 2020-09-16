from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium import webdriver
from bet import SingleGame, BestBet
import link_scraper
from openpyxl import load_workbook

# hiding browser
options = webdriver.FirefoxOptions()
options.add_argument('-headless')

# driver and url loading, you have to download geckodriver and define path here
geckodriver = 'D:\Python\geckodriver.exe'


# getting match name from site
def get_match(driver):
    for match in driver.find_elements_by_css_selector(
            "li.list-breadcrumb__item:nth-child(5)"):
        match = match.text
    return match


def get_league(driver):
    for league in driver.find_elements_by_css_selector("li.list-breadcrumb__item:nth-child(4) > a:nth-child(1)"):
        league = league.txt
    return league


# getting date
def get_date(driver):
    for date in driver.find_elements_by_id("match-date"):
        date = date.text
    return date


def sort_by_odds(dictionary):
    # yield sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
    list_sorted = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
    return list_sorted


def get_best_odd(dictionary, number=1):
    top_list = []
    # odd_list = next(sort_by_odds(dictionary))
    odd_list = sort_by_odds(dictionary)
    for i in odd_list:
        if odd_list.index(i) < number:
            top_list.append(odd_list[odd_list.index(i)])
    return top_list


def get_rows(driver):
    # getting rows odds table
    for table in driver.find_elements_by_xpath('//*[@id="sortable-1"]'):
        rows = table.find_elements_by_tag_name("tr")
    return rows


def get_cells(driver):
    # getting cells from odds table
    for table in driver.find_elements_by_xpath('//*[@id="sortable-1"]'):
        cells = table.find_elements_by_tag_name("td")
    return cells


def fix_cells(driver, table_cell):
    index = 0
    jump = 6
    increment1 = 1
    increment2 = 2
    increment3 = 3
    table_cell_fixed = []
    for cell in table_cell:
        try:
            if driver.find_element_by_class_name('h-text-right'):
                jump = 7
                if index == increment3:
                    increment3 += jump
                    index += 1
                    continue
        except NoSuchElementException:
            pass

        if index == increment1:
            increment1 += jump
            index += 1
            continue
        elif index == increment2:
            increment2 += jump
            index += 1
            continue

        table_cell_fixed.append(table_cell[index])
        index += 1

    return table_cell_fixed


def append_to_file(xlsx_file, BestBet):
    new_row_data = [
        [BestBet.game, BestBet.date, BestBet.book_home, BestBet.odd_home,
         BestBet.book_draw, BestBet.odd_draw, BestBet.book_away, BestBet.odd_away, BestBet.margin], ]
    wb = load_workbook(xlsx_file)
    # Select First Worksheet
    ws = wb.worksheets[0]

    for row_data in new_row_data:
        # Append Row Values
        ws.append(row_data)

    wb.save(xlsx_file)


file = "zaklady.xlsx"

while True:
    driver = webdriver.Firefox(executable_path=geckodriver, options=options)

    for link in link_scraper.links[80:]:

        url = link
        driver.get(url)

        html = driver.page_source

        #print(get_match(driver))

        # Checking if any odds exists
        try:
            if driver.find_element_by_id("no-odds-info"):
                continue
        except NoSuchElementException:
            pass

        try:
            table_row = get_rows(driver)
            table_cell = get_cells(driver)
        except UnboundLocalError as e:
            print(get_match(driver), "Skipped because of:", e)
            continue

        # store_rows_and_cells(driver)

        """
        print("table_row before truncating")
        for row in table_row:
            print(row.text)
        """

        # Deleting the first row 'BOOKMAKERS: ...', 'Average odds row', 'Add to my selection' row if exists and
        del table_row[0]
        table_row = table_row[:-1]
        try:
            if driver.find_elements_by_css_selector("#match-add-to-selection > tr:nth-child(2) > td:nth-child(4)"):
                table_row = table_row[:-1]
        except NoSuchElementException:
            pass

        """
        print("PRINTING ROWS FROM TABLE_ROW AFTER TRUNCATING")
        for row in table_row:
            print(row.text)
        """

        # fixing cell table - deleting free spaces
        index = 0
        jump = 6
        increment1 = 1
        increment2 = 2
        increment3 = 3
        table_cell_fixed = []
        for cell in table_cell:
            try:
                if driver.find_element_by_class_name('h-text-right'):
                    jump = 7
                    if index == increment3:
                        increment3 += jump
                        index += 1
                        continue
            except NoSuchElementException:
                pass

            if index == increment1:
                increment1 += jump
                index += 1
                continue
            elif index == increment2:
                increment2 += jump
                index += 1
                continue

            table_cell_fixed.append(table_cell[index])
            index += 1

            # print(cell.text)

        """
        print("***********************************************************")
        print("PRINTING CELLS FROM table_cell_fixed")
        for cell in table_cell_fixed:
            print(cell.text)
        
        
        for obj in odds_object_list:
            other_object.add(obj)
        
        objs[0].do_sth()
        """

        # CREATING AND APPENDING LIST OF MATCH ODDS OBJECTS AND OMITTING ONE BOOKMAKER
        index = 0
        odds_object_list = []
        dictionary_home = {}
        dictionary_draw = {}
        dictionary_away = {}
        try:
            for rows in table_row:
                if table_cell_fixed[index].text == "Betfair Exchange":
                    continue
                odds_object_list.append(SingleGame(get_match(driver), get_date(driver),
                                                   table_cell_fixed[index].text, table_cell_fixed[index + 1].text,
                                                   table_cell_fixed[index + 2].text,
                                                   table_cell_fixed[index + 3].text))
                dictionary_home[table_cell_fixed[index].text] = table_cell_fixed[index + 1].text
                dictionary_draw[table_cell_fixed[index].text] = table_cell_fixed[index + 2].text
                dictionary_away[table_cell_fixed[index].text] = table_cell_fixed[index + 3].text
                index += 4

        except StaleElementReferenceException as e:
            print(get_match(driver), "skipped, because of", e)
            continue

        """
        for object in odds_object_list:
            print(object.get_single_game())
        """

        Match = BestBet(get_match(driver), get_date(driver), get_best_odd(dictionary_home)[0][0],
                        get_best_odd(dictionary_home)[0][1], get_best_odd(dictionary_draw)[0][0],
                        get_best_odd(dictionary_draw)[0][1], get_best_odd(dictionary_away)[0][0],
                        get_best_odd(dictionary_away)[0][1])

        highest_margin = 1.022
        if Match.margin < highest_margin:
            print(Match.get_best_bet())
            if Match.book_home == "Unibet" or Match.book_draw == "Unibet" or Match.book_away == "Unibet":
                print("***************************************!!!!!!!!!!!!!!!!!!!!!BET"
                      "!!!!!!!!!!!!!!!!!!!!!***************************************")

            # append_to_file(file, Mecz)

    driver.quit()
