import threading
from queue import Queue
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import pandas as pd
from features_extraction import FeaturesExtraction
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from tqdm import tqdm

disable_warnings(InsecureRequestWarning)

# Global counters using thread-safe data structures
phishing_count = threading.local()
legitimate_count = threading.local()

def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.default_content_setting_values.notifications": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)
    return webdriver.Chrome(options=chrome_options)

def worker(queue, output_file, label, columns_lock):
    phishing_count.value = 0
    legitimate_count.value = 0

    driver = initialize_driver()
    driver.set_page_load_timeout(2)

    try:
        while True:
            url = queue.get()
            if url is None:
                break

            try:
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                extractor = FeaturesExtraction(driver, soup, url)
                vector = extractor.create_vector()
                vector.append(str(url))
                vector.append(label)

                # Write single row immediately to file with thread-safe lock
                with columns_lock:
                    df_row = pd.DataFrame([vector], columns=get_feature_columns())
                    df_row.to_csv(output_file, mode='a', header=False, index=False)

                # Update counters safely
                if label == 1:
                    phishing_count.value += 1
                    print(f"\rProcessed phishing sites: {phishing_count.value}", end="")
                elif label == 0:
                    legitimate_count.value += 1
                    print(f"\rProcessed legitimate sites: {legitimate_count.value}", end="")

            except TimeoutException:
                print(f"Timeout while loading URL: {url}")
            except Exception as e:
                print(f"Error processing URL {url}: {e}")
            finally:
                queue.task_done()
    finally:
        driver.quit()

def process_urls_threaded(input_file, output_file, label, start_row=0, end_row=1000, num_threads=4):
    nrows = end_row - start_row

    if label == 1:
        columns = ['phish_id', 'url', 'phish_detail_url', 'submission_time',
                   'verified', 'verification_time', 'online', 'target']
        data_frame = pd.read_csv(input_file,
                                 header=0,
                                 skiprows=range(1, start_row + 1),
                                 nrows=nrows,
                                 usecols=columns)
        URL_list = data_frame['url'].to_list()
    else:
        data_frame = pd.read_csv(input_file,
                                 skiprows=start_row,
                                 nrows=nrows,
                                 names=['rank', 'domain'],
                                 header=None)
        URL_list = ['http://' + domain for domain in data_frame['domain'].to_list()]

    url_queue = Queue()
    columns_lock = threading.Lock()
    threads = []

    if not pd.io.common.file_exists(output_file):
        html_columns = get_feature_columns()
        pd.DataFrame(columns=html_columns).to_csv(output_file, index=False)

    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(url_queue, output_file, label, columns_lock))
        t.daemon = True
        t.start()
        threads.append(t)

    with tqdm(total=len(URL_list), desc="Processing URLs") as pbar:
        for url in URL_list:
            url_queue.put(url)
            pbar.update(1)

    for _ in range(num_threads):
        url_queue.put(None)
    for t in threads:
        t.join()

def get_feature_columns():
    basic_columns = [
        'has_title', 'has_submit', 'has_link', 'has_email_input',
        'number_of_inputs', 'number_of_buttons', 'number_of_images',
        'number_of_option', 'number_of_list', 'number_of_href',
        'number_of_paragraph', 'number_of_script', 'length_of_title',
        'has_h1', 'has_h2', 'has_h3', 'length_of_text',
        'number_of_clickable_button', 'number_of_a', 'number_of_div',
        'has_footer', 'number_of_forms', 'has_text_area', 'has_iframe',
        'has_text_input', 'number_of_meta', 'has_nav', 'number_of_sources',
        'number_of_span', 'number_of_table', 'RequestURL' , 'AnchorURL',
        'Favicon', 'LinksInScriptTags', 'ServerFormHandler' ,'InfoEmail'
    ]

    dynamic_columns = [
        'has_mouse_tracking', 'has_keyboard_monitoring',
        'has_popups','number_of_hidden_element',
        'page_redirect','form_redirect_behavior','external_form_action'
    ]

    password_columns = [
        'password_type_count','password_name_id_count',
        'hidden_password_count','form_with_password'
    ]

    js_columns = [
        'clipboard_monitoring','form_data_collection','cookie_manipulation'
    ]

    url_features_columns = [
        'UsingIp',
        'longUrl',
        'shortUrl',
        'symbol',
        'redirecting',
        'prefixSuffix',
        'SubDomains',
        'Hppts',
        'DomainRegLen',
        'NonStdPort',
        'HTTPSDomainURL',
        'AbnormalURL',
        'WebsiteForwarding',
        'StatusBarCust',
        'DisableRightClick',
        'UsingPopupWindow',
        'IframeRedirection',
        'AgeofDomain',
        'DNSRecording',
        'WebsiteTraffic',
        'PageRank',
        'GoogleIndex',
        'LinksPointingToPage',
        'StatsReport'
    ]

    metadata_columns=['URL','label']

    return basic_columns+dynamic_columns+password_columns+js_columns+url_features_columns+metadata_columns

if __name__ == "__main__":
     PHISH_THREADS=32
     LEGITIMATE_THRESHOLD=16

     start_row_phishing=21000
     end_row_phishing=start_row_phishing+1000

     start_row_legitimate=24100
     end_row_legitimate=start_row_legitimate+200


     # print("Processing phishing websites...")
     # process_urls_threaded(
     #     "verified_online.csv",
     #     "phishing_websites.csv",
     #     label=1,
     #     start_row=start_row_phishing,
     #     end_row=end_row_phishing,
     #     num_threads=PHISH_THREADS,
     # )

     print("Processing legitimate websites...")
     process_urls_threaded(
         "tranco_list.csv",
         "legitimate_websites.csv",
         label=0,
         start_row=start_row_legitimate,
         end_row=end_row_legitimate,
         num_threads=LEGITIMATE_THRESHOLD,
     )

     print("Processing completed!")
