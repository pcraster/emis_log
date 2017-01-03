import datetime
from marshmallow import fields, post_dump, post_load, pre_load, ValidationError
from .. import ma
from .model import LogModel, priorities, severities


def must_not_be_blank(
        data):
    if not data:
        raise ValidationError("Data not provided")


def must_be_one_of(
        values):

    def validator(
            data):
        if not data in values:
            raise ValidationError("Value ({}) must be one of ({})".format(
                data, ", ".join(values)))

    return validator


class LogSchema(ma.Schema):

    class Meta:
        # Fields to include in the serialized result.
        fields = ("id", "priority", "severity", "message", "timestamp",
            "_links")

    id = fields.Int(dump_only=True)
    priority = fields.Str(required=True, validate=must_be_one_of(priorities))
    severity = fields.Str(required=True, validate=must_be_one_of(severities))
    message = fields.Str(required=True, validate=must_not_be_blank)
    timestamp = fields.DateTime(required=True)
    posted_at = fields.DateTime(dump_only=True,
        missing=datetime.datetime.utcnow().isoformat())
    _links = ma.Hyperlinks({
        "self": ma.URLFor("api.log", id="<id>"),
        "collection": ma.URLFor("api.logs")
    })


    def key(self,
            many):
        return "logs" if many else "log"


    @pre_load(
        pass_many=True)
    def unwrap(self,
            data,
            many):
        key = self.key(many)

        if key not in data:
            raise ValidationError("Input data must have a {} key".format(key))

        return data[key]


    @post_dump(
        pass_many=True)
    def wrap(self,
            data, many):
        key = self.key(many)

        return {
            key: data
        }


    @post_load
    def make_object(self,
            data):
        return LogModel(
            # id=data["id"],
            # id=5,
            priority=data["priority"],
            severity=data["severity"],
            message = data["message"],
            timestamp = data["timestamp"],
            posted_at=datetime.datetime.utcnow()
        )
