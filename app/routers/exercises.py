import ast
import sys
import io

from fastapi import APIRouter, HTTPException, Depends

import app.core.database as database
from app.core.security import get_current_user
from app.models.exercise import SolveRequest

router = APIRouter()


@router.get("/api/exercises")
async def get_exercises(email: str = Depends(get_current_user)):
    user = await database.db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    solved_ids = set(user.get("solved_exercises", []))
    friends_emails = set(user.get("friends", []))

    exercises_cursor = database.db.exercises.find()
    exercises = []
    async for ex in exercises_cursor:
        ex_id = str(ex["_id"])
        ex["id"] = ex_id
        del ex["_id"]
        ex["solved"] = ex_id in solved_ids
        ex.pop("test_cases", None)
        ex.pop("stub", None)

        # First solver info
        first_solver_email = ex.pop("first_solver_email", None)
        if first_solver_email:
            fs_user = await database.db.users.find_one({"email": first_solver_email}, {"username": 1, "avatar": 1})
            ex["first_solver"] = {"username": fs_user.get("username") if fs_user else "?", "avatar": fs_user.get("avatar") if fs_user else None}
        else:
            ex["first_solver"] = None

        # Friends who solved
        solvers_list = ex.pop("solvers", [])
        if friends_emails and solvers_list:
            friends_solved_emails = [e for e in solvers_list if e in friends_emails]
            if friends_solved_emails:
                friends_solved = []
                cursor = database.db.users.find({"email": {"$in": friends_solved_emails}}, {"username": 1, "avatar": 1})
                async for fu in cursor:
                    friends_solved.append({"username": fu.get("username"), "avatar": fu.get("avatar")})
                ex["friends_solved"] = friends_solved
            else:
                ex["friends_solved"] = []
        else:
            ex["friends_solved"] = []

        exercises.append(ex)
    return exercises


@router.get("/api/exercises/solved")
async def get_solved_exercises(email: str = Depends(get_current_user)):
    user = await database.db.users.find_one({"email": email})
    if not user:
        return []
    return user.get("solved_exercises", [])


@router.get("/api/exercises/{exercise_id}")
async def get_exercise(exercise_id: str, email: str = Depends(get_current_user)):
    from bson import ObjectId
    try:
        oid = ObjectId(exercise_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de ejercicio inválido")
    ex = await database.db.exercises.find_one({"_id": oid})
    if not ex:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

    user = await database.db.users.find_one({"email": email})
    solved_ids = set(user.get("solved_exercises", [])) if user else set()

    ex["id"] = str(ex["_id"])
    del ex["_id"]
    ex["solved"] = ex["id"] in solved_ids
    return ex


@router.post("/api/exercises/{exercise_id}/solve")
async def solve_exercise(exercise_id: str, body: SolveRequest, email: str = Depends(get_current_user)):
    from bson import ObjectId
    try:
        oid = ObjectId(exercise_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de ejercicio inválido")
    ex = await database.db.exercises.find_one({"_id": oid})
    if not ex:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

    test_cases = ex.get("test_cases", [])
    if not test_cases:
        raise HTTPException(status_code=400, detail="Este ejercicio no tiene casos de prueba configurados")

    # Only Python execution supported for now
    if body.language != "Python":
        if body.save:
            user = await database.db.users.find_one({"email": email})
            solved_ids = user.get("solved_exercises", []) if user else []
            if exercise_id not in solved_ids:
                difficulty = ex.get("difficulty", "Normal")
                elo_gain = 1 if difficulty == "Fácil" else (5 if difficulty == "Difícil" else 2)
                coins_gain = 10 if difficulty == "Fácil" else (50 if difficulty == "Difícil" else 25)

                await database.db.users.update_one(
                    {"email": email},
                    {
                        "$addToSet": {"solved_exercises": exercise_id},
                        "$inc": {"elo": elo_gain, "coins": coins_gain}
                    }
                )
                # Record solver in exercise
                ex_has_first = ex.get("first_solver_email")
                update_ex = {"$addToSet": {"solvers": email}}
                if not ex_has_first:
                    update_ex["$set"] = {"first_solver_email": email}
                await database.db.exercises.update_one({"_id": oid}, update_ex)
            return {"correct": True, "message": "¡Ejercicio guardado correctamente!"}
        return {"correct": True, "message": f"Verificación manual para {body.language}. Haz clic en Guardar si tu solución es correcta."}

    # Python execution: run each test case
    user_code = body.code
    for i, tc in enumerate(test_cases):
        test_input_str = tc["input"]
        expected_str = str(tc["expected_output"]).strip()

        # Build execution environment
        exec_globals = {}
        try:
            exec(compile(user_code, "<solution>", "exec"), exec_globals)
        except Exception as e:
            return {"correct": False, "message": f"Error de compilación: {str(e)}", "failed_case": i + 1}

        solve_fn = exec_globals.get("solve")
        if not solve_fn or not callable(solve_fn):
            return {"correct": False, "message": "No se encontró la función `solve` en tu código.", "failed_case": 0}

        # Parse arguments from test_input_str
        try:
            args_raw = f"({test_input_str},)"
            parsed_args = ast.literal_eval(args_raw)
            if not isinstance(parsed_args, tuple):
                parsed_args = (parsed_args,)
        except Exception as e:
            return {"correct": False, "message": f"Error procesando caso de prueba {i+1}: {str(e)}", "failed_case": i + 1}

        # Execute solution
        try:
            result = solve_fn(*parsed_args)
        except Exception as e:
            return {
                "correct": False,
                "message": f"Error en caso {i+1}: {str(e)}",
                "failed_case": i + 1,
                "input": test_input_str,
                "expected": expected_str
            }

        # Compare output
        actual_str = str(result).strip()
        # Normalize booleans
        if actual_str.lower() == "true": actual_str = "True"
        if actual_str.lower() == "false": actual_str = "False"
        if actual_str.replace(" ", "") == expected_str.replace(" ", ""):
            continue  # Pass
        else:
            return {
                "correct": False,
                "message": f"Caso {i+1} fallido",
                "failed_case": i + 1,
                "input": test_input_str,
                "expected": expected_str,
                "got": actual_str
            }

    # All test cases passed!
    if body.save:
        user = await database.db.users.find_one({"email": email})
        solved_ids = user.get("solved_exercises", []) if user else []
        if exercise_id not in solved_ids:
            ex_fresh = await database.db.exercises.find_one({"_id": oid})
            difficulty = ex_fresh.get("difficulty", "Normal") if ex_fresh else "Normal"
            elo_gain = 1 if difficulty == "Fácil" else (5 if difficulty == "Difícil" else 2)

            await database.db.users.update_one(
                {"email": email},
                {
                    "$addToSet": {"solved_exercises": exercise_id},
                    "$inc": {"elo": elo_gain}
                }
            )
            # Record solver in exercise + first_solver if first
            has_first = ex_fresh.get("first_solver_email") if ex_fresh else None
            update_ex = {"$addToSet": {"solvers": email}}
            if not has_first:
                update_ex["$set"] = {"first_solver_email": email}
            await database.db.exercises.update_one({"_id": oid}, update_ex)
        return {"correct": True, "message": "¡Ejercicio guardado correctamente! ✓"}

    return {"correct": True, "message": "¡Todos los casos de prueba superados! Puedes guardar tu solución."}
