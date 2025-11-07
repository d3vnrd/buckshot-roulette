package ov3ipo.code;

import java.util.*;

public class Board {
    Player player;
    Dealer dealer;
    Shotgun gun;
    String name;
    Integer health;
    Integer nItems;
    Boolean exit;
    Scanner scanner = new Scanner(System.in);
    final String topLine = "\nx" + "-".repeat(39) + "♥♦BUCKSHOTxROULETTE♣♠" + "-".repeat(39) + "x\n";
    final String bottomLine = "\nx" + "-".repeat(100) + "x";

    public Board() {
        this.health = 2;
        this.nItems = 0;
        this.exit = false;
    }

    public void start() throws InterruptedException {
        showWaiver();
        askName();
        int currentStage = 1;
        createEntities();

        while (true) {
            if (player.health <= 0) {
                System.out.println("DEALER WINS!\n");
                System.out.println("YOUR LIFE IS NOW MINE!!!\n");
                return;
            } else if (dealer.health <= 0) {
                System.out.println("\n" + name + " WINS!");
                health += 2;
                nItems += 2;
                currentStage++;
                if (currentStage > 3) {
                    System.out.println("ARGHH!!!...");
                    while(true) {
                        System.out.println("Do you want to continue (y/n)?: ");
                        String opt = scanner.next();
                        if (Objects.equals(opt, "y")) return;
                        if (Objects.equals(opt, "n")) exit=true;
                    }
                } else {
                    System.out.println("Processing stage " + "I".repeat(currentStage));
                    createEntities();
                }
            }

            showBoard();
            if(player.health>0) playerTurn();
            if(dealer.health>0) dealerTurn();
        }
    }

    private void createEntities() {
        gun = new Shotgun();
        player = new Player(health, nItems);
        dealer = new Dealer(health, nItems);
    }

    private void showBoard() {
        System.out.println(topLine);

        if (gun.rounds.isEmpty()) {
            gun.loadBullets();
            player.addRandomItems();
            dealer.addRandomItems();
            dealer.getRounds(gun);
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
        if (player.endTurn) player.endTurn = false;

        System.out.println("Your turn...");

        while (!player.endTurn) {
            System.out.print("Use (0)gun | (1)item: ");
            int[] availableChoice = new int[]{0, 1};
            int choice = scanner.nextInt();

            try {
                if (availableChoice[choice] == 0) {
                    System.out.print("Shoot (0)self | (1)dealer: ");
                    int shoot = scanner.nextInt();
                    if (availableChoice[shoot] == 0) {
                        if (!gun.shoot(player)) dealer.miss++;
                    } else gun.shoot(dealer);

                    // if player shoot end turn
                    player.endTurn = true;
                } else {
                    int index = 1;
                    for (String item : player.availableItems) {
                        System.out.print("(" + index + ") " + item + "\n");
                        index++;
                    }
                    System.out.print("Pick an item: ");
                    int itemIndex = scanner.nextInt();
                    player.useItem(itemIndex - 1, dealer, gun);
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

        System.out.println("Dealer turn...");
        Thread.sleep(500);

        // get best action base on current state of the game only end turn when shoot
        while (!player.endTurn) {
            String action = dealer.bestMove(player, gun);
            switch (action) {
                case "opt":
                    System.out.println("Dealer choose to shoot you!");
                    Thread.sleep(500);
                    gun.shoot(player);
                    // turn end only when shoot
                    dealer.endTurn = true;
                    break;
                case "self":
                    System.out.println("Dealer choose to shoot himself!");
                    Thread.sleep(500);
                    if (!gun.shoot(dealer)) player.miss++;
                    // turn end only when shoot
                    dealer.endTurn = true;
                    break;
                case "magnify", "handsaw", "cigarette", "beer", "handcuff":
                    dealer.useItem(action, player, gun);
                    break;
            }
        }
    }

    private void askName() {
        String[] unavailableNames = new String[]{"GOD", "SATAN", "DEALER"};
        while (true) {
            System.out.print("Sign the waiver? (enter your name): ");
            this.name = scanner.nextLine().replace(" ", "").toUpperCase();
            System.out.println();
            if (Arrays.asList(unavailableNames).contains(name)) {
                System.out.println("Invalid name, try again!");
            } else if (name.length() < 3 || name.length() > 6) {
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

    public void showCredit() {
        System.out.println("\n―――――――――――――――――――――――――――――――――");
        System.out.println("This game is based on the actual game 'buckshot roulette'.\nIn a nutshell, this is russian roulette.\nInfo: https://en.wikipedia.org/wiki/Buckshot_Roulette\n");
        System.out.println("This is a small project of mine toward DSA course at\nInternational University HCM");
        System.out.println("Name: Nguyen Tri Tin    ID: ITDSIU21123     Class: ITIT22IU11");
        System.out.println("―――――――――――――――――――――――――――――――――");
    }

}
