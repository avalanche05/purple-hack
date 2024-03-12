from ..data_matching_functions import create_project_role_ids, match_task_id_to_resourse_id



class Env:
    def __init__(self,
                 data_lists) -> None:
        self.data_lists = data_lists

        self.task_by_project_roles = create_project_role_ids(data_lists["tasks"])
    
    def step(self,):
        pass
