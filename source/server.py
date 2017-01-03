import os
from log import create_app


app = create_app(os.getenv("EMIS_LOG_CONFIGURATION"))
