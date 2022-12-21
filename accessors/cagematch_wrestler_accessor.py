import logging
import re

from accessors.cagematch_accessor import CagematchAccessor
from data_classes.wrestler import Wrestler
from data_classes.trainer import Trainer

class CagematchWrestlerAccessor(CagematchAccessor):

    @classmethod
    def _get_wrestler_selected_element(cls, wrestler_soup, text_search, return_text=True):
        selected_element = wrestler_soup.select(f"div.InformationBoxTitle:-soup-contains('{text_search}') + div.InformationBoxContents")
        
        if selected_element:
            try:
                if return_text:
                    return selected_element[0].text.strip()

                return selected_element[0]
            except:
                logging.warning(f"An exception was raised when attempting to get the content of the elected element in _get_wrestler_selected_element when searching for {text_search}")

        logging.info(f"No data was found when searching for {text_search}")
        return None

    @classmethod
    def _construct_wrestler_data(cls, cagematch_wrestler_id, wrestler_soup, search_result=None):
        data = {}
        if search_result:
            print("Testing")
            data['cagematch_wrestler_id'] = search_result.result_id
            data['main_name'] = search_result.gimmick
            data['dob'] = search_result.birthday
            data['birthplace'] = search_result.birthplace
            data['height'] = search_result.height
            data['weight'] = search_result.weight

        else:
            data['cagematch_wrestler_id'] = cagematch_wrestler_id
            data['main_name'] = cls._get_main_name(wrestler_soup)
            data['dob'] = cls._get_dob(cagematch_wrestler_id, wrestler_soup)
            data['birthplace'] = cls._get_birthplace(wrestler_soup)
            data['height'] = cls._get_height(wrestler_soup)
            data['weight'] = cls._get_weight(wrestler_soup)

        data['gender'] = cls._get_gender(wrestler_soup)
        data['alter_egos'] = cls._get_alter_egos(wrestler_soup)
        data['background_in_sports'] = cls._get_background_in_sports(wrestler_soup)
        data['social_media_links'] = cls._get_social_media_links(wrestler_soup)
        data['roles'] = cls._get_roles(wrestler_soup)
        data['wrestling_style'] = cls._get_wrestling_style(wrestler_soup)
        data['trainers'] = cls._get_trainers(wrestler_soup)
        data['nicknames'] = cls._get_nicknames(wrestler_soup)
        data['signature_moves'] = cls._get_signature_moves(wrestler_soup)
        
        return Wrestler(**data)

    @classmethod
    def _get_split_entries(cls, wrestler_soup, text_search):
        entry_data = cls._get_wrestler_selected_element(wrestler_soup, text_search)

        if entry_data is not None:
            try:
                return entry_data.split(", ")
            except:
                logging.warning(f"An exception was raised when attempting to split entry_data in _get_split_entries when searching for {text_search}")
                return None
        
        return None
    
    @classmethod
    def _get_br_entries(cls, wrestler_soup, text_search):
        br_data = cls._get_wrestler_selected_element(wrestler_soup, text_search, return_text=False)

        if br_data is not None:
            try:
                return [data.string for data in br_data.contents if data.string]
            except:
                logging.warning(f"An exception was raised when attempting to obtain br strings in _get_br_entries when searching for {text_search}")
                return None
        
        return None

    @classmethod
    def _get_metric(cls, metric_data, metric):
        match = re.search(fr"(\d+) {metric}", metric_data)
        
        if match:
            metric = int(match.group(1))
            return(metric)

        return None

    @classmethod
    def _get_main_name(cls, wrestler_soup):
        return wrestler_soup.find("h1").text

    @classmethod
    def _get_birthplace(cls, wrestler_soup):
        return cls._get_wrestler_selected_element(wrestler_soup, "Birthplace:")

    @classmethod
    def _get_gender(cls, wrestler_soup):
        return cls._get_wrestler_selected_element(wrestler_soup, "Gender:")

    @classmethod
    def _get_height(cls, wrestler_soup):
        height_data = cls._get_wrestler_selected_element(wrestler_soup, "Height:")

        if height_data is not None:
            return(cls._get_metric(height_data, 'cm'))
        
        return None

    @classmethod
    def _get_weight(cls, wrestler_soup):
        weight_data = cls._get_wrestler_selected_element(wrestler_soup, "Weight:")

        if weight_data is not None:
            return(cls._get_metric(weight_data, 'kg'))

        return None

    @classmethod
    def _get_background_in_sports(cls, wrestler_soup):
        return cls._get_split_entries(wrestler_soup, "Background in sports:")

    @classmethod
    def _get_social_media_links(cls, wrestler_soup):
        social_media_data = cls._get_wrestler_selected_element(wrestler_soup, "WWW:", return_text=False)

        if social_media_data is not None:
            return [link['href'] for link in social_media_data.find_all('a', href=True)]
        
        return None

    @classmethod
    def _get_wrestling_style(cls, wrestler_soup):
        return cls._get_split_entries(wrestler_soup, "Wrestling style:")

    @classmethod
    def _get_alter_egos(cls, wrestler_soup):
        alter_ego_data = cls._get_wrestler_selected_element(wrestler_soup, "Alter egos:", return_text=False)

        if alter_ego_data is not None:
            try:
                return [alter_ego.text.strip() for alter_ego in alter_ego_data.find_all('a')]
            except:
                return None
        
        return None

    @classmethod
    def _get_nicknames(cls, wrestler_soup):
        brs = cls._get_br_entries(wrestler_soup, "Nicknames:")

        if brs is not None: 
            return [nickname.strip('"') for nickname in brs]
        
        return brs

    @classmethod
    def _get_signature_moves(cls, wrestler_soup):
        return cls._get_br_entries(wrestler_soup, "Signature moves:")

    @classmethod
    def _get_dob(cls, cagematch_wrestler_id, wrestler_soup):
        search_term = cls._get_main_name(wrestler_soup).replace(" ", "+")
        search_url = f"https://www.cagematch.net/?id=2&view=workers&search={search_term}"
        search_soup = cls._scrape_data(search_url)

        table_content = cls._get_table_content(search_soup)

        for entry in table_content:
            link = entry.find('a', href=True)['href']
            link_id = cls._get_id_from_url(link)
            
            try:
                if link_id == str(cagematch_wrestler_id):
                    return entry.find_all("td")[2].text.replace(".", "/")

            except:
                logging.warning(f"An issue was found when attempting to parse the date for id {cagematch_wrestler_id}, this was done during matching regex for the id on one of the search entries.")
    
    @classmethod
    def _get_roles(cls, wrestler_soup):
        return cls._get_br_entries(wrestler_soup, "Roles:")

    @classmethod
    def _get_trainers(cls, wrestler_soup):
        trainer_entries = []

        try:
            trainers_data = cls._get_wrestler_selected_element(wrestler_soup, "Trainer:", False).find_all('a', href=True)

            for trainer_data in trainers_data:
                trainer_entries.append(
                    Trainer(
                    trainer_data.text,
                    cls._get_id_from_url(trainer_data['href'])
                ))

            return trainer_entries

        except:
            return trainer_entries

    @classmethod
    def scrape_wrestler(cls, cagematch_wrestler_id, search_result=None):
        print(search_result)
        logging.info(f"Scraping data for the wrestler with Cagematch ID of {cagematch_wrestler_id}.")
        wrestler_soup = cls._scrape_data(f"https://www.cagematch.net/?id=2&nr={str(cagematch_wrestler_id)}")
        return cls._construct_wrestler_data(cagematch_wrestler_id, wrestler_soup, search_result)
