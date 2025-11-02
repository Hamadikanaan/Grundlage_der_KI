import math
import time

# --- Definitionen (Wichtig für Tic Tac Toe) ---
PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = '.'

# Globaler Zähler für die Knoten
NODE_COUNTER = 0

# --- Spiel-Hilfsfunktionen (Wichtig für Tic Tac Toe) ---

def is_winner(board, player):
    """Prüft, ob der angegebene Spieler gewonnen hat."""
    # Horizontale Prüfung
    for row in range(3):
        if all(board[row][col] == player for col in range(3)):
            return True
    # Vertikale Prüfung
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    # Diagonale Prüfungen
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_board_full(board):
    """Prüft, ob das Spielfeld voll ist."""
    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                return False
    return True

def get_available_moves(board):
    """Gibt eine Liste aller möglichen Züge (row, col) zurück."""
    moves = []
    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                moves.append((row, col))
    return moves

# --- Version 1: Standard Minimax (Algorithmus) ---

def minimax_ohne_pruning(board, depth, is_maximizing_player):
    global NODE_COUNTER
    NODE_COUNTER += 1 # Knoten zählen

    if is_winner(board, PLAYER_O): return 10 - depth
    if is_winner(board, PLAYER_X): return depth - 10
    if is_board_full(board): return 0

    if is_maximizing_player:
        best_score = -math.inf
        for (row, col) in get_available_moves(board):
            board[row][col] = PLAYER_O
            score = minimax_ohne_pruning(board, depth + 1, False)
            board[row][col] = EMPTY
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for (row, col) in get_available_moves(board):
            board[row][col] = PLAYER_X
            score = minimax_ohne_pruning(board, depth + 1, True)
            board[row][col] = EMPTY
            best_score = min(score, best_score)
        return best_score

def find_best_move_ohne_pruning(board):
    global NODE_COUNTER
    NODE_COUNTER = 0 # Zähler zurücksetzen
    best_score = -math.inf
    
    for (row, col) in get_available_moves(board):
        board[row][col] = PLAYER_O
        move_score = minimax_ohne_pruning(board, 0, False)
        board[row][col] = EMPTY
        if move_score > best_score:
            best_score = move_score
    return NODE_COUNTER


# --- Version 2: Minimax MIT Alpha-Beta-Pruning (Algorithmus) ---

def minimax_mit_pruning(board, depth, is_maximizing_player, alpha, beta):
    global NODE_COUNTER
    NODE_COUNTER += 1 # Knoten zählen

    if is_winner(board, PLAYER_O): return 10 - depth
    if is_winner(board, PLAYER_X): return depth - 10
    if is_board_full(board): return 0

    if is_maximizing_player:
        best_score = -math.inf
        for (row, col) in get_available_moves(board):
            board[row][col] = PLAYER_O
            score = minimax_mit_pruning(board, depth + 1, False, alpha, beta)
            board[row][col] = EMPTY
            best_score = max(score, best_score)
            
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break # Beta-Schnitt
        return best_score
    else:
        best_score = math.inf
        for (row, col) in get_available_moves(board):
            board[row][col] = PLAYER_X
            score = minimax_mit_pruning(board, depth + 1, True, alpha, beta)
            board[row][col] = EMPTY
            best_score = min(score, best_score)
            
            beta = min(beta, best_score)
            if alpha >= beta:
                break # Alpha-Schnitt
        return best_score

def find_best_move_mit_pruning(board):
    global NODE_COUNTER
    NODE_COUNTER = 0 # Zähler zurücksetzen
    best_score = -math.inf

    for (row, col) in get_available_moves(board):
        board[row][col] = PLAYER_O
        move_score = minimax_mit_pruning(board, 0, False, -math.inf, math.inf)
        board[row][col] = EMPTY
        if move_score > best_score:
            best_score = move_score
    return NODE_COUNTER


# --- Hauptteil (Aufgabe 2: Vergleich der Knoten) ---

if __name__ == "__main__":
    # Szenario: Ein leeres Spielfeld.
    empty_board = [[EMPTY for _ in range(3)] for _ in range(3)]

    print("Starte Vergleich der Knotenberechnungen...")
    print("Szenario: Leeres Spielfeld (Berechnung des ersten Zugs)")
    
    time.sleep(1)

    # Test 1: Ohne Pruning
    print("\nBerechne mit Standard-Minimax...")
    start_time = time.time()
    count_ohne_pruning = find_best_move_ohne_pruning(empty_board)
    end_time = time.time()
    print(f"Standard Minimax: {count_ohne_pruning} Knoten berechnet.")
    print(f"(Benötigte Zeit: {end_time - start_time:.4f} Sekunden)")


    # Test 2: Mit Pruning
    print("\nBerechne mit Alpha-Beta-Pruning...")
    start_time = time.time()
    count_mit_pruning = find_best_move_mit_pruning(empty_board)
    end_time = time.time()
    print(f"Mit Alpha-Beta-Pruning: {count_mit_pruning} Knoten berechnet.")
    print(f"(Benötigte Zeit: {end_time - start_time:.4f} Sekunden)")

    # Ergebnis
    if count_ohne_pruning > 0:
        reduktion = 100 - (count_mit_pruning / count_ohne_pruning * 100)
        print(f"\nReduktion der Knoten: {reduktion:.2f}%")