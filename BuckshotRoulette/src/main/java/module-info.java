module ov3ipo.code {
    requires javafx.controls;
    requires javafx.fxml;

    requires org.controlsfx.controls;

    opens ov3ipo.code to javafx.fxml;
    exports ov3ipo.code;
}