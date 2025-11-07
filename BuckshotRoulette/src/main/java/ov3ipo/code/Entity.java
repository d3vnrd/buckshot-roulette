package ov3ipo.code;

import java.util.*;

abstract class Entity {
    protected int health, miss;
    protected boolean endTurn;
    protected Hashtable<String, Integer> storage;
    protected Random random;
    protected String[] availableItems = new String[]{"magnify", "handsaw", "cigarette", "beer", "handcuff"};
    protected Entity(int health) {
        this.random = new Random();
        this.health = health;
        this.miss= 0;
        this.endTurn = false;
        this.storage = new Hashtable<>();
        for (String item: availableItems) storage.put(item, 0);
    }

    protected void displayStorage() {
        for (int i = 1; i<availableItems.length+1; i++) {
            String item = availableItems[i-1];
            if (i%2 == 0) {
                System.out.print(" | " + item + ": " + this.storage.get(item )+ " | ");
            } else {
                System.out.print(item + ": " + this.storage.get(item));
            }
        }
        System.out.println();
    }

    // TODO: logic function to deal with when player use an item
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

    public void useItem(int itemIndex, Dealer dealer, Shotgun gun) throws InterruptedException {
        try {
            String item = availableItems[itemIndex];

            if (this.storage.get(item) > 0) {
                Thread.sleep(300);
                System.out.println("\nPlayer use " + item);
                this.storage.put(item, this.storage.get(item)-1);

                switch (item) {
                    case "magnify":
                        System.out.print("Inspecting the gun");
                        for (int i = 1; i<=3; i++) {
                            System.out.print(".");
                            Thread.sleep(450);
                        }
                        if (Boolean.FALSE.equals(gun.rounds.peek())) System.out.print(" Blank!");
                        else System.out.print(" Live!");
                        System.out.println();
                        Thread.sleep(1000);
                        break;
                    case "beer":
                        System.out.print("Gun has been racked");
                        for (int i = 1; i<=3; i++) {
                            System.out.print(".");
                            Thread.sleep(450);
                        }
                        if (Boolean.FALSE.equals(gun.rounds.poll())) System.out.print(" it is a blank!");
                        else System.out.print(" it is a live!");
                        System.out.println();
                        Thread.sleep(1000);
                        break;
                    case "cigarette":
                        System.out.println("Regain 1 health.");
                        Thread.sleep(1000);
                        this.health++;
                        break;
                    case "handsaw":
                        System.out.println("Double damage of the next shot!");
                        gun.doubleDamage();
                        Thread.sleep(1000);
                        break;
                    case "handcuff":
                        System.out.println("Dealer next turn is skipped...");
                        dealer.miss++;
                        Thread.sleep(1000);
                        break;
                }

            } else {
                Thread.sleep(450);
                System.out.print("\nNothing happen, try again");
                for (int i = 1; i<=3; i++) {
                    System.out.print(".");
                    Thread.sleep(300);
                }
                System.out.println();
                Thread.sleep(1000);
            }
        } catch (IndexOutOfBoundsException e) {
            System.out.println("\nTHERE ARE ONLY 5 ITEMS, OPEN YOUR EYES!");
            Thread.sleep(1000);
        }
    }
}

class Dealer extends Entity {
    public Dealer(int health) {
        super(health);
    }

    public void useItem(String item, Player player, Shotgun gun) throws InterruptedException {
        try {
            if (this.storage.get(item) > 0) {
                Thread.sleep(300);
                System.out.println("\nDealer use " + item);
                this.storage.put(item, this.storage.get(item)-1);

                switch (item) {
                    case "magnify":
                        System.out.print("Inspecting the gun");
                        for (int i = 1; i<=3; i++) {
                            System.out.print(".");
                            Thread.sleep(450);
                        }
                        if (Boolean.FALSE.equals(gun.rounds.peek())) System.out.print(" Blank!");
                        else System.out.print(" Live!");
                        System.out.println();
                        Thread.sleep(1000);
                        break;
                    case "beer":
                        System.out.print("Gun has been racked");
                        for (int i = 1; i<=3; i++) {
                            System.out.print(".");
                            Thread.sleep(450);
                        }
                        if (Boolean.FALSE.equals(gun.rounds.poll())) System.out.print(" it is a blank!");
                        else System.out.print(" it is a live!");
                        System.out.println();
                        Thread.sleep(1000);
                        break;
                    case "cigarette":
                        System.out.println("Regain 1 health.");
                        Thread.sleep(1000);
                        this.health++;
                        break;
                    case "handsaw":
                        System.out.println("Double damage of the next shot!");
                        gun.doubleDamage();
                        Thread.sleep(1000);
                        break;
                    case "handcuff":
                        System.out.println("Player next turn is skipped...");
                        player.miss++;
                        Thread.sleep(1000);
                        break;
                }

            } else {
                Thread.sleep(450);
                System.out.print("\nNothing happen, try again");
                for (int i = 1; i<=3; i++) {
                    System.out.print(".");
                    Thread.sleep(300);
                }
                System.out.println();
                Thread.sleep(1000);
            }
        } catch (IndexOutOfBoundsException e) {
            System.out.println("\nTHERE ARE ONLY 5 ITEMS, OPEN YOUR EYES!");
            Thread.sleep(1000);
        }
    }

    // TODO: create a function that implement breath first search to return item use with best possibility on either dealing damage to opponent or heal back
    public String getBestItem() {
        String item = "handcuff";
       return item;
    }

    // TODO: a function return a sequence of dealer action
    public void getAction(Player player, Shotgun gun) throws InterruptedException {

        // check if storage have any item
        if (!checkStorage()) {
            String item = getBestItem();
            useItem(item, player, gun);
        }
    }

    public boolean checkStorage() { // return false if storage has item, true when empty
        for (String item: availableItems) {
            if (this.storage.get(item) != 0) {
                return false;
            }
        }
        return true;
    }
}

class Shotgun {
    Queue<Boolean> rounds;
    Random rand;
    int damage, lives, blanks;
    public Shotgun() {
        rounds = new LinkedList<>();
        rand = new Random();
        damage = 1;
    }
    public void loadBullets() {
        ArrayList<Boolean> temp = new ArrayList<>();
        lives = rand.nextInt(1,4);
        blanks= rand.nextInt(1,4);
        System.out.println(this.lives + " Lives, " + this.blanks + " Blanks\n");

        for (int i=0; i<lives; i++) temp.add(true);
        for (int i=0; i<blanks; i++) temp.add(false);

        Collections.shuffle(temp);
        rounds.addAll(temp);
    }

    // TODO: why does this return null value?
    public boolean shoot(Entity effector) throws InterruptedException {
        if (Boolean.TRUE.equals(rounds.poll())){
            if (damage==2) {
                effector.takeDamage(damage);
                resetDamage();
            } else effector.takeDamage(damage);
            System.out.println("\nBOOM!!!\n");
            Thread.sleep(1000);
            return true;
        } else {
            System.out.println("\nCLICK!\n");
            Thread.sleep(1000);
            return false;
        }
    }

    public void doubleDamage() {
        this.damage = 2;
    }
    public void resetDamage() {
        this.damage = 1;
    }
}