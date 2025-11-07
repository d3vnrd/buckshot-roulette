package ov3ipo.code;

import java.util.*;

abstract class Entity {
    protected int health, turn;
    protected ArrayList<String> storage;
    protected Entity(int health) {
        this.health = health;
        this.turn = 0;
        this.storage = new ArrayList<>();
    }

    protected void useItem(String item) {

    }

    protected void addRandomItems(String item) {
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
        String item = "";
       return  item;
    }
}

class Shotgun {
    Queue<Boolean> rounds;
    Random random;
    int damage;
    // TODO: function to show number of lives and blanks, then load these into the shotgun rounds
    public Shotgun() {
        random = new Random();
        damage = 1;
    }
    // TODO: function to show the current lives and blanks, then load them into the shotgun
    public void loadBullet(int lives, int blanks) {
        rounds = new LinkedList<>();
        ArrayList<Boolean> temp = new ArrayList<>();
        for (int i=0; i<lives; i++) temp.add(true);
        for (int i=0; i<blanks; i++) temp.add(false);
        Collections.shuffle(temp);
        rounds.addAll(temp);
    }
    public void shoot(Entity effector) {
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