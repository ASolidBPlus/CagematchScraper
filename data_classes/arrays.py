from dataclasses import dataclass
from data_classes.cagematchobject import CagematchObject
from data_classes.search_results import *
import concurrent.futures

@dataclass
class CagematchObjectArray(CagematchObject):
    __items: list

    def get_array_type(self):
        if self.__items:
            base_type = type(self.__items[0])

            if all(isinstance(item, base_type) for item in self.__items):
                return str(self.__items[0].__class__.__name__)

        return str(self.__class__.__name__)

    def to_dict(self):
        # base_dict = {'array_type': self.get_array_type()}
        dict_data = {'array_type': self.get_array_type()}
        items_data = []
        for item in self.__items:
            items_data.append(item.to_dict())

        dict_data['items'] = items_data

        return dict_data

    def get_items(self):
        return self.__items

    def set_items(self, items):
        self.__items = items

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.__items)

    def __getitem__(self, key):
        return self.items[key]

    def __setitem__(self, key, value):
        self.__items[key] = value


@dataclass
class SearchResultArray(CagematchObjectArray):

    def non_threaded_convert_to_objects(self):
        full_objects = []

        for search_result in self:
            full_objects.append(search_result.get_full_object())

        return CagematchObjectArray(full_objects)

    def convert_to_objects(self):
        full_objects = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit tasks to be executed concurrently
            tasks = [executor.submit(search_result.get_full_object) for search_result in self]

            # Wait for all tasks to complete
            concurrent.futures.wait(tasks)

            # Retrieve the results of the tasks
            full_objects = [task.result() for task in tasks]

        return CagematchObjectArray(full_objects)
