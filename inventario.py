# gestion_inventario_corregido.py
import pandas as pd
import csv
from rich.console import Console
console = Console()

# Inventario inicial
with open('inventario.csv', newline='', encoding='utf-8') as f:
    lector = csv.reader(f)
    inventario = {
        linea[0]: {
            'cantidad': int(linea[1]),
            'precio': float(linea[2])
        } for linea in lector
    }

print(inventario)

# ------------------- Funciones ------------------- #

def otra_mas():
    otra = input('¿Otra operación (s/n)? ').lower()
    if otra == 's':
        gestion_inventario()
    else:
        console.print('¡Hasta pronto! 😊', style="#4c9ef0")
        quit()

# ------------------------------------

def actualizar_inventario(archivo):
    with open(archivo, 'w', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f)
            for producto, datos in inventario.items():
                escritor.writerow([producto, datos['cantidad'], f'{datos['precio']:.2f}'])
    return archivo

# ------------------------------------

def mostrar_inventario(inventario): 
    df_inventario = pd.DataFrame.from_dict(inventario, orient='index')
    console.print(df_inventario, style="#ffa65d")
    otra_mas()

# ------------------------------------

def consultar():
    try:
        producto = input('Introduce el producto: ').lower()
        console.print(f"{producto.upper()}: Unidades en almacén: {inventario[producto]['cantidad']} - Precio/ud: {inventario[producto]['precio']:.2f}€", style="#cc3ab9")
    except KeyError:
        console.print(f'{producto} no se encuentra en el inventario.', style="#845491")
    else:
        return producto
    finally:
        otra_mas()

# ------------------------------------

def agregar():
    try:
        producto_existente = input('Producto: ').lower()
        producto_mas_uds = int(input('Unidades añadidas: '))
        inventario[producto_existente]['cantidad'] += producto_mas_uds
    except KeyError:
        console.print(f'{producto_existente} no se encuentra en el inventario.', style="#845491")
    except ValueError:
        console.print('☝ Introduce un número entero de unidades', style="#fdb897")
    else:
        console.print('Producto actualizado', style="#a478f5")
        console.print(f"{producto_existente.upper()}: Unidades en almacén: {inventario[producto_existente]['cantidad']} - Precio/ud: {inventario[producto_existente]['precio']:.2f}€", style="#a478f5")
        actualizar_inventario('inventario.csv')
        return inventario
    finally:
        otra_mas()

# ------------------------------------

def agregar_nuevo():
    class ProductoRepetido(Exception):
        pass

    try:
        nuevo_producto = input('Nuevo producto: ').lower()
        if nuevo_producto in inventario:
            raise ProductoRepetido(f'{nuevo_producto} ya está en el inventario')

        nuevo_precio = float(input('Precio del nuevo producto: '))
        nuevo_unidades = int(input('Número de unidades añadidas: '))

        inventario[nuevo_producto] = {
            'cantidad': nuevo_unidades,
            'precio': nuevo_precio
        }

    except ProductoRepetido as pr:
        console.print(f'❌ {pr}', style='#ffaaaa')
    except ValueError:
        console.print('❌ El precio debe ser un número decimal y las unidades un número entero', style="#fdb897")
    except Exception as e:
        console.print(f'❌ Error inesperado: {e}', style="#ffaaaa")
    else:
        console.print('Nuevo producto añadido', style="#2abe63")
        console.print(f"{nuevo_producto.upper()}: Unidades en almacén: {inventario[nuevo_producto]['cantidad']} - Precio/ud: {inventario[nuevo_producto]['precio']:.2f}€", style="#2abe63")
        actualizar_inventario('inventario.csv')
        return inventario
    finally:
        otra_mas()

# ------------------------------------

def eliminar():
    class NoExiste(Exception):
        pass

    try:
        producto_kaputt = input('Producto para eliminar: ').lower()
        if producto_kaputt not in inventario:
            raise NoExiste(f'{producto_kaputt} no está en el inventario')
    except NoExiste as ne:
        console.print(f'❌ {ne}', style="#b36ca1")
    else:
        del inventario[producto_kaputt]
        console.print(f'Producto eliminado: {producto_kaputt.upper()}', style="#ca3e3e")
        actualizar_inventario('inventario.csv')
        return inventario
    finally:
        otra_mas()

# ------------------------------------

def vender():
    class NoQueda(Exception):
        pass
    class NoExiste(Exception):
        pass

    try:
        producto_vendido = input('Producto vendido: ').lower()
        producto_uds = int(input('Unidades vendidas: '))

        if producto_vendido not in inventario:
            raise NoExiste(f'{producto_vendido} no está en el inventario')

        if producto_uds > inventario[producto_vendido]['cantidad']:
            raise NoQueda(f"No hay bastantes unidades - quedan {inventario[producto_vendido]['cantidad']}")

        inventario[producto_vendido]['cantidad'] -= producto_uds
        total = inventario[producto_vendido]['precio'] * producto_uds
        console.print(f"Cantidad a cobrar: {total:.2f}€", style="#d3c64e")

    except NoQueda as nq:
        console.print(f'❌ {nq}', style="#e45e11")
    except NoExiste as ne:
        console.print(f'❌ {ne}', style="#e45e11")
    except ValueError:
        console.print("❌ Introduce un número válido de unidades", style="#fdb897")
    else:
        actualizar_inventario('inventario.csv')
        return inventario
    finally:
        otra_mas()

# ------------------------------------

# Función principal

def gestion_inventario():
    console.print('Elige opción (1/2/3/4/5/6/0):  \n1. Consultar inventario\n2. Consultar por producto\n3. Agregar\n4. Agregar nuevo\n5. Eliminar\n6. Vender\n0. Salir\n', style="#d6c669")
    opcion = input('Elige opción: ')

    match opcion:
        case '1':
            mostrar_inventario(inventario)
        case '2':
            consultar()
        case '3':
            agregar()
        case '4':
            agregar_nuevo()
        case '5':
            eliminar()
        case '6':
            vender()
        case '0':
            console.print('¡Hasta pronto! 👋', style="#4c9ef0")
        case _:
            console.print('Introduce una opción válida - 0 para salir', style="#fd5c63")
            gestion_inventario()



# Vamos a verlo funcionando ▶
gestion_inventario()
