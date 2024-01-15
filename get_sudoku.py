#cadena = "5...........8....23.....1...7..6......6...8......9..5...1.....94....7......3....6"

def get_sudoku_matrix(cadena):
    matriz = []
    # Dividir la cadena en sublistas de 9 caracteres
    subcadenas = [cadena[i:i+9] for i in range(0, len(cadena), 9)]

    for subcadena in subcadenas:
        fila = [int(char) if char != '.' else 0 for char in subcadena]
        matriz.append(fila)
    
    return matriz