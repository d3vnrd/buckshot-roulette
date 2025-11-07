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
        this.miss = 0;
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

    // TODO: logic function to deal with when player use an item
    protected void addRandomItems(int nItems) {
        for (int i = 0; i < nItems; i++) {
            String item = availableItems[random.nextInt(availableItems.length)];
            storage.put(item, storage.get(item) + 1);
        }
    }

    protected void takeDamage(int damage) {
        this.health -= damage;
    }
}

class Player extends Entity {

    public Player(int health) {
        super(health);
    }

    public void useItem(int itemIndex, Dealer dealer, Shotgun gun) throws InterruptedException {
        try {
            String item = availableItems[itemIndex];

            if (this.storage.get(item) > 0) {
                Thread.sleep(300);
                System.out.println("\nPlayer use " + item);
                this.storage.put(item, this.storage.get(item) - 1);

                switch (item) {
                    case "magnify":
                        System.out.print("Inspecting the gun");
                        for (int i = 1; i <= 3; i++) {
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
                        for (int i = 1; i <= 3; i++) {
                            System.out.print(".");
                            Thread.sleep(450);
                        }
                        if (Boolean.FALSE.equals(gun.rounds.poll())) {
                            System.out.print(" it is a blank!");
                            gun.public_chamber=false;
                        }
                        else {
                            System.out.print(" it is a live!");
                            gun.public_chamber=true;
                        }
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
                for (int i = 1; i <= 3; i++) {
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
    boolean observe; // get current status of bullet when shoot is call and when magnify or beer is used
    int lives, blanks, total; // observe current live and blank
    public Dealer(int health) {
        super(health);
    }

    public void useItem(String item, Player player, Shotgun gun) throws InterruptedException {
        if (this.storage.get(item) > 0) {
            Thread.sleep(300);
            System.out.println("\nDealer use " + item);
            this.storage.put(item, this.storage.get(item) - 1);

            switch (item) {
                case "magnify":
                   System.out.print("Inspecting the gun");
                    for (int i = 1; i <= 3; i++) {
                        System.out.print(".");
                        Thread.sleep(450);
                    }
                    System.out.println();
                    observe = Boolean.TRUE.equals(gun.rounds.peek());
                    System.out.print("Very interesting");
                    for (int i = 1; i <= 3; i++) {
                        System.out.print(".");
                        Thread.sleep(450);
                    }
                    System.out.println();
                    Thread.sleep(1000);
                    break;
                case "beer":
                    System.out.print("Gun has been racked.");
                    for (int i = 1; i <= 3; i++) {
                        System.out.print(".");
                        Thread.sleep(450);
                    }
                    if (Boolean.FALSE.equals(gun.rounds.poll())) {
                        System.out.print(" it is a blank!");
                        gun.public_chamber=false;
                    }
                    else {
                        System.out.print(" it is a live!");
                        gun.public_chamber=true;
                    }
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
            System.out.print("Nothing happen, try again");
            for (int i = 1; i <= 3; i++) {
                System.out.print(".");
                Thread.sleep(300);
            }
            System.out.println();
            Thread.sleep(1000);
        }
    }

    // TODO: function that return the best current best action for board state
    public String bestMove(Player player, Shotgun gun) {
        if (gun.public_chamber || observe) {
            this.lives--;
            this.total--;
        } else this.total--;

        List<String> actives = new LinkedList<>();
        for (String item: availableItems) {
            if (storage.get(item) > 0) {
                actives.add(item);
            }
        }

        int[] dmg = dmgCalculate(player);
        double hit_chance = (double) this.lives/this.total;

        // get current available items in storage
        if (actives.contains("cigarette") && health < player.health) {
            actives.remove("cigarette");
            return "cigarette";
        } else actives.remove("cigarette");

        return "";
    }


    public boolean checkStorage() { // return false if storage has item, true when empty
        for (String item : availableItems) {
            if (this.storage.get(item) != 0) {
                return false;
            }
        }
        return true;
    }

    public void getRounds(Shotgun gun) {
        this.lives= gun.lives;
        this.blanks= gun.blanks;
        this.total = lives+blanks;
    }

    private double expectedVal(List<String> actions, int lives, int total, int[] dmg, double hit_chance) {
        double update_hit_chance;
        if (lives <=0 || total <=0 || lives>total) return 0;

        if (actions.isEmpty()) {
            if (total > 1){
                return (dmg[0] * hit_chance) + dmg[1];
            } else return dmg[0] * hit_chance;
        }

        switch (actions.removeFirst()) {
            case "magnify":
                double see_live = expectedVal(actions, lives, total, dmg, 1);
                if (hit_chance < 1 && lives < total) {
                    update_hit_chance = (double) lives /(total-1);
                    double see_blank = expectedVal(actions, lives, total-1, dmg, update_hit_chance);
                    return (see_live * hit_chance) + (see_blank * (1-hit_chance));
                } else return 1;

            case "handcuff":
                // negate dmg from opt since they being handcuffed
                return expectedVal(actions, lives, total, dmg, hit_chance) - dmg[1];

            case "handsaw":
                // update current self damage
                int[] update_dmg = new int[]{dmg[0] * 2, dmg[1]};
                return expectedVal(actions, lives, total, update_dmg,hit_chance);

            case "beer":
                // eject 1 bullet
                update_hit_chance = (double) (lives - 1) /(total -1);
                double was_live = expectedVal(actions, lives-1, total-1, dmg, update_hit_chance);
                if (hit_chance<1 && lives<total) {
                    update_hit_chance = (double) lives/(total -1);
                    double was_blank = expectedVal(actions, lives, total-1, dmg, update_hit_chance);
                    return (was_live * hit_chance) + (was_blank * (1-hit_chance));
                } else return was_live;

            case "opt":
                if (total > 1) {
                    return (dmg[0] * hit_chance) + (double) (dmg[1] * (lives - 1)) / (total-1);
                } else return dmg[0] * hit_chance;
            case "self":
                double is_hit = -dmg[0] * hit_chance;
                if (lives>1) is_hit += (double) (dmg[1] * (lives - 1)) /(total-1);
                update_hit_chance = (double) lives /(total-1);

                double is_miss = expectedVal(actions, lives, total-1, dmg, update_hit_chance) * (1-hit_chance);
                if (lives>1 && total>2) is_miss += (double) (dmg[1] * (lives - 1)) / (total-2);
                return is_hit + is_miss;
        }
        return 0;
    }

    private int[] dmgCalculate(Player player) {
        int[] dmg = new int[]{1, -1};
        if (player.storage.get("handsaw")>0) dmg[1] = -2;
        if (player.storage.get("handcuff")>0 && lives > 1) {
            if (player.storage.get("handsaw") == 1) dmg[1] = -3;
            else if (player.storage.get("handsaw") > 1) dmg[1] = -4;
            else dmg[1] = - 2;
        }
        if (this.storage.get("handsaw")>0) dmg[0] = 2;
        return dmg;
    }
}

class Move {

}
class Shotgun {
    Queue<Boolean> rounds;
    Random rand;
    int damage, lives, blanks;
    boolean public_chamber;

    public Shotgun() {
        rounds = new LinkedList<>();
        rand = new Random();
        damage = 1;
    }

    public void loadBullets() {
        ArrayList<Boolean> temp = new ArrayList<>();
        lives = rand.nextInt(1, 4);
        blanks = rand.nextInt(1, 4);
        System.out.println(this.lives + " Lives, " + this.blanks + " Blanks\n");

        for (int i = 0; i < lives; i++) temp.add(true);
        for (int i = 0; i < blanks; i++) temp.add(false);

        Collections.shuffle(temp);
        rounds.addAll(temp);
    }

    public boolean shoot(Entity effector) throws InterruptedException {
        if (Boolean.TRUE.equals(rounds.poll())) {
            if (damage == 2) {
                effector.takeDamage(damage);
                resetDamage();
            } else effector.takeDamage(damage);
            System.out.println("\nBOOM!!!\n");
            Thread.sleep(1000);
            public_chamber=true;
        } else {
            System.out.println("\nCLICK!\n");
            Thread.sleep(1000);
            public_chamber=false;
        }
        return public_chamber;
    }

    public void doubleDamage() {
        this.damage = 2;
    }

    private void resetDamage() {
        this.damage = 1;
    }
}