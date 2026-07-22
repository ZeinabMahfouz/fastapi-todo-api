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

## Database Explorer (Stage 4)

Executed manual SQL queries using DB Browser for SQLite:

```sql
-- Count total tasks
SELECT COUNT(*) FROM tasks;

-- Fetch completed tasks
SELECT * FROM tasks WHERE done = 1;

# FastAPI Task API with Containerized PostgreSQL

A FastAPI Task CRUD application running against a PostgreSQL database inside Docker Compose.

## 🚀 Quick Start (One Command)

1. Clone the repository:
   ```bash
   git clone [https://github.com/ZeinabMahfouz/fastapi-todo-api.git](https://github.com/ZeinabMahfouz/fastapi-todo-api.git)
   cd fastapi-todo-api
   ```

2. Copy the environment variables example:
   ```bash
   cp .env.example .env
   ```

3. Start the entire stack with a single command:
   ```bash
   docker compose up --build
   ```

The API will be available at `http://localhost:8000`.

---

## 📌 API Endpoints

| Method | Endpoint | Description | Status Codes |
| :--- | :--- | :--- | :--- |
| **GET** | `/` | API Root Info | `200` |
| **GET** | `/health` | DB Health check | `200` |
| **GET** | `/tasks` | Get all tasks | `200` |
| **GET** | `/tasks/{id}` | Get task by ID | `200`, `404` |
| **POST** | `/tasks` | Create new task | `201`, `400` |
| **PUT** | `/tasks/{id}` | Update task | `200`, `400`, `404` |
| **DELETE** | `/tasks/{id}` | Delete task | `204`, `404` |

---

## 🧪 Sample Request (curl)

```bash
curl -i http://localhost:8000/tasks
```

---

## 💾 Database Persistence & Verification

To verify that tasks are stored inside PostgreSQL running in the container:

```bash
docker exec -it fastapi-todo-api-db-1 psql -U postgres -d tasks -c "SELECT * FROM tasks;"
```

