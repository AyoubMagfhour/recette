from bs4 import BeautifulSoup


def extract_data(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    data_list = []
    for tag in soup.find_all(style=lambda value: value and 'background-image' in value):
        style = tag['style']
        url = style.split('background-image:')[1].split('url(')[1].split(')')[0].strip('"\'')
        caption_tag = tag.find_next('figcaption', {'class': 'app_recipe_figcaption'})
        caption = caption_tag.text.strip() if caption_tag else ''
        figure_tag = tag.find_parent('figure', {'class': 'm-fig'})
        href = figure_tag.find('a')['href'] if figure_tag else ''
        data_list.append({'url': url, 'caption': caption, 'href': href})
    return data_list
