package ov3ipo.code;

import java.util.InputMismatchException;
import java.util.Scanner;

public class Main {
    public static int opt;
    public static void main(String[] args) throws InterruptedException {
        Scanner scanner = new Scanner(System.in);
        Game buckshot = new Game();

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
                        buckshot.showWaiver();
                        buckshot.askName();
                        buckshot.start();
                        break;
                    case 2:
                        showCredit();
                        Thread.sleep(5000);
                        break;
                    case 0:
                        buckshot.exit();
                        break;
                }
            } while(!buckshot.exit);
        } catch (InputMismatchException e) {
            System.out.println("\nI DON'T HAVE TIME TO PLAY WITH YOU, GET OUT!!!");
        }
    }

    private static void showCredit() {
        System.out.println("This is a small project of mine toward DSA course at International University HCM");
        System.out.println("Name: Nguyen Tri Tin    ID: ITDSIU21123     Class: ");
    }

}
