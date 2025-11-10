VALID_ITEMS = ["magnify", "handsaw", "cigarette", "beer", "handcuff"]

def show(opt: str) -> str:
    match opt:
        case "credit":
            return """
            """

        case "greet":
            return """
            Two enter only one leaves,\nI grants wishes for those who defeats me!\n
            (1) - Enter\n
            (2) - Credit\n
            (0) - RUN (Coward!)\n\n
            The choice is yours, choose wisely:
            """

        case "waiver":
            return """
            """

        case "help":
            return """
            """

        case _:
            return "Error: Unknow option."


