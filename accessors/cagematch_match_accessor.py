import logging
import re

from accessors.cagematch_accessor import CagematchAccessor
from data_classes.wrestler import Wrestler
from data_classes.trainer import Trainer

class CagematchWrestlerAccessor(CagematchAccessor):
    def __init__(self) -> None:
        pass

    @classmethod
    def _get_wrestler_selected_element(cls, wrestler_soup, text_search, return_text=True):
        selected_element = wrestler_soup.select(f"div.InformationBoxTitle:-soup-contains('{text_search}') + div.InformationBoxContents")
        
        if selected_element is not None:
            try:
                if return_text:
                    return selected_element[0].text.strip()

                return selected_element[0]
            except:
                logging.warning(f"An exception was raised when attempting to get the content of the elected element in _get_wrestler_selected_element when searching for {text_search}")

        logging.info(f"No data was found when searching for {text_search}")
        return None

    def _construct_wrestler_data(self, cagematch_wrestler_id, wrestler_soup):
        data = {}
        data['main_name'] = self._get_main_name(wrestler_soup)
        data['alter_egos'] = self._get_alter_egos(wrestler_soup)
        data['dob'] = self._get_dob(cagematch_wrestler_id, wrestler_soup)
        data['birthplace'] = self._get_birthplace(wrestler_soup)
        data['gender'] = self._get_gender(wrestler_soup)
        data['height'] = self._get_height(wrestler_soup)
        data['weight'] = self._get_weight(wrestler_soup)
        data['background_in_sports'] = self._get_background_in_sports(wrestler_soup)
        data['social_media_links'] = self._get_social_media_links(wrestler_soup)
        data['roles'] = self._get_roles(wrestler_soup)
        data['wrestling_style'] = self._get_wrestling_style(wrestler_soup)
        data['trainers'] = self._get_trainers(wrestler_soup)
        data['nicknames'] = self._get_nicknames(wrestler_soup)
        data['signature_moves'] = self._get_signature_moves(wrestler_soup)
        
        return Wrestler(**data)

    def _get_split_entries(self, wrestler_soup, text_search):
        entry_data = self._get_wrestler_selected_element(wrestler_soup, text_search)

        if entry_data is not None:
            try:
                return entry_data.split(", ")
            except:
                logging.warning(f"An exception was raised when attempting to split entry_data in _get_split_entries when searching for {text_search}")
                return None
        
        return None
        
    def _get_br_entries(self, wrestler_soup, text_search):
        br_data = self._get_wrestler_selected_element(wrestler_soup, text_search, return_text=False)

        if br_data is not None:
            try:
                return [data.string for data in br_data.contents if data.string]
            except:
                logging.warning(f"An exception was raised when attempting to obtain br strings in _get_br_entries when searching for {text_search}")
                return None
        
        return None

    def _get_id_from_url(self, link):
        match = re.search(r"nr=(\d+)", link)
        
        if match:
            return match.group(1)
        
        return None

    def _get_metric(self, metric_data, metric):
        match = re.search(fr"(\d+) {metric}", metric_data)
        
        if match:
            metric = int(match.group(1))
            return(metric)

        return None

    def _get_main_name(self, wrestler_soup):
        return wrestler_soup.find("h1").text

    def _get_birthplace(self, wrestler_soup):
        return self._get_wrestler_selected_element(wrestler_soup, "Birthplace:")

    def _get_gender(self, wrestler_soup):
        return self._get_wrestler_selected_element(wrestler_soup, "Gender:")

    def _get_height(self, wrestler_soup):
        height_data = self._get_wrestler_selected_element(wrestler_soup, "Height:")
        return(self._get_metric(height_data, 'cm'))

    def _get_weight(self, wrestler_soup):
        weight_data = self._get_wrestler_selected_element(wrestler_soup, "Weight:")
        return(self._get_metric(weight_data, 'kg'))

    def _get_background_in_sports(self, wrestler_soup):
        return self._get_split_entries(wrestler_soup, "Background in sports:")

    def _get_social_media_links(self, wrestler_soup):
        social_media_data = self._get_wrestler_selected_element(wrestler_soup, "WWW:", return_text=False)

        if social_media_data is not None:
            return [link['href'] for link in social_media_data.find_all('a', href=True)]
        
        return None

    def _get_wrestling_style(self, wrestler_soup):
        return self._get_split_entries(wrestler_soup, "Wrestling style:")

    def _get_alter_egos(self, wrestler_soup):
        alter_ego_data = self._get_wrestler_selected_element(wrestler_soup, "Alter egos:", return_text=False)

        if alter_ego_data is not None:
            try:
                return [alter_ego.text.strip() for alter_ego in alter_ego_data.find_all('a')]
            except:
                return None
        
        return None

    def _get_nicknames(self, wrestler_soup):
        brs = self._get_br_entries(wrestler_soup, "Nicknames:")

        if brs is not None: 
            return [nickname.strip('"') for nickname in brs]
        
        return brs

    def _get_signature_moves(self, wrestler_soup):
        return self._get_br_entries(wrestler_soup, "Signature moves:")

    def _get_dob(self, cagematch_wrestler_id, wrestler_soup):
        search_term = self._get_main_name(wrestler_soup).replace(" ", "+")
        search_url = f"https://www.cagematch.net/?id=2&view=workers&search={search_term}"
        search_soup = self._scrape_data(search_url)

        table_content = self._get_table_content(search_soup)

        for entry in table_content:
            link = entry.find('a', href=True)['href']
            link_id = self._get_id_from_url(link)
            
            try:
                if link_id == str(cagematch_wrestler_id):
                    return entry.find_all("td")[2].text.replace(".", "/")

            except:
                print(f"Warning: An issue was found when attempting to parse the date for id {cagematch_wrestler_id}, this was done during matching regex for the id on one of the search entries.")
    
    def _get_roles(self, wrestler_soup):
        return self._get_br_entries(wrestler_soup, "Roles:")

    def _get_trainers(self, wrestler_soup):
        trainer_entries = []

        try:
            trainers_data = self._get_wrestler_selected_element(wrestler_soup, "Trainer:", False).find_all('a', href=True)

            for trainer_data in trainers_data:
                trainer_entries.append(
                    Trainer(
                    trainer_data.text,
                    self._get_id_from_url(trainer_data['href'])
                ))

            return trainer_entries

        except:
            return trainer_entries

    def scrape_wrestler(self, cagematch_wrestler_id):
        logging.info(f"Scraping data for the wrestler with Cagematch ID of {cagematch_wrestler_id}.")
        wrestler_soup = self._scrape_data(f"https://www.cagematch.net/?id=2&nr={str(cagematch_wrestler_id)}")
        return self._construct_wrestler_data(cagematch_wrestler_id, wrestler_soup)
