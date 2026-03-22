# API/app/exercises_data.py

EXERCISES_SEED = [
    # --- ARRAYS ---
    # Fáciles (5)
    {
        "title": "Suma del Array",
        "description": "Dado un array de enteros, devuelve la suma de todos sus elementos.\n\nEscribe una función llamada `solve` que reciba una lista de enteros y devuelva su suma.",
        "difficulty": "Fácil", "category": "Arrays", "total_solvers": 142,
        "test_cases": [
            {"input": "[1, 2, 3, 4, 5]", "expected_output": "15"},
            {"input": "[10, -3, 7]", "expected_output": "14"},
            {"input": "[0, 0, 0]", "expected_output": "0"}
        ],
        "stub": {
            "Python": "def solve(nums):\n    # Tu código aquí\n    pass",
            "C++": "#include <vector>\nusing namespace std;\nint solve(vector<int> nums) {\n    // Tu código aquí\n    return 0;\n}",
            "Java": "public static int solve(int[] nums) {\n    // Tu código aquí\n    return 0;\n}",
            "Go": "func solve(nums []int) int {\n    // Tu código aquí\n    return 0\n}",
            "C#": "public static int Solve(int[] nums) {\n    // Tu código aquí\n    return 0;\n}"
        }
    },
    {
        "title": "Máximo Elemento",
        "description": "Encuentra el número más grande dentro de un array de enteros positivos.\n\nEscribe una función llamada `solve` que reciba una lista de enteros y devuelva el mayor.",
        "difficulty": "Fácil", "category": "Arrays", "total_solvers": 120,
        "test_cases": [
            {"input": "[3, 1, 4, 1, 5, 9, 2, 6]", "expected_output": "9"},
            {"input": "[100, 50, 75]", "expected_output": "100"},
            {"input": "[7]", "expected_output": "7"}
        ],
        "stub": {
            "Python": "def solve(nums):\n    # Tu código aquí\n    pass",
            "C++": "#include <vector>\nusing namespace std;\nint solve(vector<int> nums) {\n    return 0;\n}",
            "Java": "public static int solve(int[] nums) {\n    return 0;\n}",
            "Go": "func solve(nums []int) int {\n    return 0\n}",
            "C#": "public static int Solve(int[] nums) {\n    return 0;\n}"
        }
    },
    {
        "title": "Invertir Array",
        "description": "Invierte el orden de los elementos de un array.\n\nEscribe una función llamada `solve` que reciba una lista y devuelva la lista invertida.",
        "difficulty": "Fácil", "category": "Arrays", "total_solvers": 115,
        "test_cases": [
            {"input": "[1, 2, 3, 4, 5]", "expected_output": "[5, 4, 3, 2, 1]"},
            {"input": "[10, 20]", "expected_output": "[20, 10]"},
            {"input": "[42]", "expected_output": "[42]"}
        ],
        "stub": {
            "Python": "def solve(nums):\n    # Tu código aquí\n    pass",
            "C++": "#include <vector>\nusing namespace std;\nvector<int> solve(vector<int> nums) {\n    return {};\n}",
            "Java": "public static int[] solve(int[] nums) {\n    return new int[]{};\n}",
            "Go": "func solve(nums []int) []int {\n    return nil\n}",
            "C#": "public static int[] Solve(int[] nums) {\n    return new int[]{};\n}"
        }
    },
    {
        "title": "Contar Pares",
        "description": "Devuelve la cantidad de números pares que existen dentro de un array dado.\n\nEscribe una función llamada `solve` que reciba una lista de enteros y devuelva cuántos son pares.",
        "difficulty": "Fácil", "category": "Arrays", "total_solvers": 95,
        "test_cases": [
            {"input": "[1, 2, 3, 4, 5, 6]", "expected_output": "3"},
            {"input": "[10, 15, 20, 25]", "expected_output": "2"},
            {"input": "[1, 3, 5]", "expected_output": "0"}
        ],
        "stub": {
            "Python": "def solve(nums):\n    # Tu código aquí\n    pass",
            "C++": "#include <vector>\nusing namespace std;\nint solve(vector<int> nums) {\n    return 0;\n}",
            "Java": "public static int solve(int[] nums) {\n    return 0;\n}",
            "Go": "func solve(nums []int) int {\n    return 0\n}",
            "C#": "public static int Solve(int[] nums) {\n    return 0;\n}"
        }
    },
    {
        "title": "Eliminar Duplicados",
        "description": "Dado un array ordenado, elimina los elementos duplicados y devuelve el nuevo tamaño.\n\nEscribe una función llamada `solve` que reciba una lista ordenada y devuelva cuántos elementos únicos tiene.",
        "difficulty": "Fácil", "category": "Arrays", "total_solvers": 88,
        "test_cases": [
            {"input": "[1, 1, 2, 3, 3, 4]", "expected_output": "4"},
            {"input": "[1, 1, 1]", "expected_output": "1"},
            {"input": "[1, 2, 3]", "expected_output": "3"}
        ],
        "stub": {
            "Python": "def solve(nums):\n    # Tu código aquí\n    pass",
            "C++": "#include <vector>\nusing namespace std;\nint solve(vector<int> nums) {\n    return 0;\n}",
            "Java": "public static int solve(int[] nums) {\n    return 0;\n}",
            "Go": "func solve(nums []int) int {\n    return 0\n}",
            "C#": "public static int Solve(int[] nums) {\n    return 0;\n}"
        }
    },
    # Normales (3)
    {
        "title": "Rotación a la Izquierda",
        "description": "Rota todos los elementos de un array D posiciones hacia la izquierda.\n\nEscribe `solve(nums, d)` que reciba el array y el número de rotaciones, y devuelva el array rotado.",
        "difficulty": "Normal", "category": "Arrays", "total_solvers": 55,
        "test_cases": [
            {"input": "[1, 2, 3, 4, 5], 2", "expected_output": "[3, 4, 5, 1, 2]"},
            {"input": "[1, 2, 3], 1", "expected_output": "[2, 3, 1]"},
            {"input": "[1, 2, 3, 4], 4", "expected_output": "[1, 2, 3, 4]"}
        ],
        "stub": {
            "Python": "def solve(nums, d):\n    # Tu código aquí\n    pass",
            "C++": "#include <vector>\nusing namespace std;\nvector<int> solve(vector<int> nums, int d) {\n    return {};\n}",
            "Java": "public static int[] solve(int[] nums, int d) {\n    return new int[]{};\n}",
            "Go": "func solve(nums []int, d int) []int {\n    return nil\n}",
            "C#": "public static int[] Solve(int[] nums, int d) {\n    return new int[]{};\n}"
        }
    },
    {
        "title": "Array Zig-Zag",
        "description": "Reordena el array de forma que a < b > c < d > e. Devuelve el array modificado.\n\nEscribe `solve(nums)` que devuelva el array en formato zig-zag.",
        "difficulty": "Normal", "category": "Arrays", "total_solvers": 42,
        "test_cases": [
            {"input": "[4, 3, 7, 8, 6, 2, 1]", "expected_output": "[3, 7, 4, 8, 2, 6, 1]"},
            {"input": "[1, 2, 3]", "expected_output": "[1, 3, 2]"},
            {"input": "[5, 5, 5]", "expected_output": "[5, 5, 5]"}
        ],
        "stub": {
            "Python": "def solve(nums):\n    # Tu código aquí\n    pass",
            "C++": "#include <vector>\nusing namespace std;\nvector<int> solve(vector<int> nums) {\n    return {};\n}",
            "Java": "public static int[] solve(int[] nums) {\n    return new int[]{};\n}",
            "Go": "func solve(nums []int) []int {\n    return nil\n}",
            "C#": "public static int[] Solve(int[] nums) {\n    return new int[]{};\n}"
        }
    },
    {
        "title": "Suma de Sub-Array Máxima",
        "description": "Encuentra el sub-array contiguo dentro de un array 1D de números que posea la mayor suma. Implementa el algoritmo de Kadane.\n\nEscribe `solve(nums)` que devuelva la suma máxima.",
        "difficulty": "Normal", "category": "Arrays", "total_solvers": 39,
        "test_cases": [
            {"input": "[-2, 1, -3, 4, -1, 2, 1, -5, 4]", "expected_output": "6"},
            {"input": "[1]", "expected_output": "1"},
            {"input": "[-1, -2, -3]", "expected_output": "-1"}
        ],
        "stub": {
            "Python": "def solve(nums):\n    # Tu código aquí\n    pass",
            "C++": "#include <vector>\nusing namespace std;\nint solve(vector<int> nums) {\n    return 0;\n}",
            "Java": "public static int solve(int[] nums) {\n    return 0;\n}",
            "Go": "func solve(nums []int) int {\n    return 0\n}",
            "C#": "public static int Solve(int[] nums) {\n    return 0;\n}"
        }
    },
    # Difíciles (2)
    {
        "title": "Contenedor de Agua",
        "description": "Dado n enteros no negativos a1, a2, ..., an, donde cada uno representa la altura de una línea vertical en la posición i. Encuentra dos líneas que, junto con el eje x formen el contenedor que retenga más agua.\n\nEscribe `solve(heights)` que devuelva el volumen máximo de agua.",
        "difficulty": "Difícil", "category": "Arrays", "total_solvers": 12,
        "test_cases": [
            {"input": "[1, 8, 6, 2, 5, 4, 8, 3, 7]", "expected_output": "49"},
            {"input": "[1, 1]", "expected_output": "1"},
            {"input": "[4, 3, 2, 1, 4]", "expected_output": "16"}
        ],
        "stub": {
            "Python": "def solve(heights):\n    # Tu código aquí\n    pass",
            "C++": "#include <vector>\nusing namespace std;\nint solve(vector<int> heights) {\n    return 0;\n}",
            "Java": "public static int solve(int[] heights) {\n    return 0;\n}",
            "Go": "func solve(heights []int) int {\n    return 0\n}",
            "C#": "public static int Solve(int[] heights) {\n    return 0;\n}"
        }
    },
    {
        "title": "Mediana de Dos Arrays Ordenados",
        "description": "Dados dos arrays ordenados A y B de tamaños m y n respectivamente, retorna la mediana de todos sus elementos combinados. Complejidad esperada: O(log(min(m,n))).\n\nEscribe `solve(nums1, nums2)` que devuelva la mediana como float.",
        "difficulty": "Difícil", "category": "Arrays", "total_solvers": 4,
        "test_cases": [
            {"input": "[1, 3], [2]", "expected_output": "2.0"},
            {"input": "[1, 2], [3, 4]", "expected_output": "2.5"},
            {"input": "[0, 0], [0, 0]", "expected_output": "0.0"}
        ],
        "stub": {
            "Python": "def solve(nums1, nums2):\n    # Tu código aquí\n    pass",
            "C++": "#include <vector>\nusing namespace std;\ndouble solve(vector<int> nums1, vector<int> nums2) {\n    return 0.0;\n}",
            "Java": "public static double solve(int[] nums1, int[] nums2) {\n    return 0.0;\n}",
            "Go": "func solve(nums1 []int, nums2 []int) float64 {\n    return 0.0\n}",
            "C#": "public static double Solve(int[] nums1, int[] nums2) {\n    return 0.0;\n}"
        }
    },
    # --- STRINGS ---
    # Fáciles (5)
    {
        "title": "Palíndromo Simple",
        "description": "Verifica si un string se lee igual de izquierda a derecha que de derecha a izquierda, ignorando espacios y mayúsculas.\n\nEscribe `solve(s)` que devuelva True o False.",
        "difficulty": "Fácil", "category": "Strings", "total_solvers": 160,
        "test_cases": [
            {"input": "\"racecar\"", "expected_output": "True"},
            {"input": "\"hello\"", "expected_output": "False"},
            {"input": "\"A man a plan a canal Panama\"", "expected_output": "True"}
        ],
        "stub": {
            "Python": "def solve(s):\n    # Tu código aquí\n    pass",
            "C++": "#include <string>\nusing namespace std;\nbool solve(string s) {\n    return false;\n}",
            "Java": "public static boolean solve(String s) {\n    return false;\n}",
            "Go": "func solve(s string) bool {\n    return false\n}",
            "C#": "public static bool Solve(string s) {\n    return false;\n}"
        }
    },
    {
        "title": "Longitud de Última Palabra",
        "description": "Dado un string compuesto por palabras separadas por espacios, devuelve la longitud de la última palabra.\n\nEscribe `solve(s)` que devuelva un entero.",
        "difficulty": "Fácil", "category": "Strings", "total_solvers": 145,
        "test_cases": [
            {"input": "\"Hello World\"", "expected_output": "5"},
            {"input": "\"   fly me   to   the moon  \"", "expected_output": "4"},
            {"input": "\"luffy is still joyboy\"", "expected_output": "6"}
        ],
        "stub": {
            "Python": "def solve(s):\n    # Tu código aquí\n    pass",
            "C++": "#include <string>\nusing namespace std;\nint solve(string s) {\n    return 0;\n}",
            "Java": "public static int solve(String s) {\n    return 0;\n}",
            "Go": "func solve(s string) int {\n    return 0\n}",
            "C#": "public static int Solve(string s) {\n    return 0;\n}"
        }
    },
    {
        "title": "Contar Vocales",
        "description": "Determina cuántas vocales (a, e, i, o, u) contiene un string proporcionado.\n\nEscribe `solve(s)` que devuelva el número de vocales (sin distinguir mayúsculas).",
        "difficulty": "Fácil", "category": "Strings", "total_solvers": 133,
        "test_cases": [
            {"input": "\"hello\"", "expected_output": "2"},
            {"input": "\"AEIOU\"", "expected_output": "5"},
            {"input": "\"rhythm\"", "expected_output": "0"}
        ],
        "stub": {
            "Python": "def solve(s):\n    # Tu código aquí\n    pass",
            "C++": "#include <string>\nusing namespace std;\nint solve(string s) {\n    return 0;\n}",
            "Java": "public static int solve(String s) {\n    return 0;\n}",
            "Go": "func solve(s string) int {\n    return 0\n}",
            "C#": "public static int Solve(string s) {\n    return 0;\n}"
        }
    },
    {
        "title": "Invertir Palabras",
        "description": "Dado un string, invierte el orden de cada una de las palabras que lo componen.\n\nEscribe `solve(s)` que devuelva el string con las palabras en orden invertido.",
        "difficulty": "Fácil", "category": "Strings", "total_solvers": 110,
        "test_cases": [
            {"input": "\"the sky is blue\"", "expected_output": "blue is sky the"},
            {"input": "\"hello world\"", "expected_output": "world hello"},
            {"input": "\"a good   example\"", "expected_output": "example good a"}
        ],
        "stub": {
            "Python": "def solve(s):\n    # Tu código aquí\n    pass",
            "C++": "#include <string>\nusing namespace std;\nstring solve(string s) {\n    return \"\";\n}",
            "Java": "public static String solve(String s) {\n    return \"\";\n}",
            "Go": "func solve(s string) string {\n    return \"\"\n}",
            "C#": "public static string Solve(string s) {\n    return \"\";\n}"
        }
    },
    {
        "title": "Prefijo Común",
        "description": "Encuentra el prefijo común más largo entre un array de strings. Devuelve '' si no hay prefijo.\n\nEscribe `solve(strs)` que devuelva el prefijo común.",
        "difficulty": "Fácil", "category": "Strings", "total_solvers": 90,
        "test_cases": [
            {"input": "[\"flower\", \"flow\", \"flight\"]", "expected_output": "fl"},
            {"input": "[\"dog\", \"racecar\", \"car\"]", "expected_output": ""},
            {"input": "[\"interview\", \"interact\", \"interface\"]", "expected_output": "inter"}
        ],
        "stub": {
            "Python": "def solve(strs):\n    # Tu código aquí\n    pass",
            "C++": "#include <string>\n#include <vector>\nusing namespace std;\nstring solve(vector<string> strs) {\n    return \"\";\n}",
            "Java": "public static String solve(String[] strs) {\n    return \"\";\n}",
            "Go": "func solve(strs []string) string {\n    return \"\"\n}",
            "C#": "public static string Solve(string[] strs) {\n    return \"\";\n}"
        }
    },
    # Normales (4)
    {
        "title": "Anagrama Válido",
        "description": "Dados dos strings s y t, devuelve True si t es un anagrama exacto de s, compuesto por las mismas letras.\n\nEscribe `solve(s, t)` que devuelva True o False.",
        "difficulty": "Normal", "category": "Strings", "total_solvers": 65,
        "test_cases": [
            {"input": "\"anagram\", \"nagaram\"", "expected_output": "True"},
            {"input": "\"rat\", \"car\"", "expected_output": "False"},
            {"input": "\"listen\", \"silent\"", "expected_output": "True"}
        ],
        "stub": {
            "Python": "def solve(s, t):\n    # Tu código aquí\n    pass",
            "C++": "#include <string>\nusing namespace std;\nbool solve(string s, string t) {\n    return false;\n}",
            "Java": "public static boolean solve(String s, String t) {\n    return false;\n}",
            "Go": "func solve(s string, t string) bool {\n    return false\n}",
            "C#": "public static bool Solve(string s, string t) {\n    return false;\n}"
        }
    },
    {
        "title": "Substring sin Repetir",
        "description": "Dada una cadena, encuentra la longitud del substring más largo sin utilizar caracteres repetidos.\n\nEscribe `solve(s)` que devuelva un entero.",
        "difficulty": "Normal", "category": "Strings", "total_solvers": 48,
        "test_cases": [
            {"input": "\"abcabcbb\"", "expected_output": "3"},
            {"input": "\"bbbbb\"", "expected_output": "1"},
            {"input": "\"pwwkew\"", "expected_output": "3"}
        ],
        "stub": {
            "Python": "def solve(s):\n    # Tu código aquí\n    pass",
            "C++": "#include <string>\nusing namespace std;\nint solve(string s) {\n    return 0;\n}",
            "Java": "public static int solve(String s) {\n    return 0;\n}",
            "Go": "func solve(s string) int {\n    return 0\n}",
            "C#": "public static int Solve(string s) {\n    return 0;\n}"
        }
    },
    {
        "title": "Compresión de String",
        "description": "Comprime un string usando el recuento de caracteres repetidos (ej. 'aabcccccaaa' → 'a2b1c5a3').\n\nEscribe `solve(s)` que devuelva el string comprimido.",
        "difficulty": "Normal", "category": "Strings", "total_solvers": 45,
        "test_cases": [
            {"input": "\"aabcccccaaa\"", "expected_output": "a2b1c5a3"},
            {"input": "\"abc\"", "expected_output": "a1b1c1"},
            {"input": "\"aaaa\"", "expected_output": "a4"}
        ],
        "stub": {
            "Python": "def solve(s):\n    # Tu código aquí\n    pass",
            "C++": "#include <string>\nusing namespace std;\nstring solve(string s) {\n    return \"\";\n}",
            "Java": "public static String solve(String s) {\n    return \"\";\n}",
            "Go": "func solve(s string) string {\n    return \"\"\n}",
            "C#": "public static string Solve(string s) {\n    return \"\";\n}"
        }
    },
    {
        "title": "Distancia de Hamming",
        "description": "Calcula el número mínimo de sustituciones de caracteres para pasar del string A al string B de igual longitud.\n\nEscribe `solve(a, b)` que devuelva la distancia de Hamming.",
        "difficulty": "Normal", "category": "Strings", "total_solvers": 30,
        "test_cases": [
            {"input": "\"karolin\", \"kathrin\"", "expected_output": "3"},
            {"input": "\"abc\", \"abc\"", "expected_output": "0"},
            {"input": "\"AAAA\", \"BBBB\"", "expected_output": "4"}
        ],
        "stub": {
            "Python": "def solve(a, b):\n    # Tu código aquí\n    pass",
            "C++": "#include <string>\nusing namespace std;\nint solve(string a, string b) {\n    return 0;\n}",
            "Java": "public static int solve(String a, String b) {\n    return 0;\n}",
            "Go": "func solve(a string, b string) int {\n    return 0\n}",
            "C#": "public static int Solve(string a, string b) {\n    return 0;\n}"
        }
    },
    # Difíciles (1)
    {
        "title": "Palíndromo Substring Más Largo",
        "description": "Dado un string S, encuentra el substring palíndromo continuo más largo.\n\nEscribe `solve(s)` que devuelva el substring palíndromo más largo.",
        "difficulty": "Difícil", "category": "Strings", "total_solvers": 8,
        "test_cases": [
            {"input": "\"babad\"", "expected_output": "bab"},
            {"input": "\"cbbd\"", "expected_output": "bb"},
            {"input": "\"racecar\"", "expected_output": "racecar"}
        ],
        "stub": {
            "Python": "def solve(s):\n    # Tu código aquí\n    pass",
            "C++": "#include <string>\nusing namespace std;\nstring solve(string s) {\n    return \"\";\n}",
            "Java": "public static String solve(String s) {\n    return \"\";\n}",
            "Go": "func solve(s string) string {\n    return \"\"\n}",
            "C#": "public static string Solve(string s) {\n    return \"\";\n}"
        }
    },
    # --- MATH ---
    # Fáciles (5)
    {
        "title": "Factorial de N",
        "description": "Calcula el factorial de un número n no negativo.\n\nEscribe `solve(n)` que devuelva n! (factorial de n).",
        "difficulty": "Fácil", "category": "Math", "total_solvers": 170,
        "test_cases": [
            {"input": "5", "expected_output": "120"},
            {"input": "0", "expected_output": "1"},
            {"input": "10", "expected_output": "3628800"}
        ],
        "stub": {
            "Python": "def solve(n):\n    # Tu código aquí\n    pass",
            "C++": "long long solve(int n) {\n    return 0;\n}",
            "Java": "public static long solve(int n) {\n    return 0;\n}",
            "Go": "func solve(n int) int {\n    return 0\n}",
            "C#": "public static long Solve(int n) {\n    return 0;\n}"
        }
    },
    {
        "title": "Número Primo",
        "description": "Dado un entero n, determina si es un número primo.\n\nEscribe `solve(n)` que devuelva True si es primo, False si no.",
        "difficulty": "Fácil", "category": "Math", "total_solvers": 155,
        "test_cases": [
            {"input": "7", "expected_output": "True"},
            {"input": "4", "expected_output": "False"},
            {"input": "2", "expected_output": "True"}
        ],
        "stub": {
            "Python": "def solve(n):\n    # Tu código aquí\n    pass",
            "C++": "bool solve(int n) {\n    return false;\n}",
            "Java": "public static boolean solve(int n) {\n    return false;\n}",
            "Go": "func solve(n int) bool {\n    return false\n}",
            "C#": "public static bool Solve(int n) {\n    return false;\n}"
        }
    },
    {
        "title": "Secuencia Fibonacci",
        "description": "Devuelve el n-ésimo término de la secuencia de Fibonacci de manera iterativa.\n\nEscribe `solve(n)` donde F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2).",
        "difficulty": "Fácil", "category": "Math", "total_solvers": 140,
        "test_cases": [
            {"input": "10", "expected_output": "55"},
            {"input": "0", "expected_output": "0"},
            {"input": "1", "expected_output": "1"}
        ],
        "stub": {
            "Python": "def solve(n):\n    # Tu código aquí\n    pass",
            "C++": "int solve(int n) {\n    return 0;\n}",
            "Java": "public static int solve(int n) {\n    return 0;\n}",
            "Go": "func solve(n int) int {\n    return 0\n}",
            "C#": "public static int Solve(int n) {\n    return 0;\n}"
        }
    },
    {
        "title": "Suma de Dígitos",
        "description": "Dado un entero, suma todos sus dígitos repetidamente hasta obtener un resultado de un solo dígito.\n\nEscribe `solve(n)` que devuelva la raíz digital de n.",
        "difficulty": "Fácil", "category": "Math", "total_solvers": 112,
        "test_cases": [
            {"input": "493", "expected_output": "7"},
            {"input": "0", "expected_output": "0"},
            {"input": "9999", "expected_output": "9"}
        ],
        "stub": {
            "Python": "def solve(n):\n    # Tu código aquí\n    pass",
            "C++": "int solve(int n) {\n    return 0;\n}",
            "Java": "public static int solve(int n) {\n    return 0;\n}",
            "Go": "func solve(n int) int {\n    return 0\n}",
            "C#": "public static int Solve(int n) {\n    return 0;\n}"
        }
    },
    {
        "title": "Potencia de Dos",
        "description": "Verifica si el entero n es una potencia exacta de dos.\n\nEscribe `solve(n)` que devuelva True o False.",
        "difficulty": "Fácil", "category": "Math", "total_solvers": 105,
        "test_cases": [
            {"input": "16", "expected_output": "True"},
            {"input": "6", "expected_output": "False"},
            {"input": "1", "expected_output": "True"}
        ],
        "stub": {
            "Python": "def solve(n):\n    # Tu código aquí\n    pass",
            "C++": "bool solve(int n) {\n    return false;\n}",
            "Java": "public static boolean solve(int n) {\n    return false;\n}",
            "Go": "func solve(n int) bool {\n    return false\n}",
            "C#": "public static bool Solve(int n) {\n    return false;\n}"
        }
    },
    # Normales (3)
    {
        "title": "Sieve of Eratosthenes",
        "description": "Ejecuta el algoritmo de la Criba de Eratóstenes para contar los números primos estrictamente menores a N.\n\nEscribe `solve(n)` que devuelva la cantidad de primos menores que n.",
        "difficulty": "Normal", "category": "Math", "total_solvers": 52,
        "test_cases": [
            {"input": "10", "expected_output": "4"},
            {"input": "0", "expected_output": "0"},
            {"input": "20", "expected_output": "8"}
        ],
        "stub": {
            "Python": "def solve(n):\n    # Tu código aquí\n    pass",
            "C++": "int solve(int n) {\n    return 0;\n}",
            "Java": "public static int solve(int n) {\n    return 0;\n}",
            "Go": "func solve(n int) int {\n    return 0\n}",
            "C#": "public static int Solve(int n) {\n    return 0;\n}"
        }
    },
    {
        "title": "Invertir Entero",
        "description": "Dado un entero x de 32-bits con signo, devuelve x con todos sus dígitos invertidos. Si el resultado desborda el rango de 32-bits, devuelve 0.\n\nEscribe `solve(x)` que devuelva el entero invertido.",
        "difficulty": "Normal", "category": "Math", "total_solvers": 47,
        "test_cases": [
            {"input": "123", "expected_output": "321"},
            {"input": "-123", "expected_output": "-321"},
            {"input": "120", "expected_output": "21"}
        ],
        "stub": {
            "Python": "def solve(x):\n    # Tu código aquí\n    pass",
            "C++": "int solve(int x) {\n    return 0;\n}",
            "Java": "public static int solve(int x) {\n    return 0;\n}",
            "Go": "func solve(x int) int {\n    return 0\n}",
            "C#": "public static int Solve(int x) {\n    return 0;\n}"
        }
    },
    {
        "title": "Raíz Cuadrada Entera",
        "description": "Calcula y retorna la raíz cuadrada truncada del entero positivo X sin utilizar la función sqrt nativa.\n\nEscribe `solve(x)` que devuelva la parte entera de la raíz cuadrada.",
        "difficulty": "Normal", "category": "Math", "total_solvers": 38,
        "test_cases": [
            {"input": "4", "expected_output": "2"},
            {"input": "8", "expected_output": "2"},
            {"input": "9", "expected_output": "3"}
        ],
        "stub": {
            "Python": "def solve(x):\n    # Tu código aquí\n    pass",
            "C++": "int solve(int x) {\n    return 0;\n}",
            "Java": "public static int solve(int x) {\n    return 0;\n}",
            "Go": "func solve(x int) int {\n    return 0\n}",
            "C#": "public static int Solve(int x) {\n    return 0;\n}"
        }
    },
    # Difíciles (2)
    {
        "title": "Números Catalanes",
        "description": "Genera el n-ésimo número de Catalan. C(n) = (2n)! / ((n+1)! * n!), o bien usa la recurrencia C(0)=1, C(n+1) = C(n)*2*(2n+1)/(n+2).\n\nEscribe `solve(n)` que devuelva el n-ésimo número de Catalan.",
        "difficulty": "Difícil", "category": "Math", "total_solvers": 5,
        "test_cases": [
            {"input": "0", "expected_output": "1"},
            {"input": "3", "expected_output": "5"},
            {"input": "5", "expected_output": "42"}
        ],
        "stub": {
            "Python": "def solve(n):\n    # Tu código aquí\n    pass",
            "C++": "long long solve(int n) {\n    return 0;\n}",
            "Java": "public static long solve(int n) {\n    return 0;\n}",
            "Go": "func solve(n int) int {\n    return 0\n}",
            "C#": "public static long Solve(int n) {\n    return 0;\n}"
        }
    },
    {
        "title": "Subconjuntos con Suma K",
        "description": "Dado un vector de valores y un objetivo K, halla cuántos subconjuntos únicos suman exactamente K.\n\nEscribe `solve(nums, k)` que devuelva la cantidad de subconjuntos.",
        "difficulty": "Difícil", "category": "Math", "total_solvers": 3,
        "test_cases": [
            {"input": "[1, 2, 3, 4, 5], 5", "expected_output": "3"},
            {"input": "[1, 1, 1, 1], 2", "expected_output": "6"},
            {"input": "[3, 3, 3], 9", "expected_output": "1"}
        ],
        "stub": {
            "Python": "def solve(nums, k):\n    # Tu código aquí\n    pass",
            "C++": "#include <vector>\nusing namespace std;\nint solve(vector<int> nums, int k) {\n    return 0;\n}",
            "Java": "public static int solve(int[] nums, int k) {\n    return 0;\n}",
            "Go": "func solve(nums []int, k int) int {\n    return 0\n}",
            "C#": "public static int Solve(int[] nums, int k) {\n    return 0;\n}"
        }
    },
]
