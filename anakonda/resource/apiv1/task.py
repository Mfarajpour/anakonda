from flask_restful import Resource

from anakonda.controller.apiv1 import TaskController


class TaskResource(Resource):
    def get(self, task_id=None):
        """
        get list of tasks : GET /api/v1/tasks
        get task info :  Get /api/v1/tasks/<task_id>
        """
        if task_id is None:
            return TaskController.get_tasks()
        else:
            return TaskController.get_task(task_id)

    def post(self):
        """
        For Create new task : POST /api/v1/tasks
        """

        return TaskController.create_task()

    def patch(self, task_id):
        """
        Update task : PATCH /api/v1/tasks/<task_id>
        """
        return TaskController.update_task(task_id)

    def delete(self, task_id):
        """
        Delete task : DELETE /api/v1/task/<task_id>
        """
        return TaskController.delete_task(task_id)
