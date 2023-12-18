let data = $0.innerText.split('\n')
let copies = {}

function parseCard(card) {
    const [card_num, winningDigits, numbers] = card.split(/[:|]+/)
    const winners = winningDigits.split(" ").filter(x => x)

    const numberList = numbers.split(" ").filter(x => x)

    var matches = numberList.filter((number) => winners.includes(number))

    let points = (matches.length > 0) ? Math.pow(2, matches.length - 1) : 0

    let number = parseInt(card_num.replace(/Card +/, ''))

    if (copies.hasOwnProperty(number)) {
        copies[number] += 1
    }
    else {
        copies[number] = 1;
    }

    for (let i = number + 1; i <= matches.length + number; i++) {
        copies[i] = (copies.hasOwnProperty(i)) ? copies[i] + copies[number] : copies[number]
    }

    return points
}
data.filter(x => x).map(parseCard).reduce((a, x) => a + x)
Object.values(copies).reduce((a, b) => a + b)