import views.app_window as app_window
import controllers.upload_controller as upload_controller
import user_data_manager

from PyQt5.QtWidgets import QMessageBox

class AppController:
    def __init__(self):

        user_data_manager.UserDataManager().init_user_data()

        self.view = app_window.AppWindow()
        self.upload_controller = upload_controller.UploadController()
        self.upload_controller.app = self
        self.view.addTab(self.upload_controller.view, "Upload")
    
    def show_error_message(self, error, msg=None):
        msg = msg if msg else "An Error Occurred"
        errorMsg = QMessageBox(QMessageBox.Critical, "Error", msg+"\n\n" + str(error), QMessageBox.Ok)
        errorMsg.exec()


