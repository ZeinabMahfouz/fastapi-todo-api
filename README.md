## AI vs me

### Prompt Used:
"Build a comprehensive FastAPI Todo API with an in-memory list database. It should provide the following endpoints: GET / to return API metadata, GET /health for health checks, GET /tasks to fetch all tasks, GET /tasks/{id} to get a specific task, POST /tasks to create a new task, PUT /tasks/{id} to update a task, and DELETE /tasks/{id} to delete a task. Ensure proper data validation, error handling, and appropriate HTTP status codes."

### 1. What the AI did better:
* The AI was exceptionally fast at setting up the project structure, cleanly separating the concerns into two independent files (`ai_main.py` and `ai_model.py`) right from the start.
* It maintained consistent and standardized naming conventions across all endpoints and routes.

### 2. What the AI missed or got wrong:
* The AI introduced a critical logical bug in the `delete_task` function. It immediately executed `return Response(status_code=status.HTTP_204_NO_CONTENT)` on the very first line of the function.
* Because of this, it completely skipped searching the list or verifying if the task existed, making the subsequent 404 error handling blocks completely unreachable code. The API would falsely report a successful deletion (204) even for IDs that never existed.

### 3. What details I missed in the prompt that the AI decided on:
* I did not explicitly define the exact schema or wording for the error details and exception messages.
* The AI took the initiative to structure the error responses autonomously, deciding on a format like: `detail=f"Task {task_id} not found"`.