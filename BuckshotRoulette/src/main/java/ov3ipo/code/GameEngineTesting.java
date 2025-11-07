package ov3ipo.code;

import java.util.Scanner;
import java.util.Random;

class GameEngineTesting{

    public static void main (String[] args) throws Exception {
        PlayRoulette();
    }

    static void PlayRoulette() throws Exception {
        Scanner sc = new Scanner(System.in);

        String[] inventory1 = {"Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty"};
        String[] inventory2 = {"Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty"};

        int player1Health = 3;
        int player2Health = 3;
        int stance = 1;

        boolean[] shotgunLoad = {false, false, false, false, false, false};
        int shotgunRound = 6;

        boolean is1Handcuffed = false;
        boolean is2Handcuffed = false;
        boolean isShotgunSawed = false;

        System.out.println("Loading...");

        while (true) {
            Thread.sleep(2000);
            System.out.println(("\n".repeat(50)));
            if (shotgunRound == 6) {
                int tempRounds = 2 + ((int) (Math.random() * 3));
                System.out.println(tempRounds + " LIVE ROUNDS. " + (6 - tempRounds) + " EMPTY ROUNDS.");
                for (int i = 0; i < tempRounds; i++) {
                    shotgunLoad[i] = true;
                }
                Random rand = new Random();
                for (int i = 0; i < shotgunLoad.length; i++) {
                    int randomIndexToSwap = rand.nextInt(shotgunLoad.length);
                    boolean temp = shotgunLoad[randomIndexToSwap];
                    shotgunLoad[randomIndexToSwap] = shotgunLoad[i];
                    shotgunLoad[i] = temp;
                }
                Thread.sleep(1500);
                shotgunRound = 0;
                System.out.println();
                for (int i = 0; i < 2; i++) {
                    int rndm = (int) (Math.random() * 10);
                    switch (rndm) {
                        case 0: inventory1[canEquipItem(inventory1)] = "Handcuff";
                            System.out.println("PLAYER1 acquired \"Handcuff\". Use it on your opponent to skip his turn once.");
                            break;
                        case 1:
                        case 2: inventory1[canEquipItem(inventory1)] = "Beer";
                            System.out.println("PLAYER1 acquired \"Beer\". Drinking will rack the shotgun and discard the current round in the chamber.");
                            break;
                        case 3:
                        case 4:
                        case 5: inventory1[canEquipItem(inventory1)] = "Cigarettes";
                            System.out.println("PLAYER1 acquired \"Cigarettes\". Smoking will increase your health (unless already full).");
                            break;
                        case 6:
                        case 7: inventory1[canEquipItem(inventory1)] = "Saw";
                            System.out.println("PLAYER1 acquired \"Saw\". Sawing the shotgun doubles its damage.");
                            break;
                        case 8:
                        case 9: inventory1[canEquipItem(inventory1)] = "Hand Glass";
                            System.out.println("PLAYER1 acquired \"Hand Glass\". Seeing through it will reveal the current round in the chamber.");
                            break;
                    }
                    Thread.sleep(750);
                }
                Thread.sleep(1000);
                System.out.println();
                for (int i = 0; i < 2; i++) {
                    int rndm = (int) (Math.random() * 10);
                    switch (rndm) {
                        case 0: inventory2[canEquipItem(inventory2)] = "Handcuff";
                            System.out.println("PLAYER2 acquired \"Handcuff\". Use it on your opponent to skip his turn once.");
                            break;
                        case 1:
                        case 2: inventory2[canEquipItem(inventory2)] = "Beer";
                            System.out.println("PLAYER2 acquired \"Beer\". Drinking will rack the shotgun and discard the current round in the chamber.");
                            break;
                        case 3:
                        case 4:
                        case 5: inventory2[canEquipItem(inventory2)] = "Cigarettes";
                            System.out.println("PLAYER2 acquired \"Cigarettes\". Smoking will increase your health (unless already full).");
                            break;
                        case 6:
                        case 7: inventory2[canEquipItem(inventory2)] = "Saw";
                            System.out.println("PLAYER2 acquired \"Saw\". Sawing the shotgun doubles its damage.");
                            break;
                        case 8:
                        case 9: inventory2[canEquipItem(inventory2)] = "Hand Glass";
                            System.out.println("PLAYER2 acquired \"Hand Glass\". Seeing through it will reveal the current round in the chamber.");
                            break;
                    }
                    Thread.sleep(750);
                }
                Thread.sleep(1000);
            }
            System.out.println();
            System.out.println("PLAYER1                PLAYER2");
            System.out.println("#".repeat(player1Health) + " ".repeat(7-player1Health) + " ".repeat(16) + " ".repeat(7-player2Health) + "#".repeat(player2Health));
            Thread.sleep(500);
            System.out.println();
            if (stance == 1 && is1Handcuffed) {
                System.out.println("PLAYER1 is Handcuffed.");
                stance = 2;
                is1Handcuffed = false;
                continue;
            }
            if (stance == 2 && is2Handcuffed) {
                System.out.println("PLAYER2 is Handcuffed.");
                stance = 1;
                is2Handcuffed = false;
                continue;
            }
            System.out.println(stance == 1 ? "PLAYER1" : "PLAYER2");
            System.out.println();
            System.out.println("(a) Shotgun at Opponent");
            Thread.sleep(100);
            System.out.println("(d) Shotgun at Yourself (skips opponent's turn)");
            Thread.sleep(100);
            for (int i = 0; i < 4; i++) {
                if (stance == 1) {
                    System.out.println("(" + (i+1) + ") " + inventory1[i] + " ".repeat(21-(4+inventory1[i].length())) + "(" + (i+5) + ") " + inventory1[i+4]);
                } else if (stance == 2) {
                    System.out.println("(" + (i+1) + ") " + inventory2[i] + " ".repeat(21-(4+inventory2[i].length())) + "(" + (i+5) + ") " + inventory2[i+4]);
                }
                Thread.sleep(100);
            }
            System.out.println();
            System.out.print("> ");
            char choice = sc.next().charAt(0);
            System.out.println();
            if (choice == 'a') {
                if (shotgunLoad[shotgunRound]) {
                    System.out.println("It was a live round. The opponent suffered damage.");
                    player1Health -= stance == 2 ? (isShotgunSawed ? 2 : 1) : 0;
                    player2Health -= stance == 1 ? (isShotgunSawed ? 2 : 1) : 0;
                } else {
                    System.out.println("It was an empty round. The opponent is unaffected.");
                }
                stance = stance == 1 ? 2 : 1;
                if (isShotgunSawed) {
                    System.out.println("Shotgun has also been unsawed.");
                    isShotgunSawed = false;
                }
                shotgunRound++;
            }
            if (choice == 'd') {
                if (shotgunLoad[shotgunRound]) {
                    System.out.println("It was a live round. You suffered damage.");
                    player1Health -= stance == 1 ? (isShotgunSawed ? 2 : 1) : 0;
                    player2Health -= stance == 2 ? (isShotgunSawed ? 2 : 1) : 0;
                    stance = stance == 1 ? 2 : 1;
                } else {
                    System.out.println("It was an empty round. You are unaffected.");
                }
                if (isShotgunSawed) {
                    System.out.println("Shotgun has also been unsawed.");
                    isShotgunSawed = false;
                }
                shotgunRound++;
            }else if (Character.isDigit(choice)) {
                int ch = Integer.parseInt(choice + "");
                if (ch <= 0 || ch > 8) {
                    System.out.println("Invalid Move.");
                    continue;
                }
                ch--;
                if (stance == 1) {
                    if (inventory1[ch].equals("Empty")) {
                        System.out.println("Invalid Move.");
                        continue;
                    } else if (inventory1[ch].equals("Handcuff")) {
                        if (is2Handcuffed) {
                            System.out.println("PLAYER2 is already handcuffed.");
                            continue;
                        } else {
                            System.out.println("You Handcuffed PLAYER2. His turn will be skipped.");
                            is2Handcuffed = true;
                        }
                    } else if (inventory1[ch].equals("Beer")) {
                        System.out.println("You drank a can of Beer.");
                        System.out.println("It was " + (shotgunLoad[shotgunRound] ? "a live" : "an empty") + " round.");
                        shotgunRound++;
                    } else if (inventory1[ch].equals("Cigarettes")) {
                        System.out.print("You smoked a cigarette ");
                        if (player1Health == 4) {
                            System.out.println(" but gained no health.");
                        } else {
                            System.out.println(" and gained health.");
                            player1Health++;
                        }
                    } else if (inventory1[ch].equals("Saw")) {
                        if (isShotgunSawed) {
                            System.out.println("The shotgun is already sawed.");
                            continue;
                        } else {
                            isShotgunSawed = true;
                            System.out.println("You sawed the shotgun. It will now deal double damage.");
                        }
                    } else if (inventory1[ch].equals("Hand Glass")) {
                        System.out.println("You used your Hand Glass.");
                        System.out.println("The current round in the chamber is " + (shotgunLoad[shotgunRound] ? "a live" : "an empty") + " round.");
                    }
                    inventory1[ch] = "Empty";
                }
                if (stance == 2) {
                    if (inventory2[ch].equals("Empty")) {
                        System.out.println("Invalid Move.");
                        continue;
                    } else if (inventory2[ch].equals("Handcuff")) {
                        if (is1Handcuffed) {
                            System.out.println("PLAYER1 is already handcuffed.");
                            continue;
                        } else {
                            System.out.println("You Handcuffed PLAYER1. His turn will be skipped.");
                            is1Handcuffed = true;
                        }
                    } else if (inventory2[ch].equals("Beer")) {
                        System.out.println("You drank a can of Beer.");
                        System.out.println("It was " + (shotgunLoad[shotgunRound] ? "a live" : "an empty") + " round.");
                        shotgunRound++;
                    } else if (inventory2[ch].equals("Cigarettes")) {
                        System.out.print("You smoked a cigarette ");
                        if (player2Health == 4) {
                            System.out.println(" but gained no health.");
                        } else {
                            System.out.println(" and gained health.");
                            player2Health++;
                        }
                    } else if (inventory2[ch].equals("Saw")) {
                        if (isShotgunSawed) {
                            System.out.println("The shotgun is already sawed.");
                            continue;
                        } else {
                            isShotgunSawed = true;
                            System.out.println("You sawed the shotgun. It will now deal double damage.");
                        }
                    } else if (inventory2[ch].equals("Hand Glass")) {
                        System.out.println("You used your Hand Glass.");
                        System.out.println("The current round in the chamber is " + (shotgunLoad[shotgunRound] ? "a live" : "an empty") + " round.");
                    }
                    inventory2[ch] = "Empty";
                }
            }
            if (player1Health <= 0) {
                Thread.sleep(2000);
                System.out.println("\n\nPLAYER2 won!");
                return;
            } else if (player2Health <= 0) {
                Thread.sleep(2000);
                System.out.println("\n\nPLAYER1 won!");
                return;
            }
        }
    }

    static int canEquipItem(String[] inventory) {
        int i = 0;
        while (i < inventory.length) {
            if (inventory[i].equals("Empty")) {
                return i;
            }
            i++;
        }
        return -1;
    }
}