import math
import time

# --- Definitionen (wie oben) ---
PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = '.'

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

# --- Minimax-Algorithmus (wie oben) ---

def minimax(board, depth, is_maximizing_player):
    """
    Implementiert den Minimax-Algorithmus.
    PLAYER_O ist der maximierende Spieler (KI).
    PLAYER_X ist der minimierende Spieler (Mensch).
    """

    # 1. Terminal-Bedingungen (Ende des Spiels)
    if is_winner(board, PLAYER_O):
        return 10 - depth  # KI gewinnt
    if is_winner(board, PLAYER_X):
        return depth - 10  # Mensch gewinnt
    if is_board_full(board):
        return 0  # Unentschieden

    # 2. Rekursive Aufrufe
    if is_maximizing_player:
        best_score = -math.inf
        for (row, col) in get_available_moves(board):
            board[row][col] = PLAYER_O
            score = minimax(board, depth + 1, False)
            board[row][col] = EMPTY
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for (row, col) in get_available_moves(board):
            board[row][col] = PLAYER_X
            score = minimax(board, depth + 1, True)
            board[row][col] = EMPTY
            best_score = min(score, best_score)
        return best_score

def find_best_move(board):
    """
    Findet den besten Zug für die KI (PLAYER_O).
    """
    best_score = -math.inf
    best_move = None

    for (row, col) in get_available_moves(board):
        board[row][col] = PLAYER_O
        move_score = minimax(board, 0, False)
        board[row][col] = EMPTY

        if move_score > best_score:
            best_score = move_score
            best_move = (row, col)
            
    return best_move

# --- NEU: Spiellogik und Ausgabe ---

def print_board(board):
    """Gibt das Spielfeld hübsch in der Konsole aus."""
    print("\n  0 1 2")
    for i, row in enumerate(board):
        print(f"{i} {' '.join(row)}")
    print()

def main_game():
    """Die Haupt-Spielschleife."""
    
    # Erstellt ein leeres 3x3-Spielfeld
    board = [[EMPTY for _ in range(3)] for _ in range(3)]
    
    # Spieler X (Mensch) fängt an
    current_player = PLAYER_X

    while True:
        print_board(board)
        
        if current_player == PLAYER_X:
            # Menschlicher Spieler
            print("Spieler X (Du) ist am Zug.")
            try:
                row = int(input("Gib die Zeile ein (0, 1, oder 2): "))
                col = int(input("Gib die Spalte ein (0, 1, oder 2): "))

                if row in [0, 1, 2] and col in [0, 1, 2] and board[row][col] == EMPTY:
                    board[row][col] = PLAYER_X
                    current_player = PLAYER_O # Zum nächsten Spieler wechseln
                else:
                    print("Ungültiger Zug. Feld ist besetzt oder außerhalb des Bereichs.")
                    continue
            except ValueError:
                print("Ungültige Eingabe. Bitte nur Zahlen eingeben.")
                continue
        
        else:
            # KI-Spieler (PLAYER_O)
            print("Spieler O (KI) denkt nach...")
            #time.sleep(1) # Kleine Pause für Dramatik
            
            move = find_best_move(board)
            if move:
                board[move[0]][move[1]] = PLAYER_O
                print(f"KI spielt auf ({move[0]}, {move[1]})")
                current_player = PLAYER_X # Zum nächsten Spieler wechseln
        
        # --- Spielende prüfen ---
        if is_winner(board, PLAYER_X):
            print_board(board)
            print("Herzlichen Glückwunsch! Spieler X (Du) hat gewonnen!")
            break
            
        if is_winner(board, PLAYER_O):
            print_board(board)
            print("Schade! Spieler O (KI) hat gewonnen!")
            break
            
        if is_board_full(board):
            print_board(board)
            print("Unentschieden!")
            break

# --- Das Spiel starten ---
if __name__ == "__main__":
    main_game()