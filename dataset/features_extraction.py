from features_html import features_html
from features_url import  URLFeature


class FeaturesExtraction:
    def __init__(self, driver, soup, url):
        self.url = url
        self.driver = driver
        self.soup = soup
        self.html_features = features_html(driver, soup)
        self.url_features = URLFeature(url)

    def create_vector(self):

        # HTML static features
        html_features = [
            self.html_features.has_title(),
            self.html_features.has_submit(),
            self.html_features.has_link(),
            self.html_features.has_email_input(),
            self.html_features.number_of_inputs(),
            self.html_features.number_of_buttons(),
            self.html_features.number_of_images(),
            self.html_features.number_of_option(),
            self.html_features.number_of_list(),
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
            self.html_features.number_of_div(),
            self.html_features.has_footer(),
            self.html_features.number_of_forms(),
            self.html_features.has_text_area(),
            self.html_features.has_iframe(),
            self.html_features.has_text_input(),
            self.html_features.number_of_meta(),
            self.html_features.has_nav(),
            self.html_features.number_of_sources(),
            self.html_features.number_of_span(),
            self.html_features.number_of_table(),

            self.html_features.RequestURL(),
            self.html_features.AnchorURL(),
            self.html_features.Favicon(),
            self.html_features.LinksInScriptTags(),
            self.html_features.ServerFormHandler(),
            self.html_features.InfoEmail(),

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
        # suspicious features
        js_features = self.html_features.check_suspicious_js()
        html_features.extend([
            js_features['clipboard_monitoring'],
            js_features['form_data_collection'],
            js_features['cookie_manipulation']
        ])

        # URL 特征
        url_features = [
            self.url_features.UsingIp(),
            self.url_features.longUrl(),
            self.url_features.shortUrl(),
            self.url_features.symbol(),
            self.url_features.redirecting(),
            self.url_features.prefixSuffix(),
            self.url_features.SubDomains(),
            self.url_features.Hppts(),
            self.url_features.DomainRegLen(),
            self.url_features.NonStdPort(),
            self.url_features.HTTPSDomainURL(),
            self.url_features.AbnormalURL(),
            self.url_features.WebsiteForwarding(),
            self.url_features.StatusBarCust(),
            self.url_features.DisableRightClick(),
            self.url_features.UsingPopupWindow(),
            self.url_features.IframeRedirection(),
            self.url_features.AgeofDomain(),
            self.url_features.DNSRecording(),
            self.url_features.WebsiteTraffic(),
            self.url_features.PageRank(),
            self.url_features.GoogleIndex(),
            self.url_features.LinksPointingToPage(),
            self.url_features.StatsReport()
        ]

        return html_features+url_features