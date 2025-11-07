package ov3ipo.code;

//---------------------------------------------------------------------------------------------------------------
public class Player extends Entity {
    protected Player(int health, int number_items) {
        super(health, number_items);
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
                        gun.public_chamber = gun.rounds.poll();
                        if (Boolean.FALSE.equals(gun.public_chamber)) {
                            System.out.print(" it is a blank!");
                        } else {
                            System.out.print(" it is a live!");
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
