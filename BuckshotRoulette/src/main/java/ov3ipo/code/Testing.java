package ov3ipo.code;

import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.util.List;

public class Testing {
    public static void main(String[] args) throws InvocationTargetException, IllegalAccessException {
        Player player = new Player(10);
        player.use("magnify");
    }
}
