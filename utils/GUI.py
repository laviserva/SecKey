from verify_password import verify_password, Verify_password_state # Verify and decript
from start_app import start_app, start_app_state # Create or load
from data_window import run_gui_load_file_with_key
import sys

def main():
    gui = start_app()
    vad = verify_password()

    file = gui.init_window()
    if gui.state == start_app_state.CLOSED:
        sys.exit()
    code = vad.Validation(file)
    if vad.state == Verify_password_state.RETURN_TO_MAIN:
        main()
    if vad.state == Verify_password_state.DESTROYED and code is not None:
        run_gui_load_file_with_key(file, code)

main()