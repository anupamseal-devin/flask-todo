from app import db


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False)

    def to_dict(self):
        """Serialize the Todo instance to a dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "complete": self.complete,
        }
