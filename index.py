import tkinter as tk
from tkcolorpicker import askcolor
import re
import tkinter.simpledialog as simpledialog
from PIL import Image, ImageTk

# Crear la ventana principal
root = tk.Tk()

# Establecer el título de la ventana
root.title("Mi Ventana")

# Establecer el tamaño de la ventana
root.geometry("1024x768")  # Tamaño más grande

# Deshabilitar la opción de redimensionar la ventana
root.resizable(False, False)

# Crear un marco principal
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)


# Crear un marco para la barra de herramientas de color
left_frame = tk.Frame(main_frame)
left_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)  # Mover a la izquierda y agregar margen

# Crear el marco derecho para la barra de herramientas de capas
right_frame = tk.Frame(main_frame)
right_frame.grid(row=0, column=2, sticky="ns")

# Crear un widget Canvas con el cursor de lápiz
canvas = tk.Canvas(main_frame, bg="white", cursor="pencil")
canvas.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)  # Agregar margen

# Configurar la fila y columna para que el canvas se expanda
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)

# Tamaño del "píxel" en el canvas
pixel_size = 10

# Variables de color principal y secundario
primary_color = tk.StringVar(value="#000000")  # Negro por defecto
secondary_color = tk.StringVar(value="#FFFFFF")  # Blanco por defecto

# Variable para el modo borrador
eraser_mode = tk.BooleanVar(value=False)

# Variable para el historial
action_history = []

# Layers
layers = [[]]
current_layer_index = tk.IntVar(value=0)
# Lista para almacenar los nombres de las capas
layer_names = ["Capa 1"]

# Función para calcular un color más claro
def lighten_color(color, factor):
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return f'#{r:02x}{g:02x}{b:02x}'

# Función para seleccionar un color
def set_color(color_var):
    color_code = askcolor(title="Elige un color")[1]
    if color_code:
        color_var.set(color_code)
        update_color_squares()

# Función para abrir la rueda de colores y seleccionar un color
def choose_primary_color():
    set_color(primary_color)

def choose_secondary_color():
    set_color(secondary_color)

# Crear un marco para contener los cuadros de color
color_frame = tk.Frame(left_frame)
color_frame.pack(padx=5, pady=5)

# Crear cuadros para mostrar los colores
primary_color_square = tk.Canvas(color_frame, width=30, height=30, bg=primary_color.get(), highlightthickness=1, highlightbackground="black")
primary_color_square.grid(row=0, column=0)

secondary_color_square = tk.Canvas(color_frame, width=20, height=20, bg=secondary_color.get(), highlightthickness=1, highlightbackground="black")
secondary_color_square.grid(row=1, column=1, pady=(10, 0))  # Ajustar la posición del cuadro secundario

# Función para actualizar los cuadros de color
def update_color_squares():
    primary_color_square.config(bg=primary_color.get())
    secondary_color_square.config(bg=secondary_color.get())
    hex_entry.delete(0, tk.END)
    hex_entry.insert(0, primary_color.get())

# Crear entrada para ingresar código hexadecimal
hex_entry = tk.Entry(left_frame)
hex_entry.pack(padx=5, pady=5)

# Función para actualizar el color basado en el código hexadecimal ingresado
def set_hex_color():
    color_code = hex_entry.get()
    # Validar que el código ingresado sea un color hexadecimal válido
    if re.fullmatch(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color_code):
        primary_color.set(color_code)
    else:
        primary_color.set("#000000")  # Establecer color por defecto si no es válido
        hex_entry.delete(0, tk.END)  # Limpiar la entrada
    update_color_squares()

# Crear botón para establecer el color desde el código hexadecimal
hex_button = tk.Button(left_frame, text="Establecer color", command=set_hex_color)
hex_button.pack(padx=5, pady=5)

# Crear botón para abrir la paleta de colores y seleccionar el color primario
color_button = tk.Button(left_frame, text="Seleccionar Color Primario", command=choose_primary_color)
color_button.pack(padx=5, pady=5)


