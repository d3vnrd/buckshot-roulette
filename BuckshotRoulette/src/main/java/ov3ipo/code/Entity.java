package ov3ipo.code;

import java.util.*;

public abstract class Entity {
    protected int health, miss, number_items;
    protected boolean endTurn;
    protected Hashtable<String, Integer> storage;
    private final Random random = new Random();
    protected String[] availableItems = new String[]{"magnify", "handsaw", "cigarette", "beer", "handcuff"};

    protected Entity(int health, int number_items) {
        /*
        These value will always be initialized when object is called
        - health: current entity health
        - miss: status of entity current turn
        - number_items: number of item being added into storage
         */
        this.health = health;
        this.miss = 0;
        this.number_items = number_items;
        this.endTurn = false;
        this.storage = new Hashtable<>();
        for (String item : availableItems) storage.put(item, 0);
    }

    protected void displayStorage() {
        for (int i = 1; i < availableItems.length + 1; i++) {
            String item = availableItems[i - 1];
            if (i % 2 == 0) {
                System.out.print(" | " + item + ": " + this.storage.get(item) + " | ");
            } else {
                System.out.print(item + ": " + this.storage.get(item));
            }
        }
        System.out.println();
    }

    protected void addRandomItems() {
        for (int i = 0; i < spaceLeft(); i++) {
            String item = availableItems[random.nextInt(availableItems.length)];
            storage.put(item, storage.get(item) + 1);
        }
    }

    protected void takeDamage(int damage) {
        this.health -= damage;
    }

    // function that check whether we can add more item to the storage
    protected int spaceLeft() {
        int space_left;
        int current_size = Arrays.stream(availableItems).mapToInt(item -> storage.get(item)).sum();
        int add_size = current_size + number_items;
        if (add_size >= 8) {
            space_left = 8 - current_size;
        } else space_left = number_items;
        return space_left;
    }
}
