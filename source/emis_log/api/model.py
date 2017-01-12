from .. import db


priorities = [

    # Fix it whenever you have time.
    "low",

    # Fix it ASAP.
    "high"

]


severities = [

    # Something works, but not very good.
    "non_critical",

    # Something does not work.
    "critical"

]


class LogModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    priority = db.Column(db.Unicode(20))
    severity = db.Column(db.Unicode(20))
    message = db.Column(db.UnicodeText)
    timestamp = db.Column(db.DateTime)
    posted_at = db.Column(db.DateTime)
