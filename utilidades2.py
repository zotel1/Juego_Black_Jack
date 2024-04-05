from os import system


"""
Este modulo contiene funciones de utilidad para el manejo de datos


"""

def isint(str_numero:str)->bool:
    """
    Devuelve True si str_numero es un int, False en caso contrario

    Args:
        str_numero (str): Cadena a evaluar

    Returns:
        bool: True si str_numero es un int, False en caso contrario
    """
    try:                    # Intenta convertir str_numero a int
        int(str_numero)
    except:                 # Si no puede convertirlo devuelve False
        return False
    return True             # Si puede convertirlo devuelve True

def isfloat(str_numero:str)->bool:
    """
    Devuelve True si str_numero es un float, False en caso contrario

    Args:
        str_numero (str): Cadena a evaluar

    Returns:
        bool: True si str_numero es un float, False en caso contrario
    """
    try:
        float(str_numero)
    except:
        return False
    return True

def leer_datos(cartel,**arg):
    print(f"Argumentos: {arg}")
    valores = input(cartel).split(',')
    if len(valores) != len(arg):
        print("Número incorrecto de valores ingresados.")
        return None

    lista = []
    for i, (valor, tipo) in enumerate(zip(valores, arg.values())):
        print(f"i: {i} ==> ({valor},{tipo}) ")
        try:
            valor_convertido = tipo(valor)
            lista.append(valor_convertido)
        except ValueError:
            print(f"No se pudo convertir el valor '{valor}' al tipo '{tipo.__name__}' en la posición {i+1}.")
            return None
    return lista



def leer_numero(mensaje:str='Ingrese un número',
                minimo=-float('inf'),maximo=float('inf'),tipo:type[int|float] = int):    
    if tipo is int:
        return leer_entero(mensaje=mensaje,minimo=minimo,maximo=maximo)
    elif tipo is float:
        return leer_float(mensaje=mensaje,minimo=minimo,maximo=maximo)  
    else:
        raise ValueError("Error en el parametro tipo ==> tipo = type[int|float]")
  
            
def leer_entero(mensaje:str='Ingrese un entero: ',minimo:int=-float('inf'),maximo:int=float('inf'))->int:
    """
    Permite leer un entero desde el teclado en un rango determinado
    Args:
        mensaje (str): Mensaje a mostrar al usuario
        minimo (int): Valor minimo del rango    
        maximo (int): Valor maximo del rango   
    Returns:
        int: Entero ingresado por el usuario
    """
    todo_ok = False
    while not todo_ok:
        cadena = input(mensaje)
        if isint(cadena):
            numero = int(cadena)
            if minimo <= numero <= maximo:
                todo_ok = True
            else:
                print(f"Número {numero} fuera de rango [{minimo}] .. [{maximo}]")
        else:
            print(f"{cadena} No es un int.")    
    return int(cadena)

def leer_float(mensaje:str='Ingrese un float: ',minimo:float=-float('inf'),maximo:float=float('inf'))->float:
    """
    Permite leer un float desde el teclado en un rango determinado

    Args:
        mensaje (str): Mensaje a mostrar al usuario
        minimo (float): Valor minimo del rango
        maximo (float): Valor maximo del rango

    Returns:
        float: Float ingresado por el usuario
    """
    todo_ok = False
    while not todo_ok:
        cadena = input(mensaje)
        if isfloat(cadena):
            numero = float(cadena)
            if minimo <= numero <= maximo:
                todo_ok = True
            else:
                print(f"Número {numero} fuera de rango {minimo} .. {maximo}")
        else:
            print(f"{cadena} No es un float.")    
    return float(cadena)

# En esta línea estaba la función leer_entero_rango, ahora valida el rango leer_entero

# En esta línea estaba la función leer_float_rango,ahora valida el rango leer_float

def titulo(texto:str,largo:int=80):
    """
    Devuelve un titulo centrado con guiones

    Args:
        texto (str): Texto a mostrar en el titulo
        largo (int): Largo del titulo

    Returns:
        str: Titulo centrado con guiones
    """    
    return f"{'-'*largo}\n{texto.title().center(largo)}\n{'-'*largo}"

def obtener_largo_opcion_mas_larga(tupla_opciones):
    """
    Devuelve el largo de la opcion mas larga

    Args:
        tupla_opciones (tuple): Tupla con las opciones

    Returns:
        int: Largo de la opcion mas larga
    """    
    maximo_largo = -float('inf')
    for i,texto in enumerate(tupla_opciones):
        if len(texto) > maximo_largo:
            maximo_largo = len(texto)
    return maximo_largo

def menu(tupla_opciones:str)->int:
    """
    Muestra un menu con las opciones de la tupla
    
    La primera opcion es el titulo
    
    Las demas son las opciones
    
    Args:
        tupla_opciones (tuple): Tupla con las opciones

    Returns:    
        int: Opcion elegida por el usuario
    """
    largo = obtener_largo_opcion_mas_larga(tupla_opciones)
    system("cls")
    for index,opcion in enumerate(tupla_opciones):
        if index == 0: 
            print(titulo(opcion,largo))
        else:
            print(opcion.title())
    return leer_entero("Ingrese una opcion: ",1,8)
    
def continua(texto_pregunta):
    """
    Devuelve True si el usuario responde S, False en caso contrario

    Args:
        texto_pregunta (str): Texto a mostrar al usuario

    Returns:
        bool: True si el usuario responde S, False en caso contrario
    """
    resp = input(f'{texto_pregunta} [S/N]: ').upper()
    if resp == 'S':
        return True
    return False

def leer_datos(cartel:str,**arg)->tuple:
    tupla = ()
    print(cartel)
    for nombre_dato,tipo in arg.items():
        try:
            valor = input(f'{nombre_dato.title()}: ')
            valor_convertido = tipo(valor)
            tupla += (valor_convertido,)
        except ValueError as e:
            raise ValueError(f"No se pudo convertir el valor {valor} al tipo {tipo.__name__}.\n {e}")
            
    return tupla


if __name__ == '__main__':
    print("Esto es un modulo no un programa")
    print((1,2,3) + (3,2,1))
    print((1,2,3) * 8)
    print((4,))
    # x = leer_numero("Sueldo: ",0,10000,float)
    #a,b,c,d,e = leer_datos('Datos de un alumno',legajo=int,nombre=str,sueldo=float,edad=int,mascota=str)
    #print(a,b,c,d,e)

