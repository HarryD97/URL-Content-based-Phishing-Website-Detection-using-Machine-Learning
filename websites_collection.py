import threading
from queue import Queue
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
    """
    工作线程函数，从队列中获取 URL 并处理。
    """
    global phishing_count, legitimate_count

    # 在线程开始时创建WebDriver实例
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)

    try:
        while True:
            url = queue.get()
            if url is None:
                break

            with lock:
                if (label == 1 and phishing_count >= max_count) or \
                        (label == 0 and legitimate_count >= max_count):
                    queue.task_done()
                    break

            try:
                driver.set_page_load_timeout(10)
                driver.set_script_timeout(10)
                driver.get(url)

                extractor = FeaturesExtraction(driver)
                vector = extractor.create_vector()
                vector.append(str(url))
                vector.append(label)

                with lock:
                    if label == 1 and phishing_count < max_count:
                        data_list.append(vector)
                        phishing_count += 1
                    elif label == 0 and legitimate_count < max_count:
                        data_list.append(vector)
                        legitimate_count += 1
            except Exception as e:
                # print(f"Error processing {url}: {e}")
                continue
            finally:
                queue.task_done()
    finally:
        driver.quit()


def process_urls_threaded(input_file, output_file, label, num_threads=4, max_count=100):
    """
    使用多线程处理 URL 列表。
    """
    global phishing_count, legitimate_count

    # 重置计数器
    if label == 1:
        phishing_count = 0
    else:
        legitimate_count = 0

    # 读取文件并准备 URL 列表
    if label == 0:
        data_frame = pd.read_csv(input_file, names=['id', 'url'])
        URL_list = ["http://" + url for url in data_frame['url'].to_list()]
    else:
        data_frame = pd.read_csv(input_file)
        URL_list = data_frame['url'].to_list()

    # 创建队列和结果列表
    url_queue = Queue()
    data_list = []

    # 创建线程池
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(url_queue, data_list, label, max_count))
        t.daemon = True
        t.start()
        threads.append(t)

    # 添加URL到队列并显示进度条
    with tqdm(total=len(URL_list)) as pbar:
        for url in URL_list:
            with lock:
                if (label == 1 and phishing_count >= max_count) or \
                        (label == 0 and legitimate_count >= max_count):
                    break
            url_queue.put(url)
            pbar.update(1)

    # 添加结束标记
    for _ in range(num_threads):
        url_queue.put(None)

    # 等待所有线程完成
    for t in threads:
        t.join()

    # 保存结果到CSV文件
    html_columns = [
        'has_title', 'has_submit', 'has_link', 'has_email_input',
        'has_audio', 'has_video', 'number_of_inputs', 'number_of_buttons',
        'number_of_images', 'number_of_option', 'number_of_list',
        'number_of_th', 'number_of_tr', 'number_of_href',
        'number_of_paragraph', 'number_of_script', 'length_of_title',
        'has_h1', 'has_h2', 'has_h3', 'length_of_text',
        'number_of_clickable_button', 'number_of_a', 'number_of_img',
        'number_of_div', 'number_of_figure', 'has_footer', 'number_of_forms',
        'has_text_area', 'has_iframe', 'has_text_input', 'number_of_meta',
        'has_nav', 'has_object', 'has_picture', 'number_of_sources',
        'number_of_span', 'number_of_table', 'has_mouse_tracking',
        'has_keyboard_monitoring', 'has_popups', 'number_of_hidden_element',
        'page_redirect', 'form_redirect_behavior', 'external_form_action',
        'password_type_count', 'password_name_id_count', 'hidden_password_count',
        'form_with_password', 'URL', 'label'
    ]

    df = pd.DataFrame(data=data_list, columns=html_columns)
    df.to_csv(output_file, index=False)


if __name__ == "__main__":
    MAX_COUNT = 40
    NUM_THREADS = 4

    print("Processing phishing websites...")
    process_urls_threaded(
        "verified_online.csv",
        "phishing_websites.csv",
        label=1,
        num_threads=NUM_THREADS,
        max_count=MAX_COUNT
    )

    print("Processing legitimate websites...")
    process_urls_threaded(
        "tranco_list.csv",
        "legitimate_websites.csv",
        label=0,
        num_threads=NUM_THREADS,
        max_count=MAX_COUNT
    )

    print("Processing completed!")