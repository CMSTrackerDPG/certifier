def uniquely_sorted(list_of_elements):
    new_list = list(set(extract_numbers_from_list(list_of_elements)))
    new_list.sort()
    return new_list

