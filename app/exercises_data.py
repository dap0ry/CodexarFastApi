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

    # ══════════════════════════════════════════
    #  800 — El Tren Nocturno de Siberia
    # ══════════════════════════════════════════
    {
        "title": "El Tren Nocturno de Siberia",
        "difficulty": 800, "category": "Arrays", "total_solvers": 0,
        "description": (
            "En la helada noche siberiana, Alexei Petróvich trabaja como vigilante nocturno en la "
            "estación de ferrocarril de Novosibirsk, una de las más concurridas de Rusia. Cada noche, "
            "exactamente n trenes numerados del 1 al n deben cruzar por el andén principal. Alexei "
            "lleva un registro minucioso de cada tren que pasa, anotando su número en un cuaderno "
            "desgastado. Sin embargo, esta noche ocurrió algo inusual: debido a un fallo catastrófico "
            "en el sistema de señalización digital, uno de los trenes cruzó el sensor dos veces "
            "(registrándose por duplicado en la bitácora) mientras que otro tren tomó una vía de "
            "desvío de emergencia y nunca fue detectado por el sensor principal.\n\n"
            "Alexei tiene la lista de los n números de trenes que aparecen en su registro esta noche. "
            "Sabe con total certeza que hay exactamente un número que aparece dos veces y exactamente "
            "un número del rango [1, n] que no aparece en absoluto. Antes del amanecer debe entregar "
            "el informe a su supervisor, identificando el tren duplicado y el tren ausente.\n\n"
            "Formalmente:\n"
            "  Se te da un array arr de n enteros. Cada entero está en el rango [1, n].\n"
            "  Exactamente un número aparece dos veces y exactamente uno del rango [1,n] falta.\n"
            "  Devuelve una lista [duplicado, faltante].\n\n"
            "Restricciones:\n"
            "  2 ≤ n ≤ 10^5\n"
            "  1 ≤ arr[i] ≤ n\n\n"
            "Ejemplo 1:\n"
            "  Entrada: arr = [1, 2, 2, 4]\n"
            "  Salida: [2, 3]\n"
            "  El número 2 aparece dos veces. El 3 (esperado en [1..4]) no aparece.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: arr = [3, 1, 3, 4, 2]\n"
            "  Salida: [3, 5]\n"
            "  El número 3 aparece dos veces. El 5 (esperado en [1..5]) no aparece.\n\n"
            "Ejemplo 3:\n"
            "  Entrada: arr = [2, 2]\n"
            "  Salida: [2, 1]\n"
            "  n=2: el 2 aparece dos veces y el 1 falta.\n\n"
            "Pista: La suma esperada de [1..n] es n*(n+1)/2. La diferencia entre suma esperada y "
            "suma real te da (faltante - duplicado). Con la suma de cuadrados puedes obtener ambos.\n\n"
            "Escribe `solve(arr)` que devuelva [duplicado, faltante]."
        ),
        "test_cases": [
            {"input": "[1, 2, 2, 4]",    "expected_output": "[2, 3]"},
            {"input": "[3, 1, 3, 4, 2]", "expected_output": "[3, 5]"},
            {"input": "[2, 2]",           "expected_output": "[2, 1]"},
        ],
        "stub": {
            "Python": (
                "def solve(arr):\n"
                "    n = len(arr)\n"
                "    # Pista: suma esperada = n*(n+1)//2\n"
                "    # (faltante - duplicado) = suma_esperada - sum(arr)\n"
                "    pass"
            ),
            "C++": (
                "#include <vector>\nusing namespace std;\n"
                "vector<int> solve(vector<int> arr) {\n"
                "    int n = arr.size();\n"
                "    // Usa suma y suma de cuadrados para hallar duplicado y faltante\n"
                "    return {};\n"
                "}"
            ),
            "Java": (
                "public static int[] solve(int[] arr) {\n"
                "    int n = arr.length;\n"
                "    // Usa suma y suma de cuadrados para hallar duplicado y faltante\n"
                "    return new int[]{};\n"
                "}"
            ),
            "Go": (
                "func solve(arr []int) []int {\n"
                "    n := len(arr)\n"
                "    _ = n\n"
                "    return nil\n"
                "}"
            ),
            "C#": (
                "public static int[] Solve(int[] arr) {\n"
                "    int n = arr.Length;\n"
                "    return new int[]{};\n"
                "}"
            ),
        },
        "title_i18n": {"es": "El Tren Nocturno de Siberia", "en": "The Night Train of Siberia", "zh": "西伯利亚夜班火车"},
        "description_i18n": {
            "es": (
                "Alexei registra n trenes numerados 1..n pero uno se registró dos veces y otro falta. "
                "Dado el array arr de n enteros, devuelve [duplicado, faltante].\n\n"
                "Restricciones: 2 ≤ n ≤ 10^5, 1 ≤ arr[i] ≤ n.\n\n"
                "Ejemplo 1: [1,2,2,4] → [2,3]\n"
                "Ejemplo 2: [3,1,3,4,2] → [3,5]\n"
                "Ejemplo 3: [2,2] → [2,1]\n\n"
                "Pista: suma esperada = n*(n+1)/2. La diferencia te da faltante - duplicado.\n\n"
                "Escribe `solve(arr)` que devuelva [duplicado, faltante]."
            ),
            "en": (
                "Alexei logs n trains numbered 1..n but one was logged twice and one is missing. "
                "Given array arr of n integers, return [duplicate, missing].\n\n"
                "Constraints: 2 ≤ n ≤ 10^5, 1 ≤ arr[i] ≤ n.\n\n"
                "Example 1: [1,2,2,4] → [2,3]\n"
                "Example 2: [3,1,3,4,2] → [3,5]\n"
                "Example 3: [2,2] → [2,1]\n\n"
                "Hint: expected sum = n*(n+1)/2. The difference gives missing - duplicate.\n\n"
                "Write `solve(arr)` returning [duplicate, missing]."
            ),
            "zh": (
                "给定 n 个整数的数组 arr（范围 [1,n]），其中一个数出现两次，一个数缺失。\n"
                "返回 [重复数, 缺失数]。\n\n"
                "提示：期望总和 = n*(n+1)/2。\n\n"
                "示例 1：[1,2,2,4] → [2,3]\n示例 2：[3,1,3,4,2] → [3,5]\n\n"
                "编写 `solve(arr)`。"
            ),
        },
    },

    # ══════════════════════════════════════════
    #  1000 — La Temporada de las Lluvias
    # ══════════════════════════════════════════
    {
        "title": "La Temporada de las Lluvias",
        "difficulty": 1000, "category": "Arrays", "total_solvers": 0,
        "description": (
            "La meteoróloga Masha trabaja en el Instituto Hidrológico de San Petersburgo. Durante la "
            "temporada de lluvias, mide diariamente la altura del río local en milímetros. Tras semanas "
            "de mediciones, obtiene una secuencia de n lecturas diarias. Masha está especialmente "
            "interesada en los períodos de crecida sostenida: aquellos tramos consecutivos en los que "
            "el nivel del río sube estrictamente cada día respecto al anterior.\n\n"
            "Una crecida sostenida es una subsecuencia contigua maximal en la que cada elemento es "
            "estrictamente mayor que el anterior. Masha quiere saber cuál es la duración (en días) de "
            "la crecida sostenida más larga registrada, pues debe presentar este dato en su informe "
            "trimestral ante el Comité de Gestión de Inundaciones.\n\n"
            "Formalmente:\n"
            "  Dado un array heights de n enteros, encuentra la longitud de la subsecuencia contigua "
            "más larga estrictamente creciente.\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 10^5\n"
            "  0 ≤ heights[i] ≤ 10^9\n\n"
            "Ejemplo 1:\n"
            "  Entrada: heights = [3, 1, 2, 4, 3, 5]\n"
            "  Salida: 3\n"
            "  Explicación: El tramo [1, 2, 4] tiene longitud 3. [3,5] tiene longitud 2. "
            "El máximo es 3.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: heights = [5, 4, 3, 2, 1]\n"
            "  Salida: 1\n"
            "  Explicación: El río bajó cada día, así que la mayor crecida dura solo 1 día.\n\n"
            "Ejemplo 3:\n"
            "  Entrada: heights = [1, 2, 3, 4, 5]\n"
            "  Salida: 5\n"
            "  Explicación: Todo el período es una crecida continua.\n\n"
            "Nota: La solución óptima es O(n): mantén un contador de racha actual y actualízalo "
            "en cada paso, reiniciándolo cuando la secuencia deje de crecer.\n\n"
            "Escribe `solve(heights)` que devuelva la longitud de la racha creciente más larga."
        ),
        "test_cases": [
            {"input": "[3, 1, 2, 4, 3, 5]", "expected_output": "3"},
            {"input": "[5, 4, 3, 2, 1]",     "expected_output": "1"},
            {"input": "[1, 2, 3, 4, 5]",     "expected_output": "5"},
        ],
        "stub": {
            "Python": (
                "def solve(heights):\n"
                "    # Recorre el array manteniendo un contador de racha actual\n"
                "    pass"
            ),
            "C++": (
                "#include <vector>\nusing namespace std;\n"
                "int solve(vector<int> heights) {\n"
                "    // Recorre manteniendo contador de racha y máximo global\n"
                "    return 0;\n"
                "}"
            ),
            "Java": (
                "public static int solve(int[] heights) {\n"
                "    // Recorre manteniendo contador de racha y máximo global\n"
                "    return 0;\n"
                "}"
            ),
            "Go": ("func solve(heights []int) int {\n    return 0\n}"),
            "C#": ("public static int Solve(int[] heights) {\n    return 0;\n}"),
        },
        "title_i18n": {"es": "La Temporada de las Lluvias", "en": "The Rainy Season", "zh": "雨季"},
        "description_i18n": {
            "es": (
                "Dado un array heights de n enteros, devuelve la longitud de la subsecuencia "
                "contigua estrictamente creciente más larga.\n\n"
                "Restricciones: 1 ≤ n ≤ 10^5, 0 ≤ heights[i] ≤ 10^9.\n\n"
                "Ejemplo 1: [3,1,2,4,3,5] → 3\n"
                "Ejemplo 2: [5,4,3,2,1] → 1\n"
                "Ejemplo 3: [1,2,3,4,5] → 5\n\n"
                "Escribe `solve(heights)`."
            ),
            "en": (
                "Given array heights of n integers, return the length of the longest strictly "
                "increasing contiguous subarray.\n\n"
                "Constraints: 1 ≤ n ≤ 10^5, 0 ≤ heights[i] ≤ 10^9.\n\n"
                "Example 1: [3,1,2,4,3,5] → 3\n"
                "Example 2: [5,4,3,2,1] → 1\n"
                "Example 3: [1,2,3,4,5] → 5\n\n"
                "Write `solve(heights)`."
            ),
            "zh": (
                "给定 n 个整数的数组 heights，返回最长严格递增连续子数组的长度。\n\n"
                "示例 1：[3,1,2,4,3,5] → 3\n示例 2：[5,4,3,2,1] → 1\n\n"
                "编写 `solve(heights)`。"
            ),
        },
    },

    # ══════════════════════════════════════════
    #  1200 — El Constructor del Puente Roto
    # ══════════════════════════════════════════
    {
        "title": "El Constructor del Puente Roto",
        "difficulty": 1200, "category": "Programación Dinámica", "total_solvers": 0,
        "description": (
            "El ingeniero Borís Ivánov supervisa la construcción de un puente peatonal de n tablones "
            "numerados del 1 al n. Para cruzar el puente, una persona parte del tablón 0 (la orilla) "
            "y debe llegar al tablón n (la otra orilla), avanzando exactamente 1 o 2 tablones en cada "
            "salto. Sin embargo, durante la inspección Borís descubrió que ciertos tablones están "
            "podridos y son peligrosos: nadie puede pisar esos tablones.\n\n"
            "La empresa constructora necesita saber de cuántas maneras distintas es posible cruzar "
            "el puente sin pisar ningún tablón podrido. El número de caminos puede ser muy grande, "
            "así que Borís quiere el resultado módulo 10^9+7.\n\n"
            "Formalmente:\n"
            "  Dado n (número de tablones) y una lista forbidden de tablones prohibidos,\n"
            "  cuenta el número de formas de llegar desde el tablón 0 hasta el tablón n,\n"
            "  saltando de 1 en 1 o de 2 en 2, sin aterrizar en ningún tablón de forbidden.\n"
            "  Devuelve el resultado módulo 10^9+7.\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 10^4\n"
            "  0 ≤ len(forbidden) ≤ n\n"
            "  Los tablones prohibidos no incluyen el 0 ni el n.\n\n"
            "Ejemplo 1:\n"
            "  Entrada: n=4, forbidden=[]\n"
            "  Salida: 5\n"
            "  Los caminos: (0→1→2→3→4), (0→1→2→4), (0→1→3→4), (0→2→3→4), (0→2→4).\n\n"
            "Ejemplo 2:\n"
            "  Entrada: n=5, forbidden=[2]\n"
            "  Salida: 2\n"
            "  El tablón 2 está podrido. Caminos válidos: (0→1→3→4→5), (0→1→3→5).\n\n"
            "Ejemplo 3:\n"
            "  Entrada: n=5, forbidden=[3]\n"
            "  Salida: 2\n"
            "  Caminos válidos: (0→1→2→4→5), (0→2→4→5).\n\n"
            "Algoritmo: Programación dinámica con dp[i] = número de formas de llegar al tablón i.\n"
            "  dp[0] = 1, dp[i] = 0 si i está en forbidden.\n"
            "  dp[i] = (dp[i-1] + dp[i-2]) % MOD  para i no prohibido.\n\n"
            "Escribe `solve(n, forbidden)` que devuelva el número de caminos módulo 10^9+7."
        ),
        "test_cases": [
            {"input": "4, []",    "expected_output": "5"},
            {"input": "5, [2]",   "expected_output": "2"},
            {"input": "5, [3]",   "expected_output": "2"},
        ],
        "stub": {
            "Python": (
                "def solve(n, forbidden):\n"
                "    MOD = 10**9 + 7\n"
                "    bad = set(forbidden)\n"
                "    # dp[i] = formas de llegar al tablon i\n"
                "    pass"
            ),
            "C++": (
                "#include <vector>\n#include <unordered_set>\nusing namespace std;\n"
                "int solve(int n, vector<int> forbidden) {\n"
                "    const int MOD = 1e9 + 7;\n"
                "    unordered_set<int> bad(forbidden.begin(), forbidden.end());\n"
                "    // dp[i] = formas de llegar al tablon i\n"
                "    return 0;\n"
                "}"
            ),
            "Java": (
                "import java.util.*;\n"
                "public static int solve(int n, int[] forbidden) {\n"
                "    final int MOD = 1_000_000_007;\n"
                "    Set<Integer> bad = new HashSet<>();\n"
                "    for (int f : forbidden) bad.add(f);\n"
                "    // dp[i] = formas de llegar al tablon i\n"
                "    return 0;\n"
                "}"
            ),
            "Go": ("func solve(n int, forbidden []int) int {\n    return 0\n}"),
            "C#": ("public static int Solve(int n, int[] forbidden) {\n    return 0;\n}"),
        },
        "title_i18n": {"es": "El Constructor del Puente Roto", "en": "The Broken Bridge Builder", "zh": "破损的桥"},
        "description_i18n": {
            "es": (
                "Desde el tablón 0 hasta el tablón n, saltando 1 o 2 tablones a la vez, "
                "sin pisar los tablones de la lista forbidden. Devuelve el número de caminos módulo 10^9+7.\n\n"
                "Restricciones: 1 ≤ n ≤ 10^4.\n\n"
                "Ejemplo 1: n=4, forbidden=[] → 5\n"
                "Ejemplo 2: n=5, forbidden=[2] → 2\n"
                "Ejemplo 3: n=5, forbidden=[3] → 2\n\n"
                "Escribe `solve(n, forbidden)`."
            ),
            "en": (
                "From step 0 to step n, jumping 1 or 2 steps at a time, without landing on "
                "any step in forbidden. Return the number of paths modulo 10^9+7.\n\n"
                "Constraints: 1 ≤ n ≤ 10^4.\n\n"
                "Example 1: n=4, forbidden=[] → 5\n"
                "Example 2: n=5, forbidden=[2] → 2\n"
                "Example 3: n=5, forbidden=[3] → 2\n\n"
                "Write `solve(n, forbidden)`."
            ),
            "zh": (
                "从台阶 0 跳到台阶 n，每次跳 1 或 2 步，不能落在 forbidden 中的台阶。"
                "返回路径数对 10^9+7 取模的结果。\n\n"
                "示例 1：n=4, forbidden=[] → 5\n示例 2：n=5, forbidden=[2] → 2\n\n"
                "编写 `solve(n, forbidden)`。"
            ),
        },
    },

    # ══════════════════════════════════════════
    #  1400 — El Barrio Circular de los Piratas
    # ══════════════════════════════════════════
    {
        "title": "El Barrio Circular de los Piratas",
        "difficulty": 1400, "category": "Programación Dinámica", "total_solvers": 0,
        "description": (
            "En la isla de Tortuga, los piratas viven en casas dispuestas en círculo a lo largo "
            "de la costa. Cada casa i contiene exactamente coins[i] monedas de oro. El famoso "
            "ladrón Jack el Veloz planea robar la mayor cantidad posible de monedas esta noche.\n\n"
            "Sin embargo, Jack tiene una regla de oro: nunca roba dos casas adyacentes en la "
            "misma noche, pues los piratas de casas vecinas se alertan mutuamente. Como las casas "
            "están en círculo, la primera y la última casa también son adyacentes y no pueden ser "
            "robadas en la misma noche.\n\n"
            "Jack necesita tu ayuda para calcular el máximo botín posible.\n\n"
            "Formalmente:\n"
            "  Dado un array circular coins de n enteros (n ≥ 2), elige un subconjunto de "
            "posiciones no adyacentes (considerando la circularidad) que maximice la suma.\n\n"
            "Restricciones:\n"
            "  2 ≤ n ≤ 10^5\n"
            "  0 ≤ coins[i] ≤ 10^9\n\n"
            "Ejemplo 1:\n"
            "  Entrada: coins = [2, 3, 2]\n"
            "  Salida: 3\n"
            "  Tomar casa 1 (3 monedas). No se pueden tomar casas 0 y 2 juntas (son adyacentes "
            "en el círculo).\n\n"
            "Ejemplo 2:\n"
            "  Entrada: coins = [1, 2, 3, 1]\n"
            "  Salida: 4\n"
            "  Tomar casas 0 y 2 (1+3=4). O casas 1 y 3 (2+1=3). Óptimo: 4.\n\n"
            "Ejemplo 3:\n"
            "  Entrada: coins = [5, 1, 1, 5]\n"
            "  Salida: 6\n"
            "  No se puede tomar ambos 5 (casas 0 y 3 son adyacentes en el círculo). "
            "Mejor: casa 0 + casa 2 = 5+1=6, o casa 1 + casa 3 = 1+5=6.\n\n"
            "Algoritmo: Resuelve dos subproblemas lineales de House Robber:\n"
            "  1) Rob desde el índice 0 hasta n-2 (excluye la última casa).\n"
            "  2) Rob desde el índice 1 hasta n-1 (excluye la primera casa).\n"
            "  La respuesta es el máximo de ambos.\n\n"
            "Escribe `solve(coins)` que devuelva el máximo botín."
        ),
        "test_cases": [
            {"input": "[2, 3, 2]",    "expected_output": "3"},
            {"input": "[1, 2, 3, 1]", "expected_output": "4"},
            {"input": "[5, 1, 1, 5]", "expected_output": "6"},
        ],
        "stub": {
            "Python": (
                "def solve(coins):\n"
                "    def rob_linear(arr):\n"
                "        prev2, prev1 = 0, 0\n"
                "        for x in arr:\n"
                "            prev2, prev1 = prev1, max(prev1, prev2 + x)\n"
                "        return prev1\n"
                "    # Resuelve dos versiones lineales y toma el maximo\n"
                "    pass"
            ),
            "C++": (
                "#include <vector>\n#include <algorithm>\nusing namespace std;\n"
                "int solve(vector<int> coins) {\n"
                "    int n = coins.size();\n"
                "    if (n == 1) return coins[0];\n"
                "    // rob_linear sobre [0..n-2] y [1..n-1]\n"
                "    return 0;\n"
                "}"
            ),
            "Java": (
                "public static int solve(int[] coins) {\n"
                "    int n = coins.length;\n"
                "    if (n == 1) return coins[0];\n"
                "    // rob_linear sobre [0..n-2] y [1..n-1]\n"
                "    return 0;\n"
                "}"
            ),
            "Go": ("func solve(coins []int) int {\n    return 0\n}"),
            "C#": ("public static int Solve(int[] coins) {\n    return 0;\n}"),
        },
        "title_i18n": {"es": "El Barrio Circular de los Piratas", "en": "The Circular Pirate District", "zh": "海盗的环形街区"},
        "description_i18n": {
            "es": (
                "Casas en círculo con monedas. No puedes robar casas adyacentes (incluida la "
                "primera y última). Devuelve el máximo botín posible.\n\n"
                "Algoritmo: dos pasadas de House Robber lineal, tomando el máximo.\n\n"
                "Ejemplo 1: [2,3,2] → 3\n"
                "Ejemplo 2: [1,2,3,1] → 4\n"
                "Ejemplo 3: [5,1,1,5] → 6\n\n"
                "Escribe `solve(coins)`."
            ),
            "en": (
                "Houses in a circle with coins. Cannot rob adjacent houses (first and last are "
                "also adjacent). Return the maximum loot.\n\n"
                "Algorithm: two linear House Robber passes, take the maximum.\n\n"
                "Example 1: [2,3,2] → 3\n"
                "Example 2: [1,2,3,1] → 4\n"
                "Example 3: [5,1,1,5] → 6\n\n"
                "Write `solve(coins)`."
            ),
            "zh": (
                "环形排列的房屋，不能偷相邻的房屋（首尾也相邻）。返回最大金额。\n\n"
                "示例 1：[2,3,2] → 3\n示例 2：[1,2,3,1] → 4\n\n"
                "编写 `solve(coins)`。"
            ),
        },
    },

    # ══════════════════════════════════════════
    #  1600 — El Censo de Inversiones
    # ══════════════════════════════════════════
    {
        "title": "El Censo de Inversiones",
        "difficulty": 1600, "category": "Divide y Vencerás", "total_solvers": 0,
        "description": (
            "La estadística Daria Volkova trabaja en el Departamento de Análisis Económico de "
            "Moscú. Su jefe le ha encargado una tarea peculiar: dada una secuencia de n valores "
            "económicos registrados en orden temporal, debe contar cuántas 'inversiones' contiene "
            "la secuencia. Una inversión es un par de índices (i, j) con i < j tal que arr[i] > arr[j], "
            "es decir, un valor anterior es mayor que uno posterior, lo cual señala una anomalía "
            "en la tendencia esperada del mercado.\n\n"
            "El número de inversiones es una medida clásica de cuán 'desordenada' está una secuencia. "
            "Si la secuencia está ordenada de menor a mayor, hay 0 inversiones. Si está ordenada de "
            "mayor a menor, hay n*(n-1)/2 inversiones (el máximo posible).\n\n"
            "Formalmente:\n"
            "  Dado un array arr de n enteros distintos, cuenta el número de pares (i,j) con "
            "i < j y arr[i] > arr[j].\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 10^5\n"
            "  -10^9 ≤ arr[i] ≤ 10^9\n"
            "  Los valores son distintos entre sí.\n\n"
            "Ejemplo 1:\n"
            "  Entrada: arr = [2, 4, 1, 3, 5]\n"
            "  Salida: 3\n"
            "  Las inversiones son: (2,1), (4,1), (4,3). Los índices son (0,2), (1,2), (1,3).\n\n"
            "Ejemplo 2:\n"
            "  Entrada: arr = [1, 2, 3, 4, 5]\n"
            "  Salida: 0\n"
            "  La secuencia está perfectamente ordenada: no hay inversiones.\n\n"
            "Ejemplo 3:\n"
            "  Entrada: arr = [5, 4, 3, 2, 1]\n"
            "  Salida: 10\n"
            "  Máximo posible para n=5: 5*4/2 = 10.\n\n"
            "Algoritmo: Merge Sort modificado. Durante la fase de mezcla, cuando tomamos un elemento "
            "del sub-array derecho por encima de uno del izquierdo, sumamos el número de elementos "
            "restantes en el sub-array izquierdo al contador de inversiones. Complejidad: O(n log n).\n"
            "Alternativamente, usa un árbol de Fenwick (BIT) para consultas de prefijo.\n\n"
            "Escribe `solve(arr)` que devuelva el número total de inversiones."
        ),
        "test_cases": [
            {"input": "[2, 4, 1, 3, 5]", "expected_output": "3"},
            {"input": "[1, 2, 3, 4, 5]", "expected_output": "0"},
            {"input": "[5, 4, 3, 2, 1]", "expected_output": "10"},
        ],
        "stub": {
            "Python": (
                "def solve(arr):\n"
                "    # Merge sort modificado: cuenta inversiones durante la mezcla\n"
                "    def merge_count(a):\n"
                "        if len(a) <= 1:\n"
                "            return a, 0\n"
                "        mid = len(a) // 2\n"
                "        left, lc = merge_count(a[:mid])\n"
                "        right, rc = merge_count(a[mid:])\n"
                "        merged, mc = [], 0\n"
                "        i = j = 0\n"
                "        # Completa la mezcla y cuenta\n"
                "        pass\n"
                "    _, count = merge_count(arr)\n"
                "    return count"
            ),
            "C++": (
                "#include <vector>\nusing namespace std;\n"
                "long long merge_count(vector<int>& arr, int l, int r) {\n"
                "    if (r - l <= 1) return 0;\n"
                "    int mid = (l + r) / 2;\n"
                "    long long cnt = merge_count(arr, l, mid) + merge_count(arr, mid, r);\n"
                "    vector<int> tmp;\n"
                "    int i = l, j = mid;\n"
                "    while (i < mid && j < r) {\n"
                "        if (arr[i] <= arr[j]) tmp.push_back(arr[i++]);\n"
                "        else { cnt += mid - i; tmp.push_back(arr[j++]); }\n"
                "    }\n"
                "    while (i < mid) tmp.push_back(arr[i++]);\n"
                "    while (j < r)   tmp.push_back(arr[j++]);\n"
                "    for (int k = l; k < r; k++) arr[k] = tmp[k - l];\n"
                "    return cnt;\n"
                "}\n"
                "long long solve(vector<int> arr) {\n"
                "    return merge_count(arr, 0, arr.size());\n"
                "}"
            ),
            "Java": (
                "public static long solve(int[] arr) {\n"
                "    return mergeCount(arr, 0, arr.length);\n"
                "}\n"
                "static long mergeCount(int[] arr, int l, int r) {\n"
                "    if (r - l <= 1) return 0;\n"
                "    int mid = (l + r) / 2;\n"
                "    long cnt = mergeCount(arr, l, mid) + mergeCount(arr, mid, r);\n"
                "    int[] tmp = new int[r - l];\n"
                "    int i = l, j = mid, k = 0;\n"
                "    while (i < mid && j < r) {\n"
                "        if (arr[i] <= arr[j]) tmp[k++] = arr[i++];\n"
                "        else { cnt += mid - i; tmp[k++] = arr[j++]; }\n"
                "    }\n"
                "    while (i < mid) tmp[k++] = arr[i++];\n"
                "    while (j < r)   tmp[k++] = arr[j++];\n"
                "    System.arraycopy(tmp, 0, arr, l, r - l);\n"
                "    return cnt;\n"
                "}"
            ),
            "Go": ("func solve(arr []int) int64 {\n    return 0\n}"),
            "C#": ("public static long Solve(int[] arr) {\n    return 0;\n}"),
        },
        "title_i18n": {"es": "El Censo de Inversiones", "en": "The Inversion Census", "zh": "逆序对计数"},
        "description_i18n": {
            "es": (
                "Dado arr de n enteros distintos, cuenta los pares (i,j) con i<j y arr[i]>arr[j].\n\n"
                "Algoritmo: Merge Sort modificado, O(n log n).\n\n"
                "Ejemplo 1: [2,4,1,3,5] → 3\n"
                "Ejemplo 2: [1,2,3,4,5] → 0\n"
                "Ejemplo 3: [5,4,3,2,1] → 10\n\n"
                "Escribe `solve(arr)`."
            ),
            "en": (
                "Given array arr of n distinct integers, count pairs (i,j) with i<j and arr[i]>arr[j].\n\n"
                "Algorithm: modified Merge Sort, O(n log n).\n\n"
                "Example 1: [2,4,1,3,5] → 3\n"
                "Example 2: [1,2,3,4,5] → 0\n"
                "Example 3: [5,4,3,2,1] → 10\n\n"
                "Write `solve(arr)`."
            ),
            "zh": (
                "给定 n 个不同整数的数组，计算满足 i<j 且 arr[i]>arr[j] 的对数。\n\n"
                "算法：归并排序变体，O(n log n)。\n\n"
                "示例 1：[2,4,1,3,5] → 3\n示例 3：[5,4,3,2,1] → 10\n\n"
                "编写 `solve(arr)`。"
            ),
        },
    },

    # ══════════════════════════════════════════
    #  1800 — La Exploradora de Palíndromos
    # ══════════════════════════════════════════
    {
        "title": "La Exploradora de Palíndromos",
        "difficulty": 1800, "category": "Strings", "total_solvers": 0,
        "description": (
            "La lingüista computacional Elena Sorokina trabaja en el Laboratorio de Lingüística "
            "de la Universidad Estatal de Moscú. Su área de investigación son los palíndromos: "
            "cadenas que se leen igual de izquierda a derecha que de derecha a izquierda.\n\n"
            "Elena está analizando una cadena de texto de longitud n y quiere encontrar la "
            "subcadena contigua más larga que sea un palíndromo. Este problema tiene aplicaciones "
            "en bioinformática (búsqueda de estructuras en ADN), criptografía y compresión de datos.\n\n"
            "Una subcadena palindrómica puede expandirse desde un centro: para palíndromos de "
            "longitud impar, el centro es un único carácter; para palíndromos de longitud par, "
            "el centro está entre dos caracteres iguales consecutivos.\n\n"
            "Formalmente:\n"
            "  Dada una cadena s de longitud n, devuelve la longitud de la subcadena palindrómica "
            "más larga contenida en s.\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 1000\n"
            "  s contiene solo letras minúsculas del alfabeto inglés.\n\n"
            "Ejemplo 1:\n"
            "  Entrada: s = \"babad\"\n"
            "  Salida: 3\n"
            "  Tanto \"bab\" (posiciones 0-2) como \"aba\" (posiciones 1-3) son palíndromos de longitud 3.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: s = \"cbbd\"\n"
            "  Salida: 2\n"
            "  \"bb\" (posiciones 1-2) es el palíndromo más largo.\n\n"
            "Ejemplo 3:\n"
            "  Entrada: s = \"racecar\"\n"
            "  Salida: 7\n"
            "  Toda la cadena es un palíndromo.\n\n"
            "Algoritmo (Expand Around Center):\n"
            "  Para cada posición i, expande hacia afuera considerando:\n"
            "  a) Centro en i (palíndromos impares): s[i-k] == s[i+k]\n"
            "  b) Centro entre i e i+1 (palíndromos pares): s[i-k+1] == s[i+k]\n"
            "  Actualiza el máximo en cada expansión. Complejidad: O(n²).\n"
            "  Existe el algoritmo de Manacher que resuelve esto en O(n), si te atreves.\n\n"
            "Escribe `solve(s)` que devuelva la longitud del palíndromo más largo."
        ),
        "test_cases": [
            {"input": '"babad"',   "expected_output": "3"},
            {"input": '"cbbd"',    "expected_output": "2"},
            {"input": '"racecar"', "expected_output": "7"},
        ],
        "stub": {
            "Python": (
                "def solve(s):\n"
                "    def expand(l, r):\n"
                "        while l >= 0 and r < len(s) and s[l] == s[r]:\n"
                "            l -= 1; r += 1\n"
                "        return r - l - 1\n"
                "    # Para cada i expande impar (i,i) y par (i,i+1)\n"
                "    pass"
            ),
            "C++": (
                "#include <string>\n#include <algorithm>\nusing namespace std;\n"
                "int solve(string s) {\n"
                "    int n = s.size(), best = 1;\n"
                "    for (int i = 0; i < n; i++) {\n"
                "        // Expand impar\n"
                "        for (int l = i, r = i; l >= 0 && r < n && s[l] == s[r]; l--, r++)\n"
                "            best = max(best, r - l + 1);\n"
                "        // Expand par\n"
                "        for (int l = i, r = i+1; l >= 0 && r < n && s[l] == s[r]; l--, r++)\n"
                "            best = max(best, r - l + 1);\n"
                "    }\n"
                "    return best;\n"
                "}"
            ),
            "Java": (
                "public static int solve(String s) {\n"
                "    int n = s.length(), best = 1;\n"
                "    for (int i = 0; i < n; i++) {\n"
                "        // Expand impar\n"
                "        for (int l = i, r = i; l >= 0 && r < n && s.charAt(l)==s.charAt(r); l--, r++)\n"
                "            best = Math.max(best, r - l + 1);\n"
                "        // Expand par\n"
                "        for (int l = i, r = i+1; l >= 0 && r < n && s.charAt(l)==s.charAt(r); l--, r++)\n"
                "            best = Math.max(best, r - l + 1);\n"
                "    }\n"
                "    return best;\n"
                "}"
            ),
            "Go": ("func solve(s string) int {\n    return 0\n}"),
            "C#": ("public static int Solve(string s) {\n    return 0;\n}"),
        },
        "title_i18n": {"es": "La Exploradora de Palíndromos", "en": "The Palindrome Explorer", "zh": "回文串探索者"},
        "description_i18n": {
            "es": (
                "Dada una cadena s, devuelve la longitud de la subcadena palindrómica más larga.\n\n"
                "Restricciones: 1 ≤ len(s) ≤ 1000, solo minúsculas.\n\n"
                "Ejemplo 1: \"babad\" → 3\nEjemplo 2: \"cbbd\" → 2\nEjemplo 3: \"racecar\" → 7\n\n"
                "Escribe `solve(s)`."
            ),
            "en": (
                "Given string s, return the length of the longest palindromic substring.\n\n"
                "Constraints: 1 ≤ len(s) ≤ 1000, lowercase only.\n\n"
                "Example 1: \"babad\" → 3\nExample 2: \"cbbd\" → 2\nExample 3: \"racecar\" → 7\n\n"
                "Write `solve(s)`."
            ),
            "zh": (
                "给定字符串 s，返回最长回文子串的长度。\n\n"
                "示例 1：\"babad\" → 3\n示例 2：\"racecar\" → 7\n\n编写 `solve(s)`。"
            ),
        },
    },

    # ══════════════════════════════════════════
    #  2000 — La Teoría del NIM
    # ══════════════════════════════════════════
    {
        "title": "La Teoría del NIM",
        "difficulty": 2000, "category": "Matemáticas", "total_solvers": 0,
        "description": (
            "En el Instituto de Matemáticas Discretas de Praga, el profesor Novák enseña teoría "
            "de juegos combinatorios. Hoy toca el famoso juego del NIM, inventado y analizado "
            "matemáticamente por Charles Bouton en 1901.\n\n"
            "El juego se desarrolla así: hay n montones de piedras sobre la mesa. Dos jugadores "
            "se turnan. En cada turno, un jugador DEBE elegir exactamente uno de los montones y "
            "retirar de él cualquier número de piedras (al menos una). El jugador que retire la "
            "última piedra de la mesa GANA.\n\n"
            "Ambos jugadores juegan de forma óptima (siempre hacen la mejor jugada posible). "
            "Tu tarea es determinar si el PRIMER jugador tiene una estrategia ganadora.\n\n"
            "La solución es uno de los resultados más elegantes de la matemática combinatoria:\n"
            "  El primer jugador gana si y solo si el XOR (OR exclusivo a nivel de bits) "
            "de los tamaños de todos los montones es distinto de cero.\n\n"
            "Intuición: si XOR = 0 (posición P), cualquier movimiento del primer jugador creará "
            "XOR ≠ 0, y el segundo jugador siempre podrá restaurar XOR = 0. Si XOR ≠ 0 (posición N), "
            "el primer jugador puede siempre hacer un movimiento que deje XOR = 0.\n\n"
            "Formalmente:\n"
            "  Dado un array piles de n enteros positivos, devuelve True si el primer jugador "
            "gana con juego óptimo, False si el segundo jugador gana.\n\n"
            "Restricciones:\n"
            "  1 ≤ n ≤ 10^5\n"
            "  1 ≤ piles[i] ≤ 10^9\n\n"
            "Ejemplo 1:\n"
            "  Entrada: piles = [3, 4, 5]\n"
            "  Salida: True\n"
            "  3 XOR 4 = 7, 7 XOR 5 = 2 ≠ 0. El primer jugador gana.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: piles = [1, 2, 3]\n"
            "  Salida: False\n"
            "  1 XOR 2 = 3, 3 XOR 3 = 0. El segundo jugador gana.\n\n"
            "Ejemplo 3:\n"
            "  Entrada: piles = [4, 4]\n"
            "  Salida: False\n"
            "  4 XOR 4 = 0. El segundo jugador gana (simetría perfecta).\n\n"
            "Nota avanzada: Esta propiedad del XOR se generaliza al teorema de Sprague-Grundy, "
            "que permite analizar cualquier juego combinatorio imparcial descomponiéndolo en "
            "sub-juegos y calculando su valor Grundy.\n\n"
            "Escribe `solve(piles)` que devuelva True si gana el primer jugador."
        ),
        "test_cases": [
            {"input": "[3, 4, 5]", "expected_output": "True"},
            {"input": "[1, 2, 3]", "expected_output": "False"},
            {"input": "[4, 4]",    "expected_output": "False"},
        ],
        "stub": {
            "Python": (
                "def solve(piles):\n"
                "    # XOR de todos los montones != 0 => primer jugador gana\n"
                "    pass"
            ),
            "C++": (
                "#include <vector>\nusing namespace std;\n"
                "bool solve(vector<int> piles) {\n"
                "    int xorSum = 0;\n"
                "    for (int p : piles) xorSum ^= p;\n"
                "    return xorSum != 0;\n"
                "}"
            ),
            "Java": (
                "public static boolean solve(int[] piles) {\n"
                "    int xorSum = 0;\n"
                "    for (int p : piles) xorSum ^= p;\n"
                "    return xorSum != 0;\n"
                "}"
            ),
            "Go": ("func solve(piles []int) bool {\n    x := 0\n    for _, p := range piles { x ^= p }\n    return x != 0\n}"),
            "C#": ("public static bool Solve(int[] piles) {\n    int x = 0;\n    foreach (var p in piles) x ^= p;\n    return x != 0;\n}"),
        },
        "title_i18n": {"es": "La Teoría del NIM", "en": "The Theory of NIM", "zh": "NIM 游戏理论"},
        "description_i18n": {
            "es": (
                "Juego NIM: n montones, los jugadores turnan retirando piedras. El que retire la "
                "última gana. ¿Gana el primer jugador con juego óptimo?\n\n"
                "Solución: XOR de todos los montones ≠ 0 ⟹ primer jugador gana.\n\n"
                "Ejemplo 1: [3,4,5] → True (XOR=2)\n"
                "Ejemplo 2: [1,2,3] → False (XOR=0)\n"
                "Ejemplo 3: [4,4] → False (XOR=0)\n\n"
                "Escribe `solve(piles)`."
            ),
            "en": (
                "NIM game: n piles, players alternate removing stones. Last to remove wins. "
                "Does the first player win with optimal play?\n\n"
                "Solution: XOR of all piles ≠ 0 ⟹ first player wins.\n\n"
                "Example 1: [3,4,5] → True\nExample 2: [1,2,3] → False\n\n"
                "Write `solve(piles)`."
            ),
            "zh": (
                "NIM 游戏：n 堆石头，轮流取，取最后一颗赢。先手必胜当且仅当所有堆的 XOR ≠ 0。\n\n"
                "示例 1：[3,4,5] → True\n示例 2：[1,2,3] → False\n\n"
                "编写 `solve(piles)`。"
            ),
        },
    },

    # ══════════════════════════════════════════
    #  2200 — El Cambista del Imperio Romano
    # ══════════════════════════════════════════
    {
        "title": "El Cambista del Imperio Romano",
        "difficulty": 2200, "category": "Programación Dinámica", "total_solvers": 0,
        "description": (
            "Marco Aurelio Fortunato es cambista en el mercado central de Roma. Cada día "
            "recibe bolsas de denarios y debe cambiarlas usando las monedas disponibles en "
            "su caja. A diferencia de otros problemas de cambio de monedas, aquí no importa "
            "el número mínimo de monedas: Marco quiere saber de cuántas MANERAS DISTINTAS "
            "puede formar exactamente una cantidad dada usando las monedas disponibles, donde "
            "cada tipo de moneda puede usarse tantas veces como sea necesario.\n\n"
            "Este problema es el clásico 'Coin Change 2' y tiene aplicaciones en combinatoria, "
            "probabilidad discreta y teoría de números.\n\n"
            "Formalmente:\n"
            "  Dado un array coins de denominaciones y un entero amount,\n"
            "  devuelve el número de combinaciones distintas para formar exactamente amount.\n"
            "  Cada moneda puede usarse ilimitadas veces. El orden no importa: [1,2] y [2,1] "
            "son la misma combinación.\n\n"
            "Restricciones:\n"
            "  1 ≤ len(coins) ≤ 300\n"
            "  1 ≤ coins[i] ≤ 5000\n"
            "  0 ≤ amount ≤ 5000\n"
            "  Los valores de coins son distintos entre sí.\n\n"
            "Ejemplo 1:\n"
            "  Entrada: coins = [1, 2, 5], amount = 5\n"
            "  Salida: 4\n"
            "  Las combinaciones son: [5], [2,2,1], [2,1,1,1], [1,1,1,1,1].\n\n"
            "Ejemplo 2:\n"
            "  Entrada: coins = [2], amount = 3\n"
            "  Salida: 0\n"
            "  Es imposible formar 3 con monedas de valor 2.\n\n"
            "Ejemplo 3:\n"
            "  Entrada: coins = [1, 2, 3], amount = 4\n"
            "  Salida: 4\n"
            "  Las combinaciones: [1,1,1,1], [1,1,2], [2,2], [1,3].\n\n"
            "Algoritmo: Programación dinámica 1D.\n"
            "  dp[0] = 1 (hay exactamente 1 forma de formar 0: no usar ninguna moneda).\n"
            "  Para cada moneda c (en el exterior) y para cada j de c a amount:\n"
            "    dp[j] += dp[j - c]\n"
            "  El orden del bucle externo (monedas) vs interno (cantidad) es crucial: "
            "al iterar monedas en el exterior evitamos contar permutaciones como combinaciones.\n\n"
            "Escribe `solve(coins, amount)` que devuelva el número de combinaciones."
        ),
        "test_cases": [
            {"input": "[1, 2, 5], 5", "expected_output": "4"},
            {"input": "[2], 3",        "expected_output": "0"},
            {"input": "[1, 2, 3], 4",  "expected_output": "4"},
        ],
        "stub": {
            "Python": (
                "def solve(coins, amount):\n"
                "    dp = [0] * (amount + 1)\n"
                "    dp[0] = 1\n"
                "    # Para cada moneda, actualiza dp[j] += dp[j - coin]\n"
                "    pass"
            ),
            "C++": (
                "#include <vector>\nusing namespace std;\n"
                "int solve(vector<int> coins, int amount) {\n"
                "    vector<int> dp(amount + 1, 0);\n"
                "    dp[0] = 1;\n"
                "    for (int c : coins)\n"
                "        for (int j = c; j <= amount; j++)\n"
                "            dp[j] += dp[j - c];\n"
                "    return dp[amount];\n"
                "}"
            ),
            "Java": (
                "public static int solve(int[] coins, int amount) {\n"
                "    int[] dp = new int[amount + 1];\n"
                "    dp[0] = 1;\n"
                "    for (int c : coins)\n"
                "        for (int j = c; j <= amount; j++)\n"
                "            dp[j] += dp[j - c];\n"
                "    return dp[amount];\n"
                "}"
            ),
            "Go": ("func solve(coins []int, amount int) int {\n    dp := make([]int, amount+1)\n    dp[0] = 1\n    for _, c := range coins {\n        for j := c; j <= amount; j++ {\n            dp[j] += dp[j-c]\n        }\n    }\n    return dp[amount]\n}"),
            "C#": ("public static int Solve(int[] coins, int amount) {\n    var dp = new int[amount+1];\n    dp[0] = 1;\n    foreach (var c in coins)\n        for (int j = c; j <= amount; j++)\n            dp[j] += dp[j-c];\n    return dp[amount];\n}"),
        },
        "title_i18n": {"es": "El Cambista del Imperio Romano", "en": "The Roman Empire Money Changer", "zh": "罗马帝国的换币官"},
        "description_i18n": {
            "es": (
                "Dado coins (denominaciones) y amount, devuelve el número de combinaciones "
                "distintas para formar amount (cada moneda usable ilimitadamente, orden no importa).\n\n"
                "Restricciones: 1 ≤ len(coins) ≤ 300, 0 ≤ amount ≤ 5000.\n\n"
                "Ejemplo 1: [1,2,5], 5 → 4\n"
                "Ejemplo 2: [2], 3 → 0\n"
                "Ejemplo 3: [1,2,3], 4 → 4\n\n"
                "Escribe `solve(coins, amount)`."
            ),
            "en": (
                "Given coins (denominations) and amount, return the number of distinct combinations "
                "to make amount (unlimited use, order doesn't matter).\n\n"
                "Constraints: 1 ≤ len(coins) ≤ 300, 0 ≤ amount ≤ 5000.\n\n"
                "Example 1: [1,2,5], 5 → 4\nExample 2: [2], 3 → 0\n\n"
                "Write `solve(coins, amount)`."
            ),
            "zh": (
                "给定硬币面值列表 coins 和目标金额 amount，返回凑成 amount 的不同组合数（无限使用，顺序无关）。\n\n"
                "示例 1：[1,2,5], 5 → 4\n示例 2：[2], 3 → 0\n\n"
                "编写 `solve(coins, amount)`。"
            ),
        },
    },

    # ══════════════════════════════════════════
    #  2400 — El Editor Mínimo de Palíndromos
    # ══════════════════════════════════════════
    {
        "title": "El Editor Mínimo de Palíndromos",
        "difficulty": 2400, "category": "Programación Dinámica", "total_solvers": 0,
        "description": (
            "La editora Irina Kazárova trabaja en un periódico de Kazán especializado en "
            "palindromía literaria: textos que se leen igual de izquierda a derecha que de "
            "derecha a izquierda. Irina recibe cadenas de texto y debe transformarlas en "
            "palíndromos insertando el mínimo número posible de caracteres (puede insertar "
            "cualquier carácter en cualquier posición).\n\n"
            "Por ejemplo, para convertir \"ab\" en un palíndromo, Irina puede insertar 'a' al "
            "final obteniendo \"aba\" (1 inserción) o insertar 'b' al principio obteniendo \"bab\" "
            "(1 inserción). No hay forma de hacerlo con 0 inserciones.\n\n"
            "Formalmente:\n"
            "  Dada una cadena s, devuelve el número mínimo de inserciones de caracteres "
            "necesarias para convertirla en un palíndromo.\n\n"
            "Restricciones:\n"
            "  1 ≤ len(s) ≤ 500\n"
            "  s contiene solo letras minúsculas del alfabeto inglés.\n\n"
            "Ejemplo 1:\n"
            "  Entrada: s = \"zzazz\"\n"
            "  Salida: 0\n"
            "  \"zzazz\" ya es un palíndromo. No se necesitan inserciones.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: s = \"mbadm\"\n"
            "  Salida: 2\n"
            "  Por ejemplo, insertar 'a' y 'd': \"mbdaadm\" no funciona bien... La subsecuencia "
            "palindrómica más larga de \"mbadm\" es \"mam\" o \"mbm\" (longitud 3). "
            "Mínimas inserciones = len(s) - LPS(s) = 5 - 3 = 2.\n\n"
            "Ejemplo 3:\n"
            "  Entrada: s = \"abcd\"\n"
            "  Salida: 3\n"
            "  Todos los caracteres son distintos, LPS = 1. Mínimas inserciones = 4 - 1 = 3.\n\n"
            "Clave: El número mínimo de inserciones para hacer s palíndromo es:\n"
            "  len(s) - LPS(s)\n"
            "donde LPS(s) es la longitud de la Subsecuencia Palindrómica más Larga de s.\n\n"
            "Para calcular LPS(s): es equivalente al LCS (Longest Common Subsequence) entre s "
            "y su reverso reverse(s).\n\n"
            "Algoritmo de LCS:\n"
            "  dp[i][j] = LCS de s[0..i-1] y t[0..j-1], donde t = s[::-1]\n"
            "  Si s[i-1] == t[j-1]: dp[i][j] = dp[i-1][j-1] + 1\n"
            "  Si no: dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n\n"
            "Escribe `solve(s)` que devuelva el número mínimo de inserciones."
        ),
        "test_cases": [
            {"input": '"zzazz"', "expected_output": "0"},
            {"input": '"mbadm"', "expected_output": "2"},
            {"input": '"abcd"',  "expected_output": "3"},
        ],
        "stub": {
            "Python": (
                "def solve(s):\n"
                "    t = s[::-1]\n"
                "    n = len(s)\n"
                "    # LCS entre s y t = LPS(s)\n"
                "    # Respuesta = n - LPS(s)\n"
                "    pass"
            ),
            "C++": (
                "#include <string>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n"
                "int solve(string s) {\n"
                "    int n = s.size();\n"
                "    string t(s.rbegin(), s.rend());\n"
                "    vector<vector<int>> dp(n+1, vector<int>(n+1, 0));\n"
                "    for (int i = 1; i <= n; i++)\n"
                "        for (int j = 1; j <= n; j++)\n"
                "            dp[i][j] = s[i-1]==t[j-1] ? dp[i-1][j-1]+1 : max(dp[i-1][j], dp[i][j-1]);\n"
                "    return n - dp[n][n];\n"
                "}"
            ),
            "Java": (
                "public static int solve(String s) {\n"
                "    int n = s.length();\n"
                "    String t = new StringBuilder(s).reverse().toString();\n"
                "    int[][] dp = new int[n+1][n+1];\n"
                "    for (int i = 1; i <= n; i++)\n"
                "        for (int j = 1; j <= n; j++)\n"
                "            dp[i][j] = s.charAt(i-1)==t.charAt(j-1) ? dp[i-1][j-1]+1\n"
                "                       : Math.max(dp[i-1][j], dp[i][j-1]);\n"
                "    return n - dp[n][n];\n"
                "}"
            ),
            "Go": ("func solve(s string) int {\n    return 0\n}"),
            "C#": ("public static int Solve(string s) {\n    return 0;\n}"),
        },
        "title_i18n": {"es": "El Editor Mínimo de Palíndromos", "en": "The Minimum Palindrome Editor", "zh": "最少回文插入"},
        "description_i18n": {
            "es": (
                "Dada cadena s, devuelve el mínimo número de inserciones para hacerla palíndromo.\n\n"
                "Clave: respuesta = len(s) - LPS(s) = len(s) - LCS(s, reverse(s)).\n\n"
                "Ejemplo 1: \"zzazz\" → 0\nEjemplo 2: \"mbadm\" → 2\nEjemplo 3: \"abcd\" → 3\n\n"
                "Escribe `solve(s)`."
            ),
            "en": (
                "Given string s, return the minimum insertions to make it a palindrome.\n\n"
                "Key: answer = len(s) - LPS(s) = len(s) - LCS(s, reverse(s)).\n\n"
                "Example 1: \"zzazz\" → 0\nExample 2: \"mbadm\" → 2\nExample 3: \"abcd\" → 3\n\n"
                "Write `solve(s)`."
            ),
            "zh": (
                "给定字符串 s，返回使其成为回文所需的最少插入次数。\n\n"
                "关键：答案 = len(s) - LPS(s) = len(s) - LCS(s, reverse(s))。\n\n"
                "示例 1：\"zzazz\" → 0\n示例 2：\"mbadm\" → 2\n\n"
                "编写 `solve(s)`。"
            ),
        },
    },

    # ══════════════════════════════════════════
    #  2600 — El Gran Repartidor de Carga
    # ══════════════════════════════════════════
    {
        "title": "El Gran Repartidor de Carga",
        "difficulty": 2600, "category": "Búsqueda Binaria", "total_solvers": 0,
        "description": (
            "La empresa de logística TransSiberia necesita repartir un cargamento a lo largo "
            "de una ruta con n paradas. Cada parada i tiene un paquete de peso weights[i] que "
            "DEBE ser entregado en el mismo viaje en que se recoge (no se puede partir un paquete). "
            "Se dispone de k camiones que harán el viaje en convoy, y cada camión debe entregar "
            "un tramo contiguo de paradas (la ruta no puede reordenarse). La carga de cada "
            "camión es la suma de los pesos de los paquetes en su tramo.\n\n"
            "El director de logística, Dmitri Sokolov, quiere minimizar la carga máxima que "
            "soporta cualquier camión, para que ninguno quede sobrecargado. Tu tarea es encontrar "
            "esa carga máxima mínima posible.\n\n"
            "Formalmente:\n"
            "  Dado un array weights de n enteros y un entero k,\n"
            "  divide weights en exactamente k subarray contiguos (sin reordenar)\n"
            "  minimizando el máximo de las sumas de los subarrays.\n"
            "  Devuelve ese máximo mínimo.\n\n"
            "Restricciones:\n"
            "  1 ≤ k ≤ n ≤ 1000\n"
            "  1 ≤ weights[i] ≤ 10^6\n\n"
            "Ejemplo 1:\n"
            "  Entrada: weights = [7, 2, 5, 10, 8], k = 2\n"
            "  Salida: 18\n"
            "  La mejor partición es [7,2,5] | [10,8] con sumas 14 y 18. Máximo = 18.\n"
            "  Otras particiones dan máximos mayores (ej. [7,2,5,10]|[8] → máx=24).\n\n"
            "Ejemplo 2:\n"
            "  Entrada: weights = [1, 2, 3, 4, 5], k = 2\n"
            "  Salida: 9\n"
            "  Partición óptima: [1,2,3] | [4,5] → máx = max(6, 9) = 9.\n\n"
            "Ejemplo 3:\n"
            "  Entrada: weights = [1, 4, 4], k = 3\n"
            "  Salida: 4\n"
            "  Cada camión lleva un paquete: [1]|[4]|[4] → máx = 4.\n\n"
            "Algoritmo (Búsqueda binaria sobre la respuesta):\n"
            "  La respuesta está en el rango [max(weights), sum(weights)].\n"
            "  Función de verificación viable(cap): ¿se puede dividir en ≤ k tramos con suma ≤ cap?\n"
            "    Recorre de izquierda a derecha, acumulando hasta superar cap; cuando supera, "
            "abre un nuevo camión. Si necesitas más de k camiones, no es viable.\n"
            "  Aplica búsqueda binaria sobre cap en [lo=max(weights), hi=sum(weights)].\n\n"
            "Escribe `solve(weights, k)` que devuelva la carga máxima mínima."
        ),
        "test_cases": [
            {"input": "[7, 2, 5, 10, 8], 2", "expected_output": "18"},
            {"input": "[1, 2, 3, 4, 5], 2",  "expected_output": "9"},
            {"input": "[1, 4, 4], 3",         "expected_output": "4"},
        ],
        "stub": {
            "Python": (
                "def solve(weights, k):\n"
                "    def viable(cap):\n"
                "        trucks, current = 1, 0\n"
                "        for w in weights:\n"
                "            if current + w > cap:\n"
                "                trucks += 1\n"
                "                current = 0\n"
                "            current += w\n"
                "        return trucks <= k\n"
                "    lo, hi = max(weights), sum(weights)\n"
                "    # Busqueda binaria: encuentra el minimo cap viable\n"
                "    pass"
            ),
            "C++": (
                "#include <vector>\n#include <numeric>\n#include <algorithm>\nusing namespace std;\n"
                "bool viable(vector<int>& w, int k, long long cap) {\n"
                "    int trucks = 1; long long cur = 0;\n"
                "    for (int x : w) {\n"
                "        if (cur + x > cap) { trucks++; cur = 0; }\n"
                "        cur += x;\n"
                "    }\n"
                "    return trucks <= k;\n"
                "}\n"
                "long long solve(vector<int> weights, int k) {\n"
                "    long long lo = *max_element(weights.begin(), weights.end());\n"
                "    long long hi = accumulate(weights.begin(), weights.end(), 0LL);\n"
                "    while (lo < hi) {\n"
                "        long long mid = (lo + hi) / 2;\n"
                "        if (viable(weights, k, mid)) hi = mid;\n"
                "        else lo = mid + 1;\n"
                "    }\n"
                "    return lo;\n"
                "}"
            ),
            "Java": (
                "public static int solve(int[] weights, int k) {\n"
                "    int lo = 0, hi = 0;\n"
                "    for (int w : weights) { lo = Math.max(lo, w); hi += w; }\n"
                "    while (lo < hi) {\n"
                "        int mid = lo + (hi - lo) / 2;\n"
                "        if (viable(weights, k, mid)) hi = mid;\n"
                "        else lo = mid + 1;\n"
                "    }\n"
                "    return lo;\n"
                "}\n"
                "static boolean viable(int[] w, int k, int cap) {\n"
                "    int trucks = 1, cur = 0;\n"
                "    for (int x : w) {\n"
                "        if (cur + x > cap) { trucks++; cur = 0; }\n"
                "        cur += x;\n"
                "    }\n"
                "    return trucks <= k;\n"
                "}"
            ),
            "Go": ("func solve(weights []int, k int) int {\n    return 0\n}"),
            "C#": ("public static int Solve(int[] weights, int k) {\n    return 0;\n}"),
        },
        "title_i18n": {"es": "El Gran Repartidor de Carga", "en": "The Great Load Distributor", "zh": "最优装载分配"},
        "description_i18n": {
            "es": (
                "Divide weights en k subarray contiguos minimizando la suma máxima. "
                "Búsqueda binaria sobre la respuesta + verificación greedy.\n\n"
                "Ejemplo 1: [7,2,5,10,8], k=2 → 18\n"
                "Ejemplo 2: [1,2,3,4,5], k=2 → 9\n"
                "Ejemplo 3: [1,4,4], k=3 → 4\n\n"
                "Escribe `solve(weights, k)`."
            ),
            "en": (
                "Split weights into k contiguous subarrays minimizing the maximum sum. "
                "Binary search on the answer + greedy verification.\n\n"
                "Example 1: [7,2,5,10,8], k=2 → 18\n"
                "Example 2: [1,2,3,4,5], k=2 → 9\n\n"
                "Write `solve(weights, k)`."
            ),
            "zh": (
                "将 weights 分成 k 个连续子数组，最小化最大子数组和。二分答案 + 贪心验证。\n\n"
                "示例 1：[7,2,5,10,8], k=2 → 18\n示例 2：[1,2,3,4,5], k=2 → 9\n\n"
                "编写 `solve(weights, k)`。"
            ),
        },
    },

    # ══════════════════════════════════════════
    #  3000 — La Distancia de Edición
    # ══════════════════════════════════════════
    {
        "title": "La Distancia de Edición",
        "difficulty": 3000, "category": "Programación Dinámica", "total_solvers": 0,
        "description": (
            "El lingüista computacional Vladimir Levenshtein propuso en 1965 una medida para "
            "cuantificar la diferencia entre dos cadenas de texto: la distancia de edición, "
            "también conocida como distancia de Levenshtein. Esta métrica tiene aplicaciones "
            "fundamentales en correctores ortográficos, bioinformática (alineación de secuencias "
            "de ADN), reconocimiento de voz, búsqueda aproximada de texto y sistemas de "
            "traducción automática.\n\n"
            "La distancia de edición entre dos cadenas s y t es el número mínimo de operaciones "
            "elementales necesarias para transformar s en t, donde las operaciones permitidas son:\n"
            "  1. INSERTAR un carácter en cualquier posición de s.\n"
            "  2. ELIMINAR un carácter de cualquier posición de s.\n"
            "  3. REEMPLAZAR un carácter de s por otro carácter diferente.\n\n"
            "Cada operación tiene coste 1.\n\n"
            "Formalmente:\n"
            "  Dadas dos cadenas s y t, devuelve el número mínimo de operaciones de inserción, "
            "eliminación y reemplazo para transformar s en t.\n\n"
            "Restricciones:\n"
            "  0 ≤ len(s), len(t) ≤ 500\n"
            "  s y t contienen solo letras minúsculas del alfabeto inglés.\n\n"
            "Ejemplo 1:\n"
            "  Entrada: s = \"horse\", t = \"ros\"\n"
            "  Salida: 3\n"
            "  horse → rorse (h→r) → rose (eliminar r) → ros (eliminar e). 3 operaciones.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: s = \"intention\", t = \"execution\"\n"
            "  Salida: 5\n"
            "  Una secuencia válida de 5 operaciones transforma \"intention\" en \"execution\".\n\n"
            "Ejemplo 3:\n"
            "  Entrada: s = \"\", t = \"abc\"\n"
            "  Salida: 3\n"
            "  La cadena vacía requiere 3 inserciones para convertirse en \"abc\".\n\n"
            "Algoritmo (DP 2D):\n"
            "  dp[i][j] = distancia de edición entre s[0..i-1] y t[0..j-1].\n"
            "  Caso base: dp[i][0] = i (i eliminaciones), dp[0][j] = j (j inserciones).\n"
            "  Recurrencia:\n"
            "    Si s[i-1] == t[j-1]: dp[i][j] = dp[i-1][j-1]  (no operation needed)\n"
            "    Si no: dp[i][j] = 1 + min(dp[i-1][j],    # eliminar de s\n"
            "                               dp[i][j-1],    # insertar en s\n"
            "                               dp[i-1][j-1])  # reemplazar\n"
            "  Respuesta: dp[len(s)][len(t)].\n"
            "  Complejidad: O(m*n) tiempo y espacio (optimizable a O(min(m,n)) espacio).\n\n"
            "Escribe `solve(s, t)` que devuelva la distancia de edición mínima."
        ),
        "test_cases": [
            {"input": '"horse", "ros"',         "expected_output": "3"},
            {"input": '"intention", "execution"',"expected_output": "5"},
            {"input": '"", "abc"',               "expected_output": "3"},
        ],
        "stub": {
            "Python": (
                "def solve(s, t):\n"
                "    m, n = len(s), len(t)\n"
                "    dp = [[0]*(n+1) for _ in range(m+1)]\n"
                "    for i in range(m+1): dp[i][0] = i\n"
                "    for j in range(n+1): dp[0][j] = j\n"
                "    # Rellena dp con la recurrencia de Levenshtein\n"
                "    pass"
            ),
            "C++": (
                "#include <string>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n"
                "int solve(string s, string t) {\n"
                "    int m = s.size(), n = t.size();\n"
                "    vector<vector<int>> dp(m+1, vector<int>(n+1));\n"
                "    for (int i = 0; i <= m; i++) dp[i][0] = i;\n"
                "    for (int j = 0; j <= n; j++) dp[0][j] = j;\n"
                "    for (int i = 1; i <= m; i++)\n"
                "        for (int j = 1; j <= n; j++)\n"
                "            dp[i][j] = s[i-1]==t[j-1] ? dp[i-1][j-1]\n"
                "                       : 1 + min({dp[i-1][j], dp[i][j-1], dp[i-1][j-1]});\n"
                "    return dp[m][n];\n"
                "}"
            ),
            "Java": (
                "public static int solve(String s, String t) {\n"
                "    int m = s.length(), n = t.length();\n"
                "    int[][] dp = new int[m+1][n+1];\n"
                "    for (int i = 0; i <= m; i++) dp[i][0] = i;\n"
                "    for (int j = 0; j <= n; j++) dp[0][j] = j;\n"
                "    for (int i = 1; i <= m; i++)\n"
                "        for (int j = 1; j <= n; j++)\n"
                "            dp[i][j] = s.charAt(i-1)==t.charAt(j-1) ? dp[i-1][j-1]\n"
                "                       : 1 + Math.min(dp[i-1][j-1], Math.min(dp[i-1][j], dp[i][j-1]));\n"
                "    return dp[m][n];\n"
                "}"
            ),
            "Go": ("func solve(s, t string) int {\n    return 0\n}"),
            "C#": ("public static int Solve(string s, string t) {\n    return 0;\n}"),
        },
        "title_i18n": {"es": "La Distancia de Edición", "en": "Edit Distance", "zh": "编辑距离"},
        "description_i18n": {
            "es": (
                "Dado s y t, devuelve el mínimo de inserciones, eliminaciones y reemplazos "
                "para transformar s en t (distancia de Levenshtein).\n\n"
                "Ejemplo 1: \"horse\",\"ros\" → 3\n"
                "Ejemplo 2: \"intention\",\"execution\" → 5\n"
                "Ejemplo 3: \"\",\"abc\" → 3\n\n"
                "Escribe `solve(s, t)`."
            ),
            "en": (
                "Given s and t, return the minimum number of insert/delete/replace operations "
                "to transform s into t (Levenshtein distance).\n\n"
                "Example 1: \"horse\",\"ros\" → 3\nExample 2: \"intention\",\"execution\" → 5\n\n"
                "Write `solve(s, t)`."
            ),
            "zh": (
                "给定 s 和 t，返回将 s 转换为 t 所需的最少插入、删除、替换操作次数（编辑距离）。\n\n"
                "示例 1：\"horse\",\"ros\" → 3\n示例 2：\"\",\"abc\" → 3\n\n"
                "编写 `solve(s, t)`。"
            ),
        },
    },

    # ══════════════════════════════════════════
    #  3500 — Los Cortes del Palíndromo Mínimo
    # ══════════════════════════════════════════
    {
        "title": "Los Cortes del Palíndromo Mínimo",
        "difficulty": 3500, "category": "Programación Dinámica", "total_solvers": 0,
        "description": (
            "La investigadora Elena Krasnova trabaja en el Centro de Investigación en Algoritmos "
            "de Complejidad de Moscú. Su proyecto actual involucra la partición de cadenas en "
            "palíndromos: dada una cadena, ¿cuántos cortes mínimos se necesitan para que todos "
            "los fragmentos resultantes sean palíndromos?\n\n"
            "Este problema, conocido como 'Palindrome Partitioning II', es considerablemente más "
            "difícil que simplemente encontrar si existe una partición palindrómica, y tiene "
            "aplicaciones en compresión de texto y bioinformática (análisis de estructuras "
            "secundarias de ARN).\n\n"
            "Definiciones:\n"
            "  - Un corte en la posición k divide la cadena en s[0..k] y s[k+1..n-1].\n"
            "  - Una partición de n-1 posibles cortes divide la cadena en n partes.\n"
            "  - Se busca el número mínimo de cortes tal que todas las partes sean palíndromos.\n\n"
            "Formalmente:\n"
            "  Dada una cadena s de longitud n, devuelve el número mínimo de cortes para que "
            "cada segmento resultante sea un palíndromo.\n"
            "  Si s ya es un palíndromo, la respuesta es 0 (no se necesita ningún corte).\n\n"
            "Restricciones:\n"
            "  1 ≤ len(s) ≤ 2000\n"
            "  s contiene solo letras minúsculas del alfabeto inglés.\n\n"
            "Ejemplo 1:\n"
            "  Entrada: s = \"aab\"\n"
            "  Salida: 1\n"
            "  Partición: \"aa\" | \"b\". Ambas partes son palíndromos. 1 corte.\n\n"
            "Ejemplo 2:\n"
            "  Entrada: s = \"a\"\n"
            "  Salida: 0\n"
            "  Un solo carácter siempre es palíndromo.\n\n"
            "Ejemplo 3:\n"
            "  Entrada: s = \"ababababab\"\n"
            "  Salida: 1\n"
            "  Partición: \"ababa\" | \"babab\". Ambas son palíndromos. 1 corte es suficiente.\n\n"
            "Algoritmo (DP en dos fases):\n"
            "  Fase 1: Precalcular is_pal[i][j] = True si s[i..j] es palíndromo.\n"
            "    Método: expand around center (O(n²)) o DP:\n"
            "      is_pal[i][i] = True\n"
            "      is_pal[i][i+1] = (s[i] == s[i+1])\n"
            "      is_pal[i][j] = (s[i] == s[j]) and is_pal[i+1][j-1]  para j-i >= 2\n\n"
            "  Fase 2: Calcular cuts[i] = mínimo cortes para s[0..i].\n"
            "      cuts[i] = 0  si s[0..i] es palíndromo\n"
            "      cuts[i] = min(cuts[j-1] + 1)  para todo j en [1..i] con is_pal[j][i]\n\n"
            "  Respuesta: cuts[n-1]. Complejidad total: O(n²).\n\n"
            "Escribe `solve(s)` que devuelva el número mínimo de cortes."
        ),
        "test_cases": [
            {"input": '"aab"',         "expected_output": "1"},
            {"input": '"a"',           "expected_output": "0"},
            {"input": '"ababababab"',   "expected_output": "1"},
        ],
        "stub": {
            "Python": (
                "def solve(s):\n"
                "    n = len(s)\n"
                "    # Fase 1: precalcular is_pal[i][j]\n"
                "    is_pal = [[False]*n for _ in range(n)]\n"
                "    for i in range(n): is_pal[i][i] = True\n"
                "    for length in range(2, n+1):\n"
                "        for i in range(n - length + 1):\n"
                "            j = i + length - 1\n"
                "            if s[i] == s[j]:\n"
                "                is_pal[i][j] = (length == 2) or is_pal[i+1][j-1]\n"
                "    # Fase 2: dp de cortes minimos\n"
                "    # cuts[i] = min cortes para s[0..i]\n"
                "    pass"
            ),
            "C++": (
                "#include <string>\n#include <vector>\n#include <climits>\nusing namespace std;\n"
                "int solve(string s) {\n"
                "    int n = s.size();\n"
                "    vector<vector<bool>> pal(n, vector<bool>(n, false));\n"
                "    for (int i = 0; i < n; i++) pal[i][i] = true;\n"
                "    for (int len = 2; len <= n; len++)\n"
                "        for (int i = 0; i <= n-len; i++) {\n"
                "            int j = i+len-1;\n"
                "            pal[i][j] = (s[i]==s[j]) && (len==2 || pal[i+1][j-1]);\n"
                "        }\n"
                "    vector<int> cuts(n, INT_MAX);\n"
                "    for (int i = 0; i < n; i++) {\n"
                "        if (pal[0][i]) { cuts[i] = 0; continue; }\n"
                "        for (int j = 1; j <= i; j++)\n"
                "            if (pal[j][i] && cuts[j-1]+1 < cuts[i])\n"
                "                cuts[i] = cuts[j-1]+1;\n"
                "    }\n"
                "    return cuts[n-1];\n"
                "}"
            ),
            "Java": (
                "public static int solve(String s) {\n"
                "    int n = s.length();\n"
                "    boolean[][] pal = new boolean[n][n];\n"
                "    for (int i = 0; i < n; i++) pal[i][i] = true;\n"
                "    for (int len = 2; len <= n; len++)\n"
                "        for (int i = 0; i <= n-len; i++) {\n"
                "            int j = i+len-1;\n"
                "            pal[i][j] = (s.charAt(i)==s.charAt(j)) && (len==2 || pal[i+1][j-1]);\n"
                "        }\n"
                "    int[] cuts = new int[n];\n"
                "    java.util.Arrays.fill(cuts, Integer.MAX_VALUE);\n"
                "    for (int i = 0; i < n; i++) {\n"
                "        if (pal[0][i]) { cuts[i] = 0; continue; }\n"
                "        for (int j = 1; j <= i; j++)\n"
                "            if (pal[j][i]) cuts[i] = Math.min(cuts[i], cuts[j-1]+1);\n"
                "    }\n"
                "    return cuts[n-1];\n"
                "}"
            ),
            "Go": ("func solve(s string) int {\n    return 0\n}"),
            "C#": ("public static int Solve(string s) {\n    return 0;\n}"),
        },
        "title_i18n": {"es": "Los Cortes del Palíndromo Mínimo", "en": "Minimum Palindrome Cuts", "zh": "回文串最少分割"},
        "description_i18n": {
            "es": (
                "Dada cadena s, devuelve el mínimo número de cortes para que todos los "
                "segmentos sean palíndromos.\n\n"
                "Algoritmo: DP en dos fases — precalcular is_pal[i][j], luego cuts[i].\n\n"
                "Ejemplo 1: \"aab\" → 1\nEjemplo 2: \"a\" → 0\nEjemplo 3: \"ababababab\" → 1\n\n"
                "Escribe `solve(s)`."
            ),
            "en": (
                "Given string s, return the minimum cuts so every segment is a palindrome.\n\n"
                "Algorithm: 2-phase DP — precompute is_pal[i][j], then cuts[i].\n\n"
                "Example 1: \"aab\" → 1\nExample 2: \"a\" → 0\nExample 3: \"ababababab\" → 1\n\n"
                "Write `solve(s)`."
            ),
            "zh": (
                "给定字符串 s，返回使所有分段都是回文所需的最少切割次数。\n\n"
                "算法：两阶段 DP——预计算 is_pal[i][j]，然后计算 cuts[i]。\n\n"
                "示例 1：\"aab\" → 1\n示例 2：\"a\" → 0\n\n"
                "编写 `solve(s)`。"
            ),
        },
    },

]
