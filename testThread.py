import threading
from queue import Queue
import requests as re
from bs4 import BeautifulSoup
import pandas as pd
import features_extraction as fe
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
import time


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from features_extraction import FeaturesExtraction

disable_warnings(InsecureRequestWarning)
# 全局计数器和锁
phishing_count = 0
legitimate_count = 0
lock = threading.Lock()




def process_url(url, data_list, label, max_count):
    """
    处理单个 URL，提取特征并更新计数器。
    """
    global phishing_count, legitimate_count, driver

    try:
        # 设置Chrome选项
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # 初始化WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        # 使用FeaturesExtraction替代原来的features_extraction
        extractor = FeaturesExtraction(driver)
        vector = extractor.create_vector()
        vector.append(str(url))
        vector.append(label)

        # 更新计数器和数据列表
        with lock:
            if label == 1 and phishing_count < max_count:
                data_list.append(vector)
                phishing_count += 1
            elif label == 0 and legitimate_count < max_count:
                data_list.append(vector)
                legitimate_count += 1

        driver.quit()
        return True

    except Exception as e:
        # print(f"Error processing {url}: {e}")
        if 'driver' in locals():
            driver.quit()
        return False


def worker(queue, data_list, label, max_count):
    """
    工作线程函数，从队列中获取 URL 并处理。
    """
    while True:
        url = queue.get()
        if url is None:  # 检查是否结束任务
            break

        # 检查是否达到最大数量，提前退出线程
        with lock:
            if (label == 1 and phishing_count >= max_count) or (label == 0 and legitimate_count >= max_count):
                queue.task_done()
                break

        process_url(url, data_list, label, max_count)
        queue.task_done()


def process_urls_threaded(input_file, output_file, label, num_threads=10, max_count=100):
    """
    使用多线程处理 URL 列表。
    """
    global phishing_count, legitimate_count

    # 重置计数器（每次调用时）
    phishing_count = 0 if label == 1 else phishing_count
    legitimate_count = 0 if label == 0 else legitimate_count

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

    # 添加 URL 到队列
    for url in URL_list:
        with lock:  # 检查是否已经达到最大数量，提前停止添加 URL 到队列
            if (label == 1 and phishing_count >= max_count) or (label == 0 and legitimate_count >= max_count):
                break
        url_queue.put(url)

    # 添加结束标记（None）到队列以终止线程
    for _ in range(num_threads):
        url_queue.put(None)

    # 等待所有线程完成任务
    for t in threads:
        t.join()

    # 保存结果到 CSV 文件
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


def test_thread_performance(input_file, output_file_template, label, thread_counts):
    """
    测试不同线程数量下的处理速度。
    """
    results = []

    for num_threads in thread_counts:
        print(f"Testing with {num_threads} threads...")

        start_time = time.time()  # 开始时间记录

        process_urls_threaded(
            input_file,
            output_file_template.format(num_threads),
            label,
            num_threads=num_threads,
            max_count=40  #
        )

        end_time = time.time()  # 结束时间记录

        elapsed_time = end_time - start_time  # 耗时计算
        print(f"Threads: {num_threads}, Time Taken: {elapsed_time:.2f} seconds")

        results.append((num_threads, elapsed_time))

    return results


if __name__ == "__main__":
    phishing_input_file = "verified_online.csv"
    phishing_output_file_template = "phishing_websites_{}_threads.csv"

    legitimate_input_file = "tranco_list.csv"
    legitimate_output_file_template = "legitimate_websites_{}_threads.csv"

    thread_counts_to_test = [20]  # 测试不同的线程数量

    # print("Testing phishing websites processing speed...")
    # phishing_results = test_thread_performance(
    #     phishing_input_file,
    #     phishing_output_file_template,
    #     label=1,
    #     thread_counts=thread_counts_to_test,
    # )

    print("\nTesting legitimate websites processing speed...")
    legitimate_results = test_thread_performance(
        legitimate_input_file,
        legitimate_output_file_template,
        label=0,
        thread_counts=thread_counts_to_test,
    )

    print("\nResults:")

    # print("Phishing Websites:")
    # for num_threads, elapsed_time in phishing_results:
    #     print(f"Threads: {num_threads}, Time Taken: {elapsed_time:.2f} seconds")

    print("\nLegitimate Websites:")
    for num_threads, elapsed_time in legitimate_results:
        print(f"Threads: {num_threads}, Time Taken: {elapsed_time:.2f} seconds")