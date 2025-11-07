package ov3ipo.code;

import java.io.*;
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
    String bottomLine = "\nx" + "-".repeat(99)+ "x";

    public Game() {
        this.exit = false;
        rand = new Random();
        scanner = new Scanner(System.in);
        turns = new LinkedList<>();
    }

    public void enterStage1() throws InterruptedException {
        showWaiver();
        askName();

        this.gun = new Shotgun();
        this.player = new Player(2);
        this.dealer = new Dealer(2);

        while (dealer.health > 0) {
            showBoard(nItems);
            playerTurn();
            dealerTurn();

            // check if player health is 0
            if (player.health <= 0) {
                System.out.println("\nDEALER WINS!\n");
                System.out.println("YOUR LIFE IS NOW MINE!!!\n");
                break;
            }
        }

        if (player.health > 0) {
            System.out.println("\n" + name + " WINS!");
            System.out.println("Processing stage II ...\n");
            enterStage2();
        }
    }

    private void enterStage2() {

        this.gun = new Shotgun();
        this.player = new Player(4);
        this.dealer = new Dealer(4);
        this.nItems = 2;

        while (dealer.health > 0) {
            showBoard(nItems);
            playerTurn();
            dealerTurn();

            // check if player health is 0
            if (player.health <= 0) {
                System.out.println("DEALER WINS!\n");
                break;
            }
        }
        if (player.health > 0) {
            System.out.println("\n" + name + " WINS!");
            System.out.println("Processing stage III ...\n");
            enterStage3();
        }
    }

    private void enterStage3() {
        this.gun = new Shotgun();
        this.player = new Player(6);
        this.dealer = new Dealer(6);
        this.nItems = 6;

        while (dealer.health > 0) {
            showBoard(nItems);
            playerTurn();
            dealerTurn();

            // check if player health is 0
            if (player.health <= 0) {
                System.out.println("DEALER WINS!\n");
                break;
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

    private void showBoard(int nItems) {
        System.out.println(topLine);

        if (gun.rounds.isEmpty()) {
            gun.loadBullets();
            player.addRandomItems(nItems);
            dealer.addRandomItems(nItems);
        }

        System.out.println("DEALER: " + "♥ ".repeat(this.dealer.health));
        this.dealer.displayStorage();
        System.out.println();

        System.out.println(name + ": " + "♥ ".repeat(this.player.health));
        this.player.displayStorage();

        System.out.println(bottomLine);
    }

    private void playerTurn() {
        System.out.print("Use (0)THE GUN || (1)AN ITEM: ");
        int[] availableChoice = new int[]{0,1};
        int choice = scanner.nextInt();

        try {
            if (availableChoice[choice] == 0) {
                    System.out.print("Shoot (0)SELF  || (1)DEALER: ");
                    int shoot = scanner.nextInt();
                    if (availableChoice[shoot] == 0) gun.shoot(player, player);
                    else gun.shoot(player, dealer);
            } else {
                int index = 1;
                for (String item: player.availableItems) {
                    System.out.print("(" + index + ")" + " " + item + "\n");
                    index++;
                }
                System.out.print("Use: ");
                int itemIndex = scanner.nextInt();
                player.useItem(itemIndex-1);
            }
        } catch (IndexOutOfBoundsException e) {
            System.out.println("\nUh... That is not an option!\n");
            playerTurn();
        }
    }

    private void dealerTurn() {
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
