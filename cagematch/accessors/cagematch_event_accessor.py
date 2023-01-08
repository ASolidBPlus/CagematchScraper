import logging
from cagematch.accessors.cagematch_accessor import CagematchAccessor


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