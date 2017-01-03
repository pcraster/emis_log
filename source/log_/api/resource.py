from werkzeug.exceptions import *
from flask_restful import Resource
from flask import request
from .. import db
from .model import LogModel
from .schema import LogSchema


log_schema = LogSchema()


class LogResource(Resource):

    def get(self,
            id):

        log_record = LogModel.query.get(id)

        if log_record is None:
            raise BadRequest("Log could not be found")


        data, errors = log_schema.dump(log_record)

        if errors:
            raise InternalServerError(errors)


        return data


class LogsResource(Resource):


    def get(self):

        log_records = LogModel.query.all()
        data, errors = log_schema.dump(log_records, many=True)

        if errors:
            raise InternalServerError(errors)

        assert isinstance(data, dict), data


        return data


    def post(self):

        json_data = request.get_json()

        if json_data is None:
            raise BadRequest("No input data provided")


        # Validate and deserialize input.
        log_record, errors = log_schema.load(json_data)

        if errors:
            raise UnprocessableEntity(errors)


        # Write log to database.
        db.session.add(log_record)
        db.session.commit()


        # From record in database to dict representing a log.
        data, errors = log_schema.dump(LogModel.query.get(log_record.id))
        assert not errors, errors
        assert isinstance(data, dict), data


        return data, 201
