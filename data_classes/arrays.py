from data_classes.cagematch_object import CagematchObject
import data_classes.wrestler 
import data_classes.trainer
import data_classes.search_results
import concurrent.futures
import global_utils

class CagematchObjectArray(list, CagematchObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_dict(self, **kwargs):
        dict_data = {}
    
        dict_data['total_items'] = len(self)
        dict_data.update(kwargs)
        dict_data['items'] = [item.to_dict() if isinstance(item, CagematchObject) else item for item in self]
    
        return super().to_dict(**dict_data)
    
    def array_type(self):
        return self.__class__.__name__


class ConvertableObjectArray(CagematchObjectArray):
    def non_threaded_convert_to_objects(self):
        full_objects = []

        for partial_object in self:
            full_objects.append(partial_object.get_full_object())

        return create_array(full_objects)

    def convert_to_objects(self):

        return global_utils.concurrent_action(self, lambda x: x.get_full_object())



class SearchResultArray(ConvertableObjectArray):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search_params = kwargs        


class TrainerArray(ConvertableObjectArray):
    pass


class WrestlerArray(CagematchObjectArray):
    pass


def create_array(items: list):
    try:
        base_item_type = type(items[0])
        
        if all(isinstance(item, base_item_type) for item in items):
        
            if base_item_type == data_classes.wrestler.Wrestler:
                return WrestlerArray(items)
            
            elif base_item_type == data_classes.trainer.Trainer:
                return TrainerArray(items)
            
            elif issubclass(base_item_type, data_classes.search_results.BaseSearchEntry):
                return SearchResultArray(items)
        
        return CagematchObjectArray(items)
    
    except IndexError:
        return None