package ov3ipo.code;

import java.util.Arrays;
import java.util.Collections;
import java.util.Random;
import java.util.Scanner;

public class Game {
    boolean exit, end;
    Player player;
    Dealer dealer;
    Shotgun gun;
    Random rand;
    Scanner scanner;
    String name;
    public Game() {
        this.exit = false;
        this.end = false;
        this.player = new Player(3); // default start with 4 health
        this.dealer = new Dealer(3); // default start with 4 health
        this.gun = new Shotgun();
        rand = new Random();
        scanner = new Scanner(System.in);
    }
    public void start() {
        // TODO: start the game
        while (player.health >0 && dealer.health >0) {
            // Stage 0: greeting
            System.out.println("\n――――――――――――――――――――――――――――――――――――――――――――\n");

            // Stage 1: load the bullet to gun
            int lives = rand.nextInt(1,3);
            int blanks= rand.nextInt(1,3);
            System.out.println(lives + " lives, and " + blanks + " blanks");
            gun.loadBullet(lives, blanks);
            System.out.println("I insert the shells in an unknown order.");
            System.out.println("They enter the chamber in a hidden sequence.");
            System.out.println("\n――――――――――――――――――――――――――――――――――――――――――――\n");
            System.out.println(this.name + " ".repeat(22) + "DEALER");
            System.out.println("♥".repeat(player.health) + " ".repeat(7- player.health) + " ".repeat(16) + " ".repeat(7- dealer.health) + "♥".repeat(dealer.health));
            break;
        }
    }
    public void exit() {
        this.exit = true;
    }
    // TODO(done): a function to ask player name in order to sign the waiver
    public void askName() {
        String[] unavailableNames = new String[]{"GOD", "SATAN", "DEALER"};
        while(true) {
            System.out.println("Sign the waiver? (enter your name): ");
            this.name = scanner.nextLine().replace(" ", "").toUpperCase();
            if (Arrays.asList(unavailableNames).contains(name)) {
                System.out.println("Invalid name, try again!");
            } else if (name.length()<3 || name.length()>6) {
                System.out.println("Invalid name, try again!");
            } else {
                System.out.println("Welcome, " + this.name);
                break;
            }
        }
    }
    public void showWaiver() {
        System.out.println("\n―――――――――――――――――――――――――――――――――");
        System.out.println("This game is based on the actual game 'buckshot roulette'.\nIn a nutshell, this is russian roulette.\nInfo: https://en.wikipedia.org/wiki/Buckshot_Roulette\n");
        System.out.println("INSTRUCTIONS:");
        System.out.println("    - OBJECTIVE: SURVIVE.");
        System.out.println("    - A shotgun is loaded with a disclosed number of bullets, some of which will be blanks.");
        System.out.println("    - Participants are given a set amount of lives (default = 4) to survive.");
        System.out.println("    - You and 'The Dealer' will take turns shooting.");
        System.out.println("    - Aim at The Dealer or at yourself - shooting yourself with a blank skips the Dealers turn.");
        System.out.println("    - Participants are given items to help out. Use them wisely.");
        System.out.println("ITEMS:");
        System.out.println("    - Cigarette = Gives the user an extra life.");
        System.out.println("    - Beer = Racks the shotgun and the bullet inside will be discarded.");
        System.out.println("    - Handsaw = Shotgun will deal double damage for one turn.");
        System.out.println("    - Magnifier = User will see what bullet is in the chamber.");
        System.out.println("    - Handcuff = Handcuffs the other person so they miss their next turn.");
        System.out.println("\nGood Luck.");
        System.out.println("―――――――――――――――――――――――――――――――――");
    }
}
