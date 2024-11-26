from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class features_html:
    def __init__(self, driver):
        self.driver = driver
        self.soup = BeautifulSoup(driver.page_source, 'html.parser')
        self.wait = WebDriverWait(driver, 4)

    # 使用BeautifulSoup的静态特征提取
    def has_title(self):
        return 1 if self.soup.title else 0

    def has_submit(self):
        return 1 if self.soup.find('input', {'type': 'submit'}) else 0

    def has_link(self):
        return 1 if self.soup.find('link') else 0

    def has_email_input(self):
        inputs = self.soup.find_all('input', {'type': 'email'}) or \
                 self.soup.find_all('input', id=lambda x: x and 'email' in x.lower()) or \
                 self.soup.find_all('input', name=lambda x: x and 'email' in x.lower())
        return 1 if inputs else 0

    def has_audio(self):
        return 1 if self.soup.find('audio') else 0

    def has_video(self):
        return 1 if self.soup.find('video') else 0

    def number_of_inputs(self):
        return len(self.soup.find_all('input'))

    def number_of_buttons(self):
        return len(self.soup.find_all('button'))

    def number_of_images(self):
        return len(self.soup.find_all('img'))

    def number_of_option(self):
        return len(self.soup.find_all('option'))

    def number_of_list(self):
        return len(self.soup.find_all('li'))

    def number_of_TH(self):
        return len(self.soup.find_all('th'))

    def number_of_TR(self):
        return len(self.soup.find_all('tr'))

    def number_of_href(self):
        links = self.soup.find_all('a', href=True)
        return len(links)

    def number_of_paragraph(self):
        return len(self.soup.find_all('p'))

    def number_of_script(self):
        return len(self.soup.find_all('script'))

    def length_of_title(self):
        return len(self.soup.title.string) if self.soup.title else 0

    def has_h1(self):
        return 1 if self.soup.find('h1') else 0

    def has_h2(self):
        return 1 if self.soup.find('h2') else 0

    def has_h3(self):
        return 1 if self.soup.find('h3') else 0

    def length_of_text(self):
        return len(self.soup.get_text())

    def number_of_clickable_button(self):
        return len(self.soup.find_all('button', {'type': 'button'}))

    def number_of_a(self):
        return len(self.soup.find_all('a'))

    def number_of_img(self):
        return len(self.soup.find_all('img'))

    def number_of_div(self):
        return len(self.soup.find_all('div'))

    def number_of_figure(self):
        return len(self.soup.find_all('figure'))

    def has_footer(self):
        return 1 if self.soup.find('footer') else 0

    def number_of_forms(self):
        return len(self.soup.find_all('form'))

    def has_text_area(self):
        return 1 if self.soup.find('textarea') else 0

    def has_iframe(self):
        return 1 if self.soup.find('iframe') else 0

    def has_text_input(self):
        inputs = self.soup.find_all('input', {'type': 'text'})
        return 1 if inputs else 0

    def number_of_meta(self):
        return len(self.soup.find_all('meta'))

    def has_nav(self):
        return 1 if self.soup.find('nav') else 0

    def has_object(self):
        return 1 if self.soup.find('object') else 0

    def has_picture(self):
        return 1 if self.soup.find('picture') else 0

    def number_of_sources(self):
        return len(self.soup.find_all('source'))

    def number_of_span(self):
        return len(self.soup.find_all('span'))

    def number_of_table(self):
        return len(self.soup.find_all('table'))

    # 使用Selenium的动态特征检测
    def number_of_hidden_element(self):
        try:
            hidden_elements = self.driver.execute_script("""
                return {
                    display_none: Array.from(document.getElementsByTagName('*'))
                        .filter(el => window.getComputedStyle(el).display === 'none').length,
                    visibility_hidden: Array.from(document.getElementsByTagName('*'))
                        .filter(el => window.getComputedStyle(el).visibility === 'hidden').length,
                    hidden_inputs: Array.from(document.getElementsByTagName('input'))
                        .filter(el => el.type === 'hidden').length,
                    offscreen: Array.from(document.getElementsByTagName('*'))
                        .filter(el => {
                            const rect = el.getBoundingClientRect();
                            return rect.left < 0 || rect.top < 0;
                        }).length
                };
            """)
            return sum(hidden_elements.values())
        except:
            return 0

    def page_redirect(self):
        try:
            initial_url = self.driver.current_url
            self.wait.until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
            final_url = self.driver.current_url
            return 1 if initial_url != final_url else 0
        except:
            return 0

    def form_redirect_behavior(self):
        try:
            forms = self.driver.find_elements(By.TAG_NAME, 'form')
            current_url = self.driver.current_url
            for form in forms:
                action = form.get_attribute('action')
                if action:
                    if action == "about:blank" or action == "":
                        return 1
                    if "http" in action and current_url not in action:
                        return 1
            return 0
        except:
            return 0

    def check_external_form_action(self):
        try:
            forms = self.driver.find_elements(By.TAG_NAME, 'form')
            current_domain = self.driver.current_url.split('/')[2]
            for form in forms:
                action = form.get_attribute('action')
                if action and current_domain not in action:
                    return 1
            return 0
        except:
            return 0

    def has_mouse_tracking(self):
        script = """
            let tracking = false;
            document.addEventListener('mousemove', () => { tracking = true; });
            return tracking ? 1 : 0;
        """
        return self.driver.execute_script(script)

    def has_keyboard_monitoring(self):
        script = """
            let monitoring = false;
            document.addEventListener('keydown', () => { monitoring = true; });
            return monitoring ? 1 : 0;
        """
        return self.driver.execute_script(script)

    def check_password_fields(self):
        try:
            password_features = {
                'password_type_count': 0,
                'password_name_id_count': 0,
                'hidden_password_count': 0,
                'form_with_password': 0
            }

            forms = self.driver.find_elements(By.TAG_NAME, 'form')
            for form in forms:
                has_password = False
                inputs = form.find_elements(By.TAG_NAME, 'input')
                for input_field in inputs:
                    input_type = input_field.get_attribute('type')
                    input_name = input_field.get_attribute('name')
                    input_id = input_field.get_attribute('id')

                    if input_type == 'password':
                        password_features['password_type_count'] += 1
                        has_password = True

                    if (input_name and 'password' in input_name.lower()) or \
                            (input_id and 'password' in input_id.lower()):
                        password_features['password_name_id_count'] += 1

                    if input_type == 'hidden' and \
                            ((input_name and 'password' in input_name.lower()) or \
                             (input_id and 'password' in input_id.lower())):
                        password_features['hidden_password_count'] += 1

                if has_password:
                    password_features['form_with_password'] += 1

            return password_features
        except:
            return {
                'password_type_count': 0,
                'password_name_id_count': 0,
                'hidden_password_count': 0,
                'form_with_password': 0
            }

    def has_popups(self):
        try:
            script = """
                let hasPopup = false;
                const originalOpen = window.open;
                window.open = function() { hasPopup = true; };
                return hasPopup ? 1 : 0;
            """
            has_popup = self.driver.execute_script(script)

            dialog_script = """
                let hasDialog = false;
                ['alert', 'confirm', 'prompt'].forEach(function(dialog) {
                    const original = window[dialog];
                    window[dialog] = function() { hasDialog = true; };
                });
                return hasDialog ? 1 : 0;
            """
            has_dialog = self.driver.execute_script(dialog_script)

            return 1 if (has_popup or has_dialog) else 0
        except:
            return 0