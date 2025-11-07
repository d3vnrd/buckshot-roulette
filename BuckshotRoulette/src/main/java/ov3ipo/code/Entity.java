package ov3ipo.code;

import java.util.*;

abstract class Entity {
    protected int health, turn;
    protected ArrayList<String> storage;
    protected Random random;
    protected Entity(int health) {
        this.random = new Random();
        this.health = health;
        this.turn = 0;
        this.storage = new ArrayList<>();
        for (int i=0; i<8; i++) this.storage.add(i, null);
    }

    protected void displayStorage() {
        int choice = 1;
        for (int i=0; i<this.storage.size(); i++) {
            if (this.storage.get(i) != null) {
                System.out.print("(" + choice + ") " + this.storage.get(i) + " ");
                choice++;
            }
        }
        System.out.println();
    }

    // TODO: logic function to deal with when player use an item
    protected void useItem(String item) {

    }

    protected void addRandomItems(int nItems) {
        String[] availableItems = new String[]{"magnify", "handsaw", "cigarette", "beer", "handcuff"};
        for (int i=0; i<nItems; i++) this.storage.addFirst(availableItems[random.nextInt(availableItems.length)]);
    }

    protected void takeDamage(int damage) {
        this.health -= damage;
    }
}

class Player extends Entity{
    public Player(int health) {
        super(health);
    }
}

class Dealer extends Entity {
    public Dealer(int health) {
        super(health);
    }

    // TODO: create a function that implement breath first search to return item use with best possibility on either dealing damage to opponent or heal back
    public String getBestItem() {
        String item = " ";
       return  item;
    }
}

class Shotgun {
    Queue<Boolean> rounds;
    int damage;
    public Shotgun() {
        rounds = new LinkedList<>();
        damage = 1;
    }
    public void loadBullets(int lives, int blanks) {
        ArrayList<Boolean> temp = new ArrayList<>();
        for (int i=0; i<lives; i++) temp.add(true);
        for (int i=0; i<blanks; i++) temp.add(false);
        Collections.shuffle(temp);
        rounds.addAll(temp);
    }
    public void shoot(Entity shooter, Entity effector) {
        if (Boolean.TRUE.equals(rounds.poll())) {
            effector.takeDamage(damage);
        }
    }
    public void doubleDamage() {
        this.damage = 2;
    }
    public void resetDamage() {
        this.damage = 1;
    }
}