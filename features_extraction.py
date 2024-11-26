from bs4 import BeautifulSoup
import os
from selenium import webdriver
from features_html import features_html


class FeaturesExtraction:
    def __init__(self, driver):
        self.driver = driver
        self.html_features = features_html(driver)

    def create_vector(self):
        # HTML static features
        html_features = [
            self.html_features.has_title(),
            self.html_features.has_submit(),
            self.html_features.has_link(),
            self.html_features.has_email_input(),
            self.html_features.has_audio(),
            self.html_features.has_video(),
            self.html_features.number_of_inputs(),
            self.html_features.number_of_buttons(),
            self.html_features.number_of_images(),
            self.html_features.number_of_option(),
            self.html_features.number_of_list(),
            self.html_features.number_of_TH(),
            self.html_features.number_of_TR(),
            self.html_features.number_of_href(),
            self.html_features.number_of_paragraph(),
            self.html_features.number_of_script(),
            self.html_features.length_of_title(),
            self.html_features.has_h1(),
            self.html_features.has_h2(),
            self.html_features.has_h3(),
            self.html_features.length_of_text(),
            self.html_features.number_of_clickable_button(),
            self.html_features.number_of_a(),
            self.html_features.number_of_img(),
            self.html_features.number_of_div(),
            self.html_features.number_of_figure(),
            self.html_features.has_footer(),
            self.html_features.number_of_forms(),
            self.html_features.has_text_area(),
            self.html_features.has_iframe(),
            self.html_features.has_text_input(),
            self.html_features.number_of_meta(),
            self.html_features.has_nav(),
            self.html_features.has_object(),
            self.html_features.has_picture(),
            self.html_features.number_of_sources(),
            self.html_features.number_of_span(),
            self.html_features.number_of_table(),
            # 动态特征
            self.html_features.has_mouse_tracking(),
            self.html_features.has_keyboard_monitoring(),
            self.html_features.has_popups(),
            self.html_features.number_of_hidden_element(),
            self.html_features.page_redirect(),
            self.html_features.form_redirect_behavior(),
            self.html_features.check_external_form_action()
        ]
        # 添加密码字段特征
        password_features = self.html_features.check_password_fields()
        html_features.extend([
            password_features['password_type_count'],
            password_features['password_name_id_count'],
            password_features['hidden_password_count'],
            password_features['form_with_password']
        ])

        return html_features