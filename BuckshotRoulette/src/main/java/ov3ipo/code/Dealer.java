package ov3ipo.code;

import java.util.*;

public class Dealer extends Entity {
    Boolean observe = null; // get current status of bullet when shoot is call and when magnify or beer is used
    int lives, blanks, total, default_health; // observe current live and blank

    protected Dealer(int health, int number_items) {
        super(health, number_items);
        default_health = health;
    }

    public void useItem(String item, Player player, Shotgun gun) throws InterruptedException {
        if (this.storage.get(item) > 0) {
            Thread.sleep(300);
            System.out.println("\nDealer use " + item);
            this.storage.put(item, this.storage.get(item) - 1);

            switch (item) {
                case "magnify":
                    System.out.print("Inspecting the gun");
                    for (int i = 1; i <= 3; i++) {
                        System.out.print(".");
                        Thread.sleep(450);
                    }
                    System.out.println();
                    observe = Boolean.TRUE.equals(gun.rounds.peek());
                    System.out.print("Very interesting");
                    for (int i = 1; i <= 3; i++) {
                        System.out.print(".");
                        Thread.sleep(450);
                    }
                    System.out.println();
                    Thread.sleep(1000);
                    break;
                case "beer":
                    System.out.print("Gun has been racked.");
                    for (int i = 1; i <= 3; i++) {
                        System.out.print(".");
                        Thread.sleep(450);
                    }
                    gun.public_chamber = gun.rounds.poll();
                    if (Boolean.FALSE.equals(gun.public_chamber)) {
                        System.out.print(" it is a blank!");
                    } else {
                        System.out.print(" it is a live!");
                    }
                    System.out.println();
                    Thread.sleep(1000);
                    break;
                case "cigarette":
                    System.out.println("Regain 1 health.");
                    Thread.sleep(1000);
                    this.health++;
                    break;
                case "handsaw":
                    System.out.println("Double damage of the next shot!");
                    gun.doubleDamage();
                    Thread.sleep(1000);
                    break;
                case "handcuff":
                    System.out.println("Player next turn is skipped...");
                    player.miss++;
                    Thread.sleep(1000);
                    break;
            }
        } else {
            Thread.sleep(450);
            System.out.print("Nothing happen, try again");
            for (int i = 1; i <= 3; i++) {
                System.out.print(".");
                Thread.sleep(300);
            }
            System.out.println();
            Thread.sleep(1000);
        }
    }

    // TODO: function that return the best current best action for board state
    public String bestMove(Player player, Shotgun gun) {
        // get information about current round
        getRounds(gun);

        List<String> actives = new ArrayList<>();
        for (String item : availableItems) {
            if (storage.get(item) > 0) {
                actives.add(item);
            }
        }

        // assert current actives items
        // always use cigarette as soon as possible
        if (actives.contains("cigarette") && health < default_health) {
            return "cigarette";
        } else actives.remove("cigarette");

        // when use magnify and count of lives = 0 always shoot self
        if (Boolean.FALSE.equals(observe) || lives == 0) return "self";

        // when know next public chamber remove magnify
        if (observe !=null && actives.contains("magnify")) actives.remove("magnify");

        // do not use handcuff when amounts of lives or total bullets < 2
        if (lives<2 || total<2 && actives.contains("handcuff")) actives.remove("handcuff");

//        actives.add("opt");
//        actives.add("self");

        // from actives item generate an action pool
        // generate an action pool
        List<String> actions_pool = new ArrayList<>();
        // multiple time use item - beer this item should always be use as much as possible
        for (int i = 0; i<this.storage.get("beer"); i++) actions_pool.add("beer");
        // one time use item since there is no reason to use more than 1 in one turn
        for (String item: new String[]{"handsaw", "magnify", "handcuff"}) {
            if (actives.contains(item)) actions_pool.add(item);
        }

        // get needed parameter include dmg and hit chance
        int[] dmg = dmgCalculate(player);
        double hit_chance = (double) lives / total;
        if (Boolean.TRUE.equals(observe)) hit_chance = 1;
        else if(Boolean.FALSE.equals(observe)) hit_chance = 0;

        Set<List<String>> actions_combs = possibleActions(actions_pool); // Set is an unordered collection of objects in which duplicate values cannot be stored

        // create a hashmap to store expected value of a sequence of actions
        Map<List<String>, Double> actionValue = new HashMap<>();
        for (List<String> actions : actions_combs) {
            List<String> temp = new ArrayList<>(actions);
            actionValue.put(actions, expectedVal(temp, lives, total, dmg, hit_chance));
        }

        // special handling for handcuff
        if (actives.contains("handcuff")) {
            actions_pool.remove("handcuff");
            for (List<String> action: actionValue.keySet()) {
                if (!action.contains("handcuff")) {
                    continue;
                }

                Hashtable<String, Integer> current_storage = storage;

                List<String> current_pool = new ArrayList<>(actions_pool);

                for (String item : Arrays.asList("handsaw", "magnify")) {
                    if (action.contains(item)) {
                        if (storage.get(item) <=1)
                            current_pool.remove(item);
                        current_storage.put(item, current_storage.get(item) - 1);
                    }
                }
                int beerCount = Collections.frequency(action, "beer");
                current_storage.put("beer", current_storage.get("beer") - beerCount);

                for (int i = 0; i<beerCount; i++)
                    current_pool.remove("beer");

                Set<List<String>> nextActions = possibleActions(current_pool);
                double bestLive = nextActions.stream()
                        .mapToDouble(a -> expectedVal(a, lives - 1, total - 1, dmg, (double) (lives - 1) /(total-1)))
                        .max()
                        .orElse(0.0);

                double bestBlank = nextActions.stream()
                        .mapToDouble(a -> expectedVal(a, lives, total - 1, dmg, (double) lives /(total-1)))
                        .max()
                        .orElse(0.0);

                double updatedValue = actionValue.get(action) +
                        ((double) lives / total) * bestLive +
                        ((double) (total - lives) / total) * bestBlank;

                actionValue.put(action, updatedValue);
            }
        }

        // time complexity?
        return actionValue.entrySet().stream()
                .max(Map.Entry.comparingByValue())
                .map(e -> e.getKey().isEmpty()? "opt" : e.getKey().getFirst())
                .orElse("opt");
    }

