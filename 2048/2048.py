import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
window = tk.Tk()
window.title('2048')

#tạo bảng màu
bg_color = {
        0: 'azure4',
        2: '#eee4da',
        4: '#ede0c8',
        8: '#fabb46',
        16: '#eda53f',
        32: '#fa9146',
        64: '#f65e3b',
        128: '#edcf72',
        256: '#edcc61',
        512: '#f2b179',
        1024: '#f59563',
        2048: '#edc22e',
    }
color = {
        0: 'azure4',
        2: '#776e65',
        4: '#785E4D',
        8: '#f9f6f2',
        16: '#f9f6f2',
        32: '#f9f6f2',
        64: '#f9f6f2',
        128: '#f9f6f2',
        256: '#f9f6f2',
        512: '#776e65',
        1024: '#573202',
        2048: '#261600',
    }

#tạo biến toàn cục
board = []
value = []
score = 0

def random_number():
    global board, value, size
    if can_move() == True: #chỉ sinh thêm số khi còn bước đi
        r = random.randrange(0, size)
        c = random.randrange(0, size)
        while value[r][c] != 0:
            r = random.randrange(0, size)
            c = random.randrange(0, size)

        num = random.choice([2, 4])
        board[r][c].config(text= str(num), bg= bg_color[num], fg= color[num])
        value[r][c] = num

def reverse():
    """
    Đảo ngược thứ tự của một mảng
    """
    global value, size
    for i in range(size):
        left = 0
        right = size-1
        while (left < right):
            value[i][left], value[i][right] = value[i][right], value[i][left]
            left += 1
            right -= 1

def transpose():
    """
    Chuyển vị ma trận
    """
    global value, size
    for i in range(size):
        for j in range(i):
            value[i][j], value[j][i] = value[j][i], value[i][j]

def compress():
    """
    Dồn số theo chiều từ phải sang trái
    """
    global value, size
    for i in range(size):
        pos = 0
        if value[i] == [0]*size: #nếu dòng toàn số 0 thì không cần dồn số
            continue
        while pos < size:
            while pos < size and value[i][pos] != 0: #tìm vị trí trống đầu tiên
                pos += 1
            if pos == size or (pos == size-1 and value[i][pos] != 0): #nếu dòng đã full hoặc còn trống 1 ô cuối thì k cần compress nữa
                break
            for j in range(pos+1, size): #tìm vị trí khác 0 đầu tiên ở dằng sau để dồn
                if value[i][j] != 0:
                    value[i][pos], value[i][j] = value[i][j], value[i][pos] #hoán đổi giá trị cho nhau
                    break #chỉ dồn 1 số duy nhất để tránh việc đằng sau còn nhiều số nữa
            pos += 1

def refill():
    """
    Cập nhật lại text ở các ô
    """
    global value, size
    for i in range(size):
        for j in range(size):
            new_value = value[i][j]
            if new_value <= 2048: #nếu những con số nhỏ hơn 2048 thì dùng bảng màu 2048
                board[i][j].config(text= str(new_value), bg= bg_color[new_value], fg= color[new_value])
            else:
                board[i][j].config(text=str(new_value), bg=bg_color[2048], fg=color[2048])

def can_move():
    """
    Kiểm tra xem còn ô trống nào trên bàn cờ không
    """
    global value, size
    for i in range(size):
        for j in range(size):
            if value[i][j] == 0:
                return True
    return False

def can_merge():
    """
    Kiểm tra xem còn có thể cộng dồn lại được không
    """
    global value, size
    for i in range(size): #kiểm tra theo hàng
        for j in range(size-1):
            if value[i][j] == value[i][j + 1]:
                return True

    for i in range(size-1): #kiểm tra theo cột
        for j in range(size):
            if value[i + 1][j] == value[i][j]:
                return True
    return False

def merge():
    """
    Cộng 2 ô liên tiếp giống nhau (theo chiều từ phải sang trái)
    """
    global value, size
    for i in range(size):
        for j in range(size-1):
            if value[i][j] == value[i][j+1] and value[i][j] != 0:
                value[i][j] = value[i][j] * 2
                value[i][j + 1] = 0

def end_game():
    """
    Kiểm tra xem thắng hay thua hay còn tiếp tục chơi được
    """
    global score, target
    #kiểm tra thắng
    if score == target:
        choose = messagebox.askyesno("2048", message="You win!!!\nDo you want to continue?")
        if choose == False:
            reset()

    #kiểm tra thua
    if (can_move() == False) and (can_merge() == False):
        messagebox.showinfo("2048", message="You lose!!!")
        reset()

def reset():
    global size
    for i in range(size):
        for j in range(size):
            value[i][j] = 0
    refill()
    random_number()
    update_score()

def update_score():
    global score, score_label, size, target
    max = 0
    for i in range(size):
        for j in range(size):
            if max < value[i][j]:
                max = value[i][j]
    if max != score: #nếu khác điểm cũ thì mới cập nhật lại
        score = max
        score_label.config(text="SCORE: " + str(score) + " / " + str(target))

