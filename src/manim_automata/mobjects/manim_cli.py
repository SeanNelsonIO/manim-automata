
cli_logo = """
  __  __          _   _ _____ __  __           _    _ _______ ____  __  __       _______          _____ _      _____ 
 |  \/  |   /\   | \ | |_   _|  \/  |     /\  | |  | |__   __/ __ \|  \/  |   /\|__   __|/\      / ____| |    |_   _|
 | \  / |  /  \  |  \| | | | | \  / |    /  \ | |  | |  | | | |  | | \  / |  /  \  | |  /  \    | |    | |      | |  
 | |\/| | / /\ \ | . ` | | | | |\/| |   / /\ \| |  | |  | | | |  | | |\/| | / /\ \ | | / /\ \   | |    | |      | |  
 | |  | |/ ____ \| |\  |_| |_| |  | |  / ____ \ |__| |  | | | |__| | |  | |/ ____ \| |/ ____ \  | |____| |____ _| |_ 
 |_|  |_/_/    \_\_| \_|_____|_|  |_| /_/    \_\____/   |_|  \____/|_|  |_/_/    \_\_/_/    \_\  \_____|______|_____|

"""





class ManimAutomataCLI():


    def __init__(self) -> None:
        print(cli_logo)

    def creation_menu(self):
        options = ["Deterministic Finite Automaton", "Non-determinstic Finite Automaton", "Pushdown Automaton"]
        self.creation_option = self.display_options(options)
        self.file_path = input("Schema File Path: ")

    def display_nda_options(self):
        options = ["Non-deterministic Automaton Path Builder"]
        self.nda_option = self.display_options(options)

    def display_options(self, options) -> str:
        for index, option in enumerate(options):
            print(str(index) + ": " + option)

        return int(input("Choice: "))

    def display_dictionary_options(self, options: dict) -> int:
        for index in options:
            print(f"{index}: {options[index][0]}")

        return int(input("Choice: "))

    def non_determinstic_finite_automata_path_builder_callback(self):
        raise NotImplementedError("Not yet implemented")


if __name__ == "__main__":
    cli = ManimAutomataCLI()