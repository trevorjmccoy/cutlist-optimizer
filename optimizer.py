def best_fit(depth, kerf, stocks_lengths, stocks_quantities, cuts_lengths, cuts_quantities, cuts_left_wall_angles, cuts_right_wall_angles):
    from math import tan, radians, ceil, floor
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
        return {"error": "One or more required cuts are larger than the available stock."}

    # Initialize result with stocks
    for i, stock in enumerate(stocks):
        result[i] = [stock, [], stock]  # [original stock length, list of cuts, remaining length]

    # Allocate cuts
    for cut in cuts:
        best_fit_index = None
        min_remaining_space = float('inf')

        for index, value in result.items():
            # Check if the stock already has a cut.
            if value[1]:
                remaining_space = value[2] - (kerf + cut)
            else:
                remaining_space = value[2] - cut

            # Find the stock that minimizes the remaining space after placement.
            if remaining_space >= 0 and remaining_space < min_remaining_space:
                best_fit_index = index
                min_remaining_space = remaining_space

        # If a suitable stock was found, place the cut.
        if best_fit_index is not None:
            if result[best_fit_index][1]:
                result[best_fit_index][1].append((kerf, cut))
                result[best_fit_index][2] -= (kerf + cut)
            else:
                result[best_fit_index][1].append((0, cut))
                result[best_fit_index][2] -= cut
        else:
            return {"error": "Not enough stock to accommodate cuts."}
        
    # Round down remaining_space for better display
    for v in result.values():
        v[2] = floor(v[2] * 1000) / 1000

    # Remove empty stock
    final_result = {k: v for k, v in result.items() if v[1]!= []}
    
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

    




