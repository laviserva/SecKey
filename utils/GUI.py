from verify_password import verify_password # Verify and decript
from start_app import start_app, start_app_state # Create or load
import sys

gui = start_app()
vad = verify_password()

file = gui.init_window()
if gui.state == start_app_state.CLOSED:
    sys.exit()
code = vad.Validation(file)