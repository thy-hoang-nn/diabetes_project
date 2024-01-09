from abc import ABC, abstractmethod
from typing import Optional, List

class IWorkflow(ABC):
    @abstractmethod
    def __call__(self, **kwargs):
        return kwargs

class IWorkflowStep(ABC):
    @abstractmethod
    def __call__(self, **kwargs):
        return kwargs


class DiabetesStep(IWorkflowStep):
    @abstractmethod
    def __call__(self, **kwargs):
        super().__call__(**kwargs)

class DiabetesWorkflow(IWorkflow):
    pre_workflows: Optional[List[IWorkflow]]
    steps: List[IWorkflowStep]

    def __init__(
        self, 
        pre_workflows: Optional[List[IWorkflow]] = None,
        post_workflows: Optional[List[IWorkflow]] = None,
        steps: List[IWorkflowStep] = [],
        **kwargs
        ) -> None:
        if pre_workflows is None:
            pre_workflows = []
        if post_workflows is None:
            post_workflows = []

        super().__init__(**kwargs)
        self.pre_workflows = pre_workflows
        self.post_workflows = post_workflows
        self.steps = steps

    def __call__(self, **kwargs):
        result = super().__call__(**kwargs)

        if (len(self.pre_workflows) > 0):
            for workflow in self.pre_workflows:
                result = workflow(**result)

        if (len(self.post_workflows) > 0):
            for workflow in self.post_workflows:
                result = workflow(**result)
        
        if (len(self.steps) > 0):
            for step in self.steps:
                result = step(**result)

        return result






