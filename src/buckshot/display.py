from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Input, Static, Label, Log
from textual.binding import Binding

class PlayerCard(Static):
    """Widget to display player info"""
    
    DEFAULT_CSS = """
    PlayerCard {
        border: solid green;
        height: 100%;
        padding: 1;
        content-align: center middle;
    }
    """
    
    def __init__(self, player_name: str, **kwargs):
        super().__init__(**kwargs)
        self.player_name = player_name
        self.health = 0
        self.items = []
    
    def compose(self) -> ComposeResult:
        yield Label(self.player_name, id="player-name")
        yield Label("❤️ Health: 0", id="health")
        yield Label("🎒 Items: ", id="items")
    
    def update_display(self, health: int, items: dict[str, int]):
        """Update player stats"""
        self.health = health
        self.items = items
        
        self.query_one("#health", Label).update(f"❤️ Health: {health}")
        
        items_str = ", ".join([f"{count}x {item}" for item, count in items.items() if count > 0])
        self.query_one("#items", Label).update(f"🎒 Items: {items_str or 'None'}")

class ChamberDisplay(Static):
    """Widget to display chamber status"""
    
    DEFAULT_CSS = """
    ChamberDisplay {
        border: solid yellow;
        height: 100%;
        width: 10;
        padding: 1;
        content-align: center middle;
    }
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.live_count = 0
        self.blank_count = 0
    
    def compose(self) -> ComposeResult:
        yield Label("🔫", id="gun-icon")
        yield Label("Chamber", id="chamber-label")
        yield Label("Live: 0", id="live-count")
        yield Label("Blank: 0", id="blank-count")
    
    def update_chamber(self, live: int, blank: int):
        """Update chamber counts"""
        self.live_count = live
        self.blank_count = blank
        self.query_one("#live-count", Label).update(f"🔴 {live}")
        self.query_one("#blank-count", Label).update(f"⚪ {blank}")

class StatusConsole(Static):
    """Top status bar showing game state"""
    
    DEFAULT_CSS = """
    StatusConsole {
        height: 3;
        border: solid cyan;
        padding: 0 1;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Label("Status: Waiting for player...", id="status-text")

class GameLog(Static):
    """Enhanced game log with statistics"""
    
    DEFAULT_CSS = """
    GameLog {
        border: solid magenta;
        height: 1fr;
        padding: 1;
    }
    
    #stats-panel {
        height: 8;
        border: solid $panel;
        margin-bottom: 1;
        padding: 1;
    }
    
    #log-area {
        height: 1fr;
        border: solid $panel;
        padding: 0 1;
    }
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.log_widget = None
    
    def compose(self) -> ComposeResult:
        yield Label("📊 Game Statistics", id="stats-title")
        
        with Container(id="stats-panel"):
            yield Label("Total Shots: 0", id="total-shots")
            yield Label("Live Shots: 0", id="live-shots")
            yield Label("Blank Shots: 0", id="blank-shots")
            yield Label("Items Used: 0", id="items-used")
            yield Label("Turns Played: 0", id="turns-played")
        
        yield Label("📜 Event Log", id="log-title")
        
        with Container(id="log-area"):
            self.log_widget = Log(highlight=True)
            yield self.log_widget
    
    def add_log(self, message: str):
        """Add a message to the log"""
        if self.log_widget:
            self.log_widget.write_line(message)
    
    def update_stats(self, total_shots: int, live_shots: int, blank_shots: int, 
                     items_used: int, turns_played: int):
        """Update statistics"""
        self.query_one("#total-shots", Label).update(f"🎯 Total Shots: {total_shots}")
        self.query_one("#live-shots", Label).update(f"🔴 Live Shots: {live_shots}")
        self.query_one("#blank-shots", Label).update(f"⚪ Blank Shots: {blank_shots}")
        self.query_one("#items-used", Label).update(f"🎒 Items Used: {items_used}")
        self.query_one("#turns-played", Label).update(f"⏱️ Turns: {turns_played}")

class PlayerInteractive(Static):
    """Interactive area with detailed action menu"""
    
    DEFAULT_CSS = """
    PlayerInteractive {
        border: solid green;
        height: 50%;
        padding: 1;
    }
    
    #action-menu {
        height: 1fr;
    }
    
    #item-details {
        height: 8;
        border: solid $panel;
        margin-top: 1;
        padding: 1;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Label("⚡ Quick Actions", id="action-title")
        
        with Container(id="action-menu"):
            yield Label("\n[1] 🎯 Shoot Opponent", id="action-1")
            yield Label("[2] 🔄 Shoot Self (risky!)", id="action-2")
            yield Label("[3] 🎒 Use Item", id="action-3")
            yield Label("[4] 📋 View Inventory", id="action-4")
            yield Label("[5] 📊 View Stats", id="action-5")
        
        yield Label("\n💡 Item Info", id="item-info-title")
        
        with Container(id="item-details"):
            yield Label("🔍 Magnifier: Peek next shell", id="magnifier-help")
            yield Label("🍺 Beer: Eject current shell", id="beer-help")
            yield Label("🪚 Handsaw: Double damage", id="handsaw-help")
            yield Label("🚬 Cigarette: Heal +1 HP", id="cigarette-help")
            yield Label("⛓️ Handcuff: Skip opponent turn", id="handcuff-help")

