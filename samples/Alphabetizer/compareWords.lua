function()
    local words = {
        "Dirt",
        "UN",
        "Uncap",
        "Uncle",
        "Undo",
        "Unify",
        "Union",
        "Unit",
        "Unite",
        "Units",
        "Unset",
        "Until",
        "Unwed",
        "Unzip"
    }

    local inbox = {}

    for str in string.gmatch(words[math.random(#words)], ".") do
        table.insert(inbox, str)
    end
    table.insert(inbox, 0)

    for str in string.gmatch(words[math.random(#words)], ".") do
        table.insert(inbox, str)
    end
    table.insert(inbox, 0)

    return inbox
end