def left():
    compress()
    merge()
    compress()
    refill()
    update_score()
    random_number()
    end_game()

def right():
    reverse()
    compress()
    merge()
    compress()
    reverse()
    refill()
    update_score()
    random_number()
    end_game()

def up():
    transpose()
    compress()
    merge()
    compress()
    transpose()
    refill()
    update_score()
    random_number()
    end_game()

def down():
    transpose()
    reverse()
    compress()
    merge()
    compress()
    reverse()
    transpose()
    refill()
    update_score()
    random_number()
    end_game()


#trang mở đầu
name_of_game = tk.Label(window, text = "Welcome to 2048!!!", font=("Arial Bold", 28), fg= '#F9F5F0', bg= '#b05b3b', width= 18, height=2)
name_of_game.pack(side='top')

size_label = tk.Label(window, text= 'Choose size of board: ', font=("Calibri", 12))
size_label.pack(side='top', padx=10, pady= 10, expand=True, fill='both')

list_size = [2, 3, 4, 5]
choose_size = ttk.Combobox(window, values=list_size)
choose_size.set("Choose size")
choose_size.pack(side='top', expand=True)

target_label = tk.Label(window, text= 'Choose target score: ', font=("Calibri", 12))
target_label.pack(side='top', padx=10, pady= 10, expand=True, fill='both')

list_target = [1024, 2048, 4096]
choose_target = ttk.Combobox(window, values=list_target)
choose_target.set("Choose score")
choose_target.pack(side='top', expand=True)

def second_page():
    # đổi màu nền
    window.config(bg='azure3')

    # chia khung tạo bố cục
    frame_label = tk.Frame(window, bg='azure3', padx=10, pady=10)
    frame_label.pack(side='top')
    frame_board = tk.Frame(window, bg='#7a7877', padx=10, pady=10)
    frame_board.pack(side='top')
    frame_keys = tk.Frame(window, bg='azure3', padx=10, pady=10)
    frame_keys.pack(side='bottom')

    # tạo tên trò chơi
    label = tk.Label(frame_label, text="Welcome to\n2048", font=("Arial Bold", 24), bg='#F9F5F0', fg='#b05b3b',
                     width=10, height=2)
    label.pack(side='left', padx=10, pady=10)

    # tạo bảng điểm
    global score_label
    score_label = tk.Label(frame_label, text="SCORE: 0", font=("Arial Bold", 15), bg='#753422', fg='#F4DFBA')
    score_label.pack(side='top', padx=10, pady=10)

    # tạo nút New Game
    new_game = tk.Button(frame_label, text="NEW GAME", font=("Arial Bold", 12), bg='#eec373', fg='#5c3d2e',
                         activebackground='#f5e8c7', command=reset)
    new_game.pack(side='bottom', padx=10, pady=10)

    # tạo bảng nxn
    global size
    for i in range(size):
        rows = []
        for j in range(size):
            l = tk.Label(frame_board, text='', bg='azure4', font=('arial', 22, 'bold'), width=4, height=2)
            l.grid(row=i, column=j, padx=6, pady=6)
            rows.append(l)
        board.append(rows)

    #tạo giá trị 0 cho ma trận value
    for i in range(size):
        value.append([0] * size)

    # tạo bảng nút điều khiển
    up_key = tk.Button(frame_keys, text="Up", font=('arial bold', 15), fg="red", command=up)
    up_key.grid(row=0, column=1)
    left_key = tk.Button(frame_keys, text="Left", font=('arial bold', 15), fg="brown", command=left)
    left_key.grid(row=1, column=0)
    down_key = tk.Button(frame_keys, text="Down", font=('arial bold', 15), fg="blue", command=down)
    down_key.grid(row=1, column=1)
    right_key = tk.Button(frame_keys, text="Right", font=('arial bold', 15), fg="purple", command=right)
    right_key.grid(row=1, column=2)

    # lượt đầu tiên
    random_number()
    update_score()

def click_start_game():
    # đặt kích thước và mục tiêu, nếu không có thì để chế độ mặc định
    global size, target
    if choose_size.get() != 'Choose size':
        size = int(choose_size.get())
    else:
        size = 4

    if choose_target.get() != 'Choose score':
        target = int(choose_target.get())
    else:
        target = 2048

    #ẩn trang mở đầu
    name_of_game.pack_forget()
    size_label.pack_forget()
    choose_size.pack_forget()
    target_label.pack_forget()
    choose_target.pack_forget()
    start_game.pack_forget()
    picture.pack_forget()

    #mở trang trò chơi
    second_page()

start_game = tk.Button(window, text='Start Game', font=("Arial Bold", 14), fg= '#F9F5F0', bg= '#b05b3b', command= click_start_game)
start_game.pack(side='bottom', padx=10, pady= 10, expand=True)

#Chèn hình ảnh cho trò chơi
img = tk.PhotoImage(file="2048.ppm")
picture = tk.Label(window, image= img, width = img.width(), height = img.height())
picture.pack(side='bottom', padx=10, pady= 10)

window.mainloop()
