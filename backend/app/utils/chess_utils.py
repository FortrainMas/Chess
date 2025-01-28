def allowed_move(game_field, turn, move):
    def is_in_bounds(row, col):
        """Check if the given position is within the chessboard."""
        return 0 <= row < 8 and 0 <= col < 8

    def is_opponent_piece(piece):
        """Check if a piece belongs to the opponent."""
        if turn == "white":
            return piece.islower()
        return piece.isupper()

    def is_valid_pawn_move(start, end, piece):
        """Validate pawn moves."""
        direction = -1 if piece.isupper() else 1  # White moves up (-1), black moves down (+1)
        start_row, start_col = start
        end_row, end_col = end
        diff_row = end_row - start_row
        diff_col = abs(end_col - start_col)

        # Standard one-step forward
        if diff_row == direction and diff_col == 0 and game_field[end_row][end_col] == "":
            return True

        # Initial two-step move
        if (start_row == 6 and piece.isupper() or start_row == 1 and piece.islower()) and \
           diff_row == 2 * direction and diff_col == 0 and game_field[start_row + direction][start_col] == "" and game_field[end_row][end_col] == "":
            return True

        # Diagonal capture
        if diff_row == direction and diff_col == 1 and is_opponent_piece(game_field[end_row][end_col]):
            return True

        return False

    def is_valid_rook_move(start, end):
        """Validate rook moves."""
        start_row, start_col = start
        end_row, end_col = end

        # Ensure either the row or column is unchanged
        if start_row != end_row and start_col != end_col:
            return False

        # Check for obstruction in the path
        if start_row == end_row:  # Horizontal move
            step = 1 if start_col < end_col else -1
            for col in range(start_col + step, end_col, step):
                if game_field[start_row][col] != "":
                    return False
        else:  # Vertical move
            step = 1 if start_row < end_row else -1
            for row in range(start_row + step, end_row, step):
                if game_field[row][start_col] != "":
                    return False

        return True

    def is_valid_knight_move(start, end):
        """Validate knight moves."""
        start_row, start_col = start
        end_row, end_col = end
        diff_row = abs(end_row - start_row)
        diff_col = abs(end_col - start_col)

        return (diff_row, diff_col) in [(2, 1), (1, 2)]

    def is_valid_bishop_move(start, end):
        """Validate bishop moves."""
        start_row, start_col = start
        end_row, end_col = end
        diff_row = abs(end_row - start_row)
        diff_col = abs(end_col - start_col)

        # Ensure diagonal move
        if diff_row != diff_col:
            return False

        # Check for obstruction in the path
        step_row = 1 if end_row > start_row else -1
        step_col = 1 if end_col > start_col else -1
        for i in range(1, diff_row):
            if game_field[start_row + i * step_row][start_col + i * step_col] != "":
                return False

        return True

    def is_valid_queen_move(start, end):
        """Validate queen moves."""
        return is_valid_rook_move(start, end) or is_valid_bishop_move(start, end)

    def is_valid_king_move(start, end):
        """Validate king moves."""
        start_row, start_col = start
        end_row, end_col = end
        diff_row = abs(end_row - start_row)
        diff_col = abs(end_col - start_col)

        return max(diff_row, diff_col) == 1

    # Extract move details
    (from_row, from_col), (to_row, to_col) = move

    # Check bounds
    if not (is_in_bounds(from_row, from_col) and is_in_bounds(to_row, to_col)):
        return False

    # Check if the starting position has a piece belonging to the current player
    piece = game_field[from_row][from_col]
    if not piece or (turn == "white" and piece.islower()) or (turn == "black" and piece.isupper()):
        return False

    # Check if the destination is not occupied by the current player's piece
    target_piece = game_field[to_row][to_col]
    if (turn == "white" and target_piece.isupper()) or (turn == "black" and target_piece.islower()):
        return False

    # Validate based on piece type
    piece = piece.lower()
    if piece == "p":  # Pawn
        return is_valid_pawn_move((from_row, from_col), (to_row, to_col), game_field[from_row][from_col])
    elif piece == "r":  # Rook
        return is_valid_rook_move((from_row, from_col), (to_row, to_col))
    elif piece == "n":  # Knight
        return is_valid_knight_move((from_row, from_col), (to_row, to_col))
    elif piece == "b":  # Bishop
        return is_valid_bishop_move((from_row, from_col), (to_row, to_col))
    elif piece == "q":  # Queen
        return is_valid_queen_move((from_row, from_col), (to_row, to_col))
    elif piece == "k":  # King
        return is_valid_king_move((from_row, from_col), (to_row, to_col))

    return False
