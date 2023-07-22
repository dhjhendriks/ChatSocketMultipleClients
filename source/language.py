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

        case "Accepted new connection from":
            match LANGUAGE:
                case "nl": return "Geaccepteerde nieuwe verbinding van"
                case _:    return "Accepted new connection from"

        case "username":
            match LANGUAGE:
                case "nl": return "gebruikersnaam"
                case _:    return "username"

        case "closed connection from":
            match LANGUAGE:
                case "nl": return "Gesloten verbinding van"
                case _:    return "Closed connection from"

        case "you closed the connection":
            match LANGUAGE:
                case "nl": return "U hebt de verbinding gesloten"
                case _:    return "You closed the connection"

        case "connection closed by the server":
            match LANGUAGE:
                case "nl": return "De verbinding is gesloten door de server"
                case _:    return "Connection closed by the server"




        case _: return "-+-"