import logging
from cagematch.accessors.cagematch_accessor import CagematchAccessor
import re


class CagematchEventAccessor(CagematchAccessor):
    @classmethod
    def scrape_event(cls, cagematch_id, search_result=None):
        url = cls._build_url(id=1, nr=cagematch_id)

        event_soup = cls._scrape_data(url)
        cls._construct_event_data(event_soup)

    @classmethod
    def _construct_event_data(cls, soup):
        data = {}

        data['event_name'] = cls._get_event_name(soup)
        data['date'] = cls._get_event_date(soup)
        data['event_type'] = cls._get_event_type(soup)
        data['location'] = cls._get_event_location(soup)
        data['arena'] = cls._get_event_arena(soup)
        data['attendance'] = cls._get_event_attendance(soup)
        data['broadcast_type'] = cls._get_event_broadcast_type(soup)
        data['broadcast_date'] = cls._get_event_broadcast_date(soup)
        data['tv_station_network'] = cls._get_tv_station_network(soup)
        data['matches'] = cls._get_matches(soup)

    @classmethod
    def _get_event_name(cls, soup):
        return cls._get_element_by_text_in_information_box(soup, "Name of the event:")

    @classmethod
    def _get_event_date(cls, soup):
        return cls._get_element_by_text_in_information_box(soup, "Date:")

    @classmethod
    def _get_event_type(cls, soup):
        return cls._get_element_by_text_in_information_box(soup, "Type:")

    @classmethod
    def _get_event_location(cls, soup):
        return cls._get_element_by_text_in_information_box(soup, "Location:")

    @classmethod
    def _get_event_arena(cls, soup):
        return cls._get_element_by_text_in_information_box(soup, "Arena:")

    @classmethod
    def _get_event_attendance(cls, soup):
        return cls._get_element_by_text_in_information_box(soup, "Attendance:")

    @classmethod
    def _get_event_broadcast_type(cls, soup):
        return cls._get_element_by_text_in_information_box(soup, "Broadcast type:")

    @classmethod
    def _get_event_broadcast_date(cls, soup):
        return cls._get_element_by_text_in_information_box(soup, "Broadcast date:")

    @classmethod
    def _get_tv_station_network(cls, soup):
        return cls._get_element_by_text_in_information_box(soup, "TV station/network:")

    @classmethod
    def _get_participants_data(cls, soup):
        participants_soup = soup.find('div', class_='Caption', text='All workers').find_next_sibling()
        
        # Extract the HTML of the div
        div_html = str(participants_soup)

        # Create a regular expression to match the text and link of an anchor element
        # The regular expression will match the opening and closing anchor tags, and capture the text and link
        pattern = r'<a href="(?P<link>.*?)">(?P<text>.*?)</a>'

        # Find all occurrences of the pattern in the HTML
        matches = re.finditer(pattern, div_html)

        # Create an empty list to store the text and links
        elements_list = []

        # Iterate through the matches
        for match in matches:
            # Extract the text and link from the match
            text = match.group('text')
            link = match.group('link')
            elements_list.append({'text': text, 'link': link})  # Add the text and link to the list

        # Extract the remaining text from the HTML
        remaining_text = re.sub(pattern, '', div_html)

        # Split the remaining text into a list, using the comma and space as the delimiter
        remaining_text_list = remaining_text.split(', ')

        # Remove any blank elements from the list
        remaining_text_list = [{'text': x, 'link': None} for x in remaining_text_list if x]


        # Add the remaining text items to the list
        elements_list.extend(remaining_text_list)

        return elements_list


    @classmethod
    def _get_matches(cls, soup):
        match_soup = soup.find_all("div", class_="Match")
        participant_data = cls._get_participants_data(soup)
        print(participant_data)
