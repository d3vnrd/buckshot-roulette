package ov3ipo.code;

import java.util.InputMismatchException;
import java.util.Scanner;

public class Main {
    public static int opt;
    public static void main(String[] args) throws InterruptedException {
        Scanner scanner = new Scanner(System.in);
        Game buckshot = new Game();

        try {
            do {
                System.out.println("\nx" + "-".repeat(39) + "♥♦BUCKSHOTxROULETTE♣♠" + "-".repeat(39) + "x\n");
                System.out.println("Two enter only one leaves,\nI grants wishes for those who challenge me!\n");
                System.out.println("(1) - Enter");
                System.out.println("(2) - Credit");
                System.out.println("(0) - Exit");
                System.out.println("\nx" + "-".repeat(99)+ "x");
                System.out.print("The choice is your: ");
                opt = scanner.nextInt();

                switch (opt) {
                    case 1:
                        buckshot.enterStage1();
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
        System.out.println("\n―――――――――――――――――――――――――――――――――");
        System.out.println("This game is based on the actual game 'buckshot roulette'.\nIn a nutshell, this is russian roulette.\nInfo: https://en.wikipedia.org/wiki/Buckshot_Roulette\n");
        System.out.println("This is a small project of mine toward DSA course at\nInternational University HCM");
        System.out.println("Name: Nguyen Tri Tin    ID: ITDSIU21123     Class: ITIT22IU11");
        System.out.println("―――――――――――――――――――――――――――――――――");
    }

}
