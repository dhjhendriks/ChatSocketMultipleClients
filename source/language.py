def get_text(string,L):
    LANGUAGE = L
    match string:

        case "Argument_text":
            match LANGUAGE:
                case "nl": return "Argument 'type' moet zijn (s)erver of (c)lient"
                case _:    return "Argument 'type' has to be (s)erver or (c)lient"

        case "Listening_text":
            match LANGUAGE:
                case "nl": return "Luisteren voor verbindingen op"
                case _:    return "Listening for connections on"

        case "Enter Username":
            match LANGUAGE:
                case "nl": return "Typ Gebruikersnaam"
                case _:    return "Enter Username"

        case "The server on":
            match LANGUAGE:
                case "nl": return "De server op"
                case _:    return "The server on"

        case "accepted the username":
            match LANGUAGE:
                case "nl": return "heeft de gebruikersnaam geaccepteerd"
                case _:    return "accepted the username"

        case "welcome":
            match LANGUAGE:
                case "nl": return "Welkom bij Socket!"
                case _:    return "Welcome to Socket!"

        case "type":
            match LANGUAGE:
                case "nl": return "Tik"
                case _:    return "Type"

        case "to exit":
            match LANGUAGE:
                case "nl": return "om te stoppen"
                case _:    return "to quit"

        case "You stopped the server":
            match LANGUAGE:
                case "nl": return "U heeft de server gestopt."
                case _:    return "You stopped the server."



















        case _: return "-"