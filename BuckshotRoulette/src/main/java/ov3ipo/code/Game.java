package ov3ipo.code;

import java.util.*;

public class Game {
    boolean exit;
    int nItems;
    Queue<Integer> turns;
    Player player;
    Dealer dealer;
    Shotgun gun;
    Random rand;
    Scanner scanner;
    String name;
    String topLine = "\nx" + "-".repeat(39) + "♥♦BUCKSHOTxROULETTE♣♠" + "-".repeat(39) + "x\n";
    String bottomLine = "\nx" + "-".repeat(100)+ "x";

    public Game() {
        this.exit = false;
        rand = new Random();
        scanner = new Scanner(System.in);
        turns = new LinkedList<>();
    }

    public void enterStage1() throws InterruptedException {
        System.out.println(("\n".repeat(5)));
        showWaiver();
        askName();
        reset(2,0);

        while (dealer.health > 0) {
            System.out.println(("\n".repeat(5)));
            showBoard(nItems);
            if(player.health>0)playerTurn();
            if(dealer.health>0)dealerTurn();

            // check if player health is 0
            if (player.health <= 0) {
                System.out.println("\nDEALER WINS!\n");
                System.out.println("YOUR LIFE IS NOW MINE!!!\n");
                exit();
                return;
            }
        }

        if (player.health > 0) {
            System.out.println("\n" + name + " WINS!");
            System.out.println("Processing stage II ...\n");
            enterStage2();
        }
    }

    private void enterStage2() throws InterruptedException {
        reset(4, 2);

        while (dealer.health > 0) {
            showBoard(nItems);
            if(player.health>0)playerTurn();
            if(dealer.health>0)dealerTurn();

            // check if player health is 0
            if (player.health <= 0) {
                System.out.println("DEALER WINS!\n");
                System.out.println("YOUR LIFE IS NOW MINE!!!\n");
                exit();
                return;
            }
        }
        if (player.health > 0) {
            System.out.println("\n" + name + " WINS!");
            System.out.println("Processing stage III ...\n");
            enterStage3();
        }
    }

    private void enterStage3() throws InterruptedException {
        reset(6, 4);
        while (dealer.health > 0) {
            showBoard(nItems);
            if(player.health>0)playerTurn();
            if(dealer.health>0)dealerTurn();

            // check if player health is 0
            if (player.health <= 0) {
                System.out.println("DEALER WINS!\n");
                System.out.println("YOUR LIFE IS NOW MINE!!!\n");
                exit();
                return;
            }
        }

        while (true) {
            System.out.println("\n" + name + " WINS!\n");
            if (player.health > 0) {
                System.out.println("Do you want to continue (y/n)?: ");
                String opt = scanner.next();
                if (Objects.equals(opt, "y")) return;
                if (Objects.equals(opt, "n")) exit();
            }
        }
    }

    private void reset(int default_health, int number_items) {
        gun = new Shotgun();
        player = new Player(default_health);
        dealer = new Dealer(default_health);
        nItems = number_items;
        dealer.miss = 0;
        player.miss = 0;
    }

    private void showBoard(int nItems) {
        System.out.println(topLine);

        if (gun.rounds.isEmpty()) {
            gun.loadBullets();
            player.addRandomItems(nItems);
            dealer.addRandomItems(nItems);
        }

        System.out.println(name + ": " + "♥ ".repeat(this.player.health));
        this.player.displayStorage();
        System.out.println();

        System.out.println("DEALER: " + "♥ ".repeat(this.dealer.health));
        this.dealer.displayStorage();

        System.out.println(bottomLine);
    }

    private void playerTurn() throws InterruptedException {
        // check if current turn is missed
        if (player.miss >= 1) {
            System.out.println("Your turn is skipped...");
            player.miss--;
            return;
        }

        // reset while loop for picking item
        if (player.endTurn) player.endTurn=false;

        System.out.println("Your turn...");

        while (!player.endTurn) {
            System.out.print("Use (0)gun | (1)item: ");
            int[] availableChoice = new int[]{0,1};
            int choice = scanner.nextInt();

            try {
                if (availableChoice[choice] == 0) {
                    System.out.print("Shoot (0)self | (1)dealer: ");
                    int shoot = scanner.nextInt();
                    if (availableChoice[shoot] == 0){
                        if(!gun.shoot(player))
                            dealer.miss++;
                    }
                    else gun.shoot(dealer);

                    // if player shoot end turn
                    player.endTurn=true;
                } else {
                    int index = 1;
                    for (String item: player.availableItems) {
                        System.out.print("(" + index + ") " + item + "\n");
                        index++;
                    }
                    System.out.print("Pick an item: ");
                    int itemIndex = scanner.nextInt();
                    player.useItem(itemIndex-1, dealer, gun);
                }
            } catch (IndexOutOfBoundsException e) {
                System.out.println("\nUh... That is not an option!\n");
                playerTurn();
            }
        }
    }

    private void dealerTurn() throws InterruptedException {
        if (dealer.miss >= 1) {
            System.out.println("Dealer turn is skipped...");
            Thread.sleep(1000);
            dealer.miss--;
            return;
        }

        if (dealer.endTurn) dealer.endTurn=false;

        System.out.println("Dealer turn...");
        dealer.getAction(player, gun);
    }

    private void askName() {
        String[] unavailableNames = new String[]{"GOD", "SATAN", "DEALER"};
        while(true) {
            System.out.print("Sign the waiver? (enter your name): ");
            this.name = scanner.nextLine().replace(" ", "").toUpperCase();
            System.out.println();
            if (Arrays.asList(unavailableNames).contains(name)) {
                System.out.println("Invalid name, try again!");
            } else if (name.length()<3 || name.length()>6) {
                System.out.println("Invalid name, try again!");
            } else {
                break;
            }
        }
    }

    private void showWaiver() {
        System.out.println(topLine);
        System.out.println("INSTRUCTIONS:");
        System.out.println("    - OBJECTIVE: SURVIVE.");
        System.out.println("    - A shotgun is loaded with a disclosed number of bullets, some of which will be blanks.");
        System.out.println("    - Participants are given a set amount of lives to survive.");
        System.out.println("    - You and 'The Dealer' will take turns shooting.");
        System.out.println("    - Aim at The Dealer or at yourself - shooting yourself with a blank skips the Dealers turn.");
        System.out.println("    - Participants are given random items to help out each time the round is empty. Use them wisely.");
        System.out.println("ITEMS:");
        System.out.println("    - Cigarette = Gives the user an extra life.");
        System.out.println("    - Beer = Racks the shotgun and the bullet inside will be discarded.");
        System.out.println("    - Handsaw = Shotgun will deal double damage for one turn.");
        System.out.println("    - Magnifier = User will see what bullet is in the chamber.");
        System.out.println("    - Handcuff = Handcuffs the other person so they miss their next turn.");
        System.out.println("\nGood Luck.");
        System.out.println(bottomLine);
    }

    public void exit() {this.exit = true;}
}
