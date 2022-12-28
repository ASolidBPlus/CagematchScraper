class CagematchObject:
    """Base class for all Cagematch objects.
    
    This class serves as the base for all objects in the Cagematch system and
    provides a `to_dict` method for converting objects to dictionaries.
    
    Attributes:
        Any attributes specific to the subclass.
    """
    def _recursive_to_dict(self, obj):
        """Convert an object or a list of objects recursively to a dictionary.
        
        If the object is a CagematchObject, its `to_dict` method is called to
        convert it to a dictionary. If the object is a list, this method is
        called recursively on each item in the list. Otherwise, the object is
        returned as is.
        
        Args:
            obj (object): The object to be converted.
        
        Returns:
            dict: The converted object.
        """
        if isinstance(obj, CagematchObject):
            return obj.to_dict()

        elif isinstance(obj, list):
            return [self._recursive_to_dict(item) for item in obj]
            
        return obj
    
    def to_dict(self):
        """Convert the CagematchObject to a dictionary.
        
        This method converts the CagematchObject and all of its attributes
        to a dictionary by calling the `_recursive_to_dict` method on each
        attribute.
        
        Returns:
            dict: The converted CagematchObject.
        """
        return {attr: self._recursive_to_dict(value) for attr, value in vars(self).items()}
