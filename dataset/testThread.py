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
import time
from tqdm import tqdm

disable_warnings(InsecureRequestWarning)

# 全局计数器和锁
phishing_count = 0
legitimate_count = 0
lock = threading.Lock()


def worker(queue, data_list, label, max_count):
    global phishing_count, legitimate_count

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.default_content_setting_values.notifications": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(3)

    try:
        while True:
            url = queue.get()
            if url is None:
                break

            with lock:
                if ((label == 1 and phishing_count >= max_count) or
                        (label == 0 and legitimate_count >= max_count)):
                    queue.task_done()
                    continue

            print(f"\nProcessing URL: {url}")
            try:
                driver.get(url)
                print(f"Successfully loaded URL: {url}")

                soup = BeautifulSoup(driver.page_source, 'html.parser')
                extractor = FeaturesExtraction(driver, soup)
                vector = extractor.create_vector()
                vector.append(str(url))
                vector.append(label)

                with lock:
                    if label == 1 and phishing_count < max_count:
                        data_list.append(vector)
                        phishing_count += 1
                        print(f"\rProcessed phishing sites: {phishing_count}/{max_count}", end="")
                    elif label == 0 and legitimate_count < max_count:
                        data_list.append(vector)
                        legitimate_count += 1
                        print(f"\rProcessed legitimate sites: {legitimate_count}/{max_count}", end="")
            except TimeoutException:
                print(f"Timeout while loading URL: {url}")
                driver.quit()
                driver = webdriver.Chrome(options=chrome_options)
            except Exception as e:
                print(f"Error processing URL {url}: {str(e)}")
                continue
            finally:
                queue.task_done()
    finally:
        driver.quit()


def process_urls_threaded(input_file, output_file, label, num_threads=4, max_count=100):
    global phishing_count, legitimate_count

    if label == 1:
        phishing_count = 0
    else:
        legitimate_count = 0

    if label == 0:
        data_frame = pd.read_csv(input_file, names=['id', 'url'])
        URL_list = ["http://" + url for url in data_frame['url'].to_list()]
    else:
        data_frame = pd.read_csv(input_file)
        URL_list = data_frame['url'].to_list()

    url_queue = Queue()
    data_list = []

    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(url_queue, data_list, label, max_count))
        t.daemon = True
        t.start()
        threads.append(t)

    with tqdm(total=max_count, desc="Processing URLs") as pbar:
        for url in URL_list:
            with lock:
                if (label == 1 and phishing_count >= max_count) or \
                        (label == 0 and legitimate_count >= max_count):
                    break
            url_queue.put(url)
            if label == 1:
                pbar.update(phishing_count)
            else:
                pbar.update(legitimate_count)

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
            'number_of_span', 'number_of_table'
        ]

        dynamic_columns = [
            'has_mouse_tracking', 'has_keyboard_monitoring', 'has_popups',
            'number_of_hidden_element', 'page_redirect', 'form_redirect_behavior',
            'external_form_action'
        ]

        password_columns = [
            'password_type_count', 'password_name_id_count',
            'hidden_password_count', 'form_with_password'
        ]

        js_columns = [
            'clipboard_monitoring', 'form_data_collection', 'cookie_manipulation'
        ]

        metadata_columns = ['URL', 'label']

        return basic_columns + dynamic_columns + password_columns + js_columns + metadata_columns

    html_columns = get_feature_columns()
    df = pd.DataFrame(data=data_list, columns=html_columns)
    df.to_csv(output_file, index=False)


def test_thread_performance(input_file, output_file_template, label, thread_counts):
    results = []
    for num_threads in thread_counts:
        print(f"Testing with {num_threads} threads...")
        start_time = time.time()
        process_urls_threaded(
            input_file,
            output_file_template.format(num_threads),
            label,
            num_threads=num_threads,
            max_count=100
        )
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Threads: {num_threads}, Time Taken: {elapsed_time:.2f} seconds")
        results.append((num_threads, elapsed_time))
    return results


if __name__ == "__main__":
    thread_counts_to_test = [10,20,50]

    print("Testing legitimate websites processing speed...")
    legitimate_results = test_thread_performance(
        "tranco_list.csv",
        "legitimate_websites_{}_threads.csv",
        label=0,
        thread_counts=thread_counts_to_test
    )

    print("\nResults:")
    print("\nLegitimate Websites:")
    for num_threads, elapsed_time in legitimate_results:
        print(f"Threads: {num_threads}, Time Taken: {elapsed_time:.2f} seconds")


# if __name__ == "__main__":
#     phishing_input_file = "verified_online.csv"
#     phishing_output_file_template = "phishing_websites_{}_threads.csv"
#
#     legitimate_input_file = "tranco_list.csv"
#     legitimate_output_file_template = "legitimate_websites_{}_threads.csv"
#
#     thread_counts_to_test = [20]  # 测试不同的线程数量
#
#     # print("Testing phishing websites processing speed...")
#     # phishing_results = test_thread_performance(
#     #     phishing_input_file,
#     #     phishing_output_file_template,
#     #     label=1,
#     #     thread_counts=thread_counts_to_test,
#     # )
#
#     print("\nTesting legitimate websites processing speed...")
#     legitimate_results = test_thread_performance(
#         legitimate_input_file,
#         legitimate_output_file_template,
#         label=0,
#         thread_counts=thread_counts_to_test,
#     )
#
#     print("\nResults:")
#
#     # print("Phishing Websites:")
#     # for num_threads, elapsed_time in phishing_results:
#     #     print(f"Threads: {num_threads}, Time Taken: {elapsed_time:.2f} seconds")
#
#     print("\nLegitimate Websites:")
#     for num_threads, elapsed_time in legitimate_results:
#         print(f"Threads: {num_threads}, Time Taken: {elapsed_time:.2f} seconds")