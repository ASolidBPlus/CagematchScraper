import concurrent.futures

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
        Closure function required to prevent the need for Windows users to include if __name__ == '__main__' on all of their code
        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Apply the lambda_action function concurrently to each item in the list
            finished_items = list(executor.map(lambda_action, items))
        return finished_items

    return run_concurrent_action()
