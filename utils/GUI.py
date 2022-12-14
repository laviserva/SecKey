from utils.verify_password import verify_password, Verify_password_state # Verify and decript
from utils.start_app import start_app, start_app_state # Create or load
from utils.data_window import run_gui_load_file_with_key
import sys

def main():
    gui = start_app()
    vad = verify_password()

    file = gui.init_window()
    if gui.state == start_app_state.CLOSED:
        sys.exit()
    if gui.state == start_app_state.DESTROYED or gui.state == start_app_state.LOADING_FILE:
        data = vad.Validation(file)
    if gui.state == start_app_state.FILE_CREATED:
        data = gui.data
        vad.state = Verify_password_state.RETURN_TO_MAIN
        run_gui_load_file_with_key(file, data)
    if vad.state == Verify_password_state.RETURN_TO_MAIN:
        main()
    if vad.state == Verify_password_state.DESTROYED and data is not None:
        run_gui_load_file_with_key(file, data)

if __name__ == "__main__":
    main()