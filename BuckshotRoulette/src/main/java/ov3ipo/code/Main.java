package ov3ipo.code;

import java.util.InputMismatchException;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Scanner scanner = new Scanner(System.in);
        Board board = new Board();

        try {
            do {
                int[] availableChoice = new int[]{0, 1, 2};
                System.out.println("\nx" + "-".repeat(39) + "♥♦BUCKSHOTxROULETTE♣♠" + "-".repeat(39) + "x\n");
                System.out.println("Two enter only one leaves,\nI grants wishes for those who challenge me!\n");
                System.out.println("(1) - Enter");
                System.out.println("(2) - Credit");
                System.out.println("(0) - Exit");
                System.out.println("\nx" + "-".repeat(100)+ "x");
                System.out.print("The choice is your: ");
                int opt = scanner.nextInt();

                switch (availableChoice[opt]) {
                    case 1:
                        board.showWaiver();
                        Thread.sleep(3000);
                        board.askName();
                        board.start();
                        break;
                    case 2:
                        board.showCredit();
                        Thread.sleep(3000);
                        break;
                    case 0:
                        board.exit();
                        break;
                }
            } while(!board.exit);
        } catch (InputMismatchException | IndexOutOfBoundsException e) {
            System.out.println(e);
            System.out.println("\nI DON'T HAVE TIME TO PLAY WITH YOU, GET OUT!!!");
        }
    }
}
