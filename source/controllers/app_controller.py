import views.app_window as app_window
import controllers.upload_controller as upload_controller

class AppController:
     def __init__(self):
         self.view = app_window.AppWindow()
         self.upload_controller = upload_controller.UploadController()
         self.view.addTab(self.upload_controller.view, "Upload")


