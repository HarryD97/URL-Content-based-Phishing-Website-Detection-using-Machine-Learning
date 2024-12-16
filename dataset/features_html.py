import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class features_html:
    def __init__(self, driver, soup):
        self.driver = driver
        self.soup = soup
        self.wait = WebDriverWait(driver, 2)

    # 使用BeautifulSoup的静态特征提取
    def has_title(self):
        return 1 if self.soup.title else 0

    def has_submit(self):
        return 1 if self.soup.find('input', {'type': 'submit'}) else 0

    def has_link(self):
        return 1 if self.soup.find('link') else 0

    def has_email_input(self):
        email_inputs = self.soup.find_all('input', {'type': 'email'})
        id_inputs = self.soup.find_all('input', id=lambda x: x and 'email' in x.lower())
        name_inputs = self.soup.find_all('input', attrs={'name': lambda x: x and 'email' in x.lower()})
        return 1 if (email_inputs or id_inputs or name_inputs) else 0

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

    def number_of_div(self):
        return len(self.soup.find_all('div'))

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

    def number_of_sources(self):
        return len(self.soup.find_all('source'))

    def number_of_span(self):
        return len(self.soup.find_all('span'))

    def number_of_table(self):
        return len(self.soup.find_all('table'))

    # RequestURL
    def RequestURL(self):
        try:
            success, i = 0, 0
            for img in self.soup.find_all('img', src=True):
                dots = [x.start(0) for x in re.finditer('\.', img['src'])]
                if self.url in img['src'] or self.domain in img['src'] or len(dots) == 1:
                    success += 1
                i += 1

            for audio in self.soup.find_all('audio', src=True):
                dots = [x.start(0) for x in re.finditer('\.', audio['src'])]
                if self.url in audio['src'] or self.domain in audio['src'] or len(dots) == 1:
                    success += 1
                i += 1

            for embed in self.soup.find_all('embed', src=True):
                dots = [x.start(0) for x in re.finditer('\.', embed['src'])]
                if self.url in embed['src'] or self.domain in embed['src'] or len(dots) == 1:
                    success += 1
                i += 1

            for iframe in self.soup.find_all('iframe', src=True):
                dots = [x.start(0) for x in re.finditer('\.', iframe['src'])]
                if self.url in iframe['src'] or self.domain in iframe['src'] or len(dots) == 1:
                    success += 1
                i += 1

            percentage = (success / float(i)) * 100 if i > 0 else 0
            return 1 if percentage >= 50.0 else 0
        except:
            return 0

    # AnchorURL
    def AnchorURL(self):
        try:
            i, unsafe = 0, 0
            for a in self.soup.find_all('a', href=True):
                if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (
                        self.url in a['href'] or self.domain in a['href']):
                    unsafe += 1
                i += 1

            percentage = (unsafe / float(i)) * 100 if i > 0 else 100
            return 1 if percentage < 50.0 else 0
        except:
            return 0

    # Favicon
    def Favicon(self):
        try:
            for head in self.soup.find_all('head'):
                for head.link in self.soup.find_all('link', href=True):
                    dots = [x.start(0) for x in re.finditer('\.', head.link['href'])]
                    if self.url in head.link['href'] or len(dots) == 1 or self.domain in head.link['href']:
                        return 1
            return 0
        except:
            return 0

    # LinksInScriptTags
    def LinksInScriptTags(self):
        try:
            i, success = 0, 0

            for link in self.soup.find_all('link', href=True):
                dots = [x.start(0) for x in re.finditer('\.', link['href'])]
                if self.url in link['href'] or self.domain in link['href'] or len(dots) == 1:
                    success += 1
                i += 1

            for script in self.soup.find_all('script', src=True):
                dots = [x.start(0) for x in re.finditer('\.', script['src'])]
                if self.url in script['src'] or self.domain in script['src'] or len(dots) == 1:
                    success += 1
                i += 1

            percentage = (success / float(i)) * 100 if i > 0 else 0
            return 1 if percentage >= 50.0 else 0
        except:
            return 0

    # ServerFormHandler
    def ServerFormHandler(self):
        try:
            forms = self.soup.find_all('form', action=True)
            if len(forms) == 0:
                return 1
            else:
                for form in forms:
                    if form['action'] == "" or form['action'] == "about:blank":
                        return 0
                    elif self.url not in form['action'] and self.domain not in form['action']:
                        return 0
                    else:
                        return 1
        except:
            return 0

    # InfoEmail
    def InfoEmail(self):
        try:
            # 检查是否存在邮件相关信息（如 mailto 或 mail()）
            if re.findall(r"[mail\(\)|mailto:?]", str(self.soup)):
                return 0
            else:
                return 1
        except:
            return 0

    # 使用Selenium的动态特征检测 # JS
    def check_clipboard_access(self):
        try:
            script = """
            let hasClipboardAccess = false;
            ['copy', 'cut', 'paste'].forEach(function(event) {
                document.addEventListener(event, () => { 
                    hasClipboardAccess = true;
                });
            });
            return hasClipboardAccess ? 1 : 0;
            """
            return self.driver.execute_script(script)
        except:
            return 0

    def check_form_data_collection(self):
        try:
            script = """
            let hasFormCollection = false;
            document.querySelectorAll('form').forEach(form => {
                form.addEventListener('submit', () => {
                    hasFormCollection = true;
                });
                form.querySelectorAll('input').forEach(input => {
                    input.addEventListener('change', () => {
                        hasFormCollection = true;
                    });
                });
            });
            return hasFormCollection ? 1 : 0;
            """
            return self.driver.execute_script(script)
        except:
            return 0

    def check_cookie_manipulation(self):
        try:
            script = """
            let hasCookieManipulation = false;
            const originalCookie = Object.getOwnPropertyDescriptor(Document.prototype, 'cookie');
            Object.defineProperty(document, 'cookie', {
                get: function() {
                    hasCookieManipulation = true;
                    return originalCookie.get.call(this);
                },
                set: function(val) {
                    hasCookieManipulation = true;
                    return originalCookie.set.call(this, val);
                }
            });
            return hasCookieManipulation ? 1 : 0;
            """
            return self.driver.execute_script(script)
        except:
            return 0

    def check_suspicious_js(self):
        return {
            'clipboard_monitoring': self.check_clipboard_access(),
            'form_data_collection': self.check_form_data_collection(),
            'cookie_manipulation': self.check_cookie_manipulation()
        }

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