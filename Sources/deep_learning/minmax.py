function minimax(position, depth, maxmizingPlayer)
    if depth == 0 or game over in position
        return static evaluation of position

    if maximizingPlayer:
        maxEval = -infinity
        alpha = +infinity
        if alpha > beta:
            for each child in position:
                eval = minimax(child, depth - 1, false)
                maxEval = max(maxEval, eval)
                
        for each child of position
            eval = minimax(child, depth -1, false)
            maxEval = max(maxEval, eval)
        alpha = +infinity
            = max(maxEval, )
        return maxEval

    else
        minEval = +infinity
        for each child of position
            eval = minmax(child, depth -1, True)
            minEval = min(minEval, eval)
        return minEval