# API/app/exercises_data.py
# One real competitive-programming exercise per difficulty level (800–3500).
# Each exercise has title_i18n and description_i18n in es / en / zh.

EXERCISES_SEED = [

    # ══════════════════════════════════════════
    #  800 — Potencia de Dos (LeetCode 231)
    # ══════════════════════════════════════════
    {
        "title": "Potencia de Dos",
        "difficulty": 800, "category": "Matemáticas", "total_solvers": 0,
        "description": (
            "Dado un entero n, determina si es una potencia de dos.\n\n"
            "Un número n es potencia de dos si existe k ≥ 0 tal que n = 2^k.\n\n"
            "Truco bit a bit: si n > 0 y es potencia de dos, su representación binaria tiene "
            "exactamente un bit a 1. La operación n & (n-1) borra el bit más bajo activo, "
            "así que si n > 0 y n & (n-1) == 0, entonces n es potencia de dos.\n\n"
            "Restricciones:\n"
            "  -2^31 ≤ n ≤ 2^31-1\n\n"
            "Ejemplo 1:\n"
            "  Entrada: n=1\n"
            "  Salida: True   (2^0 = 1)\n\n"
            "Ejemplo 2:\n"
            "  Entrada: n=16\n"
            "  Salida: True   (2^4 = 16)\n\n"
            "Ejemplo 3:\n"
            "  Entrada: n=3\n"
            "  Salida: False\n\n"
            "Escribe `solve(n)` que devuelva True o False."
        ),
        "test_cases": [
            {"input": "1",  "expected_output": "True"},
            {"input": "16", "expected_output": "True"},
            {"input": "3",  "expected_output": "False"},
        ],
        "stub": {
            "Python": "def solve(n):\n    # Truco: n > 0 and (n & (n-1)) == 0\n    pass",
            "C++":    "bool solve(int n) {\n    // n > 0 && (n & (n-1)) == 0\n    return false;\n}",
            "Java":   "public static boolean solve(int n) {\n    // n > 0 && (n & (n-1)) == 0\n    return false;\n}",
            "Go":     "func solve(n int) bool {\n    // n > 0 && (n & (n-1)) == 0\n    return false\n}",
            "C#":     "public static bool Solve(int n) {\n    // n > 0 && (n & (n-1)) == 0\n    return false;\n}",
        },
        "title_i18n": {
            "es": "Potencia de Dos",
            "en": "Power of Two",
            "zh": "2 的幂",
        },
        "description_i18n": {
            "es": (
                "Dado un entero n, determina si es una potencia de dos.\n\n"
                "Truco bit a bit: si n > 0 y n & (n-1) == 0, entonces n es potencia de dos.\n\n"
                "Restricciones: -2^31 ≤ n ≤ 2^31-1\n\n"
                "Ejemplo 1: n=1 → True (2^0)\n"
                "Ejemplo 2: n=16 → True (2^4)\n"
                "Ejemplo 3: n=3 → False\n\n"
                "Escribe `solve(n)` que devuelva True o False."
            ),
            "en": (
                "Given an integer n, determine whether it is a power of two.\n\n"
                "Bit trick: if n > 0 and n & (n-1) == 0, then n is a power of two. "
                "The operation n & (n-1) clears the lowest set bit of n.\n\n"
                "Constraints: -2^31 <= n <= 2^31-1\n\n"
                "Example 1: n=1 → True (2^0)\n"
                "Example 2: n=16 → True (2^4)\n"
                "Example 3: n=3 → False\n\n"
                "Write `solve(n)` returning True or False."
            ),
            "zh": (
                "给定整数 n，判断其是否为 2 的幂次方。\n\n"
                "位运算技巧：若 n > 0 且 n & (n-1) == 0，则 n 是 2 的幂次方。\n"
                "操作 n & (n-1) 会清除 n 的最低位的 1。\n\n"
                "约束条件：-2^31 ≤ n ≤ 2^31-1\n\n"
                "示例 1：n=1 → True（2^0）\n"
                "示例 2：n=16 → True（2^4）\n"
                "示例 3：n=3 → False\n\n"
                "编写 `solve(n)` 返回 True 或 False。"
            ),
        },
    },

    # ══════════════════════════════════════════
    #  1000 — Mover Ceros al Final (LeetCode 283)
    # ══════════════════════════════════════════
    {
        "title": "Mover Ceros al Final",
        "difficulty": 1000, "category": "Arrays", "total_solvers": 0,
        "description": (
            "Dado un array de enteros nums, mueve todos los ceros al final manteniendo el orden "
            "relativo de los elementos no cero. Hazlo in-place y devuelve el array modificado.\n\n"
            "Algoritmo (dos punteros):\n"
            "  Mantén un puntero de escritura lo=0.\n"
            "  Recorre el array con hi: cuando nums[hi] != 0, copia nums[hi] en nums[lo] y avanza lo.\n"
            "  Al terminar, rellena nums[lo..n-1] con ceros.\n\n"
            "Complejidad: O(n) tiempo, O(1) espacio.\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 10^4\n"
            "  -2^31 ≤ nums[i] ≤ 2^31-1\n\n"
            "Ejemplo 1:\n"
            "  Entrada: nums=[0,1,0,3,12]\n"
            "  Salida: [1,3,12,0,0]\n\n"
            "Ejemplo 2:\n"
            "  Entrada: nums=[0]\n"
            "  Salida: [0]\n\n"
            "Escribe `solve(nums)` que devuelva el array con los ceros al final."
        ),
        "test_cases": [
            {"input": "[0,1,0,3,12]", "expected_output": "[1,3,12,0,0]"},
            {"input": "[0]",          "expected_output": "[0]"},
            {"input": "[1]",          "expected_output": "[1]"},
        ],
        "stub": {
            "Python": "def solve(nums):\n    # Dos punteros: puntero de escritura lo\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nvector<int> solve(vector<int> nums) {\n    // Dos punteros: puntero de escritura lo\n    return {};\n}",
            "Java":   "public static int[] solve(int[] nums) {\n    // Dos punteros: puntero de escritura lo\n    return new int[]{};\n}",
            "Go":     "func solve(nums []int) []int {\n    // Dos punteros: puntero de escritura lo\n    return nil\n}",
            "C#":     "public static int[] Solve(int[] nums) {\n    // Dos punteros: puntero de escritura lo\n    return new int[]{};\n}",
        },
        "title_i18n": {
            "es": "Mover Ceros al Final",
            "en": "Move Zeroes",
            "zh": "移动零",
        },
        "description_i18n": {
            "es": (
                "Dado un array nums, mueve todos los ceros al final manteniendo el orden relativo "
                "de los elementos no cero. Hazlo in-place y devuelve el array.\n\n"
                "Usa dos punteros: lo (escritura) avanza solo cuando nums[hi] != 0.\n\n"
                "Ejemplo 1: [0,1,0,3,12] → [1,3,12,0,0]\n"
                "Ejemplo 2: [0] → [0]\n\n"
                "Escribe `solve(nums)` que devuelva el array modificado."
            ),
            "en": (
                "Given an integer array nums, move all zeroes to the end while maintaining "
                "the relative order of non-zero elements. Do it in-place and return the array.\n\n"
                "Two-pointer approach: use a write pointer lo that only advances when nums[hi] != 0.\n\n"
                "Example 1: [0,1,0,3,12] → [1,3,12,0,0]\n"
                "Example 2: [0] → [0]\n\n"
                "Write `solve(nums)` returning the modified array."
            ),
            "zh": (
                "给定整数数组 nums，将所有 0 移动到末尾，同时保持非零元素的相对顺序。"
                "原地修改并返回结果数组。\n\n"
                "双指针法：写指针 lo 仅在 nums[hi] != 0 时前进。\n\n"
                "示例 1：[0,1,0,3,12] → [1,3,12,0,0]\n"
                "示例 2：[0] → [0]\n\n"
                "编写 `solve(nums)` 返回修改后的数组。"
            ),
        },
    },

    # ══════════════════════════════════════════
    #  1200 — Escalera (LeetCode 70)
    # ══════════════════════════════════════════
    {
        "title": "Escalera de Peldaños",
        "difficulty": 1200, "category": "Matemáticas", "total_solvers": 0,
        "description": (
            "Estás subiendo una escalera con n peldaños. Cada vez puedes subir 1 o 2 peldaños. "
            "¿De cuántas formas distintas puedes llegar al tope?\n\n"
            "Este problema es equivalente a la sucesión de Fibonacci:\n"
            "  formas(1) = 1\n"
            "  formas(2) = 2\n"
            "  formas(n) = formas(n-1) + formas(n-2)\n\n"
            "La intuición: el último paso puede ser de 1 peldaño (venimos de n-1) "
            "o de 2 peldaños (venimos de n-2), y ambas formas son disjuntas.\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 45\n\n"
            "Ejemplo 1:\n"
            "  Entrada: n=2\n"
            "  Salida: 2  (1+1, 2)\n\n"
            "Ejemplo 2:\n"
            "  Entrada: n=3\n"
            "  Salida: 3  (1+1+1, 1+2, 2+1)\n\n"
            "Ejemplo 3:\n"
            "  Entrada: n=10\n"
            "  Salida: 89\n\n"
            "Escribe `solve(n)` que devuelva el número de formas distintas."
        ),
        "test_cases": [
            {"input": "2",  "expected_output": "2"},
            {"input": "3",  "expected_output": "3"},
            {"input": "10", "expected_output": "89"},
        ],
        "stub": {
            "Python": "def solve(n):\n    # Fibonacci: formas(n) = formas(n-1) + formas(n-2)\n    pass",
            "C++":    "int solve(int n) {\n    // Fibonacci iterativo\n    return 0;\n}",
            "Java":   "public static int solve(int n) {\n    // Fibonacci iterativo\n    return 0;\n}",
            "Go":     "func solve(n int) int {\n    // Fibonacci iterativo\n    return 0\n}",
            "C#":     "public static int Solve(int n) {\n    // Fibonacci iterativo\n    return 0;\n}",
        },
        "title_i18n": {
            "es": "Escalera de Peldaños",
            "en": "Climbing Stairs",
            "zh": "爬楼梯",
        },
        "description_i18n": {
            "es": (
                "Tienes una escalera con n peldaños. Cada vez puedes subir 1 o 2 peldaños. "
                "¿De cuántas formas distintas puedes llegar al tope?\n\n"
                "Equivalente a Fibonacci: formas(n) = formas(n-1) + formas(n-2), "
                "con formas(1)=1 y formas(2)=2.\n\n"
                "Ejemplo 1: n=2 → 2\nEjemplo 2: n=3 → 3\nEjemplo 3: n=10 → 89\n\n"
                "Escribe `solve(n)` que devuelva el número de formas."
            ),
            "en": (
                "You are climbing a staircase with n steps. Each time you can climb 1 or 2 steps. "
                "How many distinct ways can you reach the top?\n\n"
                "Equivalent to Fibonacci: ways(n) = ways(n-1) + ways(n-2), "
                "with ways(1)=1 and ways(2)=2.\n\n"
                "Example 1: n=2 → 2\nExample 2: n=3 → 3\nExample 3: n=10 → 89\n\n"
                "Write `solve(n)` returning the number of distinct ways."
            ),
            "zh": (
                "你正在爬一个有 n 级台阶的楼梯，每次可以爬 1 或 2 级台阶。"
                "有多少种不同的方法可以爬到顶部？\n\n"
                "等价于斐波那契数列：ways(n) = ways(n-1) + ways(n-2)，"
                "其中 ways(1)=1，ways(2)=2。\n\n"
                "示例 1：n=2 → 2\n示例 2：n=3 → 3\n示例 3：n=10 → 89\n\n"
                "编写 `solve(n)` 返回不同方法的数量。"
            ),
        },
    },

    # ══════════════════════════════════════════
    #  1400 — El Ladrón (LeetCode 198)
    # ══════════════════════════════════════════
    {
        "title": "El Ladrón",
        "difficulty": 1400, "category": "Arrays", "total_solvers": 0,
        "description": (
            "Eres un ladrón profesional que planea robar casas en una calle. Cada casa i tiene "
            "nums[i] unidades de dinero. No puedes robar dos casas adyacentes (activa la alarma). "
            "Calcula el máximo dinero que puedes robar esta noche.\n\n"
            "DP: define rob como la ganancia máxima hasta la casa actual.\n"
            "  prev2 = 0  (hasta hace 2 casas)\n"
            "  prev1 = 0  (hasta la casa anterior)\n"
            "  Para cada nums[i]:\n"
            "    curr = max(prev1, prev2 + nums[i])\n"
            "    prev2, prev1 = prev1, curr\n\n"
            "Complejidad: O(n) tiempo, O(1) espacio.\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 100\n"
            "  0 ≤ nums[i] ≤ 400\n\n"
            "Ejemplo 1:\n"
            "  Entrada: nums=[1,2,3,1]\n"
            "  Salida: 4  (robar casas 0 y 2: 1+3=4)\n\n"
            "Ejemplo 2:\n"
            "  Entrada: nums=[2,7,9,3,1]\n"
            "  Salida: 12  (robar casas 0,2,4: 2+9+1=12)\n\n"
            "Escribe `solve(nums)` que devuelva el máximo dinero robable."
        ),
        "test_cases": [
            {"input": "[1,2,3,1]",   "expected_output": "4"},
            {"input": "[2,7,9,3,1]", "expected_output": "12"},
            {"input": "[2,1]",       "expected_output": "2"},
        ],
        "stub": {
            "Python": "def solve(nums):\n    # curr = max(prev1, prev2 + nums[i])\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nint solve(vector<int> nums) {\n    // curr = max(prev1, prev2 + nums[i])\n    return 0;\n}",
            "Java":   "public static int solve(int[] nums) {\n    // curr = max(prev1, prev2 + nums[i])\n    return 0;\n}",
            "Go":     "func solve(nums []int) int {\n    // curr = max(prev1, prev2 + nums[i])\n    return 0\n}",
            "C#":     "public static int Solve(int[] nums) {\n    // curr = max(prev1, prev2 + nums[i])\n    return 0;\n}",
        },
        "title_i18n": {
            "es": "El Ladrón",
            "en": "House Robber",
            "zh": "打家劫舍",
        },
        "description_i18n": {
            "es": (
                "Eres un ladrón: nums[i] es el dinero en la casa i. No puedes robar dos casas "
                "adyacentes. Calcula el máximo dinero robable.\n\n"
                "DP: curr = max(prev1, prev2 + nums[i])\n\n"
                "Ejemplo 1: [1,2,3,1] → 4\nEjemplo 2: [2,7,9,3,1] → 12\n\n"
                "Escribe `solve(nums)`."
            ),
            "en": (
                "You are a robber: nums[i] is money at house i. You cannot rob two adjacent houses. "
                "Find the maximum money you can rob.\n\n"
                "DP: curr = max(prev1, prev2 + nums[i])\n\n"
                "Example 1: [1,2,3,1] → 4\nExample 2: [2,7,9,3,1] → 12\n\n"
                "Write `solve(nums)`."
            ),
            "zh": (
                "你是一个强盗：nums[i] 是第 i 所房子的金额。不能抢劫相邻的两所房子。"
                "求能抢到的最大金额。\n\n"
                "动态规划：curr = max(prev1, prev2 + nums[i])\n\n"
                "示例 1：[1,2,3,1] → 4\n示例 2：[2,7,9,3,1] → 12\n\n"
                "编写 `solve(nums)`。"
            ),
        },
    },

    # ══════════════════════════════════════════
    #  1600 — Juego de Saltos II (LeetCode 45)
    # ══════════════════════════════════════════
    {
        "title": "Juego de Saltos II",
        "difficulty": 1600, "category": "Arrays", "total_solvers": 0,
        "description": (
            "Dado un array nums donde nums[i] es la longitud máxima de salto desde la posición i, "
            "calcula el número mínimo de saltos para llegar al último índice. "
            "Siempre existe al menos una solución.\n\n"
            "Algoritmo greedy:\n"
            "  Mantén reach (alcance máximo actual), curr_end (fin del salto actual) y jumps.\n"
            "  Para cada i en [0, n-2]:\n"
            "    reach = max(reach, i + nums[i])\n"
            "    Si i == curr_end: jumps++, curr_end = reach\n\n"
            "Complejidad: O(n) tiempo, O(1) espacio.\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 10^4\n"
            "  0 ≤ nums[i] ≤ 1000\n\n"
            "Ejemplo 1:\n"
            "  Entrada: nums=[2,3,1,1,4]\n"
            "  Salida: 2  (0→1→4)\n\n"
            "Ejemplo 2:\n"
            "  Entrada: nums=[2,3,0,1,4]\n"
            "  Salida: 2  (0→1→4)\n\n"
            "Ejemplo 3:\n"
            "  Entrada: nums=[1,1,1,1]\n"
            "  Salida: 3\n\n"
            "Escribe `solve(nums)` que devuelva el mínimo de saltos."
        ),
        "test_cases": [
            {"input": "[2,3,1,1,4]", "expected_output": "2"},
            {"input": "[2,3,0,1,4]", "expected_output": "2"},
            {"input": "[1,1,1,1]",   "expected_output": "3"},
        ],
        "stub": {
            "Python": "def solve(nums):\n    # Greedy: actualiza reach y curr_end\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nint solve(vector<int> nums) {\n    // Greedy: actualiza reach y curr_end\n    return 0;\n}",
            "Java":   "public static int solve(int[] nums) {\n    // Greedy: actualiza reach y curr_end\n    return 0;\n}",
            "Go":     "func solve(nums []int) int {\n    // Greedy: actualiza reach y curr_end\n    return 0\n}",
            "C#":     "public static int Solve(int[] nums) {\n    // Greedy: actualiza reach y curr_end\n    return 0;\n}",
        },
        "title_i18n": {
            "es": "Juego de Saltos II",
            "en": "Jump Game II",
            "zh": "跳跃游戏 II",
        },
        "description_i18n": {
            "es": (
                "nums[i] es la longitud máxima de salto desde i. Calcula el mínimo número de "
                "saltos para llegar al último índice.\n\n"
                "Greedy: mantén reach (alcance máx), curr_end (fin del salto actual) y jumps.\n"
                "Para cada i en [0,n-2]: reach=max(reach, i+nums[i]); si i==curr_end: jumps++.\n\n"
                "Ejemplo 1: [2,3,1,1,4] → 2\nEjemplo 2: [1,1,1,1] → 3\n\n"
                "Escribe `solve(nums)`."
            ),
            "en": (
                "nums[i] is the maximum jump length from index i. Return the minimum number of "
                "jumps to reach the last index.\n\n"
                "Greedy: maintain reach (max reachable), curr_end (end of current jump) and jumps.\n"
                "For each i in [0,n-2]: reach=max(reach, i+nums[i]); if i==curr_end: jumps++.\n\n"
                "Example 1: [2,3,1,1,4] → 2\nExample 2: [1,1,1,1] → 3\n\n"
                "Write `solve(nums)`."
            ),
            "zh": (
                "nums[i] 表示从下标 i 处出发可以跳跃的最大长度。返回到达最后一个下标的最少跳跃次数。\n\n"
                "贪心算法：维护 reach（当前最远可达位置）、curr_end（当前跳跃的边界）和 jumps。\n"
                "对每个 i∈[0,n-2]：reach=max(reach, i+nums[i])；若 i==curr_end 则 jumps++。\n\n"
                "示例 1：[2,3,1,1,4] → 2\n示例 2：[1,1,1,1] → 3\n\n"
                "编写 `solve(nums)`。"
            ),
        },
    },

    # ══════════════════════════════════════════
    #  1800 — Cambio de Monedas (LeetCode 322)
    # ══════════════════════════════════════════
    {
        "title": "Cambio de Monedas",
        "difficulty": 1800, "category": "Matemáticas", "total_solvers": 0,
        "description": (
            "Dado un array de denominaciones de monedas coins y un entero amount, calcula el "
            "mínimo número de monedas necesarias para formar exactamente esa cantidad. "
            "Si es imposible, devuelve -1. Puedes usar cada moneda infinitas veces.\n\n"
            "DP clásico:\n"
            "  dp[0] = 0\n"
            "  dp[i] = ∞  para i > 0  (imposible por defecto)\n"
            "  Para cada i de 1 a amount:\n"
            "    Para cada moneda c: si i ≥ c → dp[i] = min(dp[i], dp[i-c] + 1)\n\n"
            "Complejidad: O(amount × len(coins)) tiempo, O(amount) espacio.\n\n"
            "Restricciones:\n"
            "  1 ≤ len(coins) ≤ 12\n"
            "  1 ≤ coins[i] ≤ 2^31-1\n"
            "  0 ≤ amount ≤ 10^4\n\n"
            "Ejemplo 1:\n"
            "  Entrada: coins=[1,5,11], amount=15\n"
            "  Salida: 3  (5+5+5)\n\n"
            "Ejemplo 2:\n"
            "  Entrada: coins=[2], amount=3\n"
            "  Salida: -1\n\n"
            "Ejemplo 3:\n"
            "  Entrada: coins=[1,2,5], amount=11\n"
            "  Salida: 3  (5+5+1)\n\n"
            "Escribe `solve(coins, amount)` que devuelva el mínimo de monedas o -1."
        ),
        "test_cases": [
            {"input": "[1,5,11], 15", "expected_output": "3"},
            {"input": "[2], 3",       "expected_output": "-1"},
            {"input": "[1,2,5], 11",  "expected_output": "3"},
        ],
        "stub": {
            "Python": "def solve(coins, amount):\n    # dp[i] = min(dp[i], dp[i-c] + 1)\n    pass",
            "C++":    "#include <vector>\n#include <climits>\nusing namespace std;\nint solve(vector<int> coins, int amount) {\n    // dp[i] = min(dp[i], dp[i-c] + 1)\n    return 0;\n}",
            "Java":   "public static int solve(int[] coins, int amount) {\n    // dp[i] = min(dp[i], dp[i-c] + 1)\n    return 0;\n}",
            "Go":     "func solve(coins []int, amount int) int {\n    // dp[i] = min(dp[i], dp[i-c] + 1)\n    return 0\n}",
            "C#":     "public static int Solve(int[] coins, int amount) {\n    // dp[i] = min(dp[i], dp[i-c] + 1)\n    return 0;\n}",
        },
        "title_i18n": {
            "es": "Cambio de Monedas",
            "en": "Coin Change",
            "zh": "零钱兑换",
        },
        "description_i18n": {
            "es": (
                "Dado un array coins y un entero amount, calcula el mínimo número de monedas "
                "para formar esa cantidad. Si es imposible, devuelve -1.\n\n"
                "DP: dp[0]=0, dp[i]=min(dp[i-c]+1) para cada moneda c.\n\n"
                "Ejemplo 1: [1,5,11], 15 → 3\nEjemplo 2: [2], 3 → -1\n\n"
                "Escribe `solve(coins, amount)`."
            ),
            "en": (
                "Given coin denominations and a target amount, return the minimum number of coins "
                "needed. Return -1 if impossible. Unlimited uses per coin.\n\n"
                "DP: dp[0]=0, dp[i]=min(dp[i-c]+1) for each coin c.\n\n"
                "Example 1: [1,5,11], 15 → 3\nExample 2: [2], 3 → -1\n\n"
                "Write `solve(coins, amount)`."
            ),
            "zh": (
                "给定硬币面额数组和目标金额 amount，求凑成该金额所需的最少硬币数。"
                "若无法凑成则返回 -1。每种硬币可无限使用。\n\n"
                "动态规划：dp[0]=0，dp[i]=min(dp[i-c]+1)，其中 c 为每种硬币面额。\n\n"
                "示例 1：[1,5,11], 15 → 3\n示例 2：[2], 3 → -1\n\n"
                "编写 `solve(coins, amount)`。"
            ),
        },
    },

    # ══════════════════════════════════════════
    #  2000 — Subsecuencia Creciente más Larga (LeetCode 300)
    # ══════════════════════════════════════════
    {
        "title": "Subsecuencia Creciente más Larga",
        "difficulty": 2000, "category": "Arrays", "total_solvers": 0,
        "description": (
            "Dado un array de enteros nums, devuelve la longitud de la subsecuencia estrictamente "
            "creciente más larga (LIS). Una subsecuencia mantiene el orden original pero no "
            "necesita ser contigua.\n\n"
            "Solución O(n²) DP:\n"
            "  dp[i] = longitud de la LIS que termina en nums[i].\n"
            "  dp[i] = 1 + max(dp[j] para j < i si nums[j] < nums[i]).\n\n"
            "Solución O(n log n) con búsqueda binaria:\n"
            "  Mantén un array tails donde tails[k] es el menor elemento final de todas las "
            "subsecuencias crecientes de longitud k+1.\n"
            "  Para cada nums[i], haz búsqueda binaria en tails para encontrar dónde insertarlo.\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 2500\n"
            "  -10^4 ≤ nums[i] ≤ 10^4\n\n"
            "Ejemplo 1:\n"
            "  Entrada: nums=[10,9,2,5,3,7,101,18]\n"
            "  Salida: 4  (2,3,7,101 o 2,5,7,101)\n\n"
            "Ejemplo 2:\n"
            "  Entrada: nums=[0,1,0,3,2,3]\n"
            "  Salida: 4  (0,1,2,3)\n\n"
            "Ejemplo 3:\n"
            "  Entrada: nums=[7,7,7,7]\n"
            "  Salida: 1\n\n"
            "Escribe `solve(nums)` que devuelva la longitud de la LIS."
        ),
        "test_cases": [
            {"input": "[10,9,2,5,3,7,101,18]", "expected_output": "4"},
            {"input": "[0,1,0,3,2,3]",          "expected_output": "4"},
            {"input": "[7,7,7,7]",               "expected_output": "1"},
        ],
        "stub": {
            "Python": "def solve(nums):\n    # dp O(n²) o bisect O(n log n)\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nint solve(vector<int> nums) {\n    // dp O(n^2) o lower_bound O(n log n)\n    return 0;\n}",
            "Java":   "public static int solve(int[] nums) {\n    // dp O(n^2) o Arrays.binarySearch O(n log n)\n    return 0;\n}",
            "Go":     "func solve(nums []int) int {\n    // dp O(n^2) o sort.SearchInts O(n log n)\n    return 0\n}",
            "C#":     "public static int Solve(int[] nums) {\n    // dp O(n^2) o Array.BinarySearch O(n log n)\n    return 0;\n}",
        },
        "title_i18n": {
            "es": "Subsecuencia Creciente más Larga",
            "en": "Longest Increasing Subsequence",
            "zh": "最长递增子序列",
        },
        "description_i18n": {
            "es": (
                "Dado nums, devuelve la longitud de la subsecuencia estrictamente creciente más larga.\n\n"
                "DP O(n²): dp[i] = 1 + max(dp[j]) para j<i con nums[j]<nums[i].\n"
                "O(n log n): array tails + búsqueda binaria.\n\n"
                "Ejemplo 1: [10,9,2,5,3,7,101,18] → 4\nEjemplo 2: [7,7,7,7] → 1\n\n"
                "Escribe `solve(nums)`."
            ),
            "en": (
                "Given nums, return the length of the longest strictly increasing subsequence.\n\n"
                "DP O(n²): dp[i] = 1 + max(dp[j]) for j<i with nums[j]<nums[i].\n"
                "O(n log n): maintain tails array + binary search.\n\n"
                "Example 1: [10,9,2,5,3,7,101,18] → 4\nExample 2: [7,7,7,7] → 1\n\n"
                "Write `solve(nums)`."
            ),
            "zh": (
                "给定 nums，返回最长严格递增子序列的长度。\n\n"
                "动态规划 O(n²)：dp[i] = 1 + max(dp[j])，其中 j<i 且 nums[j]<nums[i]。\n"
                "O(n log n)：维护 tails 数组 + 二分查找。\n\n"
                "示例 1：[10,9,2,5,3,7,101,18] → 4\n示例 2：[7,7,7,7] → 1\n\n"
                "编写 `solve(nums)`。"
            ),
        },
    },

    # ══════════════════════════════════════════
    #  2200 — Segmentación de Palabras (LeetCode 139)
    # ══════════════════════════════════════════
    {
        "title": "Segmentación de Palabras",
        "difficulty": 2200, "category": "Strings", "total_solvers": 0,
        "description": (
            "Dada una cadena s y un diccionario wordDict (lista de strings), determina si s puede "
            "segmentarse completamente en palabras del diccionario. Las palabras pueden repetirse "
            "y no es necesario usar todas.\n\n"
            "DP:\n"
            "  dp[i] = True si s[0..i-1] puede segmentarse.\n"
            "  dp[0] = True  (cadena vacía).\n"
            "  Para i de 1 a n:\n"
            "    Para j de 0 a i-1:\n"
            "      Si dp[j] es True y s[j:i] está en wordDict → dp[i] = True.\n\n"
            "Complejidad: O(n² × max_word_len) tiempo, O(n) espacio.\n\n"
            "Restricciones:\n"
            "  1 ≤ |s| ≤ 300\n"
            "  1 ≤ |wordDict| ≤ 1000\n\n"
            "Ejemplo 1:\n"
            '  Entrada: s="leetcode", wordDict=["leet","code"]\n'
            "  Salida: True\n\n"
            "Ejemplo 2:\n"
            '  Entrada: s="applepenapple", wordDict=["apple","pen"]\n'
            "  Salida: True  (apple+pen+apple)\n\n"
            "Ejemplo 3:\n"
            '  Entrada: s="catsandog", wordDict=["cats","dog","sand","and","cat"]\n'
            "  Salida: False\n\n"
            "Escribe `solve(s, wordDict)` que devuelva True o False."
        ),
        "test_cases": [
            {"input": '"leetcode", ["leet","code"]',                          "expected_output": "True"},
            {"input": '"applepenapple", ["apple","pen"]',                     "expected_output": "True"},
            {"input": '"catsandog", ["cats","dog","sand","and","cat"]',        "expected_output": "False"},
        ],
        "stub": {
            "Python": "def solve(s, wordDict):\n    # dp[i] = any(dp[j] and s[j:i] in wordSet)\n    pass",
            "C++":    "#include <string>\n#include <vector>\n#include <unordered_set>\nusing namespace std;\nbool solve(string s, vector<string> wordDict) {\n    // dp[i] = true si s[0..i-1] segmentable\n    return false;\n}",
            "Java":   "public static boolean solve(String s, String[] wordDict) {\n    // dp[i] = s[0..i-1] segmentable\n    return false;\n}",
            "Go":     "func solve(s string, wordDict []string) bool {\n    // dp[i] = s[0..i-1] segmentable\n    return false\n}",
            "C#":     "public static bool Solve(string s, string[] wordDict) {\n    // dp[i] = s[0..i-1] segmentable\n    return false;\n}",
        },
        "title_i18n": {
            "es": "Segmentación de Palabras",
            "en": "Word Break",
            "zh": "单词拆分",
        },
        "description_i18n": {
            "es": (
                'Dada la cadena s y wordDict, determina si s puede segmentarse en palabras del diccionario.\n\n'
                "DP: dp[i]=True si s[0..i-1] es segmentable. dp[0]=True.\n"
                "Para i de 1 a n, para j de 0 a i-1: si dp[j] y s[j:i] en wordDict → dp[i]=True.\n\n"
                'Ejemplo 1: "leetcode", ["leet","code"] → True\n'
                'Ejemplo 2: "catsandog", ["cats","dog",...] → False\n\n'
                "Escribe `solve(s, wordDict)`."
            ),
            "en": (
                "Given string s and wordDict, determine if s can be segmented into dictionary words.\n\n"
                "DP: dp[i]=True if s[0..i-1] is segmentable. dp[0]=True.\n"
                "For each i from 1 to n, j from 0 to i-1: if dp[j] and s[j:i] in wordDict → dp[i]=True.\n\n"
                'Example 1: "leetcode", ["leet","code"] → True\n'
                'Example 2: "catsandog", ["cats","dog",...] → False\n\n'
                "Write `solve(s, wordDict)`."
            ),
            "zh": (
                "给定字符串 s 和单词字典 wordDict，判断 s 是否可以被拆分为字典中单词的组合。\n\n"
                "动态规划：dp[i]=True 表示 s[0..i-1] 可被拆分。dp[0]=True。\n"
                "对每个 i∈[1,n]，j∈[0,i-1]：若 dp[j] 且 s[j:i] 在 wordDict 中，则 dp[i]=True。\n\n"
                '示例 1："leetcode", ["leet","code"] → True\n'
                '示例 2："catsandog", [...] → False\n\n'
                "编写 `solve(s, wordDict)`。"
            ),
        },
    },

    # ══════════════════════════════════════════
    #  2400 — Explotar Globos (LeetCode 312)
    # ══════════════════════════════════════════
    {
        "title": "Explotar Globos",
        "difficulty": 2400, "category": "Arrays", "total_solvers": 0,
        "description": (
            "Tienes n globos representados por nums. Al explotar el globo i obtienes "
            "nums[izq]*nums[i]*nums[der] monedas, donde izq y der son los globos adyacentes "
            "aún sin explotar. Maximiza el total de monedas tras explotar todos.\n\n"
            "Añade globos virtuales: arr = [1] + nums + [1].\n\n"
            "DP de intervalos O(n³):\n"
            "  dp[lo][hi] = máx monedas al explotar todos los globos en el intervalo abierto (lo,hi).\n"
            "  Prueba cada k en (lo,hi) como el ÚLTIMO globo en explotar dentro del intervalo:\n"
            "    dp[lo][hi] = max(dp[lo][k] + arr[lo]*arr[k]*arr[hi] + dp[k][hi])\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 300\n"
            "  0 ≤ nums[i] ≤ 100\n\n"
            "Ejemplo 1:\n"
            "  Entrada: nums=[3,1,5,8]\n"
            "  Salida: 167\n\n"
            "Ejemplo 2:\n"
            "  Entrada: nums=[1,5]\n"
            "  Salida: 10\n\n"
            "Ejemplo 3:\n"
            "  Entrada: nums=[1]\n"
            "  Salida: 1\n\n"
            "Escribe `solve(nums)` que devuelva el máximo de monedas."
        ),
        "test_cases": [
            {"input": "[3,1,5,8]", "expected_output": "167"},
            {"input": "[1,5]",     "expected_output": "10"},
            {"input": "[1]",       "expected_output": "1"},
        ],
        "stub": {
            "Python": "def solve(nums):\n    # arr = [1]+nums+[1]; dp[lo][hi] = max al explotar (lo,hi)\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nint solve(vector<int> nums) {\n    // arr = {1}+nums+{1}; dp de intervalos\n    return 0;\n}",
            "Java":   "public static int solve(int[] nums) {\n    // arr = [1]+nums+[1]; dp de intervalos\n    return 0;\n}",
            "Go":     "func solve(nums []int) int {\n    // arr = [1]+nums+[1]; dp de intervalos\n    return 0\n}",
            "C#":     "public static int Solve(int[] nums) {\n    // arr = [1]+nums+[1]; dp de intervalos\n    return 0;\n}",
        },
        "title_i18n": {
            "es": "Explotar Globos",
            "en": "Burst Balloons",
            "zh": "戳气球",
        },
        "description_i18n": {
            "es": (
                "Al explotar el globo i obtienes nums[izq]*nums[i]*nums[der] monedas. "
                "Maximiza el total.\n\n"
                "Añade arr=[1]+nums+[1]. DP de intervalos: dp[lo][hi] = máx al explotar (lo,hi). "
                "Prueba cada k como el último en explotar: dp[lo][hi] = max(dp[lo][k] + arr[lo]*arr[k]*arr[hi] + dp[k][hi]).\n\n"
                "Ejemplo 1: [3,1,5,8] → 167\nEjemplo 2: [1,5] → 10\n\n"
                "Escribe `solve(nums)`."
            ),
            "en": (
                "Bursting balloon i gives nums[left]*nums[i]*nums[right] coins. Maximize total coins.\n\n"
                "Add arr=[1]+nums+[1]. Interval DP: dp[lo][hi] = max coins from bursting (lo,hi). "
                "Try each k as the last burst: dp[lo][hi] = max(dp[lo][k] + arr[lo]*arr[k]*arr[hi] + dp[k][hi]).\n\n"
                "Example 1: [3,1,5,8] → 167\nExample 2: [1,5] → 10\n\n"
                "Write `solve(nums)`."
            ),
            "zh": (
                "戳破气球 i 可获得 nums[左]*nums[i]*nums[右] 枚硬币。求戳破所有气球后的最多硬币数。\n\n"
                "令 arr=[1]+nums+[1]，区间 DP：dp[lo][hi] 表示戳破区间 (lo,hi) 内气球的最多硬币。"
                "枚举最后一个被戳破的气球 k：dp[lo][hi] = max(dp[lo][k] + arr[lo]*arr[k]*arr[hi] + dp[k][hi])。\n\n"
                "示例 1：[3,1,5,8] → 167\n示例 2：[1,5] → 10\n\n"
                "编写 `solve(nums)`。"
            ),
        },
    },

    # ══════════════════════════════════════════
    #  2600 — Suma Mínima de Ruta (LeetCode 64)
    # ══════════════════════════════════════════
    {
        "title": "Suma Mínima de Ruta",
        "difficulty": 2600, "category": "Arrays", "total_solvers": 0,
        "description": (
            "Dada una cuadrícula m×n de enteros no negativos, encuentra el camino desde la "
            "esquina superior-izquierda hasta la inferior-derecha que minimice la suma. "
            "Solo puedes moverte hacia la derecha o hacia abajo.\n\n"
            "DP:\n"
            "  dp[i][j] = mínima suma para llegar a (i,j).\n"
            "  dp[0][0] = grid[0][0]\n"
            "  dp[0][j] = dp[0][j-1] + grid[0][j]   (solo puede venir de la izquierda)\n"
            "  dp[i][0] = dp[i-1][0] + grid[i][0]   (solo puede venir de arriba)\n"
            "  dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]\n\n"
            "Complejidad: O(m×n) tiempo y espacio.\n\n"
            "Restricciones:\n"
            "  1 ≤ m, n ≤ 200\n"
            "  0 ≤ grid[i][j] ≤ 200\n\n"
            "Ejemplo 1:\n"
            "  Entrada: grid=[[1,3,1],[1,5,1],[4,2,1]]\n"
            "  Salida: 7  (1→3→1→1→1)\n\n"
            "Ejemplo 2:\n"
            "  Entrada: grid=[[1,2,3],[4,5,6]]\n"
            "  Salida: 12  (1→2→3→6)\n\n"
            "Escribe `solve(grid)` que devuelva la suma mínima de ruta."
        ),
        "test_cases": [
            {"input": "[[1,3,1],[1,5,1],[4,2,1]]", "expected_output": "7"},
            {"input": "[[1,2,3],[4,5,6]]",          "expected_output": "12"},
            {"input": "[[1]]",                       "expected_output": "1"},
        ],
        "stub": {
            "Python": "def solve(grid):\n    # dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\nint solve(vector<vector<int>> grid) {\n    // dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]\n    return 0;\n}",
            "Java":   "public static int solve(int[][] grid) {\n    // dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]\n    return 0;\n}",
            "Go":     "func solve(grid [][]int) int {\n    // dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]\n    return 0\n}",
            "C#":     "public static int Solve(int[][] grid) {\n    // dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]\n    return 0;\n}",
        },
        "title_i18n": {
            "es": "Suma Mínima de Ruta",
            "en": "Minimum Path Sum",
            "zh": "最小路径和",
        },
        "description_i18n": {
            "es": (
                "Cuadrícula m×n. Encuentra el camino de arriba-izquierda a abajo-derecha "
                "con suma mínima, moviéndote solo a la derecha o abajo.\n\n"
                "DP: dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j].\n\n"
                "Ejemplo 1: [[1,3,1],[1,5,1],[4,2,1]] → 7\n"
                "Ejemplo 2: [[1,2,3],[4,5,6]] → 12\n\n"
                "Escribe `solve(grid)`."
            ),
            "en": (
                "m×n grid. Find the path from top-left to bottom-right with minimum sum, "
                "moving only right or down.\n\n"
                "DP: dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j].\n\n"
                "Example 1: [[1,3,1],[1,5,1],[4,2,1]] → 7\n"
                "Example 2: [[1,2,3],[4,5,6]] → 12\n\n"
                "Write `solve(grid)`."
            ),
            "zh": (
                "给定 m×n 的网格，找一条从左上角到右下角路径使路径和最小，只能向右或向下移动。\n\n"
                "动态规划：dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]。\n\n"
                "示例 1：[[1,3,1],[1,5,1],[4,2,1]] → 7\n"
                "示例 2：[[1,2,3],[4,5,6]] → 12\n\n"
                "编写 `solve(grid)`。"
            ),
        },
    },

    # ══════════════════════════════════════════
    #  3000 — Mínimos Cortes de Palíndromo (LeetCode 132)
    # ══════════════════════════════════════════
    {
        "title": "Mínimos Cortes de Palíndromo",
        "difficulty": 3000, "category": "Strings", "total_solvers": 0,
        "description": (
            "Dada una cadena s, devuelve el número mínimo de cortes necesarios para que "
            "cada fragmento resultante sea un palíndromo.\n\n"
            "Algoritmo O(n²):\n"
            "  1. Precalcula isPalin[i][j] = True si s[i..j] es palíndromo.\n"
            "     Expande desde centros (par e impar) para rellenar isPalin en O(n²).\n"
            "  2. DP: dp[i] = mínimo de cortes para s[0..i].\n"
            "     Si isPalin[0][i]: dp[i] = 0.\n"
            "     Si no: dp[i] = min(dp[j-1] + 1) para j en [1..i] donde isPalin[j][i] es True.\n\n"
            "Restricciones:\n"
            "  1 ≤ |s| ≤ 2000\n"
            "  s contiene solo letras minúsculas\n\n"
            "Ejemplo 1:\n"
            "  Entrada: s=\"aab\"\n"
            "  Salida: 1  (\"aa\" | \"b\")\n\n"
            "Ejemplo 2:\n"
            "  Entrada: s=\"a\"\n"
            "  Salida: 0\n\n"
            "Ejemplo 3:\n"
            "  Entrada: s=\"ab\"\n"
            "  Salida: 1\n\n"
            "Escribe `solve(s)` que devuelva el número mínimo de cortes."
        ),
        "test_cases": [
            {"input": '"aab"', "expected_output": "1"},
            {"input": '"a"',   "expected_output": "0"},
            {"input": '"ab"',  "expected_output": "1"},
        ],
        "stub": {
            "Python": "def solve(s):\n    # isPalin[i][j] + dp[i] = min cortes para s[0..i]\n    pass",
            "C++":    "#include <string>\n#include <vector>\nusing namespace std;\nint solve(string s) {\n    // isPalin[i][j] + dp[i] = min cortes para s[0..i]\n    return 0;\n}",
            "Java":   "public static int solve(String s) {\n    // isPalin[i][j] + dp[i] = min cortes para s[0..i]\n    return 0;\n}",
            "Go":     "func solve(s string) int {\n    // isPalin[i][j] + dp[i] = min cortes para s[0..i]\n    return 0\n}",
            "C#":     "public static int Solve(string s) {\n    // isPalin[i][j] + dp[i] = min cortes para s[0..i]\n    return 0;\n}",
        },
        "title_i18n": {
            "es": "Mínimos Cortes de Palíndromo",
            "en": "Palindrome Partitioning II",
            "zh": "分割回文串 II",
        },
        "description_i18n": {
            "es": (
                "Calcula el número mínimo de cortes en s para que cada fragmento sea palíndromo.\n\n"
                "O(n²): precalcula isPalin[i][j]. Luego dp[i]=0 si s[0..i] es palíndromo, "
                "si no dp[i]=min(dp[j-1]+1) para j donde isPalin[j][i].\n\n"
                'Ejemplo 1: "aab" → 1\nEjemplo 2: "a" → 0\n\n'
                "Escribe `solve(s)`."
            ),
            "en": (
                "Return the minimum cuts to partition s so every substring is a palindrome.\n\n"
                "O(n²): precompute isPalin[i][j]. Then dp[i]=0 if s[0..i] is palindrome, "
                "else dp[i]=min(dp[j-1]+1) for j where isPalin[j][i].\n\n"
                'Example 1: "aab" → 1\nExample 2: "a" → 0\n\n'
                "Write `solve(s)`."
            ),
            "zh": (
                "返回将 s 分割为若干回文子串所需的最少分割次数。\n\n"
                "O(n²)：预计算 isPalin[i][j]。然后 dp[i]=0（若 s[0..i] 是回文串），"
                "否则 dp[i]=min(dp[j-1]+1)，其中 j 满足 isPalin[j][i] 为真。\n\n"
                '示例 1："aab" → 1\n示例 2："a" → 0\n\n'
                "编写 `solve(s)`。"
            ),
        },
    },

    # ══════════════════════════════════════════
    #  3500 — Mediana de Dos Arrays Ordenados (LeetCode 4)
    # ══════════════════════════════════════════
    {
        "title": "Mediana de Dos Arrays Ordenados",
        "difficulty": 3500, "category": "Arrays", "total_solvers": 0,
        "description": (
            "Dados dos arrays de enteros ordenados nums1 (tamaño m) y nums2 (tamaño n), "
            "devuelve la mediana del array combinado. La complejidad debe ser O(log(m+n)).\n\n"
            "Algoritmo de búsqueda binaria:\n"
            "  Asegúrate de que m ≤ n (haz swap si es necesario).\n"
            "  Haz búsqueda binaria sobre nums1 para encontrar el punto de partición i tal que:\n"
            "    i + j = (m + n + 1) // 2  donde j es el punto de partición en nums2.\n"
            "  La partición es válida cuando:\n"
            "    maxLeft1 ≤ minRight2  y  maxLeft2 ≤ minRight1\n"
            "  Si es válida:\n"
            "    Si (m+n) es impar → mediana = max(maxLeft1, maxLeft2)\n"
            "    Si es par → mediana = (max(maxLeft1,maxLeft2) + min(minRight1,minRight2)) / 2.0\n\n"
            "Restricciones:\n"
            "  0 ≤ m, n ≤ 1000\n"
            "  1 ≤ m + n ≤ 2000\n"
            "  -10^6 ≤ nums1[i], nums2[i] ≤ 10^6\n\n"
            "Ejemplo 1:\n"
            "  Entrada: nums1=[1,3], nums2=[2]\n"
            "  Salida: 2.0\n\n"
            "Ejemplo 2:\n"
            "  Entrada: nums1=[1,2], nums2=[3,4]\n"
            "  Salida: 2.5  ((2+3)/2)\n\n"
            "Escribe `solve(nums1, nums2)` que devuelva la mediana como float."
        ),
        "test_cases": [
            {"input": "[1,3], [2]",   "expected_output": "2.0"},
            {"input": "[1,2], [3,4]", "expected_output": "2.5"},
            {"input": "[0,0], [0,0]", "expected_output": "0.0"},
        ],
        "stub": {
            "Python": "def solve(nums1, nums2):\n    # Búsqueda binaria O(log(min(m,n)))\n    pass",
            "C++":    "#include <vector>\nusing namespace std;\ndouble solve(vector<int> nums1, vector<int> nums2) {\n    // Búsqueda binaria O(log(min(m,n)))\n    return 0.0;\n}",
            "Java":   "public static double solve(int[] nums1, int[] nums2) {\n    // Búsqueda binaria O(log(min(m,n)))\n    return 0.0;\n}",
            "Go":     "func solve(nums1 []int, nums2 []int) float64 {\n    // Búsqueda binaria O(log(min(m,n)))\n    return 0.0\n}",
            "C#":     "public static double Solve(int[] nums1, int[] nums2) {\n    // Búsqueda binaria O(log(min(m,n)))\n    return 0.0;\n}",
        },
        "title_i18n": {
            "es": "Mediana de Dos Arrays Ordenados",
            "en": "Median of Two Sorted Arrays",
            "zh": "寻找两个正序数组的中位数",
        },
        "description_i18n": {
            "es": (
                "Dados nums1 (tamaño m) y nums2 (tamaño n) ordenados, devuelve la mediana "
                "del array combinado en O(log(m+n)).\n\n"
                "Búsqueda binaria sobre el array más pequeño: encuentra la partición i en nums1 "
                "tal que max(left1,left2) ≤ min(right1,right2).\n\n"
                "Ejemplo 1: [1,3],[2] → 2.0\nEjemplo 2: [1,2],[3,4] → 2.5\n\n"
                "Escribe `solve(nums1, nums2)`."
            ),
            "en": (
                "Given sorted arrays nums1 (size m) and nums2 (size n), return the median "
                "of the combined array in O(log(m+n)).\n\n"
                "Binary search over the smaller array: find partition i in nums1 such that "
                "max(left1,left2) <= min(right1,right2).\n\n"
                "Example 1: [1,3],[2] → 2.0\nExample 2: [1,2],[3,4] → 2.5\n\n"
                "Write `solve(nums1, nums2)`."
            ),
            "zh": (
                "给定两个升序整数数组 nums1（大小 m）和 nums2（大小 n），"
                "返回合并后数组的中位数，要求时间复杂度 O(log(m+n))。\n\n"
                "对较小的数组进行二分查找：找到分割点 i，使得 max(left1,left2) ≤ min(right1,right2)。\n\n"
                "示例 1：[1,3],[2] → 2.0\n示例 2：[1,2],[3,4] → 2.5\n\n"
                "编写 `solve(nums1, nums2)`。"
            ),
        },
    },

]
