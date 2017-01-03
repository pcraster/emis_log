import os
from log_ import create_app


app = create_app(os.getenv("EMIS_LOG_CONFIGURATION"))
