def best_fit(depth, stocks_lengths, stocks_quantities, cuts_lengths, cuts_quantities, cuts_left_wall_angles, cuts_right_wall_angles):
    from math import tan, radians, ceil
    # Expand stocks and cuts into pieces
    stocks = []
    cuts = []
    overhangs_left = [(tan(radians(90 - (angle / 2))) * depth) for angle in cuts_left_wall_angles]
    overhangs_right = [(tan(radians(90 - (angle / 2))) * depth) for angle in cuts_right_wall_angles]
    
    for length, quantity in zip(stocks_lengths, stocks_quantities):
        stocks.extend([length] * quantity)

    for length, quantity, overhang_left, overhang_right in zip(cuts_lengths, cuts_quantities, overhangs_left, overhangs_right):
        cuts.extend([ceil((length + overhang_left + overhang_right) * 1000) / 1000] * quantity)

    stocks.sort(reverse=True)
    cuts.sort(reverse=True)

    result = {} 

    # Check for impossible cases
    if cuts and stocks and cuts[0] > stocks[0]:
        return "One or more required cuts are larger than the available stock."

    # Initialize result with stocks
    for i, stock in enumerate(stocks):
        result[i] = [stock, [], stock]  # [original stock length, list of cuts, remaining length]

    # Allocate cuts
    for cut in cuts:
        best_fit_index = None
        min_remaining_space = float('inf')

        for index, value in result.items():
            remaining_space = value[2] - cut

            # Find the stock that minimizes remaining space after placement
            if remaining_space >= 0 and remaining_space < min_remaining_space:
                best_fit_index = index
                min_remaining_space = remaining_space

        # If a suitable stock was found, place the cut
        if best_fit_index is not None:
            result[best_fit_index][1].append(cut)
            result[best_fit_index][2] -= cut
        else:
            return "Not enough stock to accommodate cuts."

    # Format output (remove remaining length)
    final_result = {k: [v[0], v[1]] for k, v in result.items()}
    
    return final_result
   

if __name__ == '__main__':

    depth = 3
    stocks_lengths = [1000,2000,300,400,500]
    stocks_quantities = [1,2,3,4,5]
    cuts_lengths = [100,200,300,400,500]
    cuts_quantities = [1,2,3,4,5]
    cuts_left_wall_angles = [90,66,45,120,180]
    cuts_right_wall_angles = [45,180,90,66,120]

    print(best_fit(stocks_lengths, stocks_quantities, cuts_lengths, cuts_quantities, cuts_left_wall_angles, cuts_right_wall_angles, depth))

    




