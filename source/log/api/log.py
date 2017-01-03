from . import api_restful
from .resource import *


# All log records.
# - Get all log records
# - Post log record
api_restful.add_resource(LogsResource,
    "/logs",
    endpoint="logs")

# Log record by id.
# - Get log record by id
api_restful.add_resource(LogResource,
    "/logs/<int:id>",
    endpoint="log")
