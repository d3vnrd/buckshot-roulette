from typing import override

from textual.reactive import reactive
from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import (
    Container,
    Horizontal,
    HorizontalGroup,
    Vertical,
)
from textual.widgets import (
    DataTable,
    Label,
    ProgressBar,
    RichLog,
)

from buckshot import BuckshotEngine

"""Static Widgets"""
class Header(Horizontal):
    @override
    def compose(self) -> ComposeResult:
        yield Label(f"[dim]{self.app.title} - {self.app.sub_title}[/dim]")
        yield Label("[dim]13:10:58[/dim]", classes="right-align")

class GameTitle(Vertical):
    @override
    def compose(self) -> ComposeResult:
        yield Label("[bold orange]BUCKSHOTxROULETTE[/bold orange]", id="title")
        yield Label(f"[dim]x{'-'*45}x[/dim]", id="divider")
        yield Label("[dim]Based on Buckshot Roulette by Mike Klubnika[/dim]", classes="other")
        yield Label("[dim]Press <Space> to continue[/dim]", classes="other")

"""Base Observer Widget"""
class TextualObserver(Widget, BuckshotEngine.BuckshotObserver):
    def __init__(self, engine: BuckshotEngine) -> None:
        Widget.__init__(self)
        engine.attach(self)

"""Reactive Widgets: GameBoard Status"""
class GameStatus(TextualObserver):
    _stage_idx: dict[int, str] = {1: "I", 2: "II", 3: "III"}

    gun_capacity = reactive(0)
    gun_bullets_left = reactive(0)
    curr_turn = reactive("")
    items_per_reload = reactive(0)
    gun_lives = reactive(0)
    stage = reactive("")

    @override
    def compose(self) -> ComposeResult:
        yield Label("Game Status", classes="pane-title")

        with HorizontalGroup():
            yield Label("Gun Chamber: ")
            yield ProgressBar(
                total=0, 
                show_percentage=False, 
                show_eta=False, 
                classes="right-align",
                id="chamber-bar"
            )

        with HorizontalGroup():
            yield Label("Current Turn: ")
            yield Label("?", classes="right-align", id="turn-label")

        with HorizontalGroup():
            yield Label("Items Per Reload: ")
            yield Label("?", classes="right-align", id="items-label")

        with HorizontalGroup():
            yield Label("Live Shells: ")
            yield Label("?", classes="right-align", id="lives-label")

        with HorizontalGroup():
            yield Label("Stage: ")
            yield Label("?", classes="right-align", id="stage-label")

    @override
    def on_engine_update(self, state: BuckshotEngine.BuckshotState):
        """Update reactive variables from state"""
        self.gun_capacity = state.stage.gun_capacity
        self.gun_bullets_left = state.shotgun.bullets_left
        self.curr_turn = state.players[state.curr_turn_idx].name
        self.items_per_reload = state.stage.items_per_reload
        self.gun_lives = state.shotgun.lives
        self.stage = self._stage_idx.get(state.stage.index, "?")

    def on_mount(self):
        """Set up watchers"""
        watchers = [
            # (attr, queried-id, widget, updater(self.query_one, v))
            ("gun_capacity", "#chamber-bar", ProgressBar, lambda u, v: u.update(total=v)),
            ("gun_bullets_left", "#chamber-bar", ProgressBar, lambda u, v: u.update(progress=v)),
            ("curr_turn", "#turn-label", Label, lambda u, v: u.update(v)),
            ("items_per_reload", "#items-label", Label, lambda u, v: u.update(str(v))),
            ("gun_lives", "#lives-label", Label, lambda u, v: u.update(str(v))),
            ("stage", "#stage-label", Label, lambda u, v: u.update(v)),
        ]

        def make_watcher(query, widget_cls, handler):
            def watch_fn(v):
                widget = self.query_one(query, widget_cls)
                handler(widget, v)
            return watch_fn
    
        for attr, query, widget, handler in watchers:
            self.watch(
                self, attr,
                make_watcher(query, widget, handler)
            )

class GameLogs(TextualObserver):
    message: reactive[str] = reactive("")

    @override
    def compose(self) -> ComposeResult:
        yield Label("Logs", classes="pane-title")
        yield RichLog(id="game-logs")

    @override
    def on_engine_update(self, state: BuckshotEngine.BuckshotState):
        self.message = state.message

    def watch_message(self, old:str , new: str):
        if new and new != old:
            self.query_one("#game-logs", RichLog).write(new)

class GameChats(TextualObserver):
    message: reactive[str] = reactive("")

    @override
    def compose(self) -> ComposeResult:
        yield Label("Chats", classes="pane-title")
        yield RichLog(wrap=True, id="game-chats")

    @override
    def on_engine_update(self, state: BuckshotEngine.BuckshotState):
        self.message = state.players[state.curr_turn_idx].message

    def watch_message(self, old:str , new: str):
        if new and new != old:
            self.query_one("#game-chats", RichLog).write(new)

"""Reactive Widgets: Player Status"""
class PlayersInfo(TextualObserver):
    players: dict[str, dict[str, reactive[str|int]]] = {
        "player1": {
            "name": reactive(""),
            "health": reactive(0),
            "total_items": reactive(0),
        },
        "player2": {
            "name": reactive(""),
            "health": reactive(0),
            "total_items": reactive(0),
        }
    }

    @override
    def compose(self) -> ComposeResult:
        for player in self.players.keys():
            with Container(classes="player-card"):
                yield Label("?", classes="pane-title", id=f"{player}-name")
                
                with HorizontalGroup():
                    yield Label("Health: ")
                    yield ProgressBar(
                        total=0,
                        show_percentage=False,
                        show_eta=False,
                        classes="right-align",
                        id=f"{player}-health"
                    )
                
                with HorizontalGroup():
                    yield Label("Total Items: ")
                    yield Label("?", classes="right-align", id=f"{player}-total-items")

    @override
    def on_engine_update(self, state: BuckshotEngine.BuckshotState):
        for i, player_attrs in enumerate(self.players.values()):
            for k in player_attrs:
                player_attrs[k] = state.players[i][k]

    def on_mount(self):
        watchers: dict[str, tuple] = {
            "name": (Label, lambda u, v: u.update(v)),
            "health": (ProgressBar, lambda u, v: u.update(progress=v)),
            "total_items": (Label, lambda u, v: u.update(str(v)))
        }

        for pid in self.players:
            for attr, (widget, handler) in watchers.items():
                query = f"#{pid}-{attr.replace("_", "-")}"
                self.watch(
                    self.players[pid],  # pyright: ignore[reportArgumentType]
                    attr,
                    lambda v, q=query, w=widget, h=handler:
                        h(self.query_one(q, w), v)
                )

class PlayersInventory(TextualObserver):
    @override
    def compose(self) -> ComposeResult:
        yield Label("Detail Inventory", classes="pane-title")
        #TODO: Learn how to use table to show player inventories
        yield DataTable()
