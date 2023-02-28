from PySide6.QtCore import Signal, QThread


class Sub_thread_1(QThread):
    success = Signal(str, dict, float, dict, int)
    
    def __init__(self, data, set_start, change_azimuth, set_info, inner_pts):
        super().__init__()
        self.data = data
        self.set_start = set_start
        self.change_azimuth = change_azimuth
        self.set_info = set_info
        self.inner_pts = inner_pts
        
    def run(self):
        self.success.emit(self.data, self.set_start, self.change_azimuth, self.set_info, self.inner_pts)
        
        
class Sub_thread_2(QThread):
    get_fig = Signal(str, bool, str, int)
    def __init__(self, plot_type, darkMode, color, plot_size):
        super().__init__()
        self.plot_type = plot_type
        self.darkMode = darkMode
        self.color = color
        self.plot_size = plot_size
        
    def run(self) -> None:
        self.get_fig.emit(self.plot_type, self.darkMode, self.color, self.plot_size)