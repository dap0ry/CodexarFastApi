# API/app/exercises_data.py
# Competitive-programming style exercises — drop the `exercises` collection before re-seeding.

EXERCISES_SEED = [

    # ══════════════════════════════════════════
    #  MATEMÁTICAS — FÁCIL
    # ══════════════════════════════════════════
    {
        "title": "Máximo Común Divisor",
        "difficulty": 800, "category": "Matemáticas", "total_solvers": 0,
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
        "difficulty": 800, "category": "Matemáticas", "total_solvers": 0,
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
        "difficulty": 800, "category": "Matemáticas", "total_solvers": 0,
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
        "difficulty": 800, "category": "Arrays", "total_solvers": 0,
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
        "difficulty": 800, "category": "Arrays", "total_solvers": 0,
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
        "difficulty": 800, "category": "Strings", "total_solvers": 0,
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
        "difficulty": 800, "category": "Strings", "total_solvers": 0,
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
        "difficulty": 800, "category": "Matemáticas", "total_solvers": 0,
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
        "difficulty": 1200, "category": "Matemáticas", "total_solvers": 0,
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
        "difficulty": 1200, "category": "Matemáticas", "total_solvers": 0,
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
        "difficulty": 1200, "category": "Arrays", "total_solvers": 0,
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
        "difficulty": 1200, "category": "Arrays", "total_solvers": 0,
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
        "difficulty": 1200, "category": "Arrays", "total_solvers": 0,
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
        "difficulty": 1200, "category": "Arrays", "total_solvers": 0,
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
        "difficulty": 1200, "category": "Strings", "total_solvers": 0,
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
        "difficulty": 1200, "category": "Matemáticas", "total_solvers": 0,
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
        "difficulty": 1600, "category": "Arrays", "total_solvers": 0,
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
        "difficulty": 1600, "category": "Strings", "total_solvers": 0,
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
        "difficulty": 1600, "category": "Strings", "total_solvers": 0,
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
        "difficulty": 1600, "category": "Arrays", "total_solvers": 0,
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
        "difficulty": 1600, "category": "Matemáticas", "total_solvers": 0,
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
        "difficulty": 1600, "category": "Arrays", "total_solvers": 0,
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
        "difficulty": 1600, "category": "Matemáticas", "total_solvers": 0,
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
        "difficulty": 800, "category": "Strings", "total_solvers": 0,
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
            {"input": '"hola"', "expected_output": "aloh"},
            {"input": '"openai"', "expected_output": "ianepo"},
            {"input": '"a"', "expected_output": "a"},
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
        "difficulty": 800, "category": "Matemáticas", "total_solvers": 0,
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
            {"input": "4", "expected_output": "Par"},
            {"input": "7", "expected_output": "Impar"},
            {"input": "0", "expected_output": "Par"},
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
        "difficulty": 800, "category": "Arrays", "total_solvers": 0,
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
        "difficulty": 800, "category": "Arrays", "total_solvers": 0,
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
        "difficulty": 800, "category": "Matemáticas", "total_solvers": 0,
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
        "difficulty": 1200, "category": "Strings", "total_solvers": 0,
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
        "difficulty": 1200, "category": "Arrays", "total_solvers": 0,
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
        "difficulty": 1200, "category": "Arrays", "total_solvers": 0,
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
        "difficulty": 1200, "category": "Strings", "total_solvers": 0,
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
        "difficulty": 1200, "category": "Arrays", "total_solvers": 0,
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
        "difficulty": 1200, "category": "Arrays", "total_solvers": 0,
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
        "difficulty": 1200, "category": "Arrays", "total_solvers": 0,
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
        "difficulty": 1200, "category": "Arrays", "total_solvers": 0,
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
        "difficulty": 1200, "category": "Strings", "total_solvers": 0,
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
        "difficulty": 1200, "category": "Strings", "total_solvers": 0,
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
        "difficulty": 1600, "category": "Arrays", "total_solvers": 0,
        "description": (
            "El problema de las n-reinas consiste en colocar n reinas en un tablero de ajedrez n x n "
            "de forma que no haya dos reinas que se amenacen mutuamente (ni en la misma fila, columna "
            "ni diagonal).\n\n"
            "Dada una variable entera n, devuelve el número total de soluciones distintas.\n\n"
            "El enfoque clásico es backtracking: coloca una reina en cada fila, explorando únicamente "
            "las columnas que no están atacadas. Usa tres conjuntos (columnas, diagonales /, diagonales \\\\) "
            "para comprobar ataques en O(1).\n\n"
            "Valores conocidos: C(1)=1, C(2)=0, C(3)=0, C(4)=2, C(5)=10, C(6)=4, C(7)=40, C(8)=92.\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 9\n\n"
            "Ejemplo 1:\n"
            "  Entrada: n=4\n"
            "  Salida: 2\n"
            "  Explicación: Existen exactamente 2 formas de colocar 4 reinas en un tablero 4x4.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: n=8\n"
            "  Salida: 92\n\n"
            "Escribe `solve(n)` que devuelva el número de soluciones."
        ),
        "test_cases": [
            {"input": "4", "expected_output": "2"},
            {"input": "1", "expected_output": "1"},
            {"input": "8", "expected_output": "92"},
        ],
        "stub": {
            "Python": "def solve(n):\n    # Backtracking: coloca una reina por fila\n    pass",
            "C++":    "int solve(int n) {\n    // Backtracking con conjuntos de columnas y diagonales\n    return 0;\n}",
            "Java":   "public static int solve(int n) {\n    // Backtracking con conjuntos de columnas y diagonales\n    return 0;\n}",
            "Go":     "func solve(n int) int {\n    // Backtracking con conjuntos de columnas y diagonales\n    return 0\n}",
            "C#":     "public static int Solve(int n) {\n    // Backtracking con conjuntos de columnas y diagonales\n    return 0;\n}",
        },
    },
    {
        "title": "Unir K Arrays Ordenados",
        "difficulty": 1600, "category": "Arrays", "total_solvers": 0,
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
            {"input": "[[1],[2],[3]]",            "expected_output": "[1,2,3]"},
            {"input": "[[5,10],[1,3,8]]",         "expected_output": "[1,3,5,8,10]"},
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
        "difficulty": 1600, "category": "Matemáticas", "total_solvers": 0,
        "description": (
            "Escribe un programa para resolver un rompecabezas Sudoku completando las celdas vacías.\n\n"
            "El tablero es de 9x9 representado como lista de listas de strings. "
            "Los espacios vacíos están indicados con '.'.\n\n"
            "El tablero siempre tendrá exactamente una solución válida.\n\n"
            "Devuelve el tablero resuelto como una cadena de 81 caracteres, concatenando las filas "
            "de arriba a abajo y las columnas de izquierda a derecha (sin separadores).\n\n"
            "Ejemplo:\n"
            "  Entrada: board=[[\"5\",\"3\",\".\",\".\",\"7\",\".\",\".\",\".\",\".\"],...]\n"
            "  Salida: \"534678912672195348198342567859761423426853791713924856961537284287419635345286179\"\n\n"
            "Sugerencia: usa backtracking — prueba cada dígito del 1 al 9 en cada celda vacía y "
            "verifica que no viole las reglas de fila, columna y caja 3x3.\n\n"
            "Escribe `solve(board)` que devuelva la cadena de 81 caracteres con la solución."
        ),
        "test_cases": [
            {"input": '[["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]', "expected_output": "534678912672195348198342567859761423426853791713924856961537284287419635345286179"},
        ],
        "stub": {
            "Python": "def solve(board):\n    # Backtracking: rellena celdas '.' con dígitos 1-9\n    # Devuelve ''.join(''.join(row) for row in board) al terminar\n    pass",
            "C++":    '#include <vector>\n#include <string>\nusing namespace std;\nstring solve(vector<vector<string>> board) {\n    // Backtracking: rellena celdas "." con digitos 1-9\n    // Devuelve la concatenacion de todas las celdas fila por fila\n    return "";\n}',
            "Java":   'public static String solve(String[][] board) {\n    // Backtracking: rellena celdas "." con digitos 1-9\n    // Devuelve la concatenacion de todas las celdas fila por fila\n    return "";\n}',
            "Go":     'func solve(board [][]string) string {\n    // Backtracking: rellena celdas "." con digitos 1-9\n    // Devuelve la concatenacion de todas las celdas fila por fila\n    return ""\n}',
            "C#":     'public static string Solve(string[][] board) {\n    // Backtracking: rellena celdas "." con digitos 1-9\n    // Devuelve la concatenacion de todas las celdas fila por fila\n    return "";\n}',
        },
    },
    {
        "title": "Paréntesis Válidos más Largos",
        "difficulty": 1600, "category": "Strings", "total_solvers": 0,
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
        "difficulty": 1600, "category": "Arrays", "total_solvers": 0,
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
        "difficulty": 1600, "category": "Arrays", "total_solvers": 0,
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
        "difficulty": 1600, "category": "Strings", "total_solvers": 0,
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
        "difficulty": 1600, "category": "Arrays", "total_solvers": 0,
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
        "difficulty": 1600, "category": "Strings", "total_solvers": 0,
        "description": (
            "Dada una matriz de caracteres board y una lista de cadenas words, devuelve cuántas "
            "palabras de la lista pueden encontrarse en el board.\n\n"
            "Una palabra puede construirse moviéndose de una celda a una celda adyacente "
            "(arriba, abajo, izquierda, derecha). No se puede reutilizar la misma celda en una "
            "misma palabra.\n\n"
            "La solución óptima usa un Trie para indexar las palabras y DFS/backtracking sobre "
            "el board. Esto evita buscar cada palabra de forma independiente.\n\n"
            "Restricciones:\n"
            "  1 ≤ m, n ≤ 12\n"
            "  1 ≤ |words| ≤ 3 × 10^4\n\n"
            "Ejemplo 1:\n"
            "  Entrada: board=[[\"o\",\"a\",\"a\",\"n\"],[\"e\",\"t\",\"a\",\"e\"],[\"i\",\"h\",\"k\",\"r\"],[\"i\",\"f\",\"l\",\"v\"]], "
            "words=[\"oath\",\"pea\",\"eat\",\"rain\"]\n"
            "  Salida: 2\n"
            "  Explicación: Se encuentran \"eat\" y \"oath\" → 2 palabras.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: board=[[\"a\",\"b\"],[\"c\",\"d\"]], words=[\"abcb\"]\n"
            "  Salida: 0\n"
            "  Explicación: \"abcb\" requeriría reutilizar 'b', no es válido.\n\n"
            "Escribe `solve(board, words)` que devuelva el número de palabras encontradas."
        ),
        "test_cases": [
            {"input": '[["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]], ["oath","pea","eat","rain"]', "expected_output": "2"},
            {"input": '[["a","b"],["c","d"]], ["abcb"]', "expected_output": "0"},
            {"input": '[["a","b"],["c","d"]], ["ab","cd","ac","abc"]', "expected_output": "3"},
        ],
        "stub": {
            "Python": "def solve(board, words):\n    # Trie + DFS backtracking\n    pass",
            "C++":    "#include <vector>\n#include <string>\n#include <unordered_set>\nusing namespace std;\nint solve(vector<vector<string>> board, vector<string> words) {\n    // Trie + DFS backtracking\n    return 0;\n}",
            "Java":   "public static int solve(String[][] board, String[] words) {\n    // Trie + DFS backtracking\n    return 0;\n}",
            "Go":     "func solve(board [][]string, words []string) int {\n    // Trie + DFS backtracking\n    return 0\n}",
            "C#":     "public static int Solve(string[][] board, string[] words) {\n    // Trie + DFS backtracking\n    return 0;\n}",
        },
    },
    {
        "title": "Inserciones para Palíndromo",
        "difficulty": 1600, "category": "Strings", "total_solvers": 0,
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
    },

    # ══════════════════════════════════════════
    #  MATEMÁTICAS — FÁCIL
    # ══════════════════════════════════════════
    {
        "title": "Secuencia de Collatz",
        "difficulty": 800, "category": "Matemáticas", "total_solvers": 0,
        "description": (
            "La conjetura de Collatz, también conocida como el problema 3n+1, es uno de los problemas "
            "abiertos más famosos en matemáticas. Fue propuesta por Lothar Collatz en 1937 y a día de hoy "
            "nadie ha podido demostrarla formalmente, aunque ha sido verificada computacionalmente para "
            "todos los enteros hasta 2^68.\n\n"
            "La regla es simple: dado un entero positivo n, aplica la siguiente transformación de forma "
            "repetida hasta llegar a 1:\n"
            "  • Si n es par → n = n / 2\n"
            "  • Si n es impar → n = 3 × n + 1\n\n"
            "La conjetura afirma que, independientemente del valor inicial, siempre se llega a 1.\n\n"
            "Tu tarea es calcular cuántos pasos son necesarios para reducir n a 1. "
            "Cada aplicación de una de las dos reglas cuenta como un paso.\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 10^6\n\n"
            "Ejemplo 1:\n"
            "  Entrada: n=6\n"
            "  Salida: 8\n"
            "  Explicación: 6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1 (8 pasos)\n\n"
            "Ejemplo 2:\n"
            "  Entrada: n=1\n"
            "  Salida: 0\n"
            "  Explicación: Ya estamos en 1, no hace falta ningún paso.\n\n"
            "Ejemplo 3:\n"
            "  Entrada: n=27\n"
            "  Salida: 111\n"
            "  Explicación: La secuencia asciende hasta 9232 antes de converger.\n\n"
            "Escribe `solve(n)` que devuelva el número de pasos hasta alcanzar 1."
        ),
        "test_cases": [
            {"input": "6",  "expected_output": "8"},
            {"input": "1",  "expected_output": "0"},
            {"input": "27", "expected_output": "111"},
        ],
        "stub": {
            "Python": "def solve(n):\n    # Aplica las reglas de Collatz hasta llegar a 1\n    pass",
            "C++":    "int solve(int n) {\n    // Aplica las reglas de Collatz hasta llegar a 1\n    return 0;\n}",
            "Java":   "public static int solve(int n) {\n    // Aplica las reglas de Collatz hasta llegar a 1\n    return 0;\n}",
            "Go":     "func solve(n int) int {\n    // Aplica las reglas de Collatz hasta llegar a 1\n    return 0\n}",
            "C#":     "public static int Solve(int n) {\n    // Aplica las reglas de Collatz hasta llegar a 1\n    return 0;\n}",
        },
    },

    # ══════════════════════════════════════════
    #  STRINGS — NORMAL
    # ══════════════════════════════════════════
    {
        "title": "Subsecuencia Común Más Larga",
        "difficulty": 1200, "category": "Strings", "total_solvers": 0,
        "description": (
            "La Subsecuencia Común Más Larga (LCS, del inglés Longest Common Subsequence) es uno de "
            "los problemas fundacionales de la programación dinámica y tiene aplicaciones directas en "
            "bioinformática (comparación de secuencias de ADN), control de versiones (diff de archivos) "
            "y compresión de datos.\n\n"
            "Una subsecuencia es un subconjunto de caracteres de una cadena que mantiene el orden "
            "relativo original, pero no necesariamente ocupa posiciones contiguas. Por ejemplo, "
            "\"ace\" es una subsecuencia de \"abcde\".\n\n"
            "La LCS de dos cadenas s1 y s2 es la subsecuencia más larga que aparece en ambas. "
            "No confundas con el substring más largo común, que sí exige contigüidad.\n\n"
            "Recurrencia:\n"
            "  dp[i][j] = longitud de la LCS de s1[0..i-1] y s2[0..j-1]\n"
            "  Si s1[i-1] == s2[j-1]: dp[i][j] = dp[i-1][j-1] + 1\n"
            "  Si no:                  dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n"
            "  Base:                   dp[0][j] = dp[i][0] = 0\n\n"
            "La complejidad es O(|s1| × |s2|) en tiempo y espacio, o O(min(|s1|,|s2|)) en espacio "
            "con la optimización de rolling array.\n\n"
            "Restricciones:\n"
            "  1 ≤ |s1|, |s2| ≤ 1000\n"
            "  Solo letras minúsculas del alfabeto inglés\n\n"
            "Ejemplo 1:\n"
            "  Entrada: s1=\"abcde\", s2=\"ace\"\n"
            "  Salida: 3\n"
            "  Explicación: La LCS es \"ace\", de longitud 3.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: s1=\"abc\", s2=\"abc\"\n"
            "  Salida: 3\n"
            "  Explicación: Las cadenas son iguales, la LCS es la propia cadena.\n\n"
            "Ejemplo 3:\n"
            "  Entrada: s1=\"abc\", s2=\"def\"\n"
            "  Salida: 0\n"
            "  Explicación: No hay ningún carácter en común.\n\n"
            "Escribe `solve(s1, s2)` que devuelva la longitud de la LCS."
        ),
        "test_cases": [
            {"input": '"abcde", "ace"',  "expected_output": "3"},
            {"input": '"abc", "abc"',    "expected_output": "3"},
            {"input": '"abc", "def"',    "expected_output": "0"},
        ],
        "stub": {
            "Python": "def solve(s1, s2):\n    # Programación dinámica O(|s1|*|s2|)\n    pass",
            "C++":    "#include <string>\nusing namespace std;\nint solve(string s1, string s2) {\n    // Programación dinámica O(|s1|*|s2|)\n    return 0;\n}",
            "Java":   "public static int solve(String s1, String s2) {\n    // Programación dinámica O(|s1|*|s2|)\n    return 0;\n}",
            "Go":     "func solve(s1 string, s2 string) int {\n    // Programación dinámica O(|s1|*|s2|)\n    return 0\n}",
            "C#":     "public static int Solve(string s1, string s2) {\n    // Programación dinámica O(|s1|*|s2|)\n    return 0;\n}",
        },
    },

    # ══════════════════════════════════════════
    #  STACK — DIFÍCIL
    # ══════════════════════════════════════════
    {
        "title": "Máximo Rectángulo en Histograma",
        "difficulty": 1600, "category": "Stack", "total_solvers": 0,
        "description": (
            "Se te da un histograma representado como un array de enteros no negativos heights, "
            "donde heights[i] es la altura de la barra i-ésima (todas las barras tienen anchura 1).\n\n"
            "Debes encontrar el área del mayor rectángulo que se puede inscribir completamente "
            "dentro del histograma.\n\n"
            "Enfoque ingenuo O(n²):\n"
            "  Para cada par (i, j) considera el rectángulo que abarca de i a j, con altura igual "
            "al mínimo del rango. Este approach supera el límite de tiempo para n > 10^4.\n\n"
            "Enfoque óptimo O(n) — Stack monotónica:\n"
            "  Mantén una pila de índices en orden creciente de altura. Cuando encuentras una barra "
            "más baja que la cima de la pila, la cima 'no puede extenderse hacia la derecha', así que "
            "calcula el área que puede formar como rectángulo:\n"
            "    anchura = índice actual − índice debajo de la cima − 1\n"
            "    área    = altura_cima × anchura\n"
            "  Al final, vacía la pila procesando los elementos restantes.\n\n"
            "Intuición: cada barra es la barra más baja de exactamente un conjunto de rectángulos "
            "candidatos. La stack garantiza que procesamos cada barra exactamente una vez.\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 10^5\n"
            "  0 ≤ heights[i] ≤ 10^4\n\n"
            "Ejemplo 1:\n"
            "  Entrada: heights=[2,1,5,6,2,3]\n"
            "  Salida: 10\n"
            "  Explicación: El rectángulo de área 10 tiene altura 5 y abarca las barras 2 y 3 "
            "(índices 2 y 3, alturas 5 y 6). Min(5,6)×2 = 10.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: heights=[2,4]\n"
            "  Salida: 4\n"
            "  Explicación: La barra de altura 4 con anchura 1 da área 4, o la combinación de "
            "ambas con min 2 da área 4. Resultado: 4.\n\n"
            "Ejemplo 3:\n"
            "  Entrada: heights=[1,1]\n"
            "  Salida: 2\n"
            "  Explicación: Ambas barras tienen altura 1, el rectángulo de anchura 2 da área 2.\n\n"
            "Escribe `solve(heights)` que devuelva el área máxima del rectángulo."
        ),
        "test_cases": [
            {"input": "[2,1,5,6,2,3]", "expected_output": "10"},
            {"input": "[2,4]",          "expected_output": "4"},
            {"input": "[1,1]",          "expected_output": "2"},
        ],
        "stub": {
            "Python": "def solve(heights):\n    # Stack monotónica O(n)\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nint solve(vector<int> heights) {\n    // Stack monotónica O(n)\n    return 0;\n}",
            "Java":   "public static int solve(int[] heights) {\n    // Stack monotónica O(n)\n    return 0;\n}",
            "Go":     "func solve(heights []int) int {\n    // Stack monotónica O(n)\n    return 0\n}",
            "C#":     "public static int Solve(int[] heights) {\n    // Stack monotónica O(n)\n    return 0;\n}",
        },
    },

    # ══════════════════════════════════════════
    #  BIT MANIPULATION — FÁCIL
    # ══════════════════════════════════════════
    {
        "title": "Contar Bits Encendidos",
        "difficulty": 800, "category": "Matemáticas", "total_solvers": 0,
        "description": (
            "Dado un entero no negativo n, devuelve el número de bits 1 en su representación "
            "binaria. Esta operación se conoce como «popcount» o «Hamming weight».\n\n"
            "Por ejemplo, el número 11 en binario es 1011, que contiene tres bits 1.\n\n"
            "Existen varias formas de resolver este problema:\n\n"
            "Enfoque 1 — bucle simple O(log n):\n"
            "  Itera extrayendo el bit menos significativo con n & 1 y desplazando n a la derecha.\n\n"
            "Enfoque 2 — truco de Brian Kernighan O(k), donde k = número de 1s:\n"
            "  La operación n = n & (n - 1) elimina el bit 1 más a la derecha de n en cada paso. "
            "Solo se itera tantas veces como bits 1 haya, no tantas como bits totales tenga n.\n"
            "  Ejemplo: n=12 (1100) → n & (n-1) = 1100 & 1011 = 1000 → 1000 & 0111 = 0000. "
            "Dos iteraciones, dos bits.\n\n"
            "Enfoque 3 — lookup table O(1) amortizado:\n"
            "  Precalcula el popcount para bloques de 8 o 16 bits y combínalos.\n\n"
            "Restricciones:\n"
            "  0 ≤ n ≤ 2^31 − 1\n\n"
            "Ejemplo 1:\n"
            "  Entrada: n=11\n"
            "  Salida: 3\n"
            "  Explicación: 11 en binario = 1011 → tres bits 1.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: n=128\n"
            "  Salida: 1\n"
            "  Explicación: 128 = 10000000 → un solo bit 1.\n\n"
            "Ejemplo 3:\n"
            "  Entrada: n=255\n"
            "  Salida: 8\n"
            "  Explicación: 255 = 11111111 → ocho bits 1.\n\n"
            "Escribe `solve(n)` que devuelva el número de bits 1 en la representación binaria de n."
        ),
        "test_cases": [
            {"input": "11",  "expected_output": "3"},
            {"input": "128", "expected_output": "1"},
            {"input": "255", "expected_output": "8"},
        ],
        "stub": {
            "Python": "def solve(n):\n    # Cuenta los bits 1 de n (Hamming weight)\n    pass",
            "C++":    "int solve(int n) {\n    // Cuenta los bits 1 de n\n    return 0;\n}",
            "Java":   "public static int solve(int n) {\n    // Cuenta los bits 1 de n\n    return 0;\n}",
            "Go":     "func solve(n int) int {\n    // Cuenta los bits 1 de n\n    return 0\n}",
            "C#":     "public static int Solve(int n) {\n    // Cuenta los bits 1 de n\n    return 0;\n}",
        },
    },

    # ══════════════════════════════════════════
    #  ARRAYS — NORMAL
    # ══════════════════════════════════════════
    {
        "title": "Ventana Deslizante Máxima",
        "difficulty": 1200, "category": "Arrays", "total_solvers": 0,
        "description": (
            "Dado un array de enteros nums y un entero k, devuelve el máximo de cada ventana "
            "deslizante de tamaño k que se desplaza de izquierda a derecha.\n\n"
            "Ejemplo visual con nums=[1,3,-1,-3,5,3,6,7] y k=3:\n"
            "  Ventana [1,3,-1]  → máx = 3\n"
            "  Ventana [3,-1,-3] → máx = 3\n"
            "  Ventana [-1,-3,5] → máx = 5\n"
            "  Ventana [-3,5,3]  → máx = 5\n"
            "  Ventana [5,3,6]   → máx = 6\n"
            "  Ventana [3,6,7]   → máx = 7\n"
            "  Resultado: [3,3,5,5,6,7]\n\n"
            "Enfoque ingenuo O(n·k): para cada posición de la ventana, busca el máximo linealmente.\n\n"
            "Enfoque óptimo O(n) — Deque monotónica decreciente:\n"
            "  Mantén una cola doble (deque) que almacene índices y garantice que los valores "
            "correspondientes en nums estén en orden decreciente. Al avanzar la ventana:\n"
            "  1. Elimina del frente los índices que ya están fuera de la ventana (i - k).\n"
            "  2. Elimina del fondo los índices cuyo valor sea ≤ al elemento actual "
            "(nunca podrán ser máximos mientras el actual esté en la ventana).\n"
            "  3. Añade el índice actual al fondo.\n"
            "  4. El frente de la deque siempre contiene el índice del máximo actual.\n\n"
            "Restricciones:\n"
            "  1 ≤ k ≤ n ≤ 10^5\n"
            "  -10^4 ≤ nums[i] ≤ 10^4\n\n"
            "Ejemplo 1:\n"
            "  Entrada: nums=[1,3,-1,-3,5,3,6,7], k=3\n"
            "  Salida: [3,3,5,5,6,7]\n\n"
            "Ejemplo 2:\n"
            "  Entrada: nums=[1], k=1\n"
            "  Salida: [1]\n\n"
            "Ejemplo 3:\n"
            "  Entrada: nums=[9,8,7,6], k=2\n"
            "  Salida: [9,8,7]\n\n"
            "Escribe `solve(nums, k)` que devuelva la lista de máximos de cada ventana."
        ),
        "test_cases": [
            {"input": "[1,3,-1,-3,5,3,6,7], 3", "expected_output": "[3,3,5,5,6,7]"},
            {"input": "[1], 1",                   "expected_output": "[1]"},
            {"input": "[9,8,7,6], 2",             "expected_output": "[9,8,7]"},
        ],
        "stub": {
            "Python": "def solve(nums, k):\n    # Deque monotónica O(n)\n    pass",
            "C++":    "#include <vector>\n#include <deque>\nusing namespace std;\nvector<int> solve(vector<int> nums, int k) {\n    // Deque monotónica O(n)\n    return {};\n}",
            "Java":   "public static int[] solve(int[] nums, int k) {\n    // Deque monotónica O(n)\n    return new int[]{};\n}",
            "Go":     "func solve(nums []int, k int) []int {\n    // Deque monotónica O(n)\n    return []int{}\n}",
            "C#":     "public static int[] Solve(int[] nums, int k) {\n    // Deque monotónica O(n)\n    return new int[]{};\n}",
        },
    },

    # ══════════════════════════════════════════
    #  DP — DIFÍCIL
    # ══════════════════════════════════════════
    {
        "title": "Partición en Subconjuntos Iguales",
        "difficulty": 1600, "category": "Programación Dinámica", "total_solvers": 0,
        "description": (
            "Dado un array de enteros positivos nums, determina si es posible particionarlo "
            "en exactamente dos subconjuntos no vacíos tal que la suma de ambos sea igual.\n\n"
            "Este problema es una variante del clásico 0/1 Knapsack y pertenece a la familia "
            "de problemas NP-completos en el caso general, aunque para valores acotados tiene "
            "solución pseudo-polinomial O(n × S/2) donde S = suma total.\n\n"
            "Observación clave:\n"
            "  Si la suma total S es impar, es imposible particionar en dos mitades iguales.\n"
            "  Si S es par, el problema se reduce a: ¿existe un subconjunto con suma exactamente S/2?\n\n"
            "Algoritmo DP:\n"
            "  Define dp[j] = True si es posible formar la suma j usando un subconjunto de los "
            "elementos procesados hasta ahora.\n"
            "  Inicialmente dp[0] = True, el resto False.\n"
            "  Para cada número x en nums:\n"
            "    Para j desde target hasta x (en orden decreciente para evitar reutilizar x):\n"
            "      dp[j] = dp[j] OR dp[j - x]\n"
            "  Resultado: dp[target]\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 200\n"
            "  1 ≤ nums[i] ≤ 100\n\n"
            "Ejemplo 1:\n"
            "  Entrada: nums=[1,5,11,5]\n"
            "  Salida: True\n"
            "  Explicación: S=22, target=11. Subconjuntos [1,5,5] y [11], ambos con suma 11.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: nums=[1,2,3,5]\n"
            "  Salida: False\n"
            "  Explicación: S=11, impar. Imposible dividir en dos partes iguales.\n\n"
            "Ejemplo 3:\n"
            "  Entrada: nums=[2,2,3,5]\n"
            "  Salida: False\n"
            "  Explicación: S=12, target=6. No hay subconjunto de suma 6.\n\n"
            "Escribe `solve(nums)` que devuelva True si es posible la partición, False en caso contrario."
        ),
        "test_cases": [
            {"input": "[1,5,11,5]",  "expected_output": "True"},
            {"input": "[1,2,3,5]",   "expected_output": "False"},
            {"input": "[2,2,3,5]",   "expected_output": "False"},
        ],
        "stub": {
            "Python": "def solve(nums):\n    # DP 0/1 Knapsack — subset sum\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nbool solve(vector<int> nums) {\n    // DP 0/1 Knapsack — subset sum\n    return false;\n}",
            "Java":   "public static boolean solve(int[] nums) {\n    // DP 0/1 Knapsack — subset sum\n    return false;\n}",
            "Go":     "func solve(nums []int) bool {\n    // DP 0/1 Knapsack — subset sum\n    return false\n}",
            "C#":     "public static bool Solve(int[] nums) {\n    // DP 0/1 Knapsack — subset sum\n    return false;\n}",
        },
    },

    # ══════════════════════════════════════════
    #  MATEMÁTICAS — FÁCIL
    # ══════════════════════════════════════════
    {
        "title": "Exponenciación Modular",
        "difficulty": 800, "category": "Matemáticas", "total_solvers": 0,
        "description": (
            "Calcula (base ^ exp) % mod de forma eficiente.\n\n"
            "La exponenciación modular es una operación fundamental en criptografía (RSA, "
            "Diffie-Hellman) y en competición, donde se pide devolver resultados módulo 10^9+7 "
            "o 998244353 para evitar desbordamientos.\n\n"
            "El enfoque ingenuo multiplica base por sí misma exp veces: O(exp). Para exp ~ 10^9 "
            "esto es completamente inviable.\n\n"
            "Exponenciación rápida (Binary Exponentiation) O(log exp):\n"
            "  Se basa en la propiedad:\n"
            "    base^exp = (base^(exp/2))^2          si exp es par\n"
            "    base^exp = base × base^(exp-1)        si exp es impar\n"
            "  Esto reduce el problema a la mitad en cada paso recursivo.\n\n"
            "  Versión iterativa:\n"
            "    resultado = 1\n"
            "    mientras exp > 0:\n"
            "        si exp es impar: resultado = (resultado × base) % mod\n"
            "        base = (base × base) % mod\n"
            "        exp = exp >> 1  (divide entre 2)\n\n"
            "  Es importante aplicar el módulo en cada multiplicación para evitar que "
            "los números intermedios desborden.\n\n"
            "Restricciones:\n"
            "  0 ≤ base ≤ 10^9\n"
            "  0 ≤ exp  ≤ 10^9\n"
            "  1 ≤ mod  ≤ 10^9\n\n"
            "Ejemplo 1:\n"
            "  Entrada: base=2, exp=10, mod=1000\n"
            "  Salida: 24\n"
            "  Explicación: 2^10 = 1024. 1024 % 1000 = 24.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: base=3, exp=5, mod=100\n"
            "  Salida: 43\n"
            "  Explicación: 3^5 = 243. 243 % 100 = 43.\n\n"
            "Ejemplo 3:\n"
            "  Entrada: base=7, exp=0, mod=1000000007\n"
            "  Salida: 1\n"
            "  Explicación: Cualquier número elevado a 0 es 1.\n\n"
            "Escribe `solve(base, exp, mod)` que devuelva (base^exp) % mod."
        ),
        "test_cases": [
            {"input": "2, 10, 1000",        "expected_output": "24"},
            {"input": "3, 5, 100",           "expected_output": "43"},
            {"input": "7, 0, 1000000007",    "expected_output": "1"},
        ],
        "stub": {
            "Python": "def solve(base, exp, mod):\n    # Exponenciación rápida O(log exp)\n    pass",
            "C++":    "long long solve(long long base, long long exp, long long mod) {\n    // Exponenciación rápida O(log exp)\n    return 0;\n}",
            "Java":   "public static long solve(long base, long exp, long mod) {\n    // Exponenciación rápida O(log exp)\n    return 0;\n}",
            "Go":     "func solve(base int, exp int, mod int) int {\n    // Exponenciación rápida O(log exp)\n    return 0\n}",
            "C#":     "public static long Solve(long base2, long exp, long mod) {\n    // Exponenciación rápida O(log exp)\n    return 0;\n}",
        },
    },

    # ══════════════════════════════════════════
    #  GRAFOS — NORMAL
    # ══════════════════════════════════════════
    {
        "title": "Número de Islas",
        "difficulty": 1200, "category": "Grafos", "total_solvers": 0,
        "description": (
            "Se te da una cuadrícula de m × n que representa un mapa donde '1' es tierra y "
            "'0' es agua. Cuenta el número de islas.\n\n"
            "Una isla está formada por celdas de tierra ('1') conectadas horizontalmente o "
            "verticalmente (no en diagonal). El mapa está rodeado de agua por todos los lados.\n\n"
            "Este es uno de los problemas más icónicos de grafos en programación competitiva y "
            "entrevistas técnicas. Modela el problema como un grafo implícito donde cada celda "
            "'1' es un nodo y las aristas conectan celdas adyacentes.\n\n"
            "Dos enfoques equivalentes:\n\n"
            "BFS (Breadth-First Search):\n"
            "  Para cada celda no visitada con valor '1', lanza un BFS que marca como visitadas "
            "todas las celdas de esa isla. Incrementa el contador de islas en 1.\n\n"
            "DFS (Depth-First Search):\n"
            "  Igual que BFS pero usando recursión o una pila explícita. Al visitar una celda, "
            "márcala como '0' (o usa un array de visitados) y explora sus 4 vecinos.\n\n"
            "Union-Find:\n"
            "  Agrupa componentes conexas con una estructura de conjuntos disjuntos.\n\n"
            "La cuadrícula se representa como una lista de strings, donde cada carácter es '0' o '1'.\n\n"
            "Restricciones:\n"
            "  1 ≤ m, n ≤ 300\n"
            "  grid[i][j] es '0' o '1'\n\n"
            "Ejemplo 1:\n"
            "  Entrada: grid=[\"11110\",\"11010\",\"11000\",\"00000\"]\n"
            "  Salida: 1\n"
            "  Explicación: Toda la tierra está conectada, formando una sola isla.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: grid=[\"11000\",\"11000\",\"00100\",\"00011\"]\n"
            "  Salida: 3\n"
            "  Explicación: Hay tres grupos de tierra desconectados.\n\n"
            "Ejemplo 3:\n"
            "  Entrada: grid=[\"1\"]\n"
            "  Salida: 1\n\n"
            "Escribe `solve(grid)` que reciba una lista de strings y devuelva el número de islas."
        ),
        "test_cases": [
            {"input": '["11110","11010","11000","00000"]', "expected_output": "1"},
            {"input": '["11000","11000","00100","00011"]', "expected_output": "3"},
            {"input": '["1"]',                             "expected_output": "1"},
        ],
        "stub": {
            "Python": "def solve(grid):\n    # BFS o DFS sobre la cuadrícula\n    pass",
            "C++":    '#include <vector>\n#include <string>\nusing namespace std;\nint solve(vector<string> grid) {\n    // BFS o DFS sobre la cuadrícula\n    return 0;\n}',
            "Java":   'public static int solve(String[] grid) {\n    // BFS o DFS sobre la cuadrícula\n    return 0;\n}',
            "Go":     'func solve(grid []string) int {\n    // BFS o DFS sobre la cuadrícula\n    return 0\n}',
            "C#":     'public static int Solve(string[] grid) {\n    // BFS o DFS sobre la cuadrícula\n    return 0;\n}',
        },
    },

    # ══════════════════════════════════════════
    #  STRINGS — DIFÍCIL
    # ══════════════════════════════════════════
    {
        "title": "Ventana Mínima que Contiene Subcadena",
        "difficulty": 1600, "category": "Strings", "total_solvers": 0,
        "description": (
            "Dadas dos cadenas s y t, devuelve la subcadena más corta de s que contenga "
            "todos los caracteres de t (incluyendo repetidos). Si no existe tal subcadena, "
            "devuelve una cadena vacía \"\".\n\n"
            "Este problema clásico de ventana deslizante aparece frecuentemente en competición "
            "y en entrevistas de empresas top. Su solución óptima O(|s| + |t|) es un ejemplo "
            "canónico de la técnica Two Pointers / Sliding Window con mapa de frecuencias.\n\n"
            "Algoritmo:\n"
            "  1. Construye un mapa need con la frecuencia de cada carácter de t.\n"
            "  2. Mantén dos punteros left y right que definen la ventana actual [left, right].\n"
            "  3. Expande right: añade s[right] al mapa window. Si su frecuencia alcanza "
            "la requerida en need, incrementa un contador formed.\n"
            "  4. Cuando formed == número de caracteres distintos en t (todos satisfechos), "
            "intenta contraer la ventana moviendo left hacia la derecha, actualizando el mínimo.\n"
            "  5. Repite hasta que right llegue al final de s.\n\n"
            "El resultado es la ventana más pequeña encontrada; si ninguna ventana satisface "
            "todos los requisitos, devuelve \"\".\n\n"
            "Restricciones:\n"
            "  1 ≤ |s|, |t| ≤ 10^5\n"
            "  s y t contienen letras mayúsculas y minúsculas del alfabeto inglés\n\n"
            "Ejemplo 1:\n"
            "  Entrada: s=\"ADOBECODEBANC\", t=\"ABC\"\n"
            "  Salida: \"BANC\"\n"
            "  Explicación: La ventana mínima que contiene A, B y C es \"BANC\" (índices 9-12).\n\n"
            "Ejemplo 2:\n"
            "  Entrada: s=\"a\", t=\"a\"\n"
            "  Salida: \"a\"\n\n"
            "Ejemplo 3:\n"
            "  Entrada: s=\"a\", t=\"b\"\n"
            "  Salida: \"\"\n"
            "  Explicación: b no existe en s, imposible satisfacer t.\n\n"
            "Escribe `solve(s, t)` que devuelva la subcadena mínima de s que contiene todos los "
            "caracteres de t, o la cadena vacía si no existe."
        ),
        "test_cases": [
            {"input": '"ADOBECODEBANC", "ABC"', "expected_output": "BANC"},
            {"input": '"a", "a"',               "expected_output": "a"},
            {"input": '"a", "b"',               "expected_output": ""},
        ],
        "stub": {
            "Python": "def solve(s, t):\n    # Ventana deslizante con mapa de frecuencias O(|s|+|t|)\n    pass",
            "C++":    '#include <string>\n#include <unordered_map>\nusing namespace std;\nstring solve(string s, string t) {\n    // Ventana deslizante con mapa de frecuencias\n    return "";\n}',
            "Java":   'public static String solve(String s, String t) {\n    // Ventana deslizante con mapa de frecuencias\n    return "";\n}',
            "Go":     'func solve(s string, t string) string {\n    // Ventana deslizante con mapa de frecuencias\n    return ""\n}',
            "C#":     'public static string Solve(string s, string t) {\n    // Ventana deslizante con mapa de frecuencias\n    return "";\n}',
        },
    },

    # ══════════════════════════════════════════
    #  ARRAYS — FÁCIL
    # ══════════════════════════════════════════
    {
        "title": "Equilibrio de Array",
        "difficulty": 800, "category": "Arrays", "total_solvers": 0,
        "description": (
            "Dado un array de enteros nums, encuentra el índice de equilibrio (pivot index). "
            "El índice de equilibrio es aquel en el que la suma de todos los elementos a su "
            "izquierda es igual a la suma de todos los elementos a su derecha.\n\n"
            "Si no existe tal índice, devuelve -1. Si existen varios, devuelve el más a la izquierda.\n\n"
            "Los elementos en el propio índice no se cuentan ni en la suma izquierda ni en la derecha.\n\n"
            "Para un índice i:\n"
            "  suma_izquierda = nums[0] + ... + nums[i-1]\n"
            "  suma_derecha   = nums[i+1] + ... + nums[n-1]\n"
            "  Condición: suma_izquierda == suma_derecha\n\n"
            "Enfoque O(n) con sumas prefijas:\n"
            "  Calcula la suma total S.\n"
            "  Recorre el array manteniendo suma_izq acumulada.\n"
            "  Para cada índice i: suma_der = S - suma_izq - nums[i]\n"
            "  Si suma_izq == suma_der, devuelve i.\n"
            "  Actualiza suma_izq += nums[i].\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 10^4\n"
            "  -1000 ≤ nums[i] ≤ 1000\n\n"
            "Ejemplo 1:\n"
            "  Entrada: nums=[1,7,3,6,5,6]\n"
            "  Salida: 3\n"
            "  Explicación: Izquierda de índice 3: 1+7+3=11. Derecha: 5+6=11. Igual.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: nums=[1,2,3]\n"
            "  Salida: -1\n"
            "  Explicación: Ningún índice tiene suma igual a ambos lados.\n\n"
            "Ejemplo 3:\n"
            "  Entrada: nums=[2,1,-1]\n"
            "  Salida: 0\n"
            "  Explicación: Izquierda de índice 0: 0 (vacío). Derecha: 1+(-1)=0. Igual.\n\n"
            "Escribe `solve(nums)` que devuelva el índice de equilibrio más a la izquierda, o -1."
        ),
        "test_cases": [
            {"input": "[1,7,3,6,5,6]", "expected_output": "3"},
            {"input": "[1,2,3]",        "expected_output": "-1"},
            {"input": "[2,1,-1]",       "expected_output": "0"},
        ],
        "stub": {
            "Python": "def solve(nums):\n    # Sumas prefijas O(n)\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nint solve(vector<int> nums) {\n    // Sumas prefijas O(n)\n    return -1;\n}",
            "Java":   "public static int solve(int[] nums) {\n    // Sumas prefijas O(n)\n    return -1;\n}",
            "Go":     "func solve(nums []int) int {\n    // Sumas prefijas O(n)\n    return -1\n}",
            "C#":     "public static int Solve(int[] nums) {\n    // Sumas prefijas O(n)\n    return -1;\n}",
        },
    },

    # ══════════════════════════════════════════
    #  STRINGS — NORMAL
    # ══════════════════════════════════════════
    {
        "title": "Decodificación de Mensajes",
        "difficulty": 1200, "category": "Programación Dinámica", "total_solvers": 0,
        "description": (
            "Un mensaje codificado se ha cifrado mediante el siguiente esquema:\n"
            "  'A' → 1\n"
            "  'B' → 2\n"
            "  ...\n"
            "  'Z' → 26\n\n"
            "Dada una cadena s que contiene solo dígitos, cuenta el número de formas distintas "
            "de decodificarla.\n\n"
            "Por ejemplo, \"12\" puede decodificarse como:\n"
            "  - \"AB\" (1, 2)\n"
            "  - \"L\"  (12)\n"
            "Son 2 formas.\n\n"
            "Este problema es análogo al problema de contar formas de subir escaleras, pero con "
            "la complejidad adicional de dígitos inválidos ('0' suelto) y bloques de dos dígitos "
            "que deben estar entre 10 y 26.\n\n"
            "Algoritmo DP:\n"
            "  dp[i] = número de formas de decodificar s[0..i-1]\n"
            "  dp[0] = 1 (cadena vacía, 1 forma)\n"
            "  dp[1] = 0 si s[0]=='0', sino 1\n"
            "  Para i de 2 a n:\n"
            "    Si s[i-1] != '0': dp[i] += dp[i-1]  (decodifica el dígito actual solo)\n"
            "    Si s[i-2..i-1] está entre '10' y '26': dp[i] += dp[i-2]  (par de dígitos)\n"
            "  Resultado: dp[n]\n\n"
            "Restricciones:\n"
            "  1 ≤ |s| ≤ 100\n"
            "  s contiene solo dígitos del '0' al '9'\n\n"
            "Ejemplo 1:\n"
            "  Entrada: s=\"12\"\n"
            "  Salida: 2\n"
            "  Explicación: \"AB\" (1,2) o \"L\" (12).\n\n"
            "Ejemplo 2:\n"
            "  Entrada: s=\"226\"\n"
            "  Salida: 3\n"
            "  Explicación: \"BZ\" (2,26), \"VF\" (22,6) y \"BBF\" (2,2,6).\n\n"
            "Ejemplo 3:\n"
            "  Entrada: s=\"06\"\n"
            "  Salida: 0\n"
            "  Explicación: '06' no es una codificación válida (0 suelto no mapea ninguna letra).\n\n"
            "Escribe `solve(s)` que devuelva el número de formas distintas de decodificar el mensaje."
        ),
        "test_cases": [
            {"input": '"12"',  "expected_output": "2"},
            {"input": '"226"', "expected_output": "3"},
            {"input": '"06"',  "expected_output": "0"},
        ],
        "stub": {
            "Python": "def solve(s):\n    # DP — conteo de decodificaciones\n    pass",
            "C++":    "#include <string>\nusing namespace std;\nint solve(string s) {\n    // DP — conteo de decodificaciones\n    return 0;\n}",
            "Java":   "public static int solve(String s) {\n    // DP — conteo de decodificaciones\n    return 0;\n}",
            "Go":     "func solve(s string) int {\n    // DP — conteo de decodificaciones\n    return 0\n}",
            "C#":     "public static int Solve(string s) {\n    // DP — conteo de decodificaciones\n    return 0;\n}",
        },
    },

    # ══════════════════════════════════════════
    #  GRAFOS — DIFÍCIL
    # ══════════════════════════════════════════
    {
        "title": "Palabras Encadenadas",
        "difficulty": 1600, "category": "Grafos", "total_solvers": 0,
        "description": (
            "Dado un diccionario de palabras y dos palabras beginWord y endWord, "
            "encuentra la longitud de la secuencia de transformación más corta de beginWord "
            "a endWord, donde:\n"
            "  1. Solo se puede cambiar un carácter a la vez.\n"
            "  2. Cada palabra intermedia debe estar en el diccionario.\n"
            "  3. beginWord no tiene por qué estar en el diccionario.\n\n"
            "Si no existe tal secuencia, devuelve 0.\n\n"
            "La longitud incluye tanto beginWord como endWord. La secuencia mínima tiene longitud 2 "
            "si beginWord difiere de endWord en exactamente una letra y endWord está en el diccionario.\n\n"
            "Este problema es un BFS clásico sobre un grafo implícito donde cada palabra es un nodo "
            "y hay arista entre dos palabras si difieren en exactamente una letra.\n\n"
            "Optimización clave — patrón genérico:\n"
            "  En lugar de comparar cada palabra con todas las demás O(n²·L), genera todos los "
            "patrones de una palabra sustituyendo cada carácter por '*' y agrupa las palabras "
            "por patrón. Así la complejidad baja a O(n·L²).\n\n"
            "Restricciones:\n"
            "  1 ≤ |beginWord|, |endWord| ≤ 10\n"
            "  1 ≤ n ≤ 5000 (tamaño del diccionario)\n"
            "  Todas las palabras tienen la misma longitud\n"
            "  Las palabras contienen solo letras minúsculas\n\n"
            "Ejemplo 1:\n"
            "  Entrada: beginWord=\"hit\", endWord=\"cog\", wordList=[\"hot\",\"dot\",\"dog\",\"lot\",\"log\",\"cog\"]\n"
            "  Salida: 5\n"
            "  Explicación: hit → hot → dot → dog → cog. Longitud 5.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: beginWord=\"hit\", endWord=\"cog\", wordList=[\"hot\",\"dot\",\"dog\",\"lot\",\"log\"]\n"
            "  Salida: 0\n"
            "  Explicación: \"cog\" no está en el diccionario, no hay camino.\n\n"
            "Ejemplo 3:\n"
            "  Entrada: beginWord=\"a\", endWord=\"c\", wordList=[\"a\",\"b\",\"c\"]\n"
            "  Salida: 2\n"
            "  Explicación: a → c. Difieren en 1 carácter, longitud 2.\n\n"
            "Escribe `solve(beginWord, endWord, wordList)` que devuelva la longitud de la secuencia "
            "mínima, o 0 si no existe."
        ),
        "test_cases": [
            {"input": '"hit", "cog", ["hot","dot","dog","lot","log","cog"]', "expected_output": "5"},
            {"input": '"hit", "cog", ["hot","dot","dog","lot","log"]',       "expected_output": "0"},
            {"input": '"a", "c", ["a","b","c"]',                             "expected_output": "2"},
        ],
        "stub": {
            "Python": "def solve(beginWord, endWord, wordList):\n    # BFS con patrones genéricos\n    pass",
            "C++":    '#include <string>\n#include <vector>\n#include <unordered_set>\n#include <queue>\nusing namespace std;\nint solve(string beginWord, string endWord, vector<string> wordList) {\n    // BFS con patrones genéricos\n    return 0;\n}',
            "Java":   'public static int solve(String beginWord, String endWord, String[] wordList) {\n    // BFS con patrones genéricos\n    return 0;\n}',
            "Go":     'func solve(beginWord string, endWord string, wordList []string) int {\n    // BFS con patrones genéricos\n    return 0\n}',
            "C#":     'public static int Solve(string beginWord, string endWord, string[] wordList) {\n    // BFS con patrones genéricos\n    return 0;\n}',
        },
    },

    # ══════════════════════════════════════════
    #  MATEMÁTICAS — FÁCIL
    # ══════════════════════════════════════════
    {
        "title": "Números Romanos a Enteros",
        "difficulty": 800, "category": "Strings", "total_solvers": 0,
        "description": (
            "Los números romanos se representan con siete símbolos:\n"
            "  I=1, V=5, X=10, L=50, C=100, D=500, M=1000\n\n"
            "Normalmente los símbolos se escriben de mayor a menor de izquierda a derecha. "
            "Sin embargo, hay seis casos especiales de sustracción:\n"
            "  IV=4, IX=9, XL=40, XC=90, CD=400, CM=900\n\n"
            "La regla de conversión es simple:\n"
            "  Si el valor de un símbolo es menor que el del símbolo siguiente, se resta.\n"
            "  En caso contrario, se suma.\n\n"
            "Ejemplo de análisis de \"MCMXCIV\":\n"
            "  M  = 1000  (suma, siguiente C < M)\n"
            "  C  = -100  (resta, siguiente M > C)\n"
            "  M  = 1000  (suma, siguiente X < M)\n"
            "  X  = -10   (resta, siguiente C > X)\n"
            "  C  = 100   (suma, siguiente I < C)\n"
            "  I  = -1    (resta, siguiente V > I)\n"
            "  V  = 5     (suma, último símbolo)\n"
            "  Total: 1000 - 100 + 1000 - 10 + 100 - 1 + 5 = 1994\n\n"
            "Restricciones:\n"
            "  1 ≤ valor ≤ 3999\n"
            "  s es un número romano válido\n\n"
            "Ejemplo 1:\n"
            "  Entrada: s=\"III\"\n"
            "  Salida: 3\n\n"
            "Ejemplo 2:\n"
            "  Entrada: s=\"LVIII\"\n"
            "  Salida: 58\n"
            "  Explicación: L=50, V=5, III=3.\n\n"
            "Ejemplo 3:\n"
            "  Entrada: s=\"MCMXCIV\"\n"
            "  Salida: 1994\n\n"
            "Escribe `solve(s)` que convierta un número romano a su valor entero."
        ),
        "test_cases": [
            {"input": '"III"',    "expected_output": "3"},
            {"input": '"LVIII"',  "expected_output": "58"},
            {"input": '"MCMXCIV"',"expected_output": "1994"},
        ],
        "stub": {
            "Python": "def solve(s):\n    # Mapea símbolos y aplica la regla de sustracción\n    pass",
            "C++":    "#include <string>\n#include <unordered_map>\nusing namespace std;\nint solve(string s) {\n    // Mapea símbolos y aplica la regla de sustracción\n    return 0;\n}",
            "Java":   "public static int solve(String s) {\n    // Mapea símbolos y aplica la regla de sustracción\n    return 0;\n}",
            "Go":     "func solve(s string) int {\n    // Mapea símbolos y aplica la regla de sustracción\n    return 0\n}",
            "C#":     "public static int Solve(string s) {\n    // Mapea símbolos y aplica la regla de sustracción\n    return 0;\n}",
        },
    },

    # ══════════════════════════════════════════
    #  ÁRBOLES — NORMAL
    # ══════════════════════════════════════════
    {
        "title": "Suma Máxima de Camino en Árbol Binario",
        "difficulty": 1200, "category": "Programación Dinámica", "total_solvers": 0,
        "description": (
            "Se te da un árbol binario representado como array en nivel BFS (valor -1001 indica "
            "nodo nulo). Encuentra la suma máxima de cualquier camino dentro del árbol.\n\n"
            "Un camino es una secuencia de nodos donde cada par de nodos adyacentes tiene "
            "una arista entre ellos. El camino debe contener al menos un nodo, no necesita "
            "pasar por la raíz y no puede reutilizar nodos.\n\n"
            "Dado que representar árboles como input es complejo, simplificamos:\n"
            "  Se te da un array plano de valores donde index 0 es la raíz, y para el nodo i:\n"
            "    hijo izquierdo: 2*i+1\n"
            "    hijo derecho:   2*i+2\n"
            "  El valor -1001 indica que esa posición no existe (nodo nulo).\n\n"
            "Algoritmo DFS con estado:\n"
            "  Para cada nodo, calcula la ganancia máxima que puede aportar hacia arriba "
            "(solo un subárbol, no ambos). Actualiza el máximo global considerando que el "
            "camino puede 'doblar' en el nodo actual: valor + izq_ganancia + der_ganancia.\n\n"
            "  def dfs(i):\n"
            "    si i fuera de rango o arr[i] == -1001: return 0\n"
            "    izq = max(0, dfs(2*i+1))\n"
            "    der = max(0, dfs(2*i+2))\n"
            "    max_global = max(max_global, arr[i] + izq + der)\n"
            "    return arr[i] + max(izq, der)   # solo un lado hacia arriba\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 127  (hasta 7 niveles completos)\n"
            "  -1000 ≤ valores ≤ 1000\n"
            "  El árbol tiene al menos un nodo real\n\n"
            "Ejemplo 1:\n"
            "  Entrada: tree=[1,2,3]\n"
            "  Salida: 6\n"
            "  Explicación: Árbol: raíz=1, hijo_izq=2, hijo_der=3. Camino 2→1→3 = 6.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: tree=[-10,9,20,-1001,-1001,15,7]\n"
            "  Salida: 42\n"
            "  Explicación: El camino óptimo es 15→20→7 = 42.\n\n"
            "Ejemplo 3:\n"
            "  Entrada: tree=[5]\n"
            "  Salida: 5\n\n"
            "Escribe `solve(tree)` que devuelva la suma máxima de cualquier camino."
        ),
        "test_cases": [
            {"input": "[1,2,3]",                           "expected_output": "6"},
            {"input": "[-10,9,20,-1001,-1001,15,7]",       "expected_output": "42"},
            {"input": "[5]",                               "expected_output": "5"},
        ],
        "stub": {
            "Python": "def solve(tree):\n    # DFS con ganancia máxima por subárbol\n    pass",
            "C++":    "#include <vector>\n#include <algorithm>\n#include <climits>\nusing namespace std;\nint solve(vector<int> tree) {\n    // DFS con ganancia máxima por subárbol\n    return 0;\n}",
            "Java":   "public static int solve(int[] tree) {\n    // DFS con ganancia máxima por subárbol\n    return 0;\n}",
            "Go":     "func solve(tree []int) int {\n    // DFS con ganancia máxima por subárbol\n    return 0\n}",
            "C#":     "public static int Solve(int[] tree) {\n    // DFS con ganancia máxima por subárbol\n    return 0;\n}",
        },
    },

    # ══════════════════════════════════════════
    #  STRINGS — DIFÍCIL
    # ══════════════════════════════════════════
    {
        "title": "Expresión Aritmética con Paréntesis Anidados",
        "difficulty": 1600, "category": "Stack", "total_solvers": 0,
        "description": (
            "Dada una cadena que representa una expresión aritmética con sumas, restas, "
            "multiplicaciones, divisiones (enteras, truncadas hacia cero) y paréntesis "
            "anidados, evalúa su valor.\n\n"
            "Los operandos son enteros no negativos. No hay espacios en la expresión. "
            "La división es entera truncada hacia cero (como en la mayoría de lenguajes de "
            "programación: -7/2 = -3, no -4).\n\n"
            "Algoritmo con stack (dos pisos):\n"
            "  Mantén una pila de (resultado_parcial, signo_multiplicador_acumulado) para "
            "manejar paréntesis, y procesa la expresión con un número actual y un signo.\n\n"
            "  Alternativa — Recursive Descent Parser:\n"
            "    parseExpr() maneja sumas/restas, llamando a parseTerm() para mult/div, "
            "que a su vez llama a parseFactor() para paréntesis y números.\n\n"
            "  Esta versión requiere respetar la precedencia de operadores:\n"
            "    * y / tienen mayor precedencia que + y -\n"
            "    Los paréntesis anulan la precedencia\n\n"
            "Restricciones:\n"
            "  1 ≤ |s| ≤ 10^4\n"
            "  s contiene dígitos, '+', '-', '*', '/', '(', ')'\n"
            "  La expresión es válida\n"
            "  El resultado cabe en un entero de 32 bits\n\n"
            "Ejemplo 1:\n"
            "  Entrada: s=\"3+2*2\"\n"
            "  Salida: 7\n"
            "  Explicación: Precedencia: 2*2=4, luego 3+4=7.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: s=\"(2+3)*4\"\n"
            "  Salida: 20\n"
            "  Explicación: Paréntesis primero: 2+3=5, luego 5*4=20.\n\n"
            "Ejemplo 3:\n"
            "  Entrada: s=\"10+2*(6-4)/2\"\n"
            "  Salida: 12\n"
            "  Explicación: 6-4=2, 2*2=4, 4/2=2, 10+2=12.\n\n"
            "Escribe `solve(s)` que evalúe la expresión y devuelva su resultado entero."
        ),
        "test_cases": [
            {"input": '"3+2*2"',          "expected_output": "7"},
            {"input": '"(2+3)*4"',         "expected_output": "20"},
            {"input": '"10+2*(6-4)/2"',    "expected_output": "12"},
        ],
        "stub": {
            "Python": "def solve(s):\n    # Recursive descent parser o stack con precedencia\n    pass",
            "C++":    "#include <string>\nusing namespace std;\nint solve(string s) {\n    // Recursive descent parser o stack con precedencia\n    return 0;\n}",
            "Java":   "public static int solve(String s) {\n    // Recursive descent parser o stack con precedencia\n    return 0;\n}",
            "Go":     "func solve(s string) int {\n    // Recursive descent parser o stack con precedencia\n    return 0\n}",
            "C#":     "public static int Solve(string s) {\n    // Recursive descent parser o stack con precedencia\n    return 0;\n}",
        },
    },
    {
    "title": "Conectividad Dinámica Offline con Eliminaciones",
    "difficulty": 2400, "category": "DSU + Segment Tree + Offline Queries", "total_solvers": 0,
    "description": (
        "Tienes un grafo no dirigido inicialmente vacío con n nodos numerados de 0 a n-1.\n\n"
        "Debes procesar una secuencia de operaciones de tres tipos:\n\n"
        "  1. add(u, v): añade una arista entre u y v\n"
        "  2. remove(u, v): elimina la arista entre u y v\n"
        "  3. query(u, v): determina si u y v están conectados en ese momento\n\n"
        "IMPORTANTE:\n"
        "  - Las aristas pueden añadirse y eliminarse múltiples veces\n"
        "  - Siempre que se hace remove(u, v), la arista existe previamente\n"
        "  - Las queries deben responderse en orden\n\n"
        "El reto es que necesitas soportar eliminaciones de aristas, lo cual rompe el uso clásico "
        "de Union-Find (DSU).\n\n"
        "Enfoque esperado (nivel competición):\n\n"
        "  1. Procesar todas las operaciones offline\n"
        "  2. Convertir la vida de cada arista en intervalos de tiempo [l, r)\n"
        "  3. Construir un Segment Tree sobre el tiempo\n"
        "  4. En cada nodo del Segment Tree, almacenar las aristas activas en ese intervalo\n"
        "  5. Recorrer el árbol con DFS aplicando DSU con rollback\n\n"
        "DSU Rollback:\n"
        "  - No usar path compression\n"
        "  - Guardar historial de cambios (padre y tamaño)\n"
        "  - Permitir deshacer uniones al volver en el DFS\n\n"
        "Complejidad esperada:\n"
        "  O((n + q) log q)\n\n"
        "Restricciones:\n"
        "  1 ≤ n ≤ 2 * 10^5\n"
        "  1 ≤ q ≤ 2 * 10^5\n"
        "  0 ≤ u, v < n\n\n"
        "Ejemplo 1:\n"
        "  Entrada:\n"
        "    n = 3\n"
        "    operations = [\n"
        "      (\"add\", 0, 1),\n"
        "      (\"query\", 0, 1),\n"
        "      (\"remove\", 0, 1),\n"
        "      (\"query\", 0, 1)\n"
        "    ]\n"
        "  Salida: [true, false]\n\n"
        "Ejemplo 2:\n"
        "  Entrada:\n"
        "    n = 4\n"
        "    operations = [\n"
        "      (\"add\", 0, 1),\n"
        "      (\"add\", 1, 2),\n"
        "      (\"query\", 0, 2),\n"
        "      (\"remove\", 1, 2),\n"
        "      (\"query\", 0, 2)\n"
        "    ]\n"
        "  Salida: [true, false]\n\n"
        "Devuelve un array de booleanos con las respuestas de cada query.\n\n"
        "Escribe `solve(n, operations)` que devuelva la lista de resultados."
    ),
    "test_cases": [
        {
            "input": "3, [(\"add\",0,1),(\"query\",0,1),(\"remove\",0,1),(\"query\",0,1)]",
            "expected_output": "[True, False]"
        },
        {
            "input": "4, [(\"add\",0,1),(\"add\",1,2),(\"query\",0,2),(\"remove\",1,2),(\"query\",0,2)]",
            "expected_output": "[True, False]"
        }
    ],
    "stub": {
        "Python": "def solve(n, operations):\n    # Segment Tree sobre tiempo + DSU rollback\n    pass",
        "C++": "#include <vector>\n#include <tuple>\nusing namespace std;\nvector<bool> solve(int n, vector<tuple<string,int,int>> operations) {\n    // Segment Tree + DSU rollback\n    return {};\n}",
        "Java": "public static boolean[] solve(int n, List<Object[]> operations) {\n    // Segment Tree + DSU rollback\n    return new boolean[0];\n}",
        "Go": "func solve(n int, operations [][]interface{}) []bool {\n    // Segment Tree + DSU rollback\n    return []bool{}\n}",
        "C#": "public static bool[] Solve(int n, List<object[]> operations) {\n    // Segment Tree + DSU rollback\n    return new bool[0];\n}",
    },
},
{
    "title": "K-ésimo Número en Subarrays Dinámicos",
    "difficulty": 3000, "category": "Persistent Segment Tree", "total_solvers": 0,
    "description": (
        "Dado un array inicial nums de tamaño n, debes procesar múltiples queries del tipo:\n\n"
        "  query(l, r, k): devuelve el k-ésimo número más pequeño en el subarray nums[l..r]\n\n"
        "Este es el problema clásico de k-th order statistics en subarrays, pero con restricciones "
        "altas que obligan a usar estructuras avanzadas.\n\n"
        "Enfoque esperado:\n\n"
        "  - Construir un Persistent Segment Tree donde cada versión representa el prefijo nums[0..i]\n"
        "  - Cada nodo almacena cuántas veces aparece un valor en ese rango\n"
        "  - Para responder query(l, r, k):\n"
        "        usar version[r] - version[l-1]\n"
        "        y bajar por el árbol para encontrar el k-ésimo valor\n\n"
        "  - Requiere compresión de coordenadas\n\n"
        "Complejidad esperada:\n"
        "  O((n + q) log n)\n\n"
        "Restricciones:\n"
        "  1 ≤ n ≤ 2 * 10^5\n"
        "  1 ≤ q ≤ 2 * 10^5\n"
        "  1 ≤ nums[i] ≤ 10^9\n"
        "  1 ≤ l ≤ r ≤ n\n"
        "  1 ≤ k ≤ r - l + 1\n\n"
        "Ejemplo 1:\n"
        "  Entrada:\n"
        "    nums = [1, 5, 2, 6, 3, 7, 4]\n"
        "    queries = [\n"
        "      (2, 5, 3),\n"
        "      (4, 4, 1)\n"
        "    ]\n"
        "  Salida: [5, 6]\n\n"
        "  Explicación:\n"
        "    Subarray [5,2,6,3] → ordenado: [2,3,5,6] → k=3 → 5\n"
        "    Subarray [6] → k=1 → 6\n\n"
        "Ejemplo 2:\n"
        "  Entrada:\n"
        "    nums = [10, 20, 30, 40, 50]\n"
        "    queries = [\n"
        "      (1, 5, 2),\n"
        "      (2, 4, 2)\n"
        "    ]\n"
        "  Salida: [20, 30]\n\n"
        "Devuelve una lista con las respuestas de cada query.\n\n"
        "Escribe `solve(nums, queries)` que resuelva el problema."
    ),
    "test_cases": [
        {
            "input": "[1,5,2,6,3,7,4], [(2,5,3),(4,4,1)]",
            "expected_output": "[5, 6]"
        },
        {
            "input": "[10,20,30,40,50], [(1,5,2),(2,4,2)]",
            "expected_output": "[20, 30]"
        }
    ],
    "stub": {
        "Python": "def solve(nums, queries):\n    # Persistent Segment Tree + coordinate compression\n    pass",
        "C++": "#include <vector>\nusing namespace std;\nvector<int> solve(vector<int>& nums, vector<vector<int>>& queries) {\n    // Persistent Segment Tree\n    return {};\n}",
        "Java": "public static int[] solve(int[] nums, int[][] queries) {\n    // Persistent Segment Tree\n    return new int[0];\n}",
        "Go": "func solve(nums []int, queries [][]int) []int {\n    // Persistent Segment Tree\n    return []int{}\n}",
        "C#": "public static int[] Solve(int[] nums, int[][] queries) {\n    // Persistent Segment Tree\n    return new int[0];\n}",
    },
},
{
    "title": "Consultas Dinámicas en Árbol con Versionado Temporal",
    "difficulty": 3500, "category": "HLD + Persistent Segment Tree + Lazy Propagation", "total_solvers": 0,
    "description": (
        "Se te da un árbol con n nodos (0 a n-1), inicialmente con valor 0 en cada nodo.\n\n"
        "Debes procesar q operaciones de tres tipos:\n\n"
        "  1. update(u, v, x): suma x a todos los nodos en el camino entre u y v\n"
        "  2. query(u, v, k): devuelve el k-ésimo valor más pequeño en el camino entre u y v\n"
        "  3. rollback(t): revierte el estado del árbol al momento después de la operación t\n\n"
        "IMPORTANTE:\n"
        "  - Las operaciones son online\n"
        "  - rollback puede ocurrir en cualquier momento\n"
        "  - Después de rollback, las nuevas operaciones continúan desde ese estado\n\n"
        "Esto implica que el árbol tiene múltiples versiones (histórico de estados).\n\n"
        "Requisitos técnicos (nivel extremo):\n\n"
        "  - Descomposición Heavy-Light (HLD) para transformar paths en rangos\n"
        "  - Segment Tree persistente para mantener versiones\n"
        "  - Cada nodo del segment tree mantiene estructura ordenada (frecuencias)\n"
        "  - Lazy propagation para updates en rangos\n"
        "  - Capacidad de rollback eficiente (persistencia parcial o total)\n\n"
        "Estrategia esperada:\n\n"
        "  - Mapear el árbol a un array usando HLD\n"
        "  - Mantener múltiples versiones del segment tree\n"
        "  - Para query(u,v,k): combinar resultados de múltiples segmentos\n"
        "  - Usar técnica tipo 'k-th smallest' en segment trees persistentes\n\n"
        "Complejidad objetivo:\n"
        "  O((n + q) log^2 n)\n\n"
        "Restricciones:\n"
        "  1 ≤ n ≤ 2 * 10^5\n"
        "  1 ≤ q ≤ 2 * 10^5\n"
        "  0 ≤ u, v < n\n"
        "  |x| ≤ 10^9\n\n"
        "Ejemplo (simplificado):\n"
        "  n = 3\n"
        "  edges = [(0,1), (1,2)]\n"
        "  operations = [\n"
        "    (\"update\", 0, 2, 5),\n"
        "    (\"query\", 0, 2, 2),\n"
        "    (\"update\", 1, 2, 3),\n"
        "    (\"rollback\", 1),\n"
        "    (\"query\", 0, 2, 2)\n"
        "  ]\n\n"
        "  Explicación:\n"
        "    Después del primer update: [5,5,5]\n"
        "    query → k=2 → 5\n"
        "    Segundo update: [5,8,8]\n"
        "    rollback al estado tras operación 1 → [5,5,5]\n"
        "    query → k=2 → 5\n\n"
        "Salida: [5, 5]\n\n"
        "Devuelve una lista con los resultados de cada query.\n\n"
        "Escribe `solve(n, edges, operations)`.\n\n"
    ),
    "test_cases": [
        {
            "input": "3, [(0,1),(1,2)], [(\"update\",0,2,5),(\"query\",0,2,2),(\"update\",1,2,3),(\"rollback\",1),(\"query\",0,2,2)]",
            "expected_output": "[5, 5]"
        }
    ],
    "stub": {
        "Python": "def solve(n, edges, operations):\n    # HLD + Persistent Segment Tree + rollback\n    pass",
        "C++": "#include <vector>\n#include <tuple>\nusing namespace std;\nvector<int> solve(int n, vector<pair<int,int>>& edges, vector<tuple<string,int,int,int>> operations) {\n    // HLD + Persistent Segment Tree + rollback\n    return {};\n}",
        "Java": "public static int[] solve(int n, int[][] edges, Object[][] operations) {\n    // HLD + Persistent Segment Tree + rollback\n    return new int[0];\n}",
        "Go": "func solve(n int, edges [][]int, operations [][]interface{}) []int {\n    // HLD + Persistent Segment Tree + rollback\n    return []int{}\n}",
        "C#": "public static int[] Solve(int n, int[][] edges, object[][] operations) {\n    // HLD + Persistent Segment Tree + rollback\n    return new int[0];\n}",
    },
},
{
    "title": "Ejercicio de Idiomas",
    "title_i18n": {
        "es": "Ejercicio de Idiomas",
        "en": "Language Exercise",
        "zh": "语言练习",
    },
    "difficulty": 800, "category": "Matemáticas", "total_solvers": 0,
    "description": (
        "Dado un entero positivo n, calcula y devuelve la suma de sus dígitos.\n\n"
        "Por ejemplo, si n = 1234, los dígitos son 1, 2, 3 y 4, y su suma es 10.\n\n"
        "Restricciones:\n"
        "  1 ≤ n ≤ 10^9\n\n"
        "Ejemplo 1:\n"
        "  Entrada: n = 123\n"
        "  Salida: 6\n"
        "  Explicación: 1 + 2 + 3 = 6\n\n"
        "Ejemplo 2:\n"
        "  Entrada: n = 9875\n"
        "  Salida: 29\n"
        "  Explicación: 9 + 8 + 7 + 5 = 29\n\n"
        "Escribe `solve(n)` que devuelva la suma de los dígitos de n."
    ),
    "description_i18n": {
        "es": (
            "Dado un entero positivo n, calcula y devuelve la suma de sus dígitos.\n\n"
            "Por ejemplo, si n = 1234, los dígitos son 1, 2, 3 y 4, y su suma es 10.\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 10^9\n\n"
            "Ejemplo 1:\n"
            "  Entrada: n = 123\n"
            "  Salida: 6\n"
            "  Explicación: 1 + 2 + 3 = 6\n\n"
            "Ejemplo 2:\n"
            "  Entrada: n = 9875\n"
            "  Salida: 29\n"
            "  Explicación: 9 + 8 + 7 + 5 = 29\n\n"
            "Escribe `solve(n)` que devuelva la suma de los dígitos de n."
        ),
        "en": (
            "Given a positive integer n, compute and return the sum of its digits.\n\n"
            "For example, if n = 1234, the digits are 1, 2, 3 and 4, and their sum is 10.\n\n"
            "Constraints:\n"
            "  1 ≤ n ≤ 10^9\n\n"
            "Example 1:\n"
            "  Input: n = 123\n"
            "  Output: 6\n"
            "  Explanation: 1 + 2 + 3 = 6\n\n"
            "Example 2:\n"
            "  Input: n = 9875\n"
            "  Output: 29\n"
            "  Explanation: 9 + 8 + 7 + 5 = 29\n\n"
            "Write `solve(n)` that returns the digit sum of n."
        ),
        "zh": (
            "给定一个正整数 n，计算并返回其各位数字之和。\n\n"
            "例如，若 n = 1234，各位数字为 1、2、3 和 4，其和为 10。\n\n"
            "约束条件：\n"
            "  1 ≤ n ≤ 10^9\n\n"
            "示例 1：\n"
            "  输入：n = 123\n"
            "  输出：6\n"
            "  解释：1 + 2 + 3 = 6\n\n"
            "示例 2：\n"
            "  输入：n = 9875\n"
            "  输出：29\n"
            "  解释：9 + 8 + 7 + 5 = 29\n\n"
            "编写 `solve(n)`，返回 n 的数字之和。"
        ),
    },
    "test_cases": [
        {"input": "123",       "expected_output": "6"},
        {"input": "9875",      "expected_output": "29"},
        {"input": "1",         "expected_output": "1"},
        {"input": "1000000000","expected_output": "1"},
        {"input": "999",       "expected_output": "27"},
    ],
    "stub": {
        "Python": "def solve(n):\n    # Suma los dígitos de n\n    pass",
        "C++":    "int solve(int n) {\n    // Suma los dígitos de n\n    return 0;\n}",
        "Java":   "public static int solve(int n) {\n    // Suma los dígitos de n\n    return 0;\n}",
        "Go":     "func solve(n int) int {\n    // Suma los dígitos de n\n    return 0\n}",
        "C#":     "public static int Solve(int n) {\n    // Suma los dígitos de n\n    return 0;\n}",
    },
},
]
