> [!info] Revisit Buckshot Roulette Text-based Game

- TODO:
    - [ ] Classes initializing and Instruction with `--help` tags
    - [ ] Way to handle user script call that align with textual
    - [x] Implement Mediator and Command design patterns
    - [x] Design a communication services between each object
    - [x] Setup a simple user interface with textual for testing
    - [ ] 3 Game mode PvP, PvE (Game-Agent), PvE (AI-Agent)
    - [x] Create a middle class follow Observer design patterns to bridge between the Board (game mediator) and Textual (game interface)
    - [ ] Commands execution & Widgets update
    - [ ] Need a custom Suggester for player input
    - [ ] Better bound commands executed conditions
    - [ ] Feature: navigate between command history

- Notes:
    - Currently focus on Single Player vs Game Agent (Dealer) so `sign` function should only allow one Player's name at a time
    - To use items, enter the command `use` + `<item-name>`. Current items does not require user to specify target, but this is likely to change in the future when more items or multiplayer game mode is added.
    - Other utilities functions include: `clear`, `exit`, `reset` & `help`.
    - When a command is entered, it will be first validated by `CmdsValidator` for command verb, and number of allowed arguments. If passed, the command will be parsed using tokenized parser, and send over to app to execute. 
    - Keep the current UI, don't make any further changes until the engine is complete and player is able to execuate command properly

