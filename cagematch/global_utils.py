import concurrent.futures
import json

def concurrent_action(items, lambda_action):
    """
    Perform concurrent execution on a list of items using a given lambda function.
    
    Parameters:
    - items: list of items to process concurrently
    - lambda_action: lambda function to apply to each item in the list
    
    Returns:
    - list of processed items in the same order as the input list
    """
    def run_concurrent_action():
        """
        Closure function required to prevent the need for Windows users to include if __name__ == '__main__' on all
        of their code
        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Apply the lambda_action function concurrently to each item in the list
            finished_items = list(executor.map(lambda_action, items))
        return finished_items

    return run_concurrent_action()

def pair(input_list):
    """Convert a list of elements to a string of the form "x, y, z & w".
    
    Args:
        input_list: The list to be converted.
    
    Returns:
        The input list as a string, with ", " between each element and " & "
        before the last element.
    """
    # If the input list is empty, return an empty string
    if not input_list:
        return ""
    
    # If the input list is not a list, return its string representation
    if not isinstance(input_list, list):
        return str(input_list)
    
    # If the input list has only one element, return the string representation of that element
    # if it is a SingleParticipant object, or call pair() recursively if it is a list
    if len(input_list) == 1:
        if isinstance(input_list[0], list):
            return pair(input_list[0])
        else:
            return str(input_list[0])
    
    # If the input list has more than one element, call pair() recursively on each element
    # and join the results with ", " and " & " as appropriate
    result_string = ", ".join(pair(x) for x in input_list[:-1])
    result_string += " & " + pair(input_list[-1])
    return result_string

def to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data.to_dict(), file, indent=4)
