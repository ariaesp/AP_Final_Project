import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import imutils
import random
import sys

class GridDialog(QDialog):
    PREPROCESSING, AUGMENTATION = range(2)
    PREPROCESSING_CASES = ["grayscale", "resize"]
    AUGMENTATION_CASES = ["flip", "90 degree rotate", "random crop", "random rotation",
                          "blur", "brightness"]
    def __init__(self, test_picture, type=1, draw_case="menu", deleted_processes=[]):
        super(GridDialog, self).__init__()
        # main widget layout
        self.setFixedSize(600, 550)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.setWindowFlags(Qt.WindowType.WindowSystemMenuHint |
                            Qt.WindowType.WindowTitleHint | Qt.WindowType.WindowCloseButtonHint)
        self.test_picture = test_picture
        self.deleted_processes = deleted_processes
        self.draw_case = draw_case
        self.type = type
        self.draw_menu()

    def draw_menu(self):
        for i in reversed(range(self.main_layout.count())):
            self.main_layout.itemAt(i).widget().setParent(None)
        self.setCursor(Qt.CursorShape.ArrowCursor)

        # upper frame
        self.upper_frame = QFrame()
        self.upper_frame.setFrameShape(QFrame.Shape.Box)
        self.upper_frame.setFrameShadow(QFrame.Shadow.Plain)
        self.upper_frame_layout = GridLayout(4, 4)
        self.upper_frame.setLayout(self.upper_frame_layout)

        # adding custom labels to upper frame for preprocessing
        cv_image = cv2.imread(r"test.jpg")
        if self.type == 0:
            for process in self.PREPROCESSING_CASES:
                if process not in self.deleted_processes:
                    process_widget = CustomLabel(cv_image, process)
                    process_widget.clicked.connect(self.show_submenu)
                    self.upper_frame_layout.add_widget(process_widget)
        elif self.type == 1:
            for process in self.AUGMENTATION_CASES:
                if process not in self.deleted_processes:
                    process_widget = CustomLabel(cv_image, process)
                    process_widget.clicked.connect(self.show_submenu)
                    self.upper_frame_layout.add_widget(process_widget)

        # bottom widget
        self.bottom_widget = QWidget()
        self.bottom_widget.setFixedHeight(50)
        self.bottom_widget_layout = QHBoxLayout()
        self.bottom_widget.setLayout(self.bottom_widget_layout)
        # add button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.exit_cancel_pressed)
        self.bottom_widget_layout.addStretch()
        self.bottom_widget_layout.addWidget(self.cancel_button)
        self.bottom_widget_layout.addStretch()

        # add widgets to main widget
        self.main_layout.addWidget(self.upper_frame)
        self.main_layout.addWidget(self.bottom_widget)

    def show_submenu(self, process_type):
        for i in reversed(range(self.main_layout.count())):
            self.main_layout.itemAt(i).widget().setParent(None)
        self.setCursor(Qt.CursorShape.ArrowCursor)

        # designing template
        self.submenu_main_widget = QWidget()
        self.submenu_main_layout = QHBoxLayout()
        self.submenu_main_widget.setLayout(self.submenu_main_layout)
        # control box widget
        self.control_widget_container = QWidget()
        self.control_widget_container.setFixedWidth(200)
        self.control_widget_container_layout = QVBoxLayout(self.control_widget_container)

        # pictures widget container + original test picture
        self.image_width, self.image_height = 300, 190
        self.pictures_widget_container = QFrame()
        self.pictures_widget_container.setFrameShape(QFrame.Shape.Box)
        self.pictures_widget_container.setFrameShadow(QFrame.Shadow.Plain)
        self.pictures_widget_container.setStyleSheet(
            "background: #ffffff;"
        )
        self.pictures_widget_container_layout = QVBoxLayout(self.pictures_widget_container)
        # original picture
        original_picture_label_image = QLabel()
        original_picture_label_image.setFixedSize(self.image_width, self.image_height)
        original_picture_label_image.setAlignment(Qt.AlignCenter)
        original_picture_pixmap = self.get_pixmap(self.test_picture)
        original_picture_pixmap = original_picture_pixmap.scaled(self.image_width, self.image_height, Qt.KeepAspectRatio)
        original_picture_label_image.setPixmap(original_picture_pixmap)
        original_picture_label_text = QLabel("Original Picture")
        original_picture_label_text.setAlignment(Qt.AlignCenter)
        self.pictures_widget_container_layout.addWidget(original_picture_label_image, alignment=Qt.AlignHCenter)
        self.pictures_widget_container_layout.addWidget(original_picture_label_text)
        self.pictures_widget_container_layout.addStretch()

        # apply and cancel buttons widget
        buttons_widget = QWidget()
        buttons_widget_layout = QHBoxLayout()
        buttons_widget.setLayout(buttons_widget_layout)
        apply_button = QPushButton("apply")
        cancel_button = QPushButton("cancel")
        buttons_widget_layout.addWidget(cancel_button)
        buttons_widget_layout.addStretch()
        buttons_widget_layout.addWidget(apply_button)
        if self.draw_case != "menu":
            cancel_button.clicked.connect(self.exit_cancel_pressed)
        else:
            cancel_button.clicked.connect(self.back_cancel_pressed)

        # adding all widgets to main layout
        self.submenu_main_layout.addWidget(self.pictures_widget_container)
        self.submenu_main_layout.addWidget(self.control_widget_container)
        self.main_layout.addWidget(self.submenu_main_widget)
        self.main_layout.addWidget(buttons_widget)

        if process_type == 0:
            if process_type == "grayscale":
                self.draw_grayscale_menu()
            elif process_type == "resize":
                self.draw_rseize_menu()
        elif process_type == 1:
            if process_type == "flip":
                self.draw_flip_menu()
            elif process_type == "90 degree rotate":
                self.draw_90rotate_menu()
            elif process_type == "random crop":
                self.draw_crop_menu()
            elif process_type == "random rotation":
                self.draw_rotate_menu()
            elif process_type == "blur":
                self.draw_blur_menu()
            elif process_type == "brightness":
                self.draw_brightness_menu()

    def draw_grayscale_menu(self):
        pass

    def draw_resize_menu(self):
        pass

    def draw_flip_menu(self):
        pass

    def draw_90rotate_menu(self):
        pass

    def draw_crop_menu(self):
        pass

    def draw_rotate_menu(self):
        pass

    def draw_blur_menu(self):
        pass

    def draw_brightness_menu(self):
        pass

    def exit_cancel_pressed(self):
        self.close()

    def back_cancel_pressed(self):
        self.draw_menu()

    def get_pixmap(self, cv_image):
        frame = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        return QPixmap.fromImage(image)

