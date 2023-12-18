// mapping includes letters that could over lap (ie oneight should be 18)
const numberMappings = {
    one: 'o1e',
    two: 't2o',
    three: 't3e',
    four: '4',
    five: '5e',
    six: '6',
    seven: '7n',
    eight: 'e8t',
    nine: 'n9e',
    zero: '0o'
}

function digitFilter(line) {
    return line.replace(/\D/g, '');
}

function sum(a, b) {
    return a + b;
}

function generateNumber(line) {
    var number = line.length == 1 ? line + line : (line[0] + line[line.length - 1]);
    return parseInt(number);
}

function partTwoMapper(line) {
    return Object.entries(numberMappings)
        .reduce((val, [number, mapping]) => val.replaceAll(number, mapping), line);
}

function partTwo(input) {
    return input.map(partTwoMapper).map(digitFilter).map(generateNumber).reduce(sum)
}


function partOne(input) {
    return input.map(digitFilter).map(generateNumber).reduce(sum)
}

