import sys
import os
import pandas as pd
import pyvista as pv
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QListWidget
)
from pyvistaqt import QtInteractor


class SpineNavigationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spine Ultrasound Navigation — MVP Prototype")
        self.resize(1200, 800)

        self.mesh = None
        self.pedicle_df = None

        # ---- Layout Setup ----
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Left panel
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        left_panel.setFixedWidth(280)

        self.load_mesh_btn = QPushButton("Load Spine Mesh (.stl)")
        self.load_mesh_btn.clicked.connect(self.load_mesh)

        self.load_pedicles_btn = QPushButton("Load Pedicle Points (.csv)")
        self.load_pedicles_btn.clicked.connect(self.load_pedicles)

        self.reset_view_btn = QPushButton("Reset Camera View")
        self.reset_view_btn.clicked.connect(self.reset_view)

        self.info_label = QLabel("No mesh loaded yet.")
        self.info_label.setWordWrap(True)

        self.vertebra_list = QListWidget()
        self.vertebra_list.itemClicked.connect(self.focus_on_vertebra)

        left_layout.addWidget(QLabel("<b>Spine Navigation Controls</b>"))
        left_layout.addWidget(self.load_mesh_btn)
        left_layout.addWidget(self.load_pedicles_btn)
        left_layout.addWidget(self.reset_view_btn)
        left_layout.addWidget(QLabel("<b>Vertebrae (click to focus):</b>"))
        left_layout.addWidget(self.vertebra_list)
        left_layout.addWidget(self.info_label)
        left_layout.addStretch()

        # Right panel — 3D viewer
        self.plotter = QtInteractor(self)

        main_layout.addWidget(left_panel)
        main_layout.addWidget(self.plotter.interactor, stretch=1)

        # disclaimer bar
        self.statusBar().showMessage(
            "Research/educational prototype only — NOT for clinical use."
        )

    def load_mesh(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Spine Mesh", "", "STL Files (*.stl)"
        )
        if not file_path:
            return

        self.plotter.clear()
        self.mesh = pv.read(file_path)
        self.plotter.add_mesh(self.mesh, color="ivory", smooth_shading=True, opacity=0.5)
        self.plotter.reset_camera()

        self.info_label.setText(
            f"Mesh loaded:\n{os.path.basename(file_path)}\n"
            f"Vertices: {self.mesh.n_points}\nFaces: {self.mesh.n_cells}"
        )

    def load_pedicles(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Pedicle CSV", "", "CSV Files (*.csv)"
        )
        if not file_path:
            return

        self.pedicle_df = pd.read_csv(file_path)
        self.vertebra_list.clear()

        for _, row in self.pedicle_df.iterrows():
            label = int(row["vertebra_label"])
            self.vertebra_list.addItem(f"Vertebra {label}")

            # centroid, left, right points plot karo
            centroid = [row["centroid_x"], row["centroid_y"], row["centroid_z"]]
            left = [row["left_pedicle_x"], row["left_pedicle_y"], row["left_pedicle_z"]]
            right = [row["right_pedicle_x"], row["right_pedicle_y"], row["right_pedicle_z"]]

            self.plotter.add_mesh(pv.Sphere(radius=4.0, center=centroid), color="green")
            self.plotter.add_mesh(pv.Sphere(radius=4.0, center=left), color="red")
            self.plotter.add_mesh(pv.Sphere(radius=4.0, center=right), color="blue")

        self.plotter.render()

        self.info_label.setText(
            f"Pedicle data loaded:\n{len(self.pedicle_df)} vertebrae\n"
            f"Green=centroid, Red=left, Blue=right"
        )

    def focus_on_vertebra(self, item):
        if self.pedicle_df is None:
            return
        label = int(item.text().split()[-1])
        row = self.pedicle_df[self.pedicle_df["vertebra_label"] == label].iloc[0]
        centroid = [row["centroid_x"], row["centroid_y"], row["centroid_z"]]
        self.plotter.camera.focal_point = centroid
        self.plotter.render()

    def reset_view(self):
        self.plotter.reset_camera()


def main():
    app = QApplication(sys.argv)
    window = SpineNavigationApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()