class CustomLabel(QWidget):
    clicked = pyqtSignal(str)
    def __init__(self, cv_image, process_type):
        super(CustomLabel, self).__init__()
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.setFixedSize(120,130)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.process_type = process_type

        # picture label
        self.get_pix_map(cv_image, process_type)
        self.image_label = QLabel()
        self.image_label.setPixmap(self.pix_map)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # text label
        self.text_label = QLabel(process_type.title())
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # adding text label and picture label to main widget
        self.main_layout.addWidget(self.image_label)
        self.main_layout.addWidget(self.text_label)

    def get_pix_map(self, cv_image, process_type):
        if process_type == "flip":
            cv_image = cv2.flip(cv_image, 0)
        elif process_type == "90 degree rotate":
            cv_image = cv2.rotate(cv_image, cv2.ROTATE_90_CLOCKWISE)
        elif process_type == "random crop":
            cv_image = cv_image[90:500, 80:490]
        elif process_type == "random rotation":
            cv_image = imutils.rotate(cv_image, 45)
        elif process_type == "blur":
            cv_image = cv2.blur(cv_image, (30, 30))
        elif process_type == "brightness":
            hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
            h,s,v = cv2.split(hsv)
            lim = 255 - 130
            v[v > lim] = 255
            v[v <= lim] += 50
            final_hsv = cv2.merge((h,s,v))
            cv_image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        frame = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        self.image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        if process_type == "grayscale":
            self.image = self.image.convertToFormat(QImage.Format.Format_Grayscale8)
        self.pix_map = QPixmap.fromImage(self.image).scaled(100, 110, Qt.AspectRatioMode.KeepAspectRatio)

    def enterEvent(self, ev):
        self.pix_map = self.pix_map.scaled(130, 140, Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(self.pix_map)

    def leaveEvent(self, ev):
        self.pix_map = self.pix_map.scaled(100, 110, Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(self.pix_map)

    def mousePressEvent(self, ev):
        self.clicked.emit(self.process_type)


class GridLayout(QVBoxLayout):
    def __init__(self, n_rows, n_columns, *args, **kwargs):
        super(GridLayout, self).__init__(*args, **kwargs)
        self.n_rows = n_rows
        self.n_columns = n_columns
        self.horizontal_layouts = {}
        for i in range(n_rows):
            horizontal_layout = QHBoxLayout()
            horizontal_layout.addStretch()
            horizontal_layout.addStretch()
            self.horizontal_layouts[horizontal_layout] = 0
            self.addLayout(horizontal_layout)
        self.addStretch()

    def add_widget(self, widget):
        for horizontal_layout, index in self.horizontal_layouts.items():
            if index < self.n_columns:
                horizontal_layout.insertWidget(index+1, widget)
                self.horizontal_layouts[horizontal_layout] += 1
                return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    test_picture = cv2.imread("lena_copy.png")
    main = GridDialog(test_picture, 0)
    main.show()

    sys.exit(app.exec())