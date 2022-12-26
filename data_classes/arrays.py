from data_classes.cagematchobject import CagematchObject
from data_classes.search_results import *
import concurrent.futures

class CagematchObjectArray(list, CagematchObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_dict(self):
        dict_data = {}
        dict_data['array_type'] = self.array_type()
        dict_data['total_items'] = len(self)
        dict_data['items'] = [self._recursive_to_dict(item) for item in self]
        
        return dict_data
    
    def array_type(self):
        return self.__class__.__name__


class ConvertableObjectArray(CagematchObjectArray):
    def non_threaded_convert_to_objects(self):
        full_objects = []

        for partial_object in self:
            full_objects.append(partial_object.get_full_object())

        return CagematchObjectArray(full_objects)

    def convert_to_objects(self):
        full_objects = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit tasks to be executed concurrently
            tasks = [executor.submit(partial_object.get_full_object) for partial_object in self]

            # Wait for all tasks to complete
            concurrent.futures.wait(tasks)

            # Retrieve the results of the tasks
            full_objects = [task.result() for task in tasks]

        return CagematchObjectArray(full_objects) 

class SearchResultArray(ConvertableObjectArray):
    pass

class TrainerArray(ConvertableObjectArray):
    pass