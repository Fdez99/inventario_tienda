# gestion_inventario_corregido.py

from rich.console import Console
console = Console()

# Inventario inicial
inventario = {
    'galletas': {'cantidad': 10, 'precio': 3.90},
    'arroz': {'cantidad': 14, 'precio': 2.90},
    'queso': {'cantidad': 8, 'precio': 6.90},
    'cerveza': {'cantidad': 22, 'precio': 1.90}
}

# ------------------- Funciones ------------------- #

def otra_mas():
    otra = input('¿Otra operación (s/n)? ').lower()
    if otra == 's':
        gestion_inventario()
    else:
        console.print('¡Hasta pronto! 😊', style="#4c9ef0")
        quit()

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
        return inventario
    finally:
        otra_mas()

# ------------------------------------

# Función principal

def gestion_inventario():
    console.print('Elige opción (1/2/3/4/5/0):  \n1. Consultar\n2. Agregar\n3. Agregar nuevo\n4. Eliminar\n5. Vender\n0. Salir\n', style="#d6c669")
    opcion = input('Elige opción: ')

    match opcion:
        case '1':
            consultar()
        case '2':
            agregar()
        case '3':
            agregar_nuevo()
        case '4':
            eliminar()
        case '5':
            vender()
        case '0':
            console.print('¡Hasta pronto! 👋', style="#4c9ef0")
        case _:
            console.print('Introduce una opción válida - 0 para salir', style="#fd5c63")
            gestion_inventario()



# Vamos a verlo funcionando ▶
gestion_inventario()
