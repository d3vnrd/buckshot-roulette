package ov3ipo.code;

import javafx.stage.Stage;

public class MStage {
    private static volatile MStage instance;
    private Stage stage;
    private MStage() { this.stage = new Stage();}
    public Stage loadStage() {
        return stage;
    }
    public static MStage getInstance() {
        MStage result = instance;
        if (result == null) {
            synchronized (MStage.class) {
                result = instance;
                if (result == null) {
                    instance = result = new MStage();
                }
            }
        }
        return result;
    }
}
