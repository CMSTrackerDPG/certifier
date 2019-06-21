def extract_numbers_from_list(list_of_elements):
    return [int(i) for i in list_of_elements if type(i) == int or i.isdigit()]

def uniquely_sorted(list_of_elements):
    new_list = list(set(extract_numbers_from_list(list_of_elements)))
    new_list.sort()
    return new_list
