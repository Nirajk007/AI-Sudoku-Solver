import streamlit as st
import copy

st.title("🧩 AI-Based Sudoku Solver")
st.write("Enter your Sudoku puzzle below and click 'Solve with AI'")


grid = []
for i in range(9):
    row = []
    cols = st.columns(9)
    for j in range(9):
        val = cols[j].text_input(f"r{i}c{j}", "", max_chars=1)
        val = val.strip()
        if val.isdigit():
            row.append(int(val))
        else:
            row.append(0)
    grid.append(row)


def is_valid(board, row, col, num):
    
    if num in board[row]: return False
    
    if num in [board[i][col] for i in range(9)]: return False
   
    box_r, box_c = 3*(row//3), 3*(col//3)
    for i in range(3):
        for j in range(3):
            if board[box_r+i][box_c+j] == num:
                return False
    return True


def find_empty(board):
    candidates = []
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                possible = [n for n in range(1,10) if is_valid(board, i, j, n)]
                candidates.append((len(possible), i, j, possible))
    if not candidates:
        return None  
    _, i, j, possible = min(candidates)
    return i, j, possible

def solve_sudoku(board):
    cell = find_empty(board)
    if cell is None:
        return True  
    i, j, possible = cell
    for num in possible:
        if is_valid(board, i, j, num):
            board[i][j] = num
            if solve_sudoku(board): return True
            board[i][j] = 0
    return False

if st.button("🧠 Solve with AI"):
    board_copy = copy.deepcopy(grid)

    if solve_sudoku(board_copy):
        st.success("✅ Sudoku Solved!")
        st.table(board_copy)
    else:
        st.error("❌ No solution found.")