# Función para dibujar un "píxel" en la posición del clic del ratón
def draw_pixel(event):
    x, y = event.x, event.y
    # Calcular la posición del "píxel" más cercano
    x1 = (x // pixel_size) * pixel_size
    y1 = (y // pixel_size) * pixel_size
    x2 = x1 + pixel_size
    y2 = y1 + pixel_size
    if eraser_mode.get():
        # Eliminar los elementos en la posición del clic
        items = canvas.find_enclosed(x1, y1, x2, y2)
        for item in items:
            action_history.append(("delete", item))
            canvas.itemconfig(item, state="hidden")
    else:
        rect = canvas.create_rectangle(x1, y1, x2, y2, fill=primary_color.get(), outline="")
        action_history.append(("create", rect))

current_bg = canvas.cget("bg")
print(f"El color de fondo actual del lienzo es: {current_bg}")


def undo_action(event=None):
    if action_history:
        action, item = action_history.pop()
        if action == "create":
            canvas.delete(item)
        elif action == "delete":
            canvas.itemconfig(item, state="normal")
            
# Control Z para deshacer la última acción
root.bind("<Control-z>", undo_action)

# Vincular el evento de clic del ratón con la función draw_pixel
canvas.bind("<Button-1>", draw_pixel)
# Vincular el evento de movimiento del ratón con la función draw_pixel
canvas.bind("<B1-Motion>", draw_pixel)


# Función para intercambiar colores
def swap_colors(event=None):
    temp_color = primary_color.get()
    primary_color.set(secondary_color.get())
    secondary_color.set(temp_color)
    update_color_squares()

# Función para manejar el clic en el cuadro de color primario
def primary_color_click(event):
    # No hacer nada, solo se selecciona el color primario para pintar
    pass

# Función para manejar el clic en el cuadro de color secundario
def secondary_color_click(event):
    swap_colors()

# Vincular la tecla 'K' para intercambiar colores
root.bind('k', swap_colors)

# Vincular los cuadros de color para manejar los clics
primary_color_square.bind("<Button-1>", primary_color_click)
secondary_color_square.bind("<Button-1>", secondary_color_click)

# Vincular el evento de doble clic en el cuadro de color primario para abrir la paleta de colores
primary_color_square.bind("<Double-Button-1>", lambda event: choose_primary_color())

# Crear controles deslizantes para tonos y saturación
def update_color_from_sliders():

    color_code = f'#{int(hue):02x}{int(saturation):02x}{int(brightness):02x}'
    primary_color.set(color_code)
    update_color_squares()




# Funciones para cambiar el tema
def set_light_theme():
    root.config(bg="white")
    left_frame.config(bg="white")
    color_frame.config(bg="white")
    # No cambiar el color del lienzo
    # canvas.config(bg="white")

def set_dark_theme():
    dark_gray = "#2e2e2e"  # Gris oscuro
    root.config(bg=dark_gray)
    left_frame.config(bg=dark_gray)
    color_frame.config(bg=dark_gray)
    # No cambiar el color del lienzo
    # canvas.config(bg="white")

def set_medium_dark_theme():
    root.config(bg="gray")
    left_frame.config(bg="gray")
    color_frame.config(bg="gray")
    # No cambiar el color del lienzo
    # canvas.config(bg="white")

# Crear el menú
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Crear el menú de temas
theme_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Tema", menu=theme_menu)
theme_menu.add_command(label="Claro", command=set_light_theme)
theme_menu.add_command(label="Oscuro", command=set_dark_theme)
theme_menu.add_command(label="Medio Oscuro", command=set_medium_dark_theme)



#region Redraw Canvas


def hide_behind_canvas():
    canvas.delete("all")  # Limpiar completamente el lienzo
    draw_grid()
    for i in range(len(layers)):
        current_layer = layers[i]
        count = 0.5
        for action in current_layer:
            if action['type'] == 'draw':
                color = action['color']
                if i < current_layer_index.get():
                    factor = count * 1.5 if i < current_layer_index.get() else 1  # Factor de atenuación para capas anteriores
                    count += 0.4
                    color = lighten_color(color, factor)  # Atenuar el color de las capas anteriores
                canvas.create_rectangle(action['x'], action['y'], action['x'] + pixel_size, action['y'] + pixel_size, fill=color, outline="")

# Función para dibujar la cuadrícula en el lienzo
def draw_grid():
    canvas.delete("grid_line")  # Eliminar las líneas de cuadrícula existentes
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    for i in range(0, width, pixel_size):
        canvas.create_line([(i, 0), (i, height)], tag='grid_line', fill='lightgray')
    for i in range(0, height, pixel_size):
        canvas.create_line([(0, i), (width, i)], tag='grid_line', fill='lightgray')


# Vincular el evento de cambio de tamaño del lienzo para redibujar la cuadrícula
canvas.bind("<Configure>", lambda event: redraw_canvas())


# Función para borrar el contenido del lienzo actual
def clear_canvas():
    current_layer_index_value = current_layer_index.get()
    layers[current_layer_index_value] = []  # Vaciar la capa actual
    redraw_canvas()  # Redibujar la cuadrícula después de borrar

# Crear botón para borrar el contenido del lienzo
clear_button = tk.Button(left_frame, text="Borrar Todo", command=clear_canvas)
clear_button.pack(padx=5, pady=5)

# Función para activar el modo borrador
def activate_eraser():
    eraser_mode.set(True)
    canvas.config(cursor="dot")  # Cambiar el cursor a un punto para indicar el modo borrador

# Crear botón para activar el modo borrador
eraser_button = tk.Button(left_frame, text="Borrador", command=activate_eraser)
eraser_button.pack(padx=5, pady=5)

# Función para activar el modo de dibujo
def activate_draw():
    eraser_mode.set(False)
    canvas.config(cursor="pencil")  # Cambiar el cursor a un lápiz para indicar el modo dibujo

# Crear botón para activar el modo de dibujo
draw_button = tk.Button(left_frame, text="Dibujar", command=activate_draw)
draw_button.pack(padx=5, pady=5)


# region Capas Frame


# Función para seleccionar un color
def set_color(color_var):
    color = askcolor()[1]
    if color:
        color_var.set(color)
        update_color_squares()

# Función para agregar una capa
def add_layer():
    layers.append([])
    layer_names.append(f"Capa {len(layer_names) + 1}")
    update_layer_list()

# Función para eliminar la capa actual
def remove_layer():
    index = current_layer_index.get()
    if len(layers) > 1:
        del layers[index]
        del layer_names[index]
        current_layer_index.set(max(0, index - 1))
        update_layer_list()
        redraw_canvas()

# Función para mover la capa actual hacia arriba
def move_layer_up():
    index = current_layer_index.get()
    if index > 0:
        layers[index], layers[index - 1] = layers[index - 1], layers[index]
        layer_names[index], layer_names[index - 1] = layer_names[index - 1], layer_names[index]
        current_layer_index.set(index - 1)
        update_layer_list()
        redraw_canvas()

# Función para mover la capa actual hacia abajo
def move_layer_down():
    index = current_layer_index.get()
    if index < len(layers) - 1:
        layers[index], layers[index + 1] = layers[index + 1], layers[index]
        layer_names[index], layer_names[index + 1] = layer_names[index + 1], layer_names[index]
        current_layer_index.set(index + 1)
        update_layer_list()
        redraw_canvas()

# Función para actualizar el Listbox de capas
def update_layer_listbox():
    layer_listbox.delete(0, tk.END)
    for i, layer in enumerate(layers):
        layer_listbox.insert(tk.END, f"Capa {i + 1}")

# Función para seleccionar una capa
def select_layer(index):
    if 0 <= index < len(layers):
        current_layer_index.set(index)
        redraw_canvas()

#region Redraw Canvas
# Función para redibujar el canvas con la capa actual
def redraw_canvas():
    canvas.delete("all")  # Limpiar completamente el lienzo
    draw_grid()
    for i in range(current_layer_index.get() + 1):
        current_layer = layers[i]
        for action in current_layer:
            if action['type'] == 'draw':
                color = action['color']
                if i < current_layer_index.get():
                    # Aplicar factores de atenuación específicos para capas anteriores
                    if i == current_layer_index.get() - 1:
                        factor = 0.5
                    elif i == current_layer_index.get() - 2:
                        factor = 0.7
                    elif i == current_layer_index.get() - 3:
                        factor = 0.9
                    elif i <= current_layer_index.get() - 4:
                        factor = 1
                    if factor < 1:
                        color = lighten_color(color, factor)  # Atenuar el color de las capas anteriores
                        canvas.create_rectangle(action['x'], action['y'], action['x'] + pixel_size, action['y'] + pixel_size, fill=color, outline="")
                else:
                    canvas.create_rectangle(action['x'], action['y'], action['x'] + pixel_size, action['y'] + pixel_size, fill=color, outline="")
    # Dibujar la capa actual si current_layer_index.get() <= 0
    if current_layer_index.get() == 0:
        current_layer = layers[current_layer_index.get()]
        for action in current_layer:
            if action['type'] == 'draw':
                color = action['color']
                canvas.create_rectangle(action['x'], action['y'], action['x'] + pixel_size, action['y'] + pixel_size, fill=color, outline="")
# Función para dibujar en el canvas
def draw(event):
    x, y = event.x - (event.x % pixel_size), event.y - (event.y % pixel_size)
    if eraser_mode.get():
        # Eliminar la acción de dibujo en la posición actual
        current_layer = layers[current_layer_index.get()]
        layers[current_layer_index.get()] = [action for action in current_layer if not (action['x'] == x and action['y'] == y)]
    else:
        color = primary_color.get()
        action = {'type': 'draw', 'x': x, 'y': y, 'color': color}
        layers[current_layer_index.get()].append(action)
    redraw_canvas()

# Vincular la función de dibujo al evento de movimiento del ratón
canvas.bind("<B1-Motion>", draw)
canvas.bind("<Button-1>", draw)


# Crear Listbox para mostrar las capas
layer_listbox = tk.Listbox(right_frame)
layer_listbox.pack(pady=10, fill=tk.BOTH, expand=True)



# Función para actualizar la lista de capas
def update_layer_list():
    layer_listbox.delete(0, tk.END)
    for name in layer_names:
        layer_listbox.insert(tk.END, name)
    layer_listbox.selection_set(current_layer_index.get())

# Función para renombrar una capa
def rename_layer(event):
    selected_index = layer_listbox.curselection()
    if selected_index:
        index = selected_index[0]
        new_name = simpledialog.askstring("Renombrar Capa", "Nuevo nombre de la capa:", initialvalue=layer_names[index])
        if new_name:
            layer_names[index] = new_name
            update_layer_list()

# Vincular el evento de doble clic en la lista de capas a la función rename_layer
layer_listbox.bind("<Double-1>", rename_layer)

# Vincular la selección de la lista de capas a la variable current_layer_index
def on_layer_select(event):
    selected_index = layer_listbox.curselection()
    if selected_index:
        current_layer_index.set(selected_index[0])
        redraw_canvas()
def update_layer_list():
    layer_listbox.delete(0, tk.END)
    for name in layer_names:
        layer_listbox.insert(tk.END, name)
    layer_listbox.selection_set(current_layer_index.get())

# Vincular la selección de la lista de capas a la variable current_layer_index
def on_layer_select(event):
    selected_index = layer_listbox.curselection()
    if selected_index:
        current_layer_index.set(selected_index[0])
        redraw_canvas()

layer_listbox.bind("<<ListboxSelect>>", on_layer_select)

# layer_listbox.bind("<<ListboxSelect>>", lambda event: select_layer(layer_listbox.curselection()[0]))



# Añadir botones de ejemplo para gestionar las capas
add_layer_button = tk.Button(right_frame, text="Añadir Capa", command=add_layer)
add_layer_button.pack(pady=10)

remove_layer_button = tk.Button(right_frame, text="Eliminar Capa", command=remove_layer)
remove_layer_button.pack(pady=10)

move_layer_up_button = tk.Button(right_frame, text="Mover Capa Arriba", command=move_layer_up)
move_layer_up_button.pack(pady=10)

move_layer_down_button = tk.Button(right_frame, text="Mover Capa Abajo", command=move_layer_down)
move_layer_down_button.pack(pady=10)


#endregion

#region Animation Frame
# Variables para la animación
is_animating = False
fps = tk.IntVar(value=10)  # Cuadros por segundo

# Función para actualizar el canvas de animación
def update_animation_frame(frame_index):
    # Establecer la opacidad de todas las capas a 0
    # Establecer la opacidad de la capa actual a 1
    hide_behind_canvas()
    current_layer_index.set(frame_index)
    redraw_canvas()

# Función para iniciar la animación
def start_animation():
    hide_behind_canvas()
    global is_animating, current_frame_index
    is_animating = True
    current_frame_index = 0  # Reiniciar el índice del frame
    animate()

# Función para detener la animación
def stop_animation():
    global is_animating
    is_animating = False

# Función para animar las capas
def animate():
    global is_animating, current_frame_index  # Asegurarse de que las variables son globales
    if is_animating:
        frame_count = len(layers)
        update_animation_frame(current_frame_index)
        current_frame_index = (current_frame_index + 1) % frame_count  # Avanzar al siguiente frame
        try:
            delay = int(1000 / int(fps.get()))
        except ValueError:
            delay = 100  # Valor por defecto en caso de error
        root.after(delay, animate)  # Programar la siguiente llamada a animate

# Crear controles para la animación
control_frame = tk.Frame(root)
control_frame.pack(side=tk.BOTTOM, fill=tk.X)

start_button = tk.Button(control_frame, text="Iniciar Animación", command=start_animation)
start_button.pack(side=tk.LEFT, padx=5, pady=5)

stop_button = tk.Button(control_frame, text="Detener Animación", command=stop_animation)
stop_button.pack(side=tk.LEFT, padx=5, pady=5)

fps_label = tk.Label(control_frame, text="FPS:")
fps_label.pack(side=tk.LEFT, padx=5, pady=5)

fps_entry = tk.Entry(control_frame, textvariable=fps, width=5)
fps_entry.pack(side=tk.LEFT, padx=5, pady=5)

# Iniciar el bucle principal de la ventana
redraw_canvas()
update_layer_list()
update_color_squares()
root.mainloop()