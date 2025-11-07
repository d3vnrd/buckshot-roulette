package ov3ipo.code;

import java.util.InputMismatchException;
import java.util.Scanner;

public class Main {
    public static int opt;
    public static void main(String[] args) throws InterruptedException {
        Scanner scanner = new Scanner(System.in);
        Game buckshot = new Game();
        opt = 0;

        //TODO: welcome page include -> title, (1) Start, (2) Credit, (0) Exit
        try {
            do {
                System.out.println(
                        "\n――――――――――――――――――――――\n" +
                        "      ♥♦ Buckshot Roulette ♣♠" +
                        "\n――――――――――――――――――――――"
                );
                System.out.println(
                        "\nTwo enter only one leaves,\n" +
                        "I grants wishes for those who challenge me!\n"
                );
                System.out.println("(1) - Enter");
                System.out.println("(2) - Credit");
                System.out.println("(0) - Exit");
                System.out.print("\nThe choice is your: ");
                opt = scanner.nextInt();

                switch (opt) {
                    case 1:
                        buckshot.start();
                        break;
                    case 2:
                        showCredit();
                        Thread.sleep(5000);
                        break;
                }
            } while(opt != 0);
        } catch (InputMismatchException e) {
            System.out.println("\nI DON'T HAVE TIME TO PLAY WITH YOU");
        }
    }

    private static void showCredit() {
        System.out.println("This is a small project of mine toward DSA course at International University HCM");
        System.out.println("Name: Nguyen Tri Tin    ID: ITDSIU21123     Class: ");
    }

    public static void showWaiver() {
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
