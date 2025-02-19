from pydantic import BaseModel

class Feedback(BaseModel):
    feedback: list[str]

    def add_feedback(self, new_entry: str):
        self.feedback.append(new_entry)
