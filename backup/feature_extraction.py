from bs4 import BeautifulSoup
import os

# Feature extraction functions
def has_title(soup):
    if soup.title is None:
        return 0
    if len(soup.title.text) > 0:
        return 1
    return 0

def has_input(soup):
    return 1 if len(soup.find_all("input")) else 0

def has_button(soup):
    return 1 if len(soup.find_all("button")) > 0 else 0

def has_image(soup):
    return 0 if len(soup.find_all("image")) == 0 else 1

def has_submit(soup):
    for button in soup.find_all("input"):
        if button.get("type") == "submit":
            return 1
    return 0

def has_link(soup):
    return 1 if len(soup.find_all("link")) > 0 else 0

def has_password(soup):
    for input in soup.find_all("input"):
        if (input.get("type") or input.get("name") or input.get("id")) == "password":
            return 1
    return 0

def has_email_input(soup):
    for input in soup.find_all("input"):
        if (input.get("type") or input.get("id") or input.get("name")) == "email":
            return 1
    return 0

def has_hidden_element(soup):
    for input in soup.find_all("input"):
        if input.get("type") == "hidden":
            return 1
    return 0

def has_audio(soup):
    return 1 if len(soup.find_all("audio")) > 0 else 0

def has_video(soup):
    return 1 if len(soup.find_all("video")) > 0 else 0

def number_of_inputs(soup):
    return len(soup.find_all("input"))

def number_of_buttons(soup):
    return len(soup.find_all("button"))

def number_of_images(soup):
    image_tags = len(soup.find_all("image"))
    count = sum(1 for meta in soup.find_all("meta")
               if meta.get("type") or meta.get("name") == "image")
    return image_tags + count

def number_of_option(soup):
    return len(soup.find_all("option"))

def number_of_list(soup):
    return len(soup.find_all("li"))

def number_of_TH(soup):
    return len(soup.find_all("th"))

def number_of_TR(soup):
    return len(soup.find_all("tr"))

def number_of_href(soup):
    return sum(1 for link in soup.find_all("link") if link.get("href"))

def number_of_paragraph(soup):
    return len(soup.find_all("p"))

def number_of_script(soup):
    return len(soup.find_all("script"))

def length_of_title(soup):
    return 0 if soup.title is None else len(soup.title.text)

def has_h1(soup):
    return 1 if len(soup.find_all("h1")) > 0 else 0

def has_h2(soup):
    return 1 if len(soup.find_all("h2")) > 0 else 0

def has_h3(soup):
    return 1 if len(soup.find_all("h3")) > 0 else 0

def length_of_text(soup):
    return len(soup.get_text())

def number_of_clickable_button(soup):
    return sum(1 for button in soup.find_all("button")
              if button.get("type") == "button")

def number_of_a(soup):
    return len(soup.find_all("a"))

def number_of_img(soup):
    return len(soup.find_all("img"))

def number_of_div(soup):
    return len(soup.find_all("div"))

def number_of_figure(soup):
    return len(soup.find_all("figure"))

def has_footer(soup):
    return 1 if len(soup.find_all("footer")) > 0 else 0

def has_form(soup):
    return 1 if len(soup.find_all("form")) > 0 else 0

def has_text_area(soup):
    return 1 if len(soup.find_all("textarea")) > 0 else 0

def has_iframe(soup):
    return 1 if len(soup.find_all("iframe")) > 0 else 0

def has_text_input(soup):
    for input in soup.find_all("input"):
        if input.get("type") == "text":
            return 1
    return 0

def number_of_meta(soup):
    return len(soup.find_all("meta"))

def has_nav(soup):
    return 1 if len(soup.find_all("nav")) > 0 else 0

def has_object(soup):
    return 1 if len(soup.find_all("object")) > 0 else 0

def has_picture(soup):
    return 1 if len(soup.find_all("picture")) > 0 else 0

def number_of_sources(soup):
    return len(soup.find_all("source"))

def number_of_span(soup):
    return len(soup.find_all("span"))

def number_of_table(soup):
    return len(soup.find_all("table"))

# File handling functions
def open_file(f_name):
    with open(f_name, "r") as f:
        return f.read()

def create_soup(text):
    return BeautifulSoup(text, "html.parser")

def create_vector(soup):
    return [
        has_title(soup), has_input(soup), has_button(soup),
        has_image(soup), has_submit(soup), has_link(soup),
        has_password(soup), has_email_input(soup), has_hidden_element(soup),
        has_audio(soup), has_video(soup), number_of_inputs(soup),
        number_of_buttons(soup), number_of_images(soup), number_of_option(soup),
        number_of_list(soup), number_of_TH(soup), number_of_TR(soup),
        number_of_href(soup), number_of_paragraph(soup), number_of_script(soup),
        length_of_title(soup), has_h1(soup), has_h2(soup),
        has_h3(soup), length_of_text(soup), number_of_clickable_button(soup),
        number_of_a(soup), number_of_img(soup), number_of_div(soup),
        number_of_figure(soup), has_footer(soup), has_form(soup),
        has_text_area(soup), has_iframe(soup), has_text_input(soup),
        number_of_meta(soup), has_nav(soup), has_object(soup),
        has_picture(soup), number_of_sources(soup), number_of_span(soup),
        number_of_table(soup)
    ]

def create_2d_list(folder_name):
    directory = os.path.join(os.getcwd(), folder_name)
    data = []
    for file in sorted(os.listdir(directory)):
        soup = create_soup(open_file(directory + "/" + file))
        data.append(create_vector(soup))
    return data

# Main execution
if __name__ == "__main__":
    folder = "mini_dataset"
    data = create_2d_list(folder)