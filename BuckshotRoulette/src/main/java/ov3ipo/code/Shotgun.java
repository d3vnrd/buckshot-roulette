package ov3ipo.code;

import java.util.*;

public class Shotgun {
    Queue<Boolean> rounds;
    Random rand;
    int damage, lives, blanks;
    Boolean public_chamber = null;

    public Shotgun() {
        rounds = new LinkedList<>();
        rand = new Random();
        damage = 1;
    }

    public void loadBullets() {
        List<Boolean> temp = new ArrayList<>();
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
            public_chamber = true;
            lives--;
        } else {
            if (damage == 2) {
                resetDamage();
            }
            System.out.println("\nCLICK!\n");
            Thread.sleep(1000);
            public_chamber = false;
            blanks--;
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
