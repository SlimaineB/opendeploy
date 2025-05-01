from model.task_result import TaskResult


class TaskService:
    def __init__(self):
        pass

    def handle_tasks(self, tasks):
        return self.execute_tasks(tasks)


    def execute_tasks(self, tasks):
        results = []
        for t in tasks:
        # Simule l'exécution de la tâche
            results.append(TaskResult(name=t.strip(), status="success"))
        return results