    private void getRounds(Shotgun gun) {
        lives = gun.lives;
        blanks = gun.blanks;
        total = lives + blanks;
    }

    // TODO: function to calculate the expected value for a sequence of actions
    // Time complexity?
    private double expectedVal(List<String> actions, int lives, int total, int[] dmg, double hit_chance) {
        double update_hit_chance;
        if (lives <= 0 || total <= 0 || lives > total) return 0;

        if (actions.isEmpty()) {
            if (total > 1) {
                return (dmg[0] * hit_chance) + dmg[1];
            } else return dmg[0] * hit_chance;
        }

        switch (actions.removeFirst()) {
            case "magnify":
                double see_live = expectedVal(actions, lives, total, dmg, 1);
                if (hit_chance < 1 && lives < total) {
                    update_hit_chance = (double) lives / (total - 1);
                    double see_blank = expectedVal(actions, lives, total - 1, dmg, update_hit_chance);
                    return (see_live * hit_chance) + (see_blank * (1 - hit_chance));
                } else return 1;

            case "handcuff":
                // negate dmg from opt since they being handcuffed
                return expectedVal(actions, lives, total, dmg, hit_chance) - dmg[1];

            case "handsaw":
                // update current self damage
                int[] update_dmg = new int[]{dmg[0] * 2, dmg[1]};
                return expectedVal(actions, lives, total, update_dmg, hit_chance);

            case "beer":
                // eject 1 bullet
                update_hit_chance = (double) (lives - 1) / (total - 1);
                double was_live = expectedVal(actions, lives - 1, total - 1, dmg, update_hit_chance);
                if (hit_chance < 1 && lives < total) {
                    update_hit_chance = (double) lives / (total - 1);
                    double was_blank = expectedVal(actions, lives, total - 1, dmg, update_hit_chance);
                    return (was_live * hit_chance) + (was_blank * (1 - hit_chance));
                } else return was_live;
        }
        return 0;
    }

    // this is O(1) only if case
    private int[] dmgCalculate(Player player) {
        int[] dmg = new int[]{1, -1};
        if (player.storage.get("handsaw") > 0) dmg[1] = -2;
        if (player.storage.get("handcuff") > 0 && lives > 1) {
            if (player.storage.get("handsaw") == 1) dmg[1] = -3;
            else if (player.storage.get("handsaw") > 1) dmg[1] = -4;
            else dmg[1] = -2;
        }
        if (this.storage.get("handsaw") > 0) dmg[0] = 2;
        return dmg;
    }

    // TODO: a function that return an sequence of actions that are possible in current state
    private Set<List<String>> possibleActions(List<String> actions_pool) {
        Set<List<String>> actions = new HashSet<>();
        actions.add(new ArrayList<>());  // Add empty list as one of the actions

        int n = actions_pool.size();
        for (int i = 1; i <= n; i++) {
            List<List<String>> combs = generateCombinations(actions_pool, i); // combination generation
            for (List<String> comb : combs) { // combination validation
                boolean valid = true;
                boolean magnify = false;
                for (String item : comb) {
                    if (item.equals("magnify")) {
                        magnify = true;
                    }
                    if (item.equals("beer") && magnify) {
                        valid = false;
                        break;
                    }
                }
                if (valid) {
                    actions.add(comb);
                }
            }
        }
        return actions;
    }

    private List<List<String>> generateCombinations(List<String> actionPool, int k) {
        List<List<String>> result = new ArrayList<>();
        generateCombinationsHelper(actionPool, k, 0, new ArrayList<>(), result);
        return result;
    }

    private void generateCombinationsHelper(List<String> actionPool, int k, int start, List<String> current, List<List<String>> result) { // Time complexity of O(2^A*A)
        if (current.size() == k) {
            result.add(new ArrayList<>(current));
            return;
        }

        for (int i = start; i < actionPool.size(); i++) {
            current.add(actionPool.get(i));
            generateCombinationsHelper(actionPool, k, i + 1, current, result);
            current.removeLast();  // Backtrack
        }
    }
}
