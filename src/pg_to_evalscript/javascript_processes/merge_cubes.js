function merge_cubes(arguments) {
    const {cube1, cube2} = arguments;
    let overlappingDimension;

    for (let dimension of cube1.dimensions) {
        const dimension2 = cube2.getDimensionByName(dimension.name)
        if (dimension.labels.length === dimension2.labels.length && dimension.labels.every(l => dimension2.labels.includes(l))) {
            continue;
        }
        overlappingDimension = dimension.name
        break;
    }
    const levelToMerge = cube1.dimensions.findIndex(d => d.name === overlappingDimension)
    merge(cube1.data, cube2.data, 0, levelToMerge)
    return cube1;
}

function merge(data1, data2, level, levelToMerge) {
    if (level === levelToMerge) {
        data1.push(...data2)
        return
    }
    level++;
    for(let i = 0; i < data1.length; i++) {
        merge(data1[i], data2[i], level, levelToMerge)
    }
}