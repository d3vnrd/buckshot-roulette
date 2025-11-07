package ov3ipo.code;

import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.util.*;
import org.apache.commons.beanutils.BeanUtils;

public class Player {
    private int health, magnify, cigarette, beer, handcuff, handsaw;

    public Player(int max_health) {
        this.health = max_health;
        this.magnify = 0;
        this.cigarette = 0;
        this.beer = 0;
        this.handcuff = 0;
        this.handsaw = 0;
    }
    //------------------------------------------------------------------------------------------
    // check if a given class has a field that was initialized
    private boolean hasField(final Class<?> c, final String field) {
        // gather all fields of this class
        List<Field> fields = new ArrayList<>();
        Collections.addAll(fields, c.getDeclaredFields());
        // check if field exists
        return fields.stream().map(Field::getName).anyMatch(f -> f.equals(field));
        // NOTE: this one can only check for current fields that are visible within the class itself not to work for classes that are inherited
    }

    //------------------------------------------------------------------------------------------
    // player use an item
    public Player use(String item) throws InvocationTargetException, IllegalAccessException {
        // TODO: make it as generic as possible to reduce setter and getter methods
        // TODO: this is heavily related to Reflection in java
        // TODO: still stuck at how to deal with copy values from a initial instance to a new one exist within class
        System.out.println("Outside loop");
        if (hasField(Player.class, item)) {
            System.out.println("Inside loop");
            Player new_player = new Player(this.health);
            Class<?> current = Player.class;
            BeanUtils.copyProperties(new_player, current);
            return new_player;
        } else {
            System.out.println("Invalid item: " + item);
            return null;
        }
    }

    public int sumItems() {
        return magnify + beer + handcuff + handsaw + cigarette;
    }
}
