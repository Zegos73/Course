import tkinter as tk
from tkinter import messagebox
user_database = {}
def register_user():
    username = username_entry.get()
    password = password_entry.get()

    if username and password:
        if username in user_database:
            messagebox.showerror("Ошибка регистрации", "Пользователь с таким именем уже существует.")
        else:
            user_database[username] = password
            messagebox.showinfo("Регистрация успешна",
                                "Регистрация прошла успешно. Пожалуйста, войдите с вашим именем и паролем.")
            clear_entries()
    else:
        messagebox.showwarning("Ошибка регистрации", "Пожалуйста, заполните оба поля.")
def login_user():
    username = username_entry.get()
    password = password_entry.get()
    if username and password:
        if username in user_database and user_database[username] == password:
            messagebox.showinfo("Вход выполнен успешно", "Вход выполнен успешно.")
            clear_entries()
            open_main_window(username)
        else:
            messagebox.showerror("Ошибка входа", "Ошибка входа. Пожалуйста, проверьте ваше имя пользователя и пароль.")
    else:
        messagebox.showwarning("Ошибка входа", "Пожалуйста, заполните оба поля.")
def clear_entries():
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
def open_main_window(username):
    root.destroy()
    main_window = tk.Tk()
    main_window.title("Главное окно")
    main_window.geometry("700x300")
    label = tk.Label(main_window, text=f"Добро пожаловать, {username}!")
    label.pack()
    main_window.mainloop()

root = tk.Tk()
root.title("Регистрация и вход")
root.geometry("300x200")
username_label = tk.Label(root, text="Имя пользователя:")
username_label.pack()

username_entry = tk.Entry(root)
username_entry.pack()

password_label = tk.Label(root, text="Пароль:")
password_label.pack()

password_entry = tk.Entry(root, show="*")
password_entry.pack()

register_button = tk.Button(root, text="Регистрация", command=register_user)
register_button.pack()

login_button = tk.Button(root, text="Вход", command=login_user)
login_button.pack()

