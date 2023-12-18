
const max_blue = 14
const max_red = 12
const max_green = 13

function getMax(game, color) {
    return Math.max(...(game.match(new RegExp(`\\d+ ${color}`, "g"))?.map(x => x.split(' ')[0] | 0)) ?? [0])
}

function parseGame(game) {
    let red = getMax(game, 'red')
    let blue = getMax(game, 'blue')
    let green = getMax(game, 'green')
    let id = parseInt(game.replace("Game ", ""));

    if (red > max_red || blue > max_blue || green > max_green) {
        return 0;
    }

    return id || 0;
}

function parseGame2(game) {
    let red = getMax(game, 'red')
    let blue = getMax(game, 'blue')
    let green = getMax(game, 'green')

    return red * blue * green;
}

function partOne(data) {
    return data.map(parseGame).reduce((a, b) => a + b);
}

function partTwo(data) {
    return data.map(parseGame2).reduce((a, b) => a + b);
}