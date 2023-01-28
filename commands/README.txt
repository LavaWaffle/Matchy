Documentation for commands:

Define a module-wide variable called NAME that holds the command name (e.g. "team" if the command is /team).
Define a module-wide variable called DESCRIPTION that holds the command description.
If the command should not be available as a prefix command, define a module-wide variable called SLASH_ONLY and set it to True.
Define a module-wide async function called run that takes the following parameters:
    ctx (the lightbulb.Context object)
    Any further arguments, like so:
        <name>: ("<description>", <type>) [= <default>]
    Examples:
        rank: ("Whether or not to rank", bool)
        year: ("The year to check", int) = time.localtime().tm_year