root.mainloop()
class CheckersApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Шашки")
        self.current_player = 1  # Начинает первый игрок
        self.board = [
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [-1, 0, -1, 0, -1, 0, -1, 0],
            [0, -1, 0, -1, 0, -1, 0, -1],
            [-1, 0, -1, 0, -1, 0, -1, 0]]
        self.selected_piece = None
        self.create_board()

    def create_board(self):
        self.canvas = tk.Canvas(self.root, width=512, height=512, bg="white")
        self.canvas.pack()

        self.load_images()
        self.draw_board()
        self.draw_pieces()

        self.canvas.bind("<Button-1>", self.on_click)

    def load_images(self):
        self.white_piece = tk.PhotoImage(file="1.png")
        self.black_piece = tk.PhotoImage(file="2.png")
        self.white_king = tk.PhotoImage(file="3.png")
        self.black_king = tk.PhotoImage(file="4.png")

    def draw_board(self):
        for i in range(8):
            for j in range(8):
                color = "white" if (i + j) % 2 == 0 else "black"
                self.canvas.create_rectangle(j * 64, i * 64, (j + 1) * 64, (i + 1) * 64, fill=color)

    def draw_pieces(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != 0:
                    x = j * 64 + 32
                    y = i * 64 + 32
                    piece = self.board[i][j]
                    if abs(piece) == 1:
                        if piece == 1:
                            self.canvas.create_image(x, y, image=self.white_piece, tags=("piece", f"{i}_{j}"))
                        else:
                            self.canvas.create_image(x, y, image=self.black_piece, tags=("piece", f"{i}_{j}"))
                    elif abs(piece) == 2:
                        if piece == 2:
                            self.canvas.create_image(x, y, image=self.white_king, tags=("piece", f"{i}_{j}"))
                        else:
                            self.canvas.create_image(x, y, image=self.black_king, tags=("piece", f"{i}_{j}"))

    def on_click(self, event):
        x, y = event.x // 64, event.y // 64
        piece = self.board[y][x]

        if piece != 0 and (piece == self.current_player or abs(piece) == 2):  # Условие для выбора дамки
            if self.selected_piece:
                self.canvas.itemconfig(self.selected_piece, outline="black")
            self.selected_piece = (x, y)
            self.canvas.create_rectangle(x * 64, y * 64, (x + 1) * 64, (y + 1) * 64, outline="red", width=3, tags="selected_outline")
        elif self.selected_piece:
            self.move_piece(x, y)

    def move_piece(self, x, y):
        piece_x, piece_y = self.selected_piece

        direction = 1 if self.current_player == 1 else -1  # Направление движения шашки вперед

        if abs(piece_x - x) == abs(piece_y - y) == 2 and self.board[y][x] == 0:
            taken_x = (piece_x + x) // 2  # Получаем координаты взятой шашки
            taken_y = (piece_y + y) // 2

            self.board[y][x] = self.board[piece_y][piece_x]
            self.board[piece_y][piece_x] = 0
            self.board[taken_y][taken_x] = 0
            self.check_kings()  # Проверка, стала ли шашка дамкой после хода
            self.draw_board()
            self.draw_pieces()

            # Передаем ход другому игроку после хода дамки
            self.current_player = -self.current_player

            self.canvas.delete("selected_outline")
            self.selected_piece = None
            self.game_over()  # Проверка завершения игры
            return

        # Условие для обычных шашек
        if (y - piece_y == direction) and abs(x - piece_x) == 1 and self.board[y][x] == 0:
            self.board[y][x] = self.board[piece_y][piece_x]
            self.board[piece_y][piece_x] = 0
            self.check_kings()  # Проверка, стала ли шашка дамкой после хода
            self.draw_board()
            self.draw_pieces()

            # Передаем ход другому игроку
            self.current_player = -self.current_player

            self.canvas.delete("selected_outline")
            self.selected_piece = None
            self.game_over()  # Проверка завершения игры
            return

        # Условие для дамок
        if abs(piece_x - x) == abs(piece_y - y) > 0 and self.board[y][x] == 0:
            blocked = False
            for i in range(1, abs(piece_x - x)):
                if self.board[piece_y + i * (1 if y > piece_y else -1)][piece_x + i * (1 if x > piece_x else -1)] != 0:
                    blocked = True
                    break
            if not blocked:
                self.board[y][x] = self.board[piece_y][piece_x]
                self.board[piece_y][piece_x] = 0
                self.check_kings()  # Проверка, стала ли шашка дамкой после хода
                self.draw_board()
                self.draw_pieces()

                # Передаем ход другому игроку после хода дамки
                self.current_player = -self.current_player

                self.canvas.delete("selected_outline")
                self.selected_piece = None
                self.game_over()  # Проверка завершения игры
                return

        self.canvas.delete("selected_outline")
        self.selected_piece = None

    def check_kings(self):
        for j in range(8):
            if self.board[0][j] == -1:
                self.board[0][j] = -2  # Черные шашки становятся дамками
            if self.board[7][j] == 1:
                self.board[7][j] = 2   # Белые шашки становятся дамками

    def count_pieces(self, player):
        count = 0
        for row in self.board:
            count += row.count(player) + row.count(player * 2)
        return count

    def game_over(self):
        white_pieces_left = self.count_pieces(1)
        black_pieces_left = self.count_pieces(-1)

        if white_pieces_left == 0:
            messagebox.showinfo("Конец игры", "Игра завершена. У белого игрока не осталось шашек.")
        elif black_pieces_left == 0:
            messagebox.showinfo("Конец игры", "Игра завершена. У черного игрока не осталось шашек.")
        elif not self.check_possible_moves(1) and not self.check_possible_moves(-1):
            messagebox.showinfo("Конец игры", "Игра завершена. Нет возможных ходов для обоих игроков.")

    def check_possible_moves(self, player):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == player or self.board[i][j] == player * 2:
                    # Проверяем возможные ходы для шашек этого игрока
                    if self.can_move_forward(i, j, player) or self.can_jump(i, j, player):
                        return True
        return False

    def can_move_forward(self, i, j, player):
        direction = 1 if player == 1 else -1
        if 0 <= i + direction < 8 and 0 <= j + 1 < 8:
            if self.board[i + direction][j + 1] == 0:
                return True
        if 0 <= i + direction < 8 and 0 <= j - 1 < 8:
            if self.board[i + direction][j - 1] == 0:
                return True
        return False

    def can_jump(self, i, j, player):
        directions = [(1, 1), (1, -1)] if player == 1 else [(-1, 1), (-1, -1)]
        for direction in directions:
            x, y = direction
            if 0 <= i + 2*x < 8 and 0 <= j + 2*y < 8:
                if self.board[i + x][j + y] == -player or self.board[i + x][j + y] == -player * 2:
                    if self.board[i + 2*x][j + 2*y] == 0:
                        return True
        return False


def main():
    root = tk.Tk()
    app = CheckersApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()


