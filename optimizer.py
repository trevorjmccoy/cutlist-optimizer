def first_fit(bin_size, items):
    bins = [[]]
    oversized_items = []

    for item in items:
        # catch items larger than max bin size
        if item > bin_size:
            oversized_items.append(item)
            continue

        else:
            # try to place item in available bin
            for bin in bins:
                if item <= bin_size - sum(bin):
                    bin.append(item)
                    break
            # no bin found; create new bin
            else:
                bins.append([item])

    if oversized_items:
        oversized_message = f"The following items are larger than the maximum available bin size: {oversized_items}"
    else:
        oversized_message = "All items fit within the bins"

    return bins, oversized_message   
    


def best_fit(bin_size, items):
    bins = [[]]
    oversized_items = []

    for item in items:
        # catch items larger than max bin size
        if item > bin_size:
            oversized_items.append(item)
            continue

        else:
            # check all bins to find the one with the tightest fit
            best_bin_index = -1
            min_space_left = bin_size + 1
            for i, bin in enumerate(bins):
                available_space = bin_size - sum(bin)
                if available_space >= item and available_space < min_space_left:
                    best_bin_index = i
                    min_space_left = available_space
            
            # place the item in the bin with the tightest fit. If no bin can fit the item, create a new bin and place the item there
            if best_bin_index == -1:
                bins.append([item])
            else:
                bins[best_bin_index].append(item)

    if oversized_items:
        oversized_message = f"The following items are larger than the maximum available bin size: {oversized_items}"
    else:
        oversized_message = "All items fit within the bins"

    return bins, oversized_message   

if __name__ == '__main__':

    item_list = [9,5,2,3,6,7,1,1,3,6,9,7,8,8,4,6,5,5]
    print('First Fit Tests: ')
    print(first_fit(10, item_list))
    print(first_fit(30, item_list))
    print(first_fit(50, item_list))
    print(first_fit(8, item_list))
    print(first_fit(4, item_list))

    print('')

    print('Best Fit Tests: ')
    print(best_fit(10, item_list))
    print(best_fit(30, item_list))
    print(best_fit(50, item_list))
    print(best_fit(8, item_list))
    print(best_fit(4, item_list))