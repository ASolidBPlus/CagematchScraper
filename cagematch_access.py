import requests
from bs4 import BeautifulSoup
import re
from data_classes import wrestler

class CagematchAccess:
    def __init__(self) -> None:
        pass

    def _scrape_data(self, url):
        r = requests.get(url, headers={'Accept-Encoding': 'identity'})
        return BeautifulSoup(r.content, features="html.parser")

class CagematchWrestlerAccess(CagematchAccess):
    def __init__(self) -> None:
        pass

    def scrape_wrestler(self, cagematch_wrestler_id):
        wrestler_soup = self._scrape_data(f"https://www.cagematch.net/?id=2&nr={str(cagematch_wrestler_id)}")
        return self._construct_wrestler_data(cagematch_wrestler_id, wrestler_soup)

    def _construct_wrestler_data(self, cagematch_wrestler_id, wrestler_soup):
        return wrestler.Wrestler(
            self._get_main_name(wrestler_soup),
            self._get_alter_egos(wrestler_soup),
            self._get_dob(cagematch_wrestler_id, wrestler_soup),
            self._get_birthplace(wrestler_soup),
            self._get_gender(wrestler_soup),
            self._get_height(wrestler_soup),
            self._get_weight(wrestler_soup),
            self._get_background_in_sports(wrestler_soup),
            self._get_social_media_links(wrestler_soup),
            [], # Roles Placeholder
            self._get_wrestling_style(wrestler_soup),
            [], # Trainer Placeholder
            self._get_nicknames(wrestler_soup),
            self._get_signature_moves(wrestler_soup))

    def _get_wrestler_data_base(self, wrestler_soup, text_search, return_text=True):
        data = wrestler_soup.body.find(text=text_search).parent.find_next_sibling()
        if return_text:
            return data.text

        return data
        
    def _get_split_entries(self, wrestler_soup, text_search):
        return self._get_wrestler_data_base(wrestler_soup, text_search).split(", ")

    def _get_br_entries(self, wrestler_soup, text_search):
        br_data = self._get_wrestler_data_base(wrestler_soup, text_search, return_text=False).findAll('br')
        return [br_data[0].previousSibling] + [br.nextSibling for br in br_data if br.nextSibling]

    def _get_main_name(self, wrestler_soup):
        return wrestler_soup.find("h1").text

    def _get_birthplace(self, wrestler_soup):
        return self._get_wrestler_data_base(wrestler_soup, "Birthplace:")

    def _get_gender(self, wrestler_soup):
        return self._get_wrestler_data_base(wrestler_soup, "Gender:")

    # TODO Re-use this method for weight too
    def _get_height(self, wrestler_soup):
        height_data = self._get_wrestler_data_base(wrestler_soup, "Height:")
        match = re.search(r"(\d+) cm", height_data)
        cm = int(match.group(1))
        
        return(cm)

    def _get_weight(self, wrestler_soup):
        weight_data = self._get_wrestler_data_base(wrestler_soup, "Weight:")
        match = re.search(r"(\d+) kg", weight_data)
        kg = int(match.group(1))
        
        return(kg)

    def _get_background_in_sports(self, wrestler_soup):
        return self._get_split_entries(wrestler_soup, "Background in sports:")

    def _get_social_media_links(self, wrestler_soup):
        social_media_data = self._get_wrestler_data_base(wrestler_soup, "WWW:", return_text=False)
        return [link['href'] for link in social_media_data.find_all('a', href=True)]

    def _get_wrestling_style(self, wrestler_soup):
        return self._get_split_entries(wrestler_soup, "Wrestling style:")

    def _get_alter_egos(self, wrestler_soup):
        alter_ego_data = self._get_wrestler_data_base(wrestler_soup, "Alter egos:", return_text=False)
        return [alter_ego.text for alter_ego in alter_ego_data.find_all('a')]

    def _get_nicknames(self, wrestler_soup):
        return [nickname.strip('"') for nickname in self._get_br_entries(wrestler_soup, "Nicknames:")]

    def _get_signature_moves(self, wrestler_soup):
        return self._get_br_entries(wrestler_soup, "Signature moves:")

    def _get_dob(self, cagematch_wrestler_id, wrestler_soup):
        search_term = self._get_main_name(wrestler_soup).replace(" ", "+")
        search_url = f"https://www.cagematch.net/?id=2&view=workers&search={search_term}"
        search_soup = self._scrape_data(search_url)

        table_content = search_soup.findAll('table')[0].find_all('tr')[1:]

        for entry in table_content:
            link = entry.find('a', href=True)['href']
            match = re.search(r"nr=(\d+)", link)
            
            try:
                if match.group(1) == str(cagematch_wrestler_id):
                    return entry.find_all("td")[2].text.replace(".", "/")

            except:
                print(f"Warning: An issue was found when attempting to parse the date for id {cagematch_wrestler_id}, this was done during matching regex for the id on one of the search entries.")
