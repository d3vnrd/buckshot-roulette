package ov3ipo.code;

import javafx.application.Application;
import javafx.stage.Stage;

public class Main extends Application {

    // Initialize a stage when first launch app
    @Override
    public void start(Stage stage) throws Exception {
        stage = MStage.getInstance().loadStage(); // create a new instance of stage
    }
}
