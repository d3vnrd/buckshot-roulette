package ov3ipo.code;

import java.util.Arrays;
import java.util.Objects;
import java.util.Random;
import java.util.Scanner;

public class Game {
    boolean exit;
    Player player;
    Dealer dealer;
    Shotgun gun;
    Random rand;
    Scanner scanner;
    String name;
    String topLine = "\nx" + "-".repeat(41) + "BUCKSHOTxROULETTE" + "-".repeat(41) + "x\n";
    String bottomLine = "\nx" + "-".repeat(99)+ "x";
    public Game() {
        this.exit = false;
        this.gun = new Shotgun();
        rand = new Random();
        scanner = new Scanner(System.in);
    }
    public void start() throws InterruptedException {
        showWaiver();
        askName();

        this.player = new Player(2);
        this.dealer = new Dealer(2);

        while (dealer.health > 0) {
            System.out.println(topLine);
            if (gun.rounds.isEmpty()) {
                int lives = rand.nextInt(1,3);
                int blanks= rand.nextInt(1,3);
                System.out.println(lives + " Lives, " + blanks + " Blanks\n");
                gun.loadBullets(lives, blanks);

                player.addRandomItems(2);
                dealer.addRandomItems(2);
            }

            // print current board
            System.out.println("DEALER: " + "♥ ".repeat(this.dealer.health));
            dealer.displayStorage();
            System.out.println("\n".repeat(1));
            System.out.println(name + ": " + "♥ ".repeat(this.player.health));
            player.displayStorage();
            System.out.println(bottomLine);

            // player turn
            System.out.println("(0) Use the gun (n) Pick a number to use items");
            System.out.print("What will you do?: ");
            int choice = scanner.nextInt();
            if (choice == 0) {
                System.out.print("Shoot (0) SELF or (1) DEALER: ");
                int shoot = scanner.nextInt();
                if (shoot == 0) gun.shoot(player, player);
                else if (shoot == 1) gun.shoot(player, dealer);
            } else player.useItem(player.storage.get(choice));
        }

        if (player.health <= 0) {
            System.out.println("DEALER WINS!\n");
            exit();
        } else {
            System.out.println("\n" + name + " WINS!\n");
            enterStage2();
        }
    }

    private void enterStage2() {
        System.out.println("Processing stage II ...");

        this.gun = new Shotgun();
        this.player = new Player(4);
        this.dealer = new Dealer(4);

        while (dealer.health > 0) {
            System.out.println(topLine);
            if (gun.rounds.isEmpty()) {
                int lives = rand.nextInt(1,4);
                int blanks= rand.nextInt(1,4);
                System.out.println(lives + " Lives, " + blanks + " Blanks\n");
                gun.loadBullets(lives, blanks);

                player.addRandomItems(4);
                dealer.addRandomItems(4);
            }

            // print current board
            System.out.println("DEALER: " + "♥ ".repeat(this.dealer.health));
            this.dealer.displayStorage();
            System.out.println("\n".repeat(1));
            System.out.println(name + ": " + "♥ ".repeat(this.player.health));
            this.player.displayStorage();
            System.out.println(bottomLine);

            // player turn
            System.out.println("(0) Use the gun (n) Pick a number to use items");
            System.out.print("What will you do?: ");
            int choice = scanner.nextInt();
            if (choice == 0) {
                System.out.print("Shoot (0) SELF or (1) DEALER: ");
                int shoot = scanner.nextInt();
                if (shoot == 0) gun.shoot(player, player);
                else if (shoot == 1) gun.shoot(player, dealer);
            } else player.useItem(player.storage.get(choice));
        }

        if (player.health <= 0) {
            System.out.println("DEALER WINS!\n");
            exit();
        } else {
            System.out.println("\n" + name + " WINS!\n");
            enterStage3();
        }
    }

    private void enterStage3() {
        System.out.println("Processing stage III ...");
        System.out.println(topLine);
        System.out.println(bottomLine);
        System.out.println("Do you want to continue (y/n)?: ");
        String opt = scanner.next();
        if (Objects.equals(opt, "y")) {
            enterStage2();
        }
        if (Objects.equals(opt, "n")) exit();
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
