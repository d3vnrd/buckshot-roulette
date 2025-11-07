package ov3ipo.code;

import java.util.*;

abstract class Entity {
    protected int health, miss;
    protected Hashtable<String, Integer> storage;
    protected Random random;
    protected String[] availableItems = new String[]{"magnify", "handsaw", "cigarette", "beer", "handcuff"};
    protected Entity(int health) {
        this.random = new Random();
        this.health = health;
        this.miss= 0;
        this.storage = new Hashtable<>();
        for (String item: availableItems) storage.put(item, 0);
    }

    protected void displayStorage() {
        for (int i = 1; i<availableItems.length+1; i++) {
            String item = availableItems[i-1];
            if (i%2 == 0) {
                System.out.print(" | " + item + ": " + storage.get(item )+ " | ");
            } else {
                System.out.print(item + ": " + storage.get(item));
            }
        }
        System.out.println();
    }

    // TODO: logic function to deal with when player use an item
    protected void useItem(int itemIndex) {
        try {
            String item = availableItems[itemIndex];

            if (this.storage.get(item) > 0) {
                System.out.println("Player use a " + item);

                switch (item) {
                    case "magnify":
                        break;
                    case "beer":
                        break;
                    case "cigarette":
                        break;
                    case "handsaw":
                        break;
                    case "handcuff":
                        break;
                }

                this.storage.put(item, this.storage.get(item)-1);
            } else {
                System.out.println("Nothing happen ...\nTry again!");
            }
        } catch (IndexOutOfBoundsException e) {
            System.out.println("THERE ARE ONLY 5 ITEMS, OPEN YOUR EYES!");
        }
    }

    protected void addRandomItems(int nItems) {
        for(int i = 0; i<nItems; i++) {
            String item = availableItems[random.nextInt(availableItems.length)];
            storage.put(item, storage.get(item) + 1);
        }
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
    int damage, lives, blanks;
    Random rand;
    public Shotgun() {
        rounds = new LinkedList<>();
        damage = 1;
        rand = new Random();
    }
    public void loadBullets() {
        ArrayList<Boolean> temp = new ArrayList<>();
        lives = rand.nextInt(1,3);
        blanks= rand.nextInt(1,3);
        System.out.println(this.lives + " Lives, " + this.blanks + " Blanks\n");

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