# API/app/exercises_data.py
# Competitive-programming style exercises — drop the `exercises` collection before re-seeding.

EXERCISES_SEED = [

    # ══════════════════════════════════════════
    #  MATEMÁTICAS — FÁCIL
    # ══════════════════════════════════════════
    {
        "title": "Máximo Común Divisor",
        "difficulty": "Fácil", "category": "Matemáticas", "total_solvers": 0,
        "description": (
            "Dados dos enteros positivos a y b, calcula su Máximo Común Divisor (MCD), "
            "es decir, el mayor entero d tal que d divide a a y d divide a b sin dejar resto.\n\n"
            "El algoritmo de Euclides establece que MCD(a, b) = MCD(b, a mod b), "
            "y que MCD(a, 0) = a. Esta recurrencia converge en O(log min(a,b)) pasos, "
            "lo que lo hace extremadamente eficiente incluso para a, b ~ 10^18.\n\n"
            "Restricciones:\n"
            "  1 ≤ a, b ≤ 10^9\n\n"
            "Ejemplo 1:\n"
            "  Entrada: a=48, b=18\n"
            "  Salida: 6\n"
            "  Explicación: 48 = 6×8, 18 = 6×3. Los divisores comunes son 1, 2, 3, 6. El mayor es 6.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: a=100, b=75\n"
            "  Salida: 25\n\n"
            "Escribe `solve(a, b)` que devuelva MCD(a, b)."
        ),
        "test_cases": [
            {"input": "48, 18",   "expected_output": "6"},
            {"input": "100, 75",  "expected_output": "25"},
            {"input": "7, 13",    "expected_output": "1"},
        ],
        "stub": {
            "Python": "def solve(a, b):\n    # Algoritmo de Euclides\n    pass",
            "C++":    "int solve(int a, int b) {\n    // Algoritmo de Euclides\n    return 0;\n}",
            "Java":   "public static int solve(int a, int b) {\n    // Algoritmo de Euclides\n    return 0;\n}",
            "Go":     "func solve(a int, b int) int {\n    // Algoritmo de Euclides\n    return 0\n}",
            "C#":     "public static int Solve(int a, int b) {\n    // Algoritmo de Euclides\n    return 0;\n}",
        },
    },
    {
        "title": "Test de Primalidad",
        "difficulty": "Fácil", "category": "Matemáticas", "total_solvers": 0,
        "description": (
            "Dado un entero n ≥ 2, determina si es un número primo.\n\n"
            "Un número primo es aquel divisible únicamente por 1 y por sí mismo. "
            "Para verificarlo eficientemente no hace falta probar todos los divisores hasta n: "
            "basta con probar los enteros d desde 2 hasta ⌊√n⌋. Si ninguno divide a n, entonces n es primo.\n\n"
            "Esta optimización reduce la complejidad de O(n) a O(√n), permitiendo comprobar "
            "números de hasta 10^12 en microsegundos.\n\n"
            "Restricciones:\n"
            "  2 ≤ n ≤ 10^9\n\n"
            "Ejemplo 1:\n"
            "  Entrada: n=7\n"
            "  Salida: True\n"
            "  Explicación: √7 ≈ 2.6. Comprobamos d=2: 7 mod 2 = 1 ≠ 0. No hay divisores → primo.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: n=12\n"
            "  Salida: False\n"
            "  Explicación: 12 = 2×6, divisible por 2.\n\n"
            "Escribe `solve(n)` que devuelva True si n es primo, False en caso contrario."
        ),
        "test_cases": [
            {"input": "7",   "expected_output": "True"},
            {"input": "12",  "expected_output": "False"},
            {"input": "97",  "expected_output": "True"},
        ],
        "stub": {
            "Python": "def solve(n):\n    # Prueba divisores hasta sqrt(n)\n    pass",
            "C++":    "bool solve(int n) {\n    // Prueba divisores hasta sqrt(n)\n    return false;\n}",
            "Java":   "public static boolean solve(int n) {\n    // Prueba divisores hasta sqrt(n)\n    return false;\n}",
            "Go":     "func solve(n int) bool {\n    // Prueba divisores hasta sqrt(n)\n    return false\n}",
            "C#":     "public static bool Solve(int n) {\n    // Prueba divisores hasta sqrt(n)\n    return false;\n}",
        },
    },
    {
        "title": "Fibonacci Iterativo",
        "difficulty": "Fácil", "category": "Matemáticas", "total_solvers": 0,
        "description": (
            "La sucesión de Fibonacci se define como:\n"
            "  F(0) = 0\n"
            "  F(1) = 1\n"
            "  F(n) = F(n-1) + F(n-2)  para n ≥ 2\n\n"
            "Sus primeros términos son: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, ...\n\n"
            "La aproximación recursiva ingenua tiene complejidad exponencial O(2^n). "
            "Tu tarea es implementar la versión iterativa que calcula F(n) en O(n) tiempo "
            "y O(1) espacio, manteniendo únicamente los dos valores previos.\n\n"
            "Restricciones:\n"
            "  0 ≤ n ≤ 45  (F(45) = 1134903170, cabe en un entero de 32 bits)\n\n"
            "Ejemplo 1:\n"
            "  Entrada: n=10\n"
            "  Salida: 55\n"
            "  Explicación: F(10) = 55.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: n=0\n"
            "  Salida: 0\n\n"
            "Escribe `solve(n)` que devuelva el n-ésimo número de Fibonacci."
        ),
        "test_cases": [
            {"input": "10", "expected_output": "55"},
            {"input": "0",  "expected_output": "0"},
            {"input": "20", "expected_output": "6765"},
        ],
        "stub": {
            "Python": "def solve(n):\n    # Implementación iterativa O(n)\n    pass",
            "C++":    "int solve(int n) {\n    // Implementación iterativa O(n)\n    return 0;\n}",
            "Java":   "public static int solve(int n) {\n    // Implementación iterativa O(n)\n    return 0;\n}",
            "Go":     "func solve(n int) int {\n    // Implementación iterativa O(n)\n    return 0\n}",
            "C#":     "public static int Solve(int n) {\n    // Implementación iterativa O(n)\n    return 0;\n}",
        },
    },

    # ══════════════════════════════════════════
    #  ARRAYS — FÁCIL
    # ══════════════════════════════════════════
    {
        "title": "Búsqueda Binaria Clásica",
        "difficulty": "Fácil", "category": "Arrays", "total_solvers": 0,
        "description": (
            "Dado un array de enteros ordenado de forma estrictamente ascendente y un valor objetivo "
            "target, devuelve el índice (base 0) de target en el array. Si target no se encuentra, "
            "devuelve -1.\n\n"
            "La búsqueda lineal tiene complejidad O(n). La búsqueda binaria explota el hecho de que "
            "el array está ordenado para descartar la mitad del espacio de búsqueda en cada paso, "
            "logrando O(log n) comparaciones.\n\n"
            "Algoritmo:\n"
            "  Mantén dos punteros lo=0 y hi=n-1.\n"
            "  En cada iteración calcula mid = (lo+hi)//2.\n"
            "  Si nums[mid] == target → devuelve mid.\n"
            "  Si nums[mid] < target  → lo = mid + 1.\n"
            "  Si nums[mid] > target  → hi = mid - 1.\n"
            "  Si lo > hi             → devuelve -1.\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 10^4\n"
            "  El array no contiene duplicados\n\n"
            "Ejemplo 1:\n"
            "  Entrada: nums=[1,3,5,7,9,11], target=7\n"
            "  Salida: 3\n"
            "  Explicación: nums[3] = 7.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: nums=[2,4,6,8,10], target=5\n"
            "  Salida: -1\n\n"
            "Escribe `solve(nums, target)` que devuelva el índice o -1."
        ),
        "test_cases": [
            {"input": "[1,3,5,7,9,11], 7",   "expected_output": "3"},
            {"input": "[2,4,6,8,10], 5",      "expected_output": "-1"},
            {"input": "[1,2,3,4,5,6,7,8,9,10], 10", "expected_output": "9"},
        ],
        "stub": {
            "Python": "def solve(nums, target):\n    lo, hi = 0, len(nums) - 1\n    # Completa la búsqueda binaria\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nint solve(vector<int> nums, int target) {\n    int lo = 0, hi = (int)nums.size() - 1;\n    // Completa la búsqueda binaria\n    return -1;\n}",
            "Java":   "public static int solve(int[] nums, int target) {\n    int lo = 0, hi = nums.length - 1;\n    // Completa la búsqueda binaria\n    return -1;\n}",
            "Go":     "func solve(nums []int, target int) int {\n    lo, hi := 0, len(nums)-1\n    // Completa la búsqueda binaria\n    return -1\n}",
            "C#":     "public static int Solve(int[] nums, int target) {\n    int lo = 0, hi = nums.Length - 1;\n    // Completa la búsqueda binaria\n    return -1;\n}",
        },
    },
    {
        "title": "Array de Sumas de Prefijo",
        "difficulty": "Fácil", "category": "Arrays", "total_solvers": 0,
        "description": (
            "Dado un array de enteros nums de longitud n, construye y devuelve el array de sumas de "
            "prefijo prefix de la misma longitud, donde:\n"
            "  prefix[0] = nums[0]\n"
            "  prefix[i] = nums[0] + nums[1] + ... + nums[i]  para i > 0\n\n"
            "El array de sumas de prefijo es una técnica fundamental en programación competitiva: "
            "una vez construido en O(n), permite responder consultas del tipo "
            "\"¿cuál es la suma del subarray nums[l..r]?\" en O(1) mediante la fórmula "
            "prefix[r] - prefix[l-1].\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 10^5\n"
            "  -10^4 ≤ nums[i] ≤ 10^4\n\n"
            "Ejemplo 1:\n"
            "  Entrada: nums=[1,2,3,4,5]\n"
            "  Salida: [1,3,6,10,15]\n"
            "  Explicación: 1, 1+2=3, 1+2+3=6, 1+2+3+4=10, 1+2+3+4+5=15.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: nums=[3,1,4,1,5]\n"
            "  Salida: [3,4,8,9,14]\n\n"
            "Escribe `solve(nums)` que devuelva el array de sumas de prefijo."
        ),
        "test_cases": [
            {"input": "[1,2,3,4,5]",  "expected_output": "[1,3,6,10,15]"},
            {"input": "[3,1,4,1,5]",  "expected_output": "[3,4,8,9,14]"},
            {"input": "[10,20,30]",    "expected_output": "[10,30,60]"},
        ],
        "stub": {
            "Python": "def solve(nums):\n    # Construye el array prefix en O(n)\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nvector<int> solve(vector<int> nums) {\n    // Construye el array prefix en O(n)\n    return {};\n}",
            "Java":   "public static int[] solve(int[] nums) {\n    // Construye el array prefix en O(n)\n    return new int[]{};\n}",
            "Go":     "func solve(nums []int) []int {\n    // Construye el array prefix en O(n)\n    return nil\n}",
            "C#":     "public static int[] Solve(int[] nums) {\n    // Construye el array prefix en O(n)\n    return new int[]{};\n}",
        },
    },

    # ══════════════════════════════════════════
    #  STRINGS — FÁCIL
    # ══════════════════════════════════════════
    {
        "title": "Verificar Palíndromo",
        "difficulty": "Fácil", "category": "Strings", "total_solvers": 0,
        "description": (
            "Una cadena es un palíndromo si se lee igual de izquierda a derecha que de derecha a "
            "izquierda. Para esta tarea ignoraremos mayúsculas/minúsculas y solo consideraremos "
            "caracteres alfanuméricos (letras y dígitos), descartando espacios y puntuación.\n\n"
            "Pasos recomendados:\n"
            "  1. Filtra la cadena dejando solo caracteres alfanuméricos y conviértelos a minúsculas.\n"
            "  2. Compara la cadena filtrada con su reverso.\n\n"
            "Restricciones:\n"
            "  1 ≤ |s| ≤ 2×10^5\n\n"
            "Ejemplo 1:\n"
            "  Entrada: s=\"A man, a plan, a canal: Panama\"\n"
            "  Salida: True\n"
            "  Explicación: Filtrado → \"amanaplanacanalpanama\", que es palíndromo.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: s=\"race a car\"\n"
            "  Salida: False\n"
            "  Explicación: Filtrado → \"raceacar\", que no es palíndromo.\n\n"
            "Ejemplo 3:\n"
            "  Entrada: s=\"12321\"\n"
            "  Salida: True\n\n"
            "Escribe `solve(s)` que devuelva True o False."
        ),
        "test_cases": [
            {"input": '"A man, a plan, a canal: Panama"', "expected_output": "True"},
            {"input": '"race a car"',                     "expected_output": "False"},
            {"input": '"12321"',                          "expected_output": "True"},
        ],
        "stub": {
            "Python": "def solve(s):\n    # Filtra alfanuméricos, convierte a minúsculas y compara\n    pass",
            "C++":    "#include <string>\n#include <algorithm>\n#include <cctype>\nusing namespace std;\nbool solve(string s) {\n    // Filtra alfanuméricos y compara con reverso\n    return false;\n}",
            "Java":   "public static boolean solve(String s) {\n    // Filtra alfanuméricos y compara con reverso\n    return false;\n}",
            "Go":     "func solve(s string) bool {\n    // Filtra alfanuméricos y compara con reverso\n    return false\n}",
            "C#":     "public static bool Solve(string s) {\n    // Filtra alfanuméricos y compara con reverso\n    return false;\n}",
        },
    },
    {
        "title": "Anagrama Válido",
        "difficulty": "Fácil", "category": "Strings", "total_solvers": 0,
        "description": (
            "Dos cadenas s y t son anagramas si una puede obtenerse reordenando los caracteres "
            "de la otra. En otras palabras, ambas deben contener exactamente los mismos caracteres "
            "con exactamente las mismas frecuencias.\n\n"
            "Estrategia eficiente:\n"
            "  Construye una tabla de frecuencias (array de 26 posiciones para letras minúsculas, "
            "o un mapa hash para caracteres arbitrarios). Incrementa la cuenta al recorrer s y "
            "decreméntala al recorrer t. Si todas las cuentas son cero al final, las cadenas son "
            "anagramas.\n\n"
            "Complejidad esperada: O(n) tiempo, O(1) espacio extra (alfabeto fijo).\n\n"
            "Restricciones:\n"
            "  1 ≤ |s|, |t| ≤ 5×10^4\n"
            "  s y t solo contienen letras minúsculas en inglés\n\n"
            "Ejemplo 1:\n"
            "  Entrada: s=\"anagram\", t=\"nagaram\"\n"
            "  Salida: True\n\n"
            "Ejemplo 2:\n"
            "  Entrada: s=\"rat\", t=\"car\"\n"
            "  Salida: False\n\n"
            "Ejemplo 3:\n"
            "  Entrada: s=\"listen\", t=\"silent\"\n"
            "  Salida: True\n\n"
            "Escribe `solve(s, t)` que devuelva True o False."
        ),
        "test_cases": [
            {"input": '"anagram", "nagaram"', "expected_output": "True"},
            {"input": '"rat", "car"',          "expected_output": "False"},
            {"input": '"listen", "silent"',    "expected_output": "True"},
        ],
        "stub": {
            "Python": "def solve(s, t):\n    # Compara tablas de frecuencias\n    pass",
            "C++":    "#include <string>\n#include <unordered_map>\nusing namespace std;\nbool solve(string s, string t) {\n    // Compara tablas de frecuencias\n    return false;\n}",
            "Java":   "public static boolean solve(String s, String t) {\n    // Compara tablas de frecuencias\n    return false;\n}",
            "Go":     "func solve(s string, t string) bool {\n    // Compara tablas de frecuencias\n    return false\n}",
            "C#":     "public static bool Solve(string s, string t) {\n    // Compara tablas de frecuencias\n    return false;\n}",
        },
    },
    {
        "title": "Contar Bits (Popcount)",
        "difficulty": "Fácil", "category": "Matemáticas", "total_solvers": 0,
        "description": (
            "Dado un entero no negativo n, devuelve el número de bits en '1' que tiene "
            "su representación en binario. Esta operación se llama 'population count' o popcount.\n\n"
            "Ejemplos de representaciones binarias:\n"
            "  n=11 → 1011₂ → tres unos\n"
            "  n=7  → 0111₂ → tres unos\n"
            "  n=128 → 10000000₂ → un uno\n\n"
            "Truco de Kernighan:\n"
            "  La operación n = n & (n-1) elimina el bit menos significativo que sea 1 "
            "en cada iteración. Repitiendo hasta que n=0 contamos exactamente los bits activos. "
            "Este algoritmo se ejecuta en O(k) donde k es el número de bits a 1, no en O(log n).\n\n"
            "Restricciones:\n"
            "  0 ≤ n ≤ 2^31 - 1\n\n"
            "Ejemplo 1:\n"
            "  Entrada: n=11\n"
            "  Salida: 3\n"
            "  Explicación: 11 = 1011₂ → tres bits a 1.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: n=128\n"
            "  Salida: 1\n\n"
            "Escribe `solve(n)` que devuelva el número de bits a 1 en la representación binaria de n."
        ),
        "test_cases": [
            {"input": "11",         "expected_output": "3"},
            {"input": "128",        "expected_output": "1"},
            {"input": "2147483647", "expected_output": "31"},
        ],
        "stub": {
            "Python": "def solve(n):\n    # Truco de Kernighan: n &= n-1 elimina el LSB activo\n    pass",
            "C++":    "int solve(int n) {\n    // Truco de Kernighan: n &= n-1\n    return 0;\n}",
            "Java":   "public static int solve(int n) {\n    // Truco de Kernighan: n &= n-1\n    return 0;\n}",
            "Go":     "func solve(n int) int {\n    // Truco de Kernighan: n &= n-1\n    return 0\n}",
            "C#":     "public static int Solve(int n) {\n    // Truco de Kernighan: n &= n-1\n    return 0;\n}",
        },
    },

    # ══════════════════════════════════════════
    #  MATEMÁTICAS — NORMAL
    # ══════════════════════════════════════════
    {
        "title": "Criba de Eratóstenes",
        "difficulty": "Normal", "category": "Matemáticas", "total_solvers": 0,
        "description": (
            "Dado un entero n, utiliza la Criba de Eratóstenes para contar cuántos números "
            "primos existen estrictamente menores que n.\n\n"
            "El algoritmo opera sobre un array booleano primes[0..n-1] inicializado a True. "
            "Para cada entero p desde 2 hasta ⌊√(n-1)⌋, si primes[p] sigue siendo True, "
            "marca como False todos sus múltiplos p², p²+p, p²+2p, ... hasta n-1. "
            "Al terminar, los índices que permanecen True (excepto 0 y 1) son primos.\n\n"
            "Complejidad: O(n log log n) tiempo, O(n) espacio.\n\n"
            "Restricciones:\n"
            "  0 ≤ n ≤ 5×10^6\n\n"
            "Ejemplo 1:\n"
            "  Entrada: n=10\n"
            "  Salida: 4\n"
            "  Explicación: Los primos menores que 10 son 2, 3, 5, 7.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: n=20\n"
            "  Salida: 8\n"
            "  Explicación: 2, 3, 5, 7, 11, 13, 17, 19.\n\n"
            "Escribe `solve(n)` que devuelva la cantidad de primos estrictamente menores que n."
        ),
        "test_cases": [
            {"input": "10", "expected_output": "4"},
            {"input": "20", "expected_output": "8"},
            {"input": "2",  "expected_output": "0"},
        ],
        "stub": {
            "Python": "def solve(n):\n    # Criba de Eratóstenes\n    if n < 2: return 0\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nint solve(int n) {\n    // Criba de Eratóstenes\n    if (n < 2) return 0;\n    return 0;\n}",
            "Java":   "public static int solve(int n) {\n    // Criba de Eratóstenes\n    if (n < 2) return 0;\n    return 0;\n}",
            "Go":     "func solve(n int) int {\n    // Criba de Eratóstenes\n    if n < 2 { return 0 }\n    return 0\n}",
            "C#":     "public static int Solve(int n) {\n    // Criba de Eratóstenes\n    if (n < 2) return 0;\n    return 0;\n}",
        },
    },
    {
        "title": "Exponenciación Modular",
        "difficulty": "Normal", "category": "Matemáticas", "total_solvers": 0,
        "description": (
            "Calcula (base^exp) mod m de forma eficiente usando el algoritmo de exponenciación "
            "rápida (binary exponentiation).\n\n"
            "La idea central es que:\n"
            "  base^exp = (base^(exp/2))²    si exp es par\n"
            "  base^exp = base × base^(exp-1) si exp es impar\n\n"
            "Esto reduce la complejidad de O(exp) multiplicaciones a solo O(log exp), "
            "fundamental en criptografía y teoría de números donde exp puede tener cientos de dígitos.\n\n"
            "Recuerda aplicar el módulo en cada multiplicación para evitar desbordamiento:\n"
            "  resultado = (a × b) % m\n\n"
            "Restricciones:\n"
            "  0 ≤ base ≤ 10^9\n"
            "  0 ≤ exp  ≤ 10^9\n"
            "  1 ≤ m    ≤ 10^9\n\n"
            "Ejemplo 1:\n"
            "  Entrada: base=2, exp=10, m=1000000007\n"
            "  Salida: 1024\n"
            "  Explicación: 2^10 = 1024 < 10^9+7, así que el resultado es 1024.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: base=2, exp=30, m=1000000007\n"
            "  Salida: 73741817\n"
            "  Explicación: 2^30 = 1073741824; 1073741824 mod (10^9+7) = 73741817.\n\n"
            "Escribe `solve(base, exp, m)` que devuelva (base^exp) mod m."
        ),
        "test_cases": [
            {"input": "2, 10, 1000000007", "expected_output": "1024"},
            {"input": "2, 30, 1000000007", "expected_output": "73741817"},
            {"input": "5, 8, 1000",        "expected_output": "625"},
        ],
        "stub": {
            "Python": "def solve(base, exp, m):\n    # Exponenciación rápida en O(log exp)\n    pass",
            "C++":    "long long solve(long long base, long long exp, long long m) {\n    // Exponenciación rápida en O(log exp)\n    return 0;\n}",
            "Java":   "public static long solve(long base, long exp, long m) {\n    // Exponenciación rápida en O(log exp)\n    return 0;\n}",
            "Go":     "func solve(base int, exp int, m int) int {\n    // Exponenciación rápida en O(log exp)\n    return 0\n}",
            "C#":     "public static long Solve(long baseVal, long exp, long m) {\n    // Exponenciación rápida en O(log exp)\n    return 0;\n}",
        },
    },

    # ══════════════════════════════════════════
    #  ARRAYS — NORMAL
    # ══════════════════════════════════════════
    {
        "title": "Suma de Dos Elementos (Two Sum)",
        "difficulty": "Normal", "category": "Arrays", "total_solvers": 0,
        "description": (
            "Dado un array de enteros nums y un entero objetivo target, devuelve los índices "
            "de los dos elementos que suman target. Puedes asumir que existe exactamente "
            "una solución y que no puedes usar el mismo elemento dos veces.\n\n"
            "Devuelve los índices en orden ascendente: [i, j] con i < j.\n\n"
            "Solución ingenua O(n²): para cada par (i, j) verificar si nums[i]+nums[j]==target.\n\n"
            "Solución óptima O(n) con tabla hash:\n"
            "  Recorre el array. Para cada nums[i], calcula complemento = target - nums[i].\n"
            "  Si complemento ya está en el mapa, devuelve [mapa[complemento], i].\n"
            "  Si no, añade nums[i] → i al mapa.\n\n"
            "Restricciones:\n"
            "  2 ≤ n ≤ 10^4\n"
            "  -10^9 ≤ nums[i] ≤ 10^9\n"
            "  Exactamente una solución garantizada\n\n"
            "Ejemplo 1:\n"
            "  Entrada: nums=[2,7,11,15], target=9\n"
            "  Salida: [0,1]\n"
            "  Explicación: nums[0] + nums[1] = 2 + 7 = 9.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: nums=[3,2,4], target=6\n"
            "  Salida: [1,2]\n\n"
            "Escribe `solve(nums, target)` que devuelva [i, j]."
        ),
        "test_cases": [
            {"input": "[2,7,11,15], 9", "expected_output": "[0,1]"},
            {"input": "[3,2,4], 6",     "expected_output": "[1,2]"},
            {"input": "[3,3], 6",       "expected_output": "[0,1]"},
        ],
        "stub": {
            "Python": "def solve(nums, target):\n    # Solución O(n) con tabla hash\n    pass",
            "C++":    "#include <vector>\n#include <unordered_map>\nusing namespace std;\nvector<int> solve(vector<int> nums, int target) {\n    // Solución O(n) con tabla hash\n    return {};\n}",
            "Java":   "public static int[] solve(int[] nums, int target) {\n    // Solución O(n) con tabla hash (HashMap ya disponible)\n    return new int[]{};\n}",
            "Go":     "func solve(nums []int, target int) []int {\n    // Solución O(n) con tabla hash\n    return nil\n}",
            "C#":     "public static int[] Solve(int[] nums, int target) {\n    // Solución O(n) con tabla hash\n    return new int[]{};\n}",
        },
    },
    {
        "title": "Máximo Subarray (Kadane)",
        "difficulty": "Normal", "category": "Arrays", "total_solvers": 0,
        "description": (
            "Dado un array de enteros nums (puede contener negativos), encuentra el subarray "
            "contiguo de suma máxima y devuelve dicha suma.\n\n"
            "El algoritmo de Kadane resuelve este problema clásico en O(n) manteniendo "
            "dos variables:\n"
            "  - current: suma máxima del subarray que termina en la posición actual\n"
            "  - best: mayor suma vista hasta ahora\n\n"
            "En cada paso:\n"
            "  current = max(nums[i], current + nums[i])\n"
            "  best    = max(best, current)\n\n"
            "La intuición es: si current se vuelve negativo conviene empezar un subarray nuevo "
            "desde la posición actual.\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 10^5\n"
            "  -10^4 ≤ nums[i] ≤ 10^4\n"
            "  Al menos un elemento en el array\n\n"
            "Ejemplo 1:\n"
            "  Entrada: nums=[-2,1,-3,4,-1,2,1,-5,4]\n"
            "  Salida: 6\n"
            "  Explicación: El subarray [4,-1,2,1] tiene la suma máxima = 6.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: nums=[5,4,-1,7,8]\n"
            "  Salida: 23\n"
            "  Explicación: Todo el array suma 23.\n\n"
            "Escribe `solve(nums)` que devuelva la suma máxima del subarray contiguo."
        ),
        "test_cases": [
            {"input": "[-2,1,-3,4,-1,2,1,-5,4]", "expected_output": "6"},
            {"input": "[1]",                       "expected_output": "1"},
            {"input": "[5,4,-1,7,8]",              "expected_output": "23"},
        ],
        "stub": {
            "Python": "def solve(nums):\n    # Algoritmo de Kadane O(n)\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nint solve(vector<int> nums) {\n    // Algoritmo de Kadane O(n)\n    return 0;\n}",
            "Java":   "public static int solve(int[] nums) {\n    // Algoritmo de Kadane O(n)\n    return 0;\n}",
            "Go":     "func solve(nums []int) int {\n    // Algoritmo de Kadane O(n)\n    return 0\n}",
            "C#":     "public static int Solve(int[] nums) {\n    // Algoritmo de Kadane O(n)\n    return 0;\n}",
        },
    },
    {
        "title": "Búsqueda en Array Rotado",
        "difficulty": "Normal", "category": "Arrays", "total_solvers": 0,
        "description": (
            "Un array de enteros distintos ordenado ascendentemente fue rotado en algún punto "
            "pivote desconocido. Por ejemplo, [0,1,2,4,5,6,7] podría convertirse en [4,5,6,7,0,1,2].\n\n"
            "Dado el array rotado nums y un entero target, devuelve el índice de target si existe, "
            "o -1 si no.\n\n"
            "Debes lograrlo en O(log n).\n\n"
            "Clave: aunque el array está rotado, en cada paso al menos una de las dos mitades "
            "[lo..mid] o [mid..hi] es contigua y ordenada. Puedes determinar cuál es la "
            "mitad ordenada comparando nums[lo] con nums[mid].\n\n"
            "  Si nums[lo] ≤ nums[mid]: la mitad izquierda es ordenada.\n"
            "    - Si nums[lo] ≤ target < nums[mid]: busca a la izquierda.\n"
            "    - En caso contrario: busca a la derecha.\n"
            "  Si nums[lo] > nums[mid]: la mitad derecha es ordenada.\n"
            "    - Si nums[mid] < target ≤ nums[hi]: busca a la derecha.\n"
            "    - En caso contrario: busca a la izquierda.\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 5000, todos los valores son distintos\n\n"
            "Ejemplo 1:\n"
            "  Entrada: nums=[4,5,6,7,0,1,2], target=0\n"
            "  Salida: 4\n\n"
            "Ejemplo 2:\n"
            "  Entrada: nums=[4,5,6,7,0,1,2], target=3\n"
            "  Salida: -1\n\n"
            "Escribe `solve(nums, target)` que devuelva el índice o -1."
        ),
        "test_cases": [
            {"input": "[4,5,6,7,0,1,2], 0", "expected_output": "4"},
            {"input": "[4,5,6,7,0,1,2], 3", "expected_output": "-1"},
            {"input": "[1], 0",              "expected_output": "-1"},
        ],
        "stub": {
            "Python": "def solve(nums, target):\n    # Búsqueda binaria modificada O(log n)\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nint solve(vector<int> nums, int target) {\n    // Búsqueda binaria modificada O(log n)\n    return -1;\n}",
            "Java":   "public static int solve(int[] nums, int target) {\n    // Búsqueda binaria modificada O(log n)\n    return -1;\n}",
            "Go":     "func solve(nums []int, target int) int {\n    // Búsqueda binaria modificada O(log n)\n    return -1\n}",
            "C#":     "public static int Solve(int[] nums, int target) {\n    // Búsqueda binaria modificada O(log n)\n    return -1;\n}",
        },
    },
    {
        "title": "Caminos Únicos en una Cuadrícula",
        "difficulty": "Normal", "category": "Arrays", "total_solvers": 0,
        "description": (
            "Un robot parte de la esquina superior-izquierda de una cuadrícula de m filas × n "
            "columnas. El robot solo puede moverse hacia la derecha o hacia abajo. "
            "¿De cuántas maneras distintas puede llegar a la esquina inferior-derecha?\n\n"
            "Solución por programación dinámica:\n"
            "  Sea dp[i][j] = número de caminos únicos para llegar a la celda (i,j).\n"
            "  Caso base: dp[0][j] = 1 para toda j (solo se puede mover a la derecha en la fila 0),\n"
            "             dp[i][0] = 1 para toda i (solo se puede bajar en la columna 0).\n"
            "  Transición: dp[i][j] = dp[i-1][j] + dp[i][j-1].\n\n"
            "Equivalencia combinatoria: la respuesta es C(m+n-2, m-1) = (m+n-2)! / ((m-1)! (n-1)!), "
            "el número de formas de elegir los m-1 movimientos hacia abajo del total de m+n-2.\n\n"
            "Restricciones:\n"
            "  1 ≤ m, n ≤ 100\n\n"
            "Ejemplo 1:\n"
            "  Entrada: m=3, n=7\n"
            "  Salida: 28\n\n"
            "Ejemplo 2:\n"
            "  Entrada: m=3, n=2\n"
            "  Salida: 3\n"
            "  Explicación: Los 3 caminos son ↓↓→, ↓→↓, →↓↓.\n\n"
            "Escribe `solve(m, n)` que devuelva el número de caminos únicos."
        ),
        "test_cases": [
            {"input": "3, 7", "expected_output": "28"},
            {"input": "3, 2", "expected_output": "3"},
            {"input": "7, 3", "expected_output": "28"},
        ],
        "stub": {
            "Python": "def solve(m, n):\n    # DP O(m*n) o combinatoria O(min(m,n))\n    pass",
            "C++":    "int solve(int m, int n) {\n    // DP O(m*n) o combinatoria O(min(m,n))\n    return 0;\n}",
            "Java":   "public static int solve(int m, int n) {\n    // DP O(m*n) o combinatoria O(min(m,n))\n    return 0;\n}",
            "Go":     "func solve(m int, n int) int {\n    // DP O(m*n) o combinatoria O(min(m,n))\n    return 0\n}",
            "C#":     "public static int Solve(int m, int n) {\n    // DP O(m*n) o combinatoria O(min(m,n))\n    return 0;\n}",
        },
    },

    # ══════════════════════════════════════════
    #  STRINGS — NORMAL
    # ══════════════════════════════════════════
    {
        "title": "Substring sin Caracteres Repetidos",
        "difficulty": "Normal", "category": "Strings", "total_solvers": 0,
        "description": (
            "Dada una cadena s, encuentra la longitud del substring más largo que no contenga "
            "caracteres repetidos.\n\n"
            "Técnica de ventana deslizante (sliding window):\n"
            "  Mantén dos punteros, lo y hi, que delimitan la ventana actual.\n"
            "  Mantén un conjunto (o mapa) con los caracteres dentro de la ventana.\n"
            "  Al avanzar hi, si s[hi] ya está en la ventana, contrae la ventana "
            "incrementando lo hasta eliminar la primera ocurrencia de s[hi].\n"
            "  Actualiza la respuesta con hi - lo + 1 en cada paso.\n\n"
            "Complejidad: O(n) amortizado, O(min(n, |alfabeto|)) espacio.\n\n"
            "Restricciones:\n"
            "  0 ≤ |s| ≤ 5×10^4\n"
            "  s puede contener letras, dígitos, símbolos y espacios\n\n"
            "Ejemplo 1:\n"
            "  Entrada: s=\"abcabcbb\"\n"
            "  Salida: 3\n"
            "  Explicación: La ventana \"abc\" (índices 0-2) tiene longitud 3 sin repeticiones.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: s=\"bbbbb\"\n"
            "  Salida: 1\n"
            "  Explicación: Solo el carácter \"b\" sin repetición.\n\n"
            "Ejemplo 3:\n"
            "  Entrada: s=\"pwwkew\"\n"
            "  Salida: 3\n"
            "  Explicación: La ventana \"wke\" tiene longitud 3.\n\n"
            "Escribe `solve(s)` que devuelva la longitud máxima."
        ),
        "test_cases": [
            {"input": '"abcabcbb"', "expected_output": "3"},
            {"input": '"bbbbb"',    "expected_output": "1"},
            {"input": '"pwwkew"',   "expected_output": "3"},
        ],
        "stub": {
            "Python": "def solve(s):\n    # Ventana deslizante O(n)\n    pass",
            "C++":    "#include <string>\n#include <unordered_map>\nusing namespace std;\nint solve(string s) {\n    // Ventana deslizante O(n)\n    return 0;\n}",
            "Java":   "public static int solve(String s) {\n    // Ventana deslizante O(n)\n    return 0;\n}",
            "Go":     "func solve(s string) int {\n    // Ventana deslizante O(n)\n    return 0\n}",
            "C#":     "public static int Solve(string s) {\n    // Ventana deslizante O(n)\n    return 0;\n}",
        },
    },
    {
        "title": "Fila k de Pascal",
        "difficulty": "Normal", "category": "Matemáticas", "total_solvers": 0,
        "description": (
            "El triángulo de Pascal es una matriz triangular donde cada elemento es la suma de "
            "los dos elementos directamente encima. Las primeras filas son:\n\n"
            "  Fila 0: [1]\n"
            "  Fila 1: [1, 1]\n"
            "  Fila 2: [1, 2, 1]\n"
            "  Fila 3: [1, 3, 3, 1]\n"
            "  Fila 4: [1, 4, 6, 4, 1]\n"
            "  Fila 5: [1, 5, 10, 10, 5, 1]\n\n"
            "Los elementos de la fila k son los coeficientes binomiales C(k,0), C(k,1), ..., C(k,k), "
            "donde C(k,j) = k! / (j! (k-j)!).\n\n"
            "Restricción de memoria: devuelve únicamente la fila k usando O(k) espacio. "
            "Puedes actualizar un solo array in-place, iterando de derecha a izquierda:\n"
            "  row[j] += row[j-1]\n\n"
            "Restricciones:\n"
            "  0 ≤ k ≤ 33  (C(33,16) ≈ 1.17×10^9, cabe en 32 bits)\n\n"
            "Ejemplo 1:\n"
            "  Entrada: k=3\n"
            "  Salida: [1,3,3,1]\n\n"
            "Ejemplo 2:\n"
            "  Entrada: k=0\n"
            "  Salida: [1]\n\n"
            "Escribe `solve(k)` que devuelva la fila k del triángulo de Pascal como lista."
        ),
        "test_cases": [
            {"input": "3", "expected_output": "[1,3,3,1]"},
            {"input": "0", "expected_output": "[1]"},
            {"input": "5", "expected_output": "[1,5,10,10,5,1]"},
        ],
        "stub": {
            "Python": "def solve(k):\n    # Construye la fila k en O(k) espacio\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nvector<int> solve(int k) {\n    // Construye la fila k en O(k) espacio\n    return {};\n}",
            "Java":   "public static int[] solve(int k) {\n    // Construye la fila k en O(k) espacio\n    return new int[]{};\n}",
            "Go":     "func solve(k int) []int {\n    // Construye la fila k en O(k) espacio\n    return nil\n}",
            "C#":     "public static int[] Solve(int k) {\n    // Construye la fila k en O(k) espacio\n    return new int[]{};\n}",
        },
    },

    # ══════════════════════════════════════════
    #  DIFÍCILES
    # ══════════════════════════════════════════
    {
        "title": "Agua Atrapada entre Muros",
        "difficulty": "Difícil", "category": "Arrays", "total_solvers": 0,
        "description": (
            "Dado un array de enteros heights donde heights[i] representa la altura de un muro "
            "de ancho 1 unidad, calcula cuántas unidades de agua pueden quedar atrapadas "
            "después de llover.\n\n"
            "El agua sobre la posición i fica en min(máximo_a_la_izquierda[i], "
            "máximo_a_la_derecha[i]) - heights[i] (siempre que sea positivo).\n\n"
            "Solución O(n) con dos punteros:\n"
            "  Mantén lo=0 y hi=n-1, maxL=0 y maxR=0, resultado=0.\n"
            "  Mientras lo < hi:\n"
            "    Si heights[lo] ≤ heights[hi]:\n"
            "      Si heights[lo] ≥ maxL: maxL = heights[lo]\n"
            "      Si no: resultado += maxL - heights[lo]\n"
            "      lo++\n"
            "    Si no: análogo con maxR y hi--\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 3×10^4\n"
            "  0 ≤ heights[i] ≤ 10^5\n\n"
            "Ejemplo 1:\n"
            "  Entrada: heights=[0,1,0,2,1,0,1,3,2,1,2,1]\n"
            "  Salida: 6\n"
            "  Visualización: el agua se acumula en los valles entre los muros.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: heights=[4,2,0,3,2,5]\n"
            "  Salida: 9\n\n"
            "Escribe `solve(heights)` que devuelva las unidades totales de agua atrapada."
        ),
        "test_cases": [
            {"input": "[0,1,0,2,1,0,1,3,2,1,2,1]", "expected_output": "6"},
            {"input": "[4,2,0,3,2,5]",               "expected_output": "9"},
            {"input": "[3,0,3]",                      "expected_output": "3"},
        ],
        "stub": {
            "Python": "def solve(heights):\n    # Dos punteros O(n)\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nint solve(vector<int> heights) {\n    // Dos punteros O(n)\n    return 0;\n}",
            "Java":   "public static int solve(int[] heights) {\n    // Dos punteros O(n)\n    return 0;\n}",
            "Go":     "func solve(heights []int) int {\n    // Dos punteros O(n)\n    return 0\n}",
            "C#":     "public static int Solve(int[] heights) {\n    // Dos punteros O(n)\n    return 0;\n}",
        },
    },
    {
        "title": "Distancia de Edición (Levenshtein)",
        "difficulty": "Difícil", "category": "Strings", "total_solvers": 0,
        "description": (
            "Dadas dos cadenas s1 y s2, calcula el número mínimo de operaciones necesarias para "
            "convertir s1 en s2. Las operaciones permitidas son:\n"
            "  - Insertar un carácter\n"
            "  - Eliminar un carácter\n"
            "  - Reemplazar un carácter\n\n"
            "Esta métrica, conocida como Distancia de Levenshtein, se usa en correctores "
            "ortográficos, alineación de ADN y búsqueda difusa.\n\n"
            "Solución DP en O(|s1|·|s2|):\n"
            "  Sea dp[i][j] = distancia entre s1[0..i-1] y s2[0..j-1].\n"
            "  Caso base: dp[i][0] = i (eliminar i caracteres), dp[0][j] = j.\n"
            "  Transición:\n"
            "    Si s1[i-1] == s2[j-1]: dp[i][j] = dp[i-1][j-1]  (sin coste)\n"
            "    Si no: dp[i][j] = 1 + min(dp[i-1][j],   (eliminar de s1)\n"
            "                                dp[i][j-1],   (insertar en s1)\n"
            "                                dp[i-1][j-1]) (reemplazar)\n\n"
            "Restricciones:\n"
            "  0 ≤ |s1|, |s2| ≤ 500\n\n"
            "Ejemplo 1:\n"
            "  Entrada: s1=\"horse\", s2=\"ros\"\n"
            "  Salida: 3\n"
            "  Explicación: horse→rorse (reemplazar h→r), rorse→rose (eliminar r), rose→ros (eliminar e).\n\n"
            "Ejemplo 2:\n"
            "  Entrada: s1=\"intention\", s2=\"execution\"\n"
            "  Salida: 5\n\n"
            "Escribe `solve(s1, s2)` que devuelva la distancia de edición."
        ),
        "test_cases": [
            {"input": '"horse", "ros"',           "expected_output": "3"},
            {"input": '"intention", "execution"', "expected_output": "5"},
            {"input": '"abc", "abc"',             "expected_output": "0"},
        ],
        "stub": {
            "Python": "def solve(s1, s2):\n    # DP O(|s1|*|s2|)\n    pass",
            "C++":    "#include <string>\n#include <vector>\nusing namespace std;\nint solve(string s1, string s2) {\n    // DP O(|s1|*|s2|)\n    return 0;\n}",
            "Java":   "public static int solve(String s1, String s2) {\n    // DP O(|s1|*|s2|)\n    return 0;\n}",
            "Go":     "func solve(s1 string, s2 string) int {\n    // DP O(|s1|*|s2|)\n    return 0\n}",
            "C#":     "public static int Solve(string s1, string s2) {\n    // DP O(|s1|*|s2|)\n    return 0;\n}",
        },
    },
    {
        "title": "Subsecuencia Común más Larga (LCS)",
        "difficulty": "Difícil", "category": "Strings", "total_solvers": 0,
        "description": (
            "Dadas dos cadenas s1 y s2, calcula la longitud de su subsecuencia común más larga (LCS). "
            "Una subsecuencia es una secuencia de caracteres que aparece en el mismo orden relativo "
            "en ambas cadenas, aunque no necesariamente de forma contigua.\n\n"
            "Por ejemplo, la LCS de \"abcde\" y \"ace\" es \"ace\" con longitud 3.\n\n"
            "Solución DP en O(|s1|·|s2|):\n"
            "  Sea dp[i][j] = longitud de LCS entre s1[0..i-1] y s2[0..j-1].\n"
            "  Caso base: dp[i][0] = dp[0][j] = 0.\n"
            "  Transición:\n"
            "    Si s1[i-1] == s2[j-1]: dp[i][j] = dp[i-1][j-1] + 1\n"
            "    Si no:                  dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n\n"
            "El LCS tiene múltiples aplicaciones: diff en control de versiones (git diff), "
            "alineación de secuencias genéticas, detección de plagio.\n\n"
            "Restricciones:\n"
            "  1 ≤ |s1|, |s2| ≤ 1000\n"
            "  Las cadenas contienen solo letras minúsculas\n\n"
            "Ejemplo 1:\n"
            "  Entrada: s1=\"abcde\", s2=\"ace\"\n"
            "  Salida: 3\n"
            "  Explicación: LCS es \"ace\".\n\n"
            "Ejemplo 2:\n"
            "  Entrada: s1=\"bl\", s2=\"yby\"\n"
            "  Salida: 1\n"
            "  Explicación: LCS es \"b\".\n\n"
            "Escribe `solve(s1, s2)` que devuelva la longitud de la LCS."
        ),
        "test_cases": [
            {"input": '"abcde", "ace"', "expected_output": "3"},
            {"input": '"abc", "abc"',   "expected_output": "3"},
            {"input": '"bl", "yby"',    "expected_output": "1"},
        ],
        "stub": {
            "Python": "def solve(s1, s2):\n    # DP O(|s1|*|s2|)\n    pass",
            "C++":    "#include <string>\n#include <vector>\nusing namespace std;\nint solve(string s1, string s2) {\n    // DP O(|s1|*|s2|)\n    return 0;\n}",
            "Java":   "public static int solve(String s1, String s2) {\n    // DP O(|s1|*|s2|)\n    return 0;\n}",
            "Go":     "func solve(s1 string, s2 string) int {\n    // DP O(|s1|*|s2|)\n    return 0\n}",
            "C#":     "public static int Solve(string s1, string s2) {\n    // DP O(|s1|*|s2|)\n    return 0;\n}",
        },
    },
    {
        "title": "Mochila 0/1 (Knapsack)",
        "difficulty": "Difícil", "category": "Arrays", "total_solvers": 0,
        "description": (
            "Tienes una mochila con capacidad máxima W kilogramos y n objetos. "
            "Cada objeto i tiene un peso weights[i] y un valor values[i]. "
            "Solo puedes llevar cada objeto como máximo una vez (0/1). "
            "¿Cuál es el valor máximo que puedes transportar sin exceder la capacidad W?\n\n"
            "Solución DP en O(n·W):\n"
            "  Sea dp[j] = valor máximo alcanzable con capacidad j.\n"
            "  Inicialmente dp[j] = 0 para todo j.\n"
            "  Para cada objeto i, itera j de W hacia weights[i]:\n"
            "    dp[j] = max(dp[j], dp[j - weights[i]] + values[i])\n\n"
            "La iteración inversa garantiza que cada objeto se use como máximo una vez "
            "(a diferencia de la Mochila Fraccionaria o la Mochila con repetición).\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 100\n"
            "  1 ≤ W ≤ 1000\n"
            "  1 ≤ weights[i], values[i] ≤ 100\n\n"
            "Ejemplo 1:\n"
            "  Entrada: weights=[1,2,3], values=[6,10,12], W=5\n"
            "  Salida: 22\n"
            "  Explicación: Tomar objetos 1 y 2 (peso=2+3=5, valor=10+12=22).\n\n"
            "Ejemplo 2:\n"
            "  Entrada: weights=[10,20,30], values=[60,100,120], W=50\n"
            "  Salida: 220\n"
            "  Explicación: Tomar objetos 1 y 2 (peso=20+30=50, valor=100+120=220).\n\n"
            "Escribe `solve(weights, values, W)` que devuelva el valor máximo."
        ),
        "test_cases": [
            {"input": "[1,2,3], [6,10,12], 5",     "expected_output": "22"},
            {"input": "[2,3,4,5], [3,4,5,6], 5",   "expected_output": "7"},
            {"input": "[10,20,30], [60,100,120], 50", "expected_output": "220"},
        ],
        "stub": {
            "Python": "def solve(weights, values, W):\n    # DP O(n*W), iterar j de W hacia weights[i]\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nint solve(vector<int> weights, vector<int> values, int W) {\n    // DP O(n*W)\n    return 0;\n}",
            "Java":   "public static int solve(int[] weights, int[] values, int W) {\n    // DP O(n*W)\n    return 0;\n}",
            "Go":     "func solve(weights []int, values []int, W int) int {\n    // DP O(n*W)\n    return 0\n}",
            "C#":     "public static int Solve(int[] weights, int[] values, int W) {\n    // DP O(n*W)\n    return 0;\n}",
        },
    },
    {
        "title": "Multiplicación de Cadena de Matrices",
        "difficulty": "Difícil", "category": "Matemáticas", "total_solvers": 0,
        "description": (
            "Dada una secuencia de n matrices A₁, A₂, ..., Aₙ donde la matriz Aᵢ tiene "
            "dimensiones dims[i-1] × dims[i], determina el número mínimo de multiplicaciones "
            "escalares necesarias para calcular el producto A₁·A₂·...·Aₙ.\n\n"
            "El orden de los paréntesis afecta radicalmente al coste. Multiplicar una "
            "matriz de p×q por una de q×r cuesta p·q·r operaciones.\n\n"
            "Solución DP en O(n³):\n"
            "  Sea dp[i][j] = mínimo coste de multiplicar Aᵢ ... Aⱼ (índices base 0).\n"
            "  Caso base: dp[i][i] = 0.\n"
            "  Transición (longitud de cadena l = 2..n):\n"
            "    Para cada par (i, j) con j = i+l-1:\n"
            "      dp[i][j] = min sobre k en [i..j-1] de:\n"
            "        dp[i][k] + dp[k+1][j] + dims[i]·dims[k+1]·dims[j+1]\n\n"
            "Restricciones:\n"
            "  2 ≤ len(dims) ≤ 15  (hasta 14 matrices)\n"
            "  1 ≤ dims[i] ≤ 100\n\n"
            "Ejemplo 1:\n"
            "  Entrada: dims=[1,2,3,4]\n"
            "  Salida: 18\n"
            "  Explicación: 3 matrices (1×2)(2×3)(3×4).\n"
            "    Opción A: ((A₁·A₂)·A₃) → 1·2·3=6 luego 1·3·4=12 → total 18.\n"
            "    Opción B: (A₁·(A₂·A₃)) → 2·3·4=24 luego 1·2·4=8 → total 32.\n"
            "    Mínimo: 18.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: dims=[40,20,30,10,30]\n"
            "  Salida: 26000\n\n"
            "Escribe `solve(dims)` que devuelva el mínimo de multiplicaciones escalares."
        ),
        "test_cases": [
            {"input": "[1,2,3,4]",        "expected_output": "18"},
            {"input": "[40,20,30,10,30]", "expected_output": "26000"},
            {"input": "[10,30,5,60]",     "expected_output": "4500"},
        ],
        "stub": {
            "Python": "def solve(dims):\n    n = len(dims) - 1  # número de matrices\n    # dp[i][j] = min coste de multiplicar matrices i..j\n    pass",
            "C++":    "#include <vector>\n#include <climits>\nusing namespace std;\nint solve(vector<int> dims) {\n    int n = dims.size() - 1;\n    // dp[i][j] = min coste de multiplicar matrices i..j\n    return 0;\n}",
            "Java":   "public static int solve(int[] dims) {\n    int n = dims.length - 1;\n    // dp[i][j] = min coste de multiplicar matrices i..j\n    return 0;\n}",
            "Go":     "func solve(dims []int) int {\n    n := len(dims) - 1\n    // dp[i][j] = min coste de multiplicar matrices i..j\n    return 0\n}",
            "C#":     "public static int Solve(int[] dims) {\n    int n = dims.Length - 1;\n    // dp[i][j] = min coste de multiplicar matrices i..j\n    return 0;\n}",
        },
    },
    {
        "title": "Conteo de Inversiones (Merge Sort)",
        "difficulty": "Difícil", "category": "Arrays", "total_solvers": 0,
        "description": (
            "Un par de índices (i, j) con i < j forma una inversión si nums[i] > nums[j]. "
            "El número de inversiones mide qué tan desordenado está un array: 0 inversiones "
            "significa array ordenado; n·(n-1)/2 inversiones significa orden completamente inverso.\n\n"
            "La solución ingenua O(n²) recorre todos los pares. El desafío es resolverlo en O(n log n) "
            "modificando el algoritmo Merge Sort.\n\n"
            "Clave: durante la fase de fusión (merge) de dos mitades ya ordenadas, cada vez que "
            "tomamos un elemento de la mitad derecha antes que uno de la izquierda, el elemento "
            "derecho forma una inversión con todos los elementos restantes de la mitad izquierda.\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 10^5\n"
            "  -10^9 ≤ nums[i] ≤ 10^9\n\n"
            "Ejemplo 1:\n"
            "  Entrada: nums=[2,4,1,3,5]\n"
            "  Salida: 3\n"
            "  Explicación: Las inversiones son (2,1), (4,1), (4,3).\n\n"
            "Ejemplo 2:\n"
            "  Entrada: nums=[5,4,3,2,1]\n"
            "  Salida: 10\n"
            "  Explicación: n=5, inversiones = 5·4/2 = 10. Todas las parejas son inversiones.\n\n"
            "Ejemplo 3:\n"
            "  Entrada: nums=[1,2,3,4,5]\n"
            "  Salida: 0\n\n"
            "Escribe `solve(nums)` que devuelva el número total de inversiones."
        ),
        "test_cases": [
            {"input": "[2,4,1,3,5]",   "expected_output": "3"},
            {"input": "[5,4,3,2,1]",   "expected_output": "10"},
            {"input": "[1,2,3,4,5]",   "expected_output": "0"},
        ],
        "stub": {
            "Python": "def solve(nums):\n    # Merge Sort modificado O(n log n)\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nlong long solve(vector<int> nums) {\n    // Merge Sort modificado O(n log n)\n    return 0;\n}",
            "Java":   "public static long solve(int[] nums) {\n    // Merge Sort modificado O(n log n)\n    return 0;\n}",
            "Go":     "func solve(nums []int) int {\n    // Merge Sort modificado O(n log n)\n    return 0\n}",
            "C#":     "public static long Solve(int[] nums) {\n    // Merge Sort modificado O(n log n)\n    return 0;\n}",
        },
    },
    {
        "title": "Número de Catalan",
        "difficulty": "Difícil", "category": "Matemáticas", "total_solvers": 0,
        "description": (
            "El n-ésimo número de Catalan Cₙ cuenta el número de muchas estructuras combinatorias "
            "distintas, entre ellas:\n"
            "  - Formas de triangular un polígono convexo de n+2 vértices.\n"
            "  - Árboles binarios completos con n+1 hojas.\n"
            "  - Secuencias de n pares de paréntesis correctamente balanceados.\n"
            "  - Formas de colocar paréntesis en una cadena de n+1 factores.\n\n"
            "La fórmula cerrada es:\n"
            "  Cₙ = C(2n, n) / (n+1) = (2n)! / ((n+1)! · n!)\n\n"
            "Los primeros valores son: C₀=1, C₁=1, C₂=2, C₃=5, C₄=14, C₅=42, C₆=132, ...\n\n"
            "Recurrencia eficiente para calcularlos iterativamente sin desbordamiento:\n"
            "  C₀ = 1\n"
            "  Cₙ = Cₙ₋₁ × 2(2n-1) / (n+1)\n\n"
            "Restricciones:\n"
            "  0 ≤ n ≤ 19  (C₁₉ = 1767263190, cabe en 32 bits)\n\n"
            "Ejemplo 1:\n"
            "  Entrada: n=5\n"
            "  Salida: 42\n\n"
            "Ejemplo 2:\n"
            "  Entrada: n=0\n"
            "  Salida: 1\n\n"
            "Escribe `solve(n)` que devuelva el n-ésimo número de Catalan."
        ),
        "test_cases": [
            {"input": "5",  "expected_output": "42"},
            {"input": "0",  "expected_output": "1"},
            {"input": "10", "expected_output": "16796"},
        ],
        "stub": {
            "Python": "def solve(n):\n    # Usa la recurrencia C(n) = C(n-1) * 2(2n-1) / (n+1)\n    pass",
            "C++":    "long long solve(int n) {\n    // Usa la recurrencia C(n) = C(n-1) * 2*(2n-1) / (n+1)\n    return 0;\n}",
            "Java":   "public static long solve(int n) {\n    // Usa la recurrencia C(n) = C(n-1) * 2*(2n-1) / (n+1)\n    return 0;\n}",
            "Go":     "func solve(n int) int {\n    // Usa la recurrencia C(n) = C(n-1) * 2*(2n-1) / (n+1)\n    return 0\n}",
            "C#":     "public static long Solve(int n) {\n    // Usa la recurrencia C(n) = C(n-1) * 2*(2n-1) / (n+1)\n    return 0;\n}",
        },
    },
    {
        "title": "Invertir una Cadena",
        "difficulty": "Fácil", "category": "Strings", "total_solvers": 0,
        "description": (
            "Dada una cadena de texto s, devuelve la cadena invertida.\n\n"
            "Restricciones:\n"
            "  1 ≤ |s| ≤ 10^5\n\n"
            "Ejemplo 1:\n"
            "  Entrada: s=\"hola\"\n"
            "  Salida: \"aloh\"\n\n"
            "Escribe `solve(s)` que devuelva la cadena invertida."
        ),
        "test_cases": [
            {"input": '"hola"', "expected_output": '"aloh"'},
            {"input": '"openai"', "expected_output": '"ianepo"'},
            {"input": '"a"', "expected_output": '"a"'},
        ],
        "stub": {
            "Python": "def solve(s):\n    pass",
            "C++":    "#include <string>\nusing namespace std;\nstring solve(string s) {\n    return \"\";\n}",
            "Java":   "public static String solve(String s) {\n    return \"\";\n}",
            "Go":     "func solve(s string) string {\n    return \"\"\n}",
            "C#":     "public static string Solve(string s) {\n    return \"\";\n}",
        },
    },
    {
        "title": "Número Par o Impar",
        "difficulty": "Fácil", "category": "Matemáticas", "total_solvers": 0,
        "description": (
            "Dado un número entero n, devuelve \"Par\" si es par y \"Impar\" si es impar.\n\n"
            "Restricciones:\n"
            "  -10^9 ≤ n ≤ 10^9\n\n"
            "Ejemplo 1:\n"
            "  Entrada: n=4\n"
            "  Salida: \"Par\"\n\n"
            "Ejemplo 2:\n"
            "  Entrada: n=7\n"
            "  Salida: \"Impar\"\n\n"
            "Escribe `solve(n)` que devuelva \"Par\" o \"Impar\"."
        ),
        "test_cases": [
            {"input": "4", "expected_output": '"Par"'},
            {"input": "7", "expected_output": '"Impar"'},
            {"input": "0", "expected_output": '"Par"'},
        ],
        "stub": {
            "Python": "def solve(n):\n    pass",
            "C++":    "#include <string>\nusing namespace std;\nstring solve(int n) {\n    return \"\";\n}",
            "Java":   "public static String solve(int n) {\n    return \"\";\n}",
            "Go":     "func solve(n int) string {\n    return \"\"\n}",
            "C#":     "public static string Solve(int n) {\n    return \"\";\n}",
        },
    },
    {
        "title": "Suma de Elementos",
        "difficulty": "Fácil", "category": "Arrays", "total_solvers": 0,
        "description": (
            "Dado un array de enteros, devuelve la suma de todos sus elementos.\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 10^4\n"
            "  -1000 ≤ nums[i] ≤ 1000\n\n"
            "Ejemplo 1:\n"
            "  Entrada: nums=[1,2,3]\n"
            "  Salida: 6\n\n"
            "Escribe `solve(nums)` que devuelva la suma."
        ),
        "test_cases": [
            {"input": "[1,2,3]", "expected_output": "6"},
            {"input": "[-1,1]",  "expected_output": "0"},
            {"input": "[5]",     "expected_output": "5"},
        ],
        "stub": {
            "Python": "def solve(nums):\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nint solve(vector<int> nums) {\n    return 0;\n}",
            "Java":   "public static int solve(int[] nums) {\n    return 0;\n}",
            "Go":     "func solve(nums []int) int {\n    return 0\n}",
            "C#":     "public static int Solve(int[] nums) {\n    return 0;\n}",
        },
    },
    {
        "title": "Encontrar el Máximo",
        "difficulty": "Fácil", "category": "Arrays", "total_solvers": 0,
        "description": (
            "Dado un array de enteros, encuentra y devuelve el valor máximo.\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 10^4\n"
            "  -10^9 ≤ nums[i] ≤ 10^9\n\n"
            "Ejemplo 1:\n"
            "  Entrada: nums=[4,7,2,9,1]\n"
            "  Salida: 9\n\n"
            "Escribe `solve(nums)` que devuelva el máximo."
        ),
        "test_cases": [
            {"input": "[4,7,2,9,1]", "expected_output": "9"},
            {"input": "[-5,-1,-10]", "expected_output": "-1"},
            {"input": "[0]",         "expected_output": "0"},
        ],
        "stub": {
            "Python": "def solve(nums):\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nint solve(vector<int> nums) {\n    return 0;\n}",
            "Java":   "public static int solve(int[] nums) {\n    return 0;\n}",
            "Go":     "func solve(nums []int) int {\n    return 0\n}",
            "C#":     "public static int Solve(int[] nums) {\n    return 0;\n}",
        },
    },
    {
        "title": "FizzBuzz",
        "difficulty": "Fácil", "category": "Matemáticas", "total_solvers": 0,
        "description": (
            "Dado un entero n, devuelve un array de strings desde 1 hasta n donde:\n"
            " - \"FizzBuzz\" si i es divisible por 3 y 5.\n"
            " - \"Fizz\" si i es divisible por 3.\n"
            " - \"Buzz\" si i es divisible por 5.\n"
            " - \"i\" (como string) si no cumple ninguna.\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 10^4\n\n"
            "Ejemplo 1:\n"
            "  Entrada: n=3\n"
            "  Salida: [\"1\",\"2\",\"Fizz\"]\n\n"
            "Escribe `solve(n)` que devuelva la lista."
        ),
        "test_cases": [
            {"input": "3",  "expected_output": '["1","2","Fizz"]'},
            {"input": "5",  "expected_output": '["1","2","Fizz","4","Buzz"]'},
            {"input": "15", "expected_output": '["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]'},
        ],
        "stub": {
            "Python": "def solve(n):\n    pass",
            "C++":    "#include <vector>\n#include <string>\nusing namespace std;\nvector<string> solve(int n) {\n    return {};\n}",
            "Java":   "public static String[] solve(int n) {\n    return new String[]{};\n}",
            "Go":     "func solve(n int) []string {\n    return nil\n}",
            "C#":     "public static string[] Solve(int n) {\n    return new string[]{};\n}",
        },
    },
    {
        "title": "Validar Paréntesis",
        "difficulty": "Normal", "category": "Strings", "total_solvers": 0,
        "description": (
            "Dada una cadena s que contiene solo los caracteres '(', ')', '{', '}', '[' y ']', "
            "determina si la cadena es válida.\n\n"
            "Una cadena es válida si:\n"
            " 1. Los paréntesis abiertos se cierran con el mismo tipo de paréntesis.\n"
            " 2. Los paréntesis abiertos se cierran en el orden correcto.\n\n"
            "Restricciones:\n"
            "  1 ≤ |s| ≤ 10^4\n\n"
            "Ejemplo 1:\n"
            "  Entrada: s=\"()[]{}\"\n"
            "  Salida: True\n\n"
            "Ejemplo 2:\n"
            "  Entrada: s=\"([)]\"\n"
            "  Salida: False\n\n"
            "Escribe `solve(s)` que devuelva True o False."
        ),
        "test_cases": [
            {"input": '"()[]{}"', "expected_output": "True"},
            {"input": '"([)]"',   "expected_output": "False"},
            {"input": '"{[]}"',   "expected_output": "True"},
        ],
        "stub": {
            "Python": "def solve(s):\n    pass",
            "C++":    "#include <string>\nusing namespace std;\nbool solve(string s) {\n    return false;\n}",
            "Java":   "public static boolean solve(String s) {\n    return false;\n}",
            "Go":     "func solve(s string) bool {\n    return false\n}",
            "C#":     "public static bool Solve(string s) {\n    return false;\n}",
        },
    },
    {
        "title": "Producto Excepto Él Mismo",
        "difficulty": "Normal", "category": "Arrays", "total_solvers": 0,
        "description": (
            "Dado un array de enteros nums, devuelve un array respuesta donde respuesta[i] es "
            "igual al producto de todos los elementos de nums excepto nums[i].\n\n"
            "El algoritmo debe correr en tiempo O(n) y no puedes usar el operador de división.\n\n"
            "Restricciones:\n"
            "  2 ≤ n ≤ 10^5\n"
            "  El producto de cualquier prefijo o sufijo cabe en 32 bits.\n\n"
            "Ejemplo 1:\n"
            "  Entrada: nums=[1,2,3,4]\n"
            "  Salida: [24,12,8,6]\n\n"
            "Escribe `solve(nums)` que devuelva el array de productos."
        ),
        "test_cases": [
            {"input": "[1,2,3,4]", "expected_output": "[24,12,8,6]"},
            {"input": "[-1,1,0,-3,3]", "expected_output": "[0,0,9,0,0]"},
        ],
        "stub": {
            "Python": "def solve(nums):\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nvector<int> solve(vector<int> nums) {\n    return {};\n}",
            "Java":   "public static int[] solve(int[] nums) {\n    return new int[]{};\n}",
            "Go":     "func solve(nums []int) []int {\n    return nil\n}",
            "C#":     "public static int[] Solve(int[] nums) {\n    return new int[]{};\n}",
        },
    },
    {
        "title": "Matriz Espiral",
        "difficulty": "Normal", "category": "Arrays", "total_solvers": 0,
        "description": (
            "Dada una matriz m x n de enteros, devuelve todos los elementos de la matriz en orden espiral.\n\n"
            "Restricciones:\n"
            "  1 ≤ m, n ≤ 10\n"
            "  -100 ≤ matriz[i][j] ≤ 100\n\n"
            "Ejemplo 1:\n"
            "  Entrada: matriz=[[1,2,3],[4,5,6],[7,8,9]]\n"
            "  Salida: [1,2,3,6,9,8,7,4,5]\n\n"
            "Escribe `solve(matriz)` que devuelva una lista con el recorrido espiral."
        ),
        "test_cases": [
            {"input": "[[1,2,3],[4,5,6],[7,8,9]]", "expected_output": "[1,2,3,6,9,8,7,4,5]"},
            {"input": "[[1,2,3,4],[5,6,7,8],[9,10,11,12]]", "expected_output": "[1,2,3,4,8,12,11,10,9,5,6,7]"},
        ],
        "stub": {
            "Python": "def solve(matriz):\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nvector<int> solve(vector<vector<int>> matriz) {\n    return {};\n}",
            "Java":   "public static int[] solve(int[][] matriz) {\n    return new int[]{};\n}",
            "Go":     "func solve(matriz [][]int) []int {\n    return nil\n}",
            "C#":     "public static int[] Solve(int[][] matriz) {\n    return new int[]{};\n}",
        },
    },
    {
        "title": "Agrupar Anagramas",
        "difficulty": "Normal", "category": "Strings", "total_solvers": 0,
        "description": (
            "Dado un array de strings, agrupa los anagramas entre sí. Puedes devolver la respuesta en cualquier orden.\n\n"
            "Restricciones:\n"
            "  1 ≤ longitud del array ≤ 10^4\n"
            "  Las cadenas consisten en letras minúsculas en inglés.\n\n"
            "Ejemplo 1:\n"
            "  Entrada: strs=[\"eat\",\"tea\",\"tan\",\"ate\",\"nat\",\"bat\"]\n"
            "  Salida: [[\"bat\"],[\"nat\",\"tan\"],[\"ate\",\"eat\",\"tea\"]]\n\n"
            "Escribe `solve(strs)` que devuelva la agrupación."
        ),
        "test_cases": [
            {"input": '["eat","tea","tan","ate","nat","bat"]', "expected_output": '[["eat","tea","ate"],["tan","nat"],["bat"]]'},
            {"input": '[""]', "expected_output": '[[""]]'},
            {"input": '["a"]', "expected_output": '[["a"]]'},
        ],
        "stub": {
            "Python": "def solve(strs):\n    pass",
            "C++":    "#include <vector>\n#include <string>\nusing namespace std;\nvector<vector<string>> solve(vector<string> strs) {\n    return {};\n}",
            "Java":   "public static String[][] solve(String[] strs) {\n    return new String[][]{};\n}",
            "Go":     "func solve(strs []string) [][]string {\n    return nil\n}",
            "C#":     "public static string[][] Solve(string[] strs) {\n    return new string[][]{};\n}",
        },
    },
    {
        "title": "Número Faltante",
        "difficulty": "Normal", "category": "Arrays", "total_solvers": 0,
        "description": (
            "Dado un array nums que contiene n números distintos en el rango [0, n], "
            "devuelve el único número en el rango que falta en el array.\n\n"
            "Intenta resolverlo en completo O(1) de espacio adicional y tiempo O(n).\n\n"
            "Restricciones:\n"
            "  n = len(nums)\n"
            "  1 ≤ n ≤ 10^4\n\n"
            "Ejemplo 1:\n"
            "  Entrada: nums=[3,0,1]\n"
            "  Salida: 2\n\n"
            "Escribe `solve(nums)` que devuelva el número faltante."
        ),
        "test_cases": [
            {"input": "[3,0,1]", "expected_output": "2"},
            {"input": "[0,1]", "expected_output": "2"},
            {"input": "[9,6,4,2,3,5,7,0,1]", "expected_output": "8"},
        ],
        "stub": {
            "Python": "def solve(nums):\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nint solve(vector<int> nums) {\n    return 0;\n}",
            "Java":   "public static int solve(int[] nums) {\n    return 0;\n}",
            "Go":     "func solve(nums []int) int {\n    return 0\n}",
            "C#":     "public static int Solve(int[] nums) {\n    return 0;\n}",
        },
    },
    {
        "title": "Generar Permutaciones",
        "difficulty": "Normal", "category": "Arrays", "total_solvers": 0,
        "description": (
            "Dado un array nums de enteros distintos, devuelve todas las posibles permutaciones. "
            "Puedes devolver la respuesta en cualquier orden.\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 6\n\n"
            "Ejemplo 1:\n"
            "  Entrada: nums=[1,2,3]\n"
            "  Salida: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]\n\n"
            "Escribe `solve(nums)` que devuelva la lista de permutaciones."
        ),
        "test_cases": [
            {"input": "[1,2,3]", "expected_output": "[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]"},
            {"input": "[0,1]", "expected_output": "[[0,1],[1,0]]"},
        ],
        "stub": {
            "Python": "def solve(nums):\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nvector<vector<int>> solve(vector<int> nums) {\n    return {};\n}",
            "Java":   "public static int[][] solve(int[] nums) {\n    return new int[][]{};\n}",
            "Go":     "func solve(nums []int) [][]int {\n    return nil\n}",
            "C#":     "public static int[][] Solve(int[] nums) {\n    return new int[][]{};\n}",
        },
    },
    {
        "title": "Buscar en Matriz 2D",
        "difficulty": "Normal", "category": "Arrays", "total_solvers": 0,
        "description": (
            "Dada una matriz m x n en la que cada fila está ordenada de izquierda a derecha "
            "y el primer entero de cada fila es mayor que el último entero de la fila anterior, "
            "determina si el valor target existe.\n\n"
            "Restricciones:\n"
            "  1 ≤ m, n ≤ 100\n\n"
            "Ejemplo 1:\n"
            "  Entrada: matriz=[[1,3,5,7],[10,11,16,20],[23,30,34,60]], target=3\n"
            "  Salida: True\n\n"
            "Escribe `solve(matriz, target)` que devuelva True o False."
        ),
        "test_cases": [
            {"input": "[[1,3,5,7],[10,11,16,20],[23,30,34,60]], 3", "expected_output": "True"},
            {"input": "[[1,3,5,7],[10,11,16,20],[23,30,34,60]], 13", "expected_output": "False"},
        ],
        "stub": {
            "Python": "def solve(matriz, target):\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nbool solve(vector<vector<int>> matriz, int target) {\n    return false;\n}",
            "Java":   "public static boolean solve(int[][] matriz, int target) {\n    return false;\n}",
            "Go":     "func solve(matriz [][]int, target int) bool {\n    return false\n}",
            "C#":     "public static bool Solve(int[][] matriz, int target) {\n    return false;\n}",
        },
    },
    {
        "title": "Tres Suma",
        "difficulty": "Normal", "category": "Arrays", "total_solvers": 0,
        "description": (
            "Dado un array de enteros nums, devuelve todos los tripletes "
            "[nums[i], nums[j], nums[k]] tales que i != j, i != k, y j != k, "
            "y nums[i] + nums[j] + nums[k] == 0.\n\n"
            "Puedes devolver las tuplas en cualquier orden, pero no debe haber tripletes duplicados.\n\n"
            "Restricciones:\n"
            "  3 ≤ n ≤ 3000\n\n"
            "Ejemplo 1:\n"
            "  Entrada: nums=[-1,0,1,2,-1,-4]\n"
            "  Salida: [[-1,-1,2],[-1,0,1]]\n\n"
            "Escribe `solve(nums)` que devuelva la lista de tripletes."
        ),
        "test_cases": [
            {"input": "[-1,0,1,2,-1,-4]", "expected_output": "[[-1,-1,2],[-1,0,1]]"},
            {"input": "[0,1,1]", "expected_output": "[]"},
            {"input": "[0,0,0]", "expected_output": "[[0,0,0]]"},
        ],
        "stub": {
            "Python": "def solve(nums):\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nvector<vector<int>> solve(vector<int> nums) {\n    return {};\n}",
            "Java":   "public static int[][] solve(int[] nums) {\n    return new int[][]{};\n}",
            "Go":     "func solve(nums []int) [][]int {\n    return nil\n}",
            "C#":     "public static int[][] Solve(int[] nums) {\n    return new int[][]{};\n}",
        },
    },
    {
        "title": "Palíndromo más Largo",
        "difficulty": "Normal", "category": "Strings", "total_solvers": 0,
        "description": (
            "Dada una cadena s, devuelve el substring palindrómico más largo en s.\n\n"
            "Restricciones:\n"
            "  1 ≤ |s| ≤ 1000\n\n"
            "Ejemplo 1:\n"
            "  Entrada: s=\"babad\"\n"
            "  Salida: \"bab\" (o \"aba\")\n\n"
            "Escribe `solve(s)` que devuelva la cadena palindrómica más larga."
        ),
        "test_cases": [
            {"input": '"babad"', "expected_output": '"bab"'},
            {"input": '"cbbd"', "expected_output": '"bb"'},
        ],
        "stub": {
            "Python": "def solve(s):\n    pass",
            "C++":    "#include <string>\nusing namespace std;\nstring solve(string s) {\n    return \"\";\n}",
            "Java":   "public static String solve(String s) {\n    return \"\";\n}",
            "Go":     "func solve(s string) string {\n    return \"\"\n}",
            "C#":     "public static string Solve(string s) {\n    return \"\";\n}",
        },
    },
    {
        "title": "Letras de de Teléfono",
        "difficulty": "Normal", "category": "Strings", "total_solvers": 0,
        "description": (
            "Dada una cadena con dígitos del 2 al 9, devuelve todas las posibles combinaciones "
            "de letras que el número podría representar (como en un teclado telefónico).\n\n"
            "Restricciones:\n"
            "  0 ≤ |digits| ≤ 4\n\n"
            "Ejemplo 1:\n"
            "  Entrada: digits=\"23\"\n"
            "  Salida: [\"ad\",\"ae\",\"af\",\"bd\",\"be\",\"bf\",\"cd\",\"ce\",\"cf\"]\n\n"
            "Escribe `solve(digits)` que devuelva la lista de strings."
        ),
        "test_cases": [
            {"input": '"23"', "expected_output": '["ad","ae","af","bd","be","bf","cd","ce","cf"]'},
            {"input": '""', "expected_output": "[]"},
            {"input": '"2"', "expected_output": '["a","b","c"]'},
        ],
        "stub": {
            "Python": "def solve(digits):\n    pass",
            "C++":    "#include <vector>\n#include <string>\nusing namespace std;\nvector<string> solve(string digits) {\n    return {};\n}",
            "Java":   "public static String[] solve(String digits) {\n    return new String[]{};\n}",
            "Go":     "func solve(digits string) []string {\n    return nil\n}",
            "C#":     "public static string[] Solve(string digits) {\n    return new string[]{};\n}",
        },
    },
    {
        "title": "N Reinas",
        "difficulty": "Difícil", "category": "Arrays", "total_solvers": 0,
        "description": (
            "El problema de las n-reinas consiste en colocar n reinas en un tablero de ajedrez n x n "
            "de forma que no haya dos reinas que se amenacen mutuamente.\n\n"
            "Dada una variable entera n, devuelve todas las soluciones distintas. Cada solución "
            "contiene un tablero con 'Q' representando una reina y '.' representando un espacio vacío.\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 9\n\n"
            "Ejemplo 1:\n"
            "  Entrada: n=4\n"
            "  Salida: [[\".Q..\",\"...Q\",\"Q...\",\"..Q.\"],[\"..Q.\",\"Q...\",\"...Q\",\".Q..\"]]\n\n"
            "Escribe `solve(n)` que devuelva la lista de tableros."
        ),
        "test_cases": [
            {"input": "4", "expected_output": '[["\\.Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q","\\.Q.."]]'},
            {"input": "1", "expected_output": '[["Q"]]'},
        ],
        "stub": {
            "Python": "def solve(n):\n    pass",
            "C++":    "#include <vector>\n#include <string>\nusing namespace std;\nvector<vector<string>> solve(int n) {\n    return {};\n}",
            "Java":   "public static String[][] solve(int n) {\n    return new String[][]{};\n}",
            "Go":     "func solve(n int) [][]string {\n    return nil\n}",
            "C#":     "public static string[][] Solve(int n) {\n    return new string[][]{};\n}",
        },
    },
    {
        "title": "Unir K Arrays Ordenados",
        "difficulty": "Difícil", "category": "Arrays", "total_solvers": 0,
        "description": (
            "Se te da un array k arrays de enteros, donde cada array está ordenado ascendentemente.\n\n"
            "Únelos todos en un solo array ordenado y devuélvelo. Este algoritmo debe correr "
            "en O(N log k) usando una cola de prioridad.\n\n"
            "Restricciones:\n"
            "  0 ≤ k ≤ 10^4\n"
            "  0 ≤ arrays[i].length ≤ 500\n\n"
            "Ejemplo 1:\n"
            "  Entrada: arrays=[[1,4,5],[1,3,4],[2,6]]\n"
            "  Salida: [1,1,2,3,4,4,5,6]\n\n"
            "Escribe `solve(arrays)` que devuelva el array fusionado."
        ),
        "test_cases": [
            {"input": "[[1,4,5],[1,3,4],[2,6]]", "expected_output": "[1,1,2,3,4,4,5,6]"},
            {"input": "[]", "expected_output": "[]"},
            {"input": "[[]]", "expected_output": "[]"},
        ],
        "stub": {
            "Python": "def solve(arrays):\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nvector<int> solve(vector<vector<int>> arrays) {\n    return {};\n}",
            "Java":   "public static int[] solve(int[][] arrays) {\n    return new int[]{};\n}",
            "Go":     "func solve(arrays [][]int) []int {\n    return nil\n}",
            "C#":     "public static int[] Solve(int[][] arrays) {\n    return new int[]{};\n}",
        },
    },
    {
        "title": "Resolver Sudoku",
        "difficulty": "Difícil", "category": "Matemáticas", "total_solvers": 0,
        "description": (
            "Escribe un programa para resolver un rompecabezas Sudoku completando las celdas vacías.\n\n"
            "El tablero es de 9x9. Los espacios vacíos están indicados con el espacio en blanco o '.'\n\n"
            "Debes modificar la matriz in-place o devolver el sudoku resuelto.\n\n"
            "Restricciones:\n"
            "  El tablero siempre tendrá exactamente una solución válida.\n\n"
            "Escribe `solve(board)` que devuelva el board."
        ),
        "test_cases": [
            {"input": '[["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]', "expected_output": '[["5","3","4","6","7","8","9","1","2"],["6","7","2","1","9","5","3","4","8"],["1","9","8","3","4","2","5","6","7"],["8","5","9","7","6","1","4","2","3"],["4","2","6","8","5","3","7","9","1"],["7","1","3","9","2","4","8","5","6"],["9","6","1","5","3","7","2","8","4"],["2","8","7","4","1","9","6","3","5"],["3","4","5","2","8","6","1","7","9"]]'},
        ],
        "stub": {
            "Python": "def solve(board):\n    pass",
            "C++":    "#include <vector>\n#include <string>\nusing namespace std;\nvector<vector<string>> solve(vector<vector<string>> board) {\n    return {};\n}",
            "Java":   "public static String[][] solve(String[][] board) {\n    return new String[][]{};\n}",
            "Go":     "func solve(board [][]string) [][]string {\n    return nil\n}",
            "C#":     "public static string[][] Solve(string[][] board) {\n    return new string[][]{};\n}",
        },
    },
    {
        "title": "Paréntesis Válidos más Largos",
        "difficulty": "Difícil", "category": "Strings", "total_solvers": 0,
        "description": (
            "Dada una cadena que contiene solo los caracteres '(' y ')', encuentra la longitud de "
            "la subcadena contigua más larga que contiene paréntesis bien formados.\n\n"
            "Restricciones:\n"
            "  0 ≤ |s| ≤ 3 * 10^4\n\n"
            "Ejemplo 1:\n"
            "  Entrada: s=\")()())\"\n"
            "  Salida: 4\n\n"
            "Escribe `solve(s)` que devuelva la longitud."
        ),
        "test_cases": [
            {"input": '")()())"', "expected_output": "4"},
            {"input": '"(()"', "expected_output": "2"},
            {"input": '""', "expected_output": "0"},
        ],
        "stub": {
            "Python": "def solve(s):\n    pass",
            "C++":    "#include <string>\nusing namespace std;\nint solve(string s) {\n    return 0;\n}",
            "Java":   "public static int solve(String s) {\n    return 0;\n}",
            "Go":     "func solve(s string) int {\n    return 0\n}",
            "C#":     "public static int Solve(string s) {\n    return 0;\n}",
        },
    },
    {
        "title": "Rectángulo Histograma",
        "difficulty": "Difícil", "category": "Arrays", "total_solvers": 0,
        "description": (
            "Dado un array de enteros heights que representa la altura de las barras de un "
            "histograma donde el ancho de cada barra es 1, devuelve el área del rectángulo más "
            "grande en el histograma.\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 10^5\n"
            "  0 ≤ heights[i] ≤ 10^4\n\n"
            "Ejemplo 1:\n"
            "  Entrada: heights=[2,1,5,6,2,3]\n"
            "  Salida: 10\n\n"
            "Escribe `solve(heights)` que devuelva el área máxima."
        ),
        "test_cases": [
            {"input": "[2,1,5,6,2,3]", "expected_output": "10"},
            {"input": "[2,4]", "expected_output": "4"},
            {"input": "[5,4,4,6,3,2,9,5,2,6]", "expected_output": "20"},
        ],
        "stub": {
            "Python": "def solve(heights):\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nint solve(vector<int> heights) {\n    return 0;\n}",
            "Java":   "public static int solve(int[] heights) {\n    return 0;\n}",
            "Go":     "func solve(heights []int) int {\n    return 0\n}",
            "C#":     "public static int Solve(int[] heights) {\n    return 0;\n}",
        },
    },
    {
        "title": "Mediana de Dos Arrays",
        "difficulty": "Difícil", "category": "Arrays", "total_solvers": 0,
        "description": (
            "Dados dos arrays ordenados nums1 y nums2 de tamaño m y n respectivamente, "
            "devuelve la mediana de los dos arrays ordenados.\n\n"
            "La complejidad de tiempo global debe ser O(log(m+n)).\n\n"
            "Restricciones:\n"
            "  0 ≤ m, n ≤ 1000\n"
            "  1 ≤ m + n ≤ 2000\n\n"
            "Ejemplo 1:\n"
            "  Entrada: nums1=[1,3], nums2=[2]\n"
            "  Salida: 2.0\n\n"
            "Ejemplo 2:\n"
            "  Entrada: nums1=[1,2], nums2=[3,4]\n"
            "  Salida: 2.5\n\n"
            "Escribe `solve(nums1, nums2)` que devuelva un float o double."
        ),
        "test_cases": [
            {"input": "[1,3], [2]", "expected_output": "2.0"},
            {"input": "[1,2], [3,4]", "expected_output": "2.5"},
        ],
        "stub": {
            "Python": "def solve(nums1, nums2):\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\ndouble solve(vector<int> nums1, vector<int> nums2) {\n    return 0.0;\n}",
            "Java":   "public static double solve(int[] nums1, int[] nums2) {\n    return 0.0;\n}",
            "Go":     "func solve(nums1 []int, nums2 []int) float64 {\n    return 0.0\n}",
            "C#":     "public static double Solve(int[] nums1, int[] nums2) {\n    return 0.0;\n}",
        },
    },
    {
        "title": "Expresión Regular",
        "difficulty": "Difícil", "category": "Strings", "total_solvers": 0,
        "description": (
            "Dada una cadena de texto s y un patrón p, implementa el soporte de expresiones "
            "regulares con '.' (cualquier carácter individual) y '*' (cero o más del carácter anterior).\n\n"
            "La coincidencia debe cubrir toda la cadena s (no parcial).\n\n"
            "Restricciones:\n"
            "  1 ≤ |s|, |p| ≤ 20\n\n"
            "Ejemplo 1:\n"
            "  Entrada: s=\"aa\", p=\"a*\"\n"
            "  Salida: True\n\n"
            "Ejemplo 2:\n"
            "  Entrada: s=\"ab\", p=\".*\"\n"
            "  Salida: True\n\n"
            "Escribe `solve(s, p)` que devuelva True o False."
        ),
        "test_cases": [
            {"input": '"aa", "a*"', "expected_output": "True"},
            {"input": '"ab", ".*"', "expected_output": "True"},
            {"input": '"mississippi", "mis*is*p*."', "expected_output": "False"},
        ],
        "stub": {
            "Python": "def solve(s, p):\n    pass",
            "C++":    "#include <string>\nusing namespace std;\nbool solve(string s, string p) {\n    return false;\n}",
            "Java":   "public static boolean solve(String s, String p) {\n    return false;\n}",
            "Go":     "func solve(s string, p string) bool {\n    return false\n}",
            "C#":     "public static bool Solve(string s, string p) {\n    return false;\n}",
        },
    },
    {
        "title": "Máximo Rectángulo",
        "difficulty": "Difícil", "category": "Arrays", "total_solvers": 0,
        "description": (
            "Dada una matriz binaria de 2 dimensiones, llena de los caracteres '0' y '1', "
            "encuentra el rectángulo más grande conformado únicamente por unos y devuelve su área.\n\n"
            "Restricciones:\n"
            "  1 ≤ filas, columnas ≤ 200\n\n"
            "Ejemplo 1:\n"
            "  Entrada: matriz=[[\"1\",\"0\",\"1\",\"0\",\"0\"],[\"1\",\"0\",\"1\",\"1\",\"1\"],[\"1\",\"1\",\"1\",\"1\",\"1\"],[\"1\",\"0\",\"0\",\"1\",\"0\"]]\n"
            "  Salida: 6\n\n"
            "Escribe `solve(matriz)` que devuelva el área (entero)."
        ),
        "test_cases": [
            {"input": '[["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]', "expected_output": "6"},
            {"input": '[["0"]]', "expected_output": "0"},
            {"input": '[["1"]]', "expected_output": "1"},
        ],
        "stub": {
            "Python": "def solve(matriz):\n    pass",
            "C++":    "#include <vector>\n#include <string>\nusing namespace std;\nint solve(vector<vector<string>> matriz) {\n    return 0;\n}",
            "Java":   "public static int solve(String[][] matriz) {\n    return 0;\n}",
            "Go":     "func solve(matriz [][]string) int {\n    return 0\n}",
            "C#":     "public static int Solve(string[][] matriz) {\n    return 0;\n}",
        },
    },
    {
        "title": "Buscar Palabra II",
        "difficulty": "Difícil", "category": "Strings", "total_solvers": 0,
        "description": (
            "Dada una matriz de caracteres board y una lista de cadenas words, devuelve todas las "
            "palabras en el board. Cada palabra debe ser construida al pasar de una celda a otra adyacente.\n\n"
            "Restricciones:\n"
            "  1 ≤ m, n ≤ 12\n"
            "  1 ≤ |words| ≤ 3 * 10^4\n\n"
            "Ejemplo 1:\n"
            "  Entrada: board=[[\"o\",\"a\",\"a\",\"n\"],[\"e\",\"t\",\"a\",\"e\"],[\"i\",\"h\",\"k\",\"r\"],[\"i\",\"f\",\"l\",\"v\"]], words=[\"oath\",\"pea\",\"eat\",\"rain\"]\n"
            "  Salida: [\"eat\",\"oath\"]\n\n"
            "Escribe `solve(board, words)` que devuelva la lista de palabras."
        ),
        "test_cases": [
            {"input": '[["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]], ["oath","pea","eat","rain"]', "expected_output": '["eat","oath"]'},
            {"input": '[["a","b"],["c","d"]], ["abcb"]', "expected_output": '[]'},
        ],
        "stub": {
            "Python": "def solve(board, words):\n    pass",
            "C++":    "#include <vector>\n#include <string>\nusing namespace std;\nvector<string> solve(vector<vector<string>> board, vector<string> words) {\n    return {};\n}",
            "Java":   "public static String[] solve(String[][] board, String[] words) {\n    return new String[]{};\n}",
            "Go":     "func solve(board [][]string, words []string) []string {\n    return nil\n}",
            "C#":     "public static string[] Solve(string[][] board, string[] words) {\n    return new string[]{};\n}",
        },
    },
    {
        "title": "Inserciones para Palíndromo",
        "difficulty": "Difícil", "category": "Strings", "total_solvers": 0,
        "description": (
            "Dada una cadena s, inserta los caracteres mínimos requeridos para convertir la cadena en un palíndromo.\n\n"
            "Devuelve el número mínimo de caracteres que deben insertarse.\n\n"
            "Restricciones:\n"
            "  1 ≤ |s| ≤ 500\n\n"
            "Ejemplo 1:\n"
            "  Entrada: s=\"zzazz\"\n"
            "  Salida: 0\n\n"
            "Ejemplo 2:\n"
            "  Entrada: s=\"mbadm\"\n"
            "  Salida: 2\n"
            "  Explicación: Puedes convertirla a \"mbdadbm\" ó \"mdbabdm\".\n\n"
            "Escribe `solve(s)` que devuelva el mínimo."
        ),
        "test_cases": [
            {"input": '"zzazz"', "expected_output": "0"},
            {"input": '"mbadm"', "expected_output": "2"},
            {"input": '"leetcode"', "expected_output": "5"},
        ],
        "stub": {
            "Python": "def solve(s):\n    pass",
            "C++":    "#include <string>\nusing namespace std;\nint solve(string s) {\n    return 0;\n}",
            "Java":   "public static int solve(String s) {\n    return 0;\n}",
            "Go":     "func solve(s string) int {\n    return 0\n}",
            "C#":     "public static int Solve(string s) {\n    return 0;\n}",
        },
    }
]
