# inventario.py
import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Cargar inventario desde el archivo CSV
def cargar_inventario(archivo='inventario.csv'):
    inventario = {}
    if not os.path.exists(archivo):
        # Crear archivo vacío si no existe
        with open(archivo, 'w', newline='', encoding='utf-8') as f:
            pass
        return inventario
    
    with open(archivo, newline='', encoding='utf-8') as f:
        lector = csv.reader(f)
        for linea in lector:
            if not linea:
                continue
            try:
                producto = linea[0].strip().lower()
                if producto:
                    inventario[producto] = {
                        'cantidad': int(linea[1]),
                        'precio': float(linea[2])
                    }
            except (IndexError, ValueError):
                # Ignorar líneas mal formateadas
                continue
    return inventario

# Guardar inventario en el archivo CSV
def guardar_inventario(inventario, archivo='inventario.csv'):
    with open(archivo, 'w', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f)
        for producto, datos in inventario.items():
            escritor.writerow([producto, datos['cantidad'], f"{datos['precio']:.2f}"])

class InventarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Inventario - Tienda de Doña Conchi")
        self.root.geometry("1020x680")
        self.root.minsize(980, 600)
        self.root.configure(bg="#1e1e2e")

        # Cargar datos
        self.inventario = cargar_inventario()

        # Paleta de Colores (Catppuccin Mocha modificado)
        self.colors = {
            "bg": "#1e1e2e",
            "card_bg": "#252538",
            "text": "#cdd6f4",
            "text_muted": "#a6adc8",
            "accent": "#89b4fa",
            "success": "#a6e3a1",
            "warning": "#f9e2af",
            "danger": "#f38ba8",
            "entry_bg": "#313244",
            "active_btn": "#b4befe"
        }

        # Configurar Estilos ttk
        self.setup_styles()

        # Crear Interfaz
        self.create_widgets()

        # Cargar datos en la tabla inicialmente
        self.actualizar_tabla()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Configuración básica
        self.style.configure('.', background=self.colors["bg"], foreground=self.colors["text"], fieldbackground=self.colors["entry_bg"])
        self.style.configure('TFrame', background=self.colors["bg"])
        self.style.configure('Card.TFrame', background=self.colors["card_bg"], relief='flat', borderwidth=0)
        self.style.configure('TLabel', background=self.colors["bg"], foreground=self.colors["text"], font=("Segoe UI", 10))
        self.style.configure('Card.TLabel', background=self.colors["card_bg"], foreground=self.colors["text"], font=("Segoe UI", 10))
        
        # Estilos de Títulos
        self.style.configure('Title.TLabel', background=self.colors["bg"], foreground=self.colors["accent"], font=("Segoe UI", 16, "bold"))
        self.style.configure('Header.TLabel', background=self.colors["card_bg"], foreground=self.colors["accent"], font=("Segoe UI", 11, "bold"))
        
        # Combobox
        self.style.configure('TCombobox', background=self.colors["entry_bg"], foreground=self.colors["text"], fieldbackground=self.colors["entry_bg"])
        self.root.option_add('*TCombobox*Listbox.background', self.colors["entry_bg"])
        self.root.option_add('*TCombobox*Listbox.foreground', self.colors["text"])
        self.root.option_add('*TCombobox*Listbox.selectBackground', self.colors["accent"])
        self.root.option_add('*TCombobox*Listbox.selectForeground', "#11111b")

        # Treeview (Tabla)
        self.style.configure('Treeview', 
                             background=self.colors["card_bg"], 
                             foreground=self.colors["text"], 
                             fieldbackground=self.colors["card_bg"], 
                             rowheight=28, 
                             font=("Segoe UI", 10))
        self.style.configure('Treeview.Heading', 
                             background=self.colors["entry_bg"], 
                             foreground=self.colors["accent"], 
                             bordercolor=self.colors["bg"],
                             font=("Segoe UI", 10, "bold"))
        self.style.map('Treeview', 
                       background=[('selected', self.colors["accent"])], 
                       foreground=[('selected', '#11111b')])

    def create_widgets(self):
        # 1. BANNER SUPERIOR
        banner_frame = ttk.Frame(self.root, padding=(20, 15, 20, 10))
        banner_frame.pack(fill="x")
        
        lbl_titulo = ttk.Label(banner_frame, text="Gestión de Inventario - Tienda de Doña Conchi 👵", style="Title.TLabel")
        lbl_titulo.pack(side="left")
        
        lbl_tagline = ttk.Label(banner_frame, text="Control de Stock y Ventas en tiempo real", font=("Segoe UI", 9, "italic"), foreground=self.colors["text_muted"])
        lbl_tagline.pack(side="right", pady=5)

        # Contenedor Principal (2 Columnas)
        main_container = ttk.Frame(self.root, padding=10)
        main_container.pack(fill="both", expand=True)

        # --- COLUMNA IZQUIERDA (Acciones y Formularios) ---
        left_col = ttk.Frame(main_container, width=380, padding=5)
        left_col.pack(side="left", fill="both", expand=False)
        left_col.pack_propagate(False) # Mantener ancho fijo

        # CARD 1: AGREGAR NUEVO PRODUCTO
        card_nuevo = ttk.Frame(left_col, style="Card.TFrame", padding=15)
        card_nuevo.pack(fill="x", pady=(0, 10))

        lbl_nuevo_title = ttk.Label(card_nuevo, text="➕ Agregar Nuevo Producto", style="Header.TLabel")
        lbl_nuevo_title.pack(anchor="w", pady=(0, 10))

        # Campos
        frm_nuevo_fields = ttk.Frame(card_nuevo, style="Card.TFrame")
        frm_nuevo_fields.pack(fill="x")
        frm_nuevo_fields.columnconfigure(1, weight=1)

        # Nombre
        ttk.Label(frm_nuevo_fields, text="Nombre:", style="Card.TLabel").grid(row=0, column=0, sticky="w", pady=5, padx=(0, 10))
        self.ent_nuevo_nombre = tk.Entry(frm_nuevo_fields, bg=self.colors["entry_bg"], fg=self.colors["text"], insertbackground=self.colors["text"], relief="flat", font=("Segoe UI", 10), bd=5)
        self.ent_nuevo_nombre.grid(row=0, column=1, sticky="ew", pady=5)

        # Precio
        ttk.Label(frm_nuevo_fields, text="Precio (€):", style="Card.TLabel").grid(row=1, column=0, sticky="w", pady=5, padx=(0, 10))
        self.ent_nuevo_precio = tk.Entry(frm_nuevo_fields, bg=self.colors["entry_bg"], fg=self.colors["text"], insertbackground=self.colors["text"], relief="flat", font=("Segoe UI", 10), bd=5)
        self.ent_nuevo_precio.grid(row=1, column=1, sticky="ew", pady=5)

        # Cantidad
        ttk.Label(frm_nuevo_fields, text="Cantidad:", style="Card.TLabel").grid(row=2, column=0, sticky="w", pady=5, padx=(0, 10))
        self.ent_nuevo_cantidad = tk.Entry(frm_nuevo_fields, bg=self.colors["entry_bg"], fg=self.colors["text"], insertbackground=self.colors["text"], relief="flat", font=("Segoe UI", 10), bd=5)
        self.ent_nuevo_cantidad.grid(row=2, column=1, sticky="ew", pady=5)

        # Botón Añadir Nuevo
        btn_crear = tk.Button(card_nuevo, text="Añadir Producto Nuevo", bg=self.colors["success"], fg="#11111b", activebackground=self.colors["active_btn"], relief="flat", font=("Segoe UI", 10, "bold"), bd=0, cursor="hand2", command=self.agregar_nuevo_producto)
        btn_crear.pack(fill="x", pady=(10, 0), ipady=6)


        # CARD 2: OPERACIONES DE STOCK (REPONER / VENDER)
        card_ops = ttk.Frame(left_col, style="Card.TFrame", padding=15)
        card_ops.pack(fill="x", pady=(0, 10))

        lbl_ops_title = ttk.Label(card_ops, text="🔄 Operaciones de Stock / Ventas", style="Header.TLabel")
        lbl_ops_title.pack(anchor="w", pady=(0, 10))

        frm_ops_fields = ttk.Frame(card_ops, style="Card.TFrame")
        frm_ops_fields.pack(fill="x")
        frm_ops_fields.columnconfigure(1, weight=1)

        # Seleccionar Producto
        ttk.Label(frm_ops_fields, text="Producto:", style="Card.TLabel").grid(row=0, column=0, sticky="w", pady=5, padx=(0, 10))
        self.combo_producto = ttk.Combobox(frm_ops_fields, state="readonly", font=("Segoe UI", 10))
        self.combo_producto.grid(row=0, column=1, sticky="ew", pady=5)
        self.combo_producto.bind("<<ComboboxSelected>>", self.actualizar_precio_estimado)

        # Cantidad Unidades
        ttk.Label(frm_ops_fields, text="Cantidad:", style="Card.TLabel").grid(row=1, column=0, sticky="w", pady=5, padx=(0, 10))
        self.var_cantidad_ops = tk.StringVar()
        self.var_cantidad_ops.trace_add("write", self.actualizar_precio_estimado)
        self.ent_cantidad_ops = tk.Entry(frm_ops_fields, textvariable=self.var_cantidad_ops, bg=self.colors["entry_bg"], fg=self.colors["text"], insertbackground=self.colors["text"], relief="flat", font=("Segoe UI", 10), bd=5)
        self.ent_cantidad_ops.grid(row=1, column=1, sticky="ew", pady=5)

        # Label precio estimado
        self.lbl_precio_estimado = ttk.Label(card_ops, text="Total estimado: 0.00€", font=("Segoe UI", 10, "bold"), foreground=self.colors["warning"], style="Card.TLabel")
        self.lbl_precio_estimado.pack(anchor="w", pady=(5, 5))

        # Botones de Operación (Reponer y Vender)
        frm_buttons = ttk.Frame(card_ops, style="Card.TFrame")
        frm_buttons.pack(fill="x", pady=(5, 0))
        frm_buttons.columnconfigure(0, weight=1)
        frm_buttons.columnconfigure(1, weight=1)

        btn_reponer = tk.Button(frm_buttons, text="Reponer Stock", bg=self.colors["accent"], fg="#11111b", activebackground=self.colors["active_btn"], relief="flat", font=("Segoe UI", 10, "bold"), bd=0, cursor="hand2", command=self.reponer_stock)
        btn_reponer.grid(row=0, column=0, sticky="ew", padx=(0, 5), ipady=6)

        btn_vender = tk.Button(frm_buttons, text="Registrar Venta", bg=self.colors["warning"], fg="#11111b", activebackground=self.colors["active_btn"], relief="flat", font=("Segoe UI", 10, "bold"), bd=0, cursor="hand2", command=self.registrar_venta)
        btn_vender.grid(row=0, column=1, sticky="ew", padx=(5, 0), ipady=6)


        # CARD 3: ACCIONES RÁPIDAS (ELIMINAR SELECCIONADO)
        card_eliminar = ttk.Frame(left_col, style="Card.TFrame", padding=15)
        card_eliminar.pack(fill="x", expand=True)

        lbl_el_title = ttk.Label(card_eliminar, text="⚠️ Zona de Peligro", style="Header.TLabel", foreground=self.colors["danger"])
        lbl_el_title.pack(anchor="w", pady=(0, 10))

        btn_eliminar = tk.Button(card_eliminar, text="Eliminar Producto Seleccionado", bg=self.colors["danger"], fg="#11111b", activebackground=self.colors["active_btn"], relief="flat", font=("Segoe UI", 10, "bold"), bd=0, cursor="hand2", command=self.eliminar_producto)
        btn_eliminar.pack(fill="x", ipady=6)


        # --- COLUMNA DERECHA (Lista de Productos y Estadísticas) ---
        right_col = ttk.Frame(main_container, padding=5)
        right_col.pack(side="right", fill="both", expand=True)

        # Buscador superior
        frm_buscar = ttk.Frame(right_col, padding=(0, 0, 0, 10))
        frm_buscar.pack(fill="x")
        
        ttk.Label(frm_buscar, text="🔍 Buscar producto:", font=("Segoe UI", 10)).pack(side="left", padx=(0, 10))
        self.entry_buscar = tk.Entry(frm_buscar, bg=self.colors["entry_bg"], fg=self.colors["text"], insertbackground=self.colors["text"], relief="flat", font=("Segoe UI", 10), bd=5, width=30)
        self.entry_buscar.pack(side="left", fill="x", expand=True)
        self.entry_buscar.bind("<KeyRelease>", lambda e: self.actualizar_tabla())

        # Tabla de Inventario (Treeview)
        tree_frame = ttk.Frame(right_col)
        tree_frame.pack(fill="both", expand=True)

        columnas = ("producto", "cantidad", "precio", "total")
        self.tree = ttk.Treeview(tree_frame, columns=columnas, show="headings", selectmode="browse")
        
        self.tree.heading("producto", text="Producto")
        self.tree.heading("cantidad", text="Cantidad en Stock")
        self.tree.heading("precio", text="Precio Unitario")
        self.tree.heading("total", text="Valor Total Stock")
        
        self.tree.column("producto", anchor="w", width=200)
        self.tree.column("cantidad", anchor="center", width=120)
        self.tree.column("precio", anchor="center", width=120)
        self.tree.column("total", anchor="center", width=140)

        # Scrollbar para la tabla
        scroll_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        # Vincular selección de tabla con combobox y campos
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Panel de Estadísticas (Inferior derecho)
        card_stats = ttk.Frame(right_col, style="Card.TFrame", padding=15)
        card_stats.pack(fill="x", pady=(10, 0))

        # Grid de estadísticas
        card_stats.columnconfigure(0, weight=1)
        card_stats.columnconfigure(1, weight=1)
        card_stats.columnconfigure(2, weight=1)

        # Stat 1: Total Productos
        stat1_frame = ttk.Frame(card_stats, style="Card.TFrame")
        stat1_frame.grid(row=0, column=0)
        ttk.Label(stat1_frame, text="Productos Diferentes", style="Card.TLabel", font=("Segoe UI", 9), foreground=self.colors["text_muted"]).pack()
        self.lbl_stat_productos = ttk.Label(stat1_frame, text="0", style="Card.TLabel", font=("Segoe UI", 16, "bold"), foreground=self.colors["accent"])
        self.lbl_stat_productos.pack()

        # Stat 2: Total Unidades
        stat2_frame = ttk.Frame(card_stats, style="Card.TFrame")
        stat2_frame.grid(row=0, column=1)
        ttk.Label(stat2_frame, text="Unidades en Almacén", style="Card.TLabel", font=("Segoe UI", 9), foreground=self.colors["text_muted"]).pack()
        self.lbl_stat_unidades = ttk.Label(stat2_frame, text="0", style="Card.TLabel", font=("Segoe UI", 16, "bold"), foreground=self.colors["success"])
        self.lbl_stat_unidades.pack()

        # Stat 3: Valor Total
        stat3_frame = ttk.Frame(card_stats, style="Card.TFrame")
        stat3_frame.grid(row=0, column=2)
        ttk.Label(stat3_frame, text="Valor Total Inventario", style="Card.TLabel", font=("Segoe UI", 9), foreground=self.colors["text_muted"]).pack()
        self.lbl_stat_valor = ttk.Label(stat3_frame, text="0.00€", style="Card.TLabel", font=("Segoe UI", 16, "bold"), foreground=self.colors["warning"])
        self.lbl_stat_valor.pack()


        # 3. BARRA DE ESTADO
        self.status_bar = tk.Label(self.root, text="Aplicación lista. 👵", bd=1, relief="flat", anchor="w", bg="#11111b", fg=self.colors["text_muted"], font=("Segoe UI", 9), padx=10, pady=4)
        self.status_bar.pack(side="bottom", fill="x")

    # --- LÓGICA Y EVENTOS ---

    def set_status(self, text, type="info"):
        fg_color = self.colors["text_muted"]
        if type == "success":
            fg_color = self.colors["success"]
        elif type == "error":
            fg_color = self.colors["danger"]
        elif type == "warning":
            fg_color = self.colors["warning"]
            
        self.status_bar.config(text=text, fg=fg_color)

    def actualizar_precio_estimado(self, *args):
        prod = self.combo_producto.get().strip().lower()
        cant_str = self.var_cantidad_ops.get().strip()
        if prod in self.inventario and cant_str.isdigit():
            cant = int(cant_str)
            precio_unitario = self.inventario[prod]['precio']
            total = precio_unitario * cant
            self.lbl_precio_estimado.config(text=f"Total estimado: {total:.2f}€")
        else:
            self.lbl_precio_estimado.config(text="Total estimado: 0.00€")

    def on_tree_select(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            item = selected_items[0]
            values = self.tree.item(item, 'values')
            if values:
                prod_name = values[0]
                self.combo_producto.set(prod_name)
                self.actualizar_precio_estimado()

    def actualizar_combo_productos(self):
        productos = sorted(list(self.inventario.keys()))
        self.combo_producto['values'] = productos
        # Mantener selección si aún existe
        current = self.combo_producto.get()
        if current not in self.inventario:
            if productos:
                self.combo_producto.set(productos[0])
            else:
                self.combo_producto.set("")
        self.actualizar_precio_estimado()

    def actualizar_stats(self):
        total_productos = len(self.inventario)
        total_unidades = sum(d['cantidad'] for d in self.inventario.values())
        valor_total = sum(d['cantidad'] * d['precio'] for d in self.inventario.values())
        
        self.lbl_stat_productos.config(text=str(total_productos))
        self.lbl_stat_unidades.config(text=str(total_unidades))
        self.lbl_stat_valor.config(text=f"{valor_total:.2f}€")

    def actualizar_tabla(self):
        # Limpiar la tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        filtro = self.entry_buscar.get().strip().lower()
        
        for prod, datos in sorted(self.inventario.items()):
            if filtro and filtro not in prod:
                continue
            cant = datos['cantidad']
            prec = datos['precio']
            total = cant * prec
            self.tree.insert('', 'end', values=(prod, cant, f"{prec:.2f}€", f"{total:.2f}€"))
            
        self.actualizar_stats()
        self.actualizar_combo_productos()

    def agregar_nuevo_producto(self):
        nombre = self.ent_nuevo_nombre.get().strip().lower()
        precio_str = self.ent_nuevo_precio.get().strip()
        cantidad_str = self.ent_nuevo_cantidad.get().strip()

        if not nombre:
            messagebox.showerror("Error", "El nombre del producto no puede estar vacío.")
            return
        
        if nombre in self.inventario:
            messagebox.showerror("Error", f"El producto '{nombre}' ya existe en el inventario.\nUsa el panel de reposición de stock.")
            return

        try:
            precio = float(precio_str)
            if precio < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número decimal positivo.")
            return

        try:
            cantidad = int(cantidad_str)
            if cantidad < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero positivo o cero.")
            return

        # Agregar al inventario
        self.inventario[nombre] = {
            'cantidad': cantidad,
            'precio': precio
        }

        guardar_inventario(self.inventario)
        self.actualizar_tabla()
        
        # Limpiar campos
        self.ent_nuevo_nombre.delete(0, tk.END)
        self.ent_nuevo_precio.delete(0, tk.END)
        self.ent_nuevo_cantidad.delete(0, tk.END)

        self.set_status(f"Producto '{nombre.upper()}' añadido correctamente.", "success")

    def reponer_stock(self):
        prod = self.combo_producto.get().strip()
        cant_str = self.ent_cantidad_ops.get().strip()

        if not prod:
            messagebox.showerror("Error", "Por favor, selecciona un producto de la lista.")
            return

        try:
            cant = int(cant_str)
            if cant <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "La cantidad a añadir debe ser un número entero mayor que cero.")
            return

        if prod not in self.inventario:
            messagebox.showerror("Error", f"El producto '{prod}' ya no está en el inventario.")
            return

        self.inventario[prod]['cantidad'] += cant
        guardar_inventario(self.inventario)
        self.actualizar_tabla()
        
        self.ent_cantidad_ops.delete(0, tk.END)
        self.set_status(f"Stock de '{prod.upper()}' incrementado en {cant} uds.", "success")

    def registrar_venta(self):
        prod = self.combo_producto.get().strip()
        cant_str = self.ent_cantidad_ops.get().strip()

        if not prod:
            messagebox.showerror("Error", "Por favor, selecciona un producto de la lista.")
            return

        try:
            cant = int(cant_str)
            if cant <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "La cantidad a vender debe ser un número entero mayor que cero.")
            return

        if prod not in self.inventario:
            messagebox.showerror("Error", f"El producto '{prod}' ya no está en el inventario.")
            return

        stock_actual = self.inventario[prod]['cantidad']
        if cant > stock_actual:
            messagebox.showerror("Error", f"No hay suficientes unidades de '{prod}'.\nQuedan {stock_actual} unidades.")
            return

        # Registrar la venta
        self.inventario[prod]['cantidad'] -= cant
        total_venta = self.inventario[prod]['precio'] * cant
        
        guardar_inventario(self.inventario)
        self.actualizar_tabla()
        
        self.ent_cantidad_ops.delete(0, tk.END)
        
        # Diálogo de confirmación de venta con el precio a cobrar
        messagebox.showinfo("Venta Registrada", f"Cobrar: {total_venta:.2f}€\n(Se han descontado {cant} unidades de {prod})")
        self.set_status(f"Venta registrada: {cant} uds de '{prod.upper()}' (Total: {total_venta:.2f}€).", "success")

    def eliminar_producto(self):
        prod = self.combo_producto.get().strip()

        if not prod:
            messagebox.showerror("Error", "Por favor, selecciona el producto que deseas eliminar (puedes seleccionarlo en la tabla).")
            return

        if prod not in self.inventario:
            messagebox.showerror("Error", f"El producto '{prod}' no existe en el inventario.")
            return

        confirmar = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que deseas eliminar permanentemente '{prod.upper()}' del inventario?")
        if confirmar:
            del self.inventario[prod]
            guardar_inventario(self.inventario)
            self.actualizar_tabla()
            self.set_status(f"Producto '{prod.upper()}' eliminado permanentemente.", "warning")

if __name__ == "__main__":
    root = tk.Tk()
    app = InventarioApp(root)
    root.mainloop()
