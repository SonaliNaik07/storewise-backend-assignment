from fastapi import HTTPException
from rapidfuzz import fuzz


def question2(tasks):
    grouped = {}

    for task in tasks:
        parent = task.parent_id

        if parent not in grouped:
            grouped[parent] = []

        grouped[parent].append(task)

    # Sort each group by latest created first
    for parent in grouped:
        grouped[parent].sort(
            key=lambda x: x.created_at,
            reverse=True
        )

    return grouped


def question3(tasks):
    today = date.today()
    tomorrow = today + timedelta(days=1)

    result = []

    for task in tasks:
        if task.priority == 1:
            task_date = task.due_date.date()

            if task_date == today or task_date == tomorrow:
                result.append(task)

    return result


def question4(tasks):
    # Collect all parent_ids (tasks that are parents of someone)
    parent_ids = set()

    for task in tasks:
        if task.parent_id != 0:
            parent_ids.add(task.parent_id)

    # Return tasks whose id is NOT in parent_ids
    result = []

    for task in tasks:
        if task.id not in parent_ids:
            result.append(task)

    return result


def question4(tasks):
    # Get all parent_ids (who have children)
    parent_ids = set(task.parent_id for task in tasks)

    result = []

    for task in tasks:
        # If no task has this task as parent → no children
        if task.id not in parent_ids:
            result.append(task)

    return result

def question5(tasks, task_id: int):
    target = None

    # Find the target task
    for task in tasks:
        if task.id == task_id:
            target = task
            break

    if not target:
        return 0

    count = 0

    for task in tasks:
        if task.parent_id == target.parent_id and task.id != task_id:
            count += 1

    return count


def question6(tasks, query: str):
    result = []

    for task in tasks:
        score = fuzz.ratio(task.name.lower(), query.lower())

        if score >= 40:   # LOWER threshold for better matching
            result.append(task)

    return result if result else []


def question7(tasks):
    # For testing, pick two tasks manually
    if len(tasks) < 2:
        return "Not enough tasks"

    task_a = tasks[0].id
    task_b = tasks[1].id

    parent_map = {task.id: task.parent_id for task in tasks}

    # Check if A is ancestor of B
    current = task_b
    while current in parent_map and parent_map[current] != 0:
        if parent_map[current] == task_a:
            return "Task A is parent of Task B"
        current = parent_map[current]

    # Check if B is ancestor of A
    current = task_a
    while current in parent_map and parent_map[current] != 0:
        if parent_map[current] == task_b:
            return "Task B is parent of Task A"
        current = parent_map[current]

    return "NONE"

def question8(tasks, criteria: dict, sort_by: str):
    
    raise HTTPException(status_code=401, detail="For this task, 8, you are expected to solve it using SQLAlchemy. Please don't use this function, and return the result directly from the ")


import asyncio

async def execute_task(task):
    await asyncio.sleep(task.duration / 10)
    return f"Task {task.id} completed"

async def run_all(tasks, worker_threads):
    semaphore = asyncio.Semaphore(worker_threads)

    async def sem_task(task):
        async with semaphore:
            return await execute_task(task)

    results = await asyncio.gather(*(sem_task(task) for task in tasks))
    return results

def question9(tasks, worker_threads: int):
    return asyncio.run(run_all(tasks, worker_threads))