class ChatSection(Static):
    """Chat/command input section"""
    
    DEFAULT_CSS = """
    ChatSection {
        border: solid blue;
        height: 10;
        padding: 1;
    }
    
    #chat-log {
        height: 1fr;
        border: solid $panel;
        padding: 0 1;
        margin-bottom: 1;
    }
    
    #chat-input-container {
        height: 3;
    }
    
    Input {
        width: 100%;
    }
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chat_log = None
    
    def compose(self) -> ComposeResult:
        yield Label("💬 Chat / Commands", id="chat-title")
        
        # Chat log area
        with Container(id="chat-log"):
            self.chat_log = Log(highlight=True)
            yield self.chat_log
        
        # Input area
        with Container(id="chat-input-container"):
            yield Label("Type command:", id="input-label")
            yield Input(placeholder="shoot, use magnifier, help...", id="chat-input")
    
    def add_message(self, message: str, sender: str = "System"):
        """Add a message to chat"""
        if self.chat_log:
            self.chat_log.write_line(f"[bold]{sender}:[/bold] {message}")

class BuckshotRouletteApp(App):
    """Buckshot Roulette TUI Application"""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    #status-row {
        height: 3;
        dock: top;
    }
    
    #players-row {
        height: 12;
    }
    
    #game-area-row {
        height: 1fr;
    }
    
    Horizontal {
        height: 100%;
    }
    
    #player1-card {
        width: 1fr;
    }
    
    #chamber {
        width: 12;
    }
    
    #player2-card {
        width: 1fr;
    }
    
    /* Game log takes 50% of horizontal space */
    #game-log {
        width: 50%;
    }
    
    /* Right panel takes 50% of horizontal space */
    #right-panel {
        width: 50%;
    }
    
    /* Chat and interactive split vertically within right panel */
    #chat-section {
        height: 50%;
    }
    
    #interactive-area {
        height: 50%;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("1", "shoot_opponent", "Shoot Opponent"),
        Binding("2", "shoot_self", "Shoot Self"),
        Binding("3", "use_item", "Use Item"),
    ]
    
    def compose(self) -> ComposeResult:
        """Create child widgets"""
        yield Header(name="BUCKSHOTxROULETTE")
        
        # Status Console at top
        with Container(id="status-row"):
            yield StatusConsole()
        
        # Players and Chamber row
        with Container(id="players-row"):
            with Horizontal():
                yield PlayerCard("Player 1", id="player1-card")
                yield ChamberDisplay(id="chamber")
                yield PlayerCard("Player 2", id="player2-card")
        
        # Game log and right panel (chat + interactive)
        with Container(id="game-area-row"):
            with Horizontal():
                yield GameLog(id="game-log")
                
                # Right panel with chat and interactive stacked
                with Vertical(id="right-panel"):
                    yield ChatSection(id="chat-section")
                    yield PlayerInteractive(id="interactive-area")

    
    def on_mount(self) -> None:
        """Called when app starts"""
        self.title = "Buckshot Roulette"
        self.sub_title = "A game of chance and strategy"
        
        # Initialize with demo data
        self.query_one("#player1-card", PlayerCard).update_display(
            health=5,
            items={"magnifier": 1, "beer": 2, "handsaw": 1}
        )
        
        self.query_one("#player2-card", PlayerCard).update_display(
            health=4,
            items={"cigarette": 1, "handcuff": 1}
        )
        
        self.query_one("#chamber", ChamberDisplay).update_chamber(
            live=3,
            blank=2
        )
        
        game_log = self.query_one("#game-log", GameLog)
        game_log.add_log("🎮 Game started!")
        game_log.add_log("🔫 Chamber loaded: 3 live, 2 blank")
        game_log.add_log("👤 Player 1's turn")
    
    def action_shoot_opponent(self) -> None:
        """Handle shoot opponent action"""
        game_log = self.query_one("#game-log", GameLog)
        game_log.add_log("💥 Player 1 shoots Player 2!")
    
    def action_shoot_self(self) -> None:
        """Handle shoot self action"""
        game_log = self.query_one("#game-log", GameLog)
        game_log.add_log("🎯 Player 1 shoots themselves!")
    
    def action_use_item(self) -> None:
        """Handle use item action"""
        game_log = self.query_one("#game-log", GameLog)
        game_log.add_log("🎒 Player 1 uses an item!")

