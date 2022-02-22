function merge_cubes(arguments) {
  const { cube1, cube2, overlap_resolver = null, context = null } = arguments;
  let overlappingDimensionName;

  if (overlap_resolver && context) {
    overlap_resolver.context = { ...context, ...overlap_resolver.context };
  }

  for (let dimension of cube1.dimensions) {
    const dimension2 = cube2.getDimensionByName(dimension.name);
    if (
      dimension.name === dimension2.name &&
      dimension.type === dimension2.type &&
      dimension.labels.length === dimension2.labels.length &&
      dimension.labels.every((l) => dimension2.labels.includes(l))
    ) {
      continue;
    }

    if (dimension.labels.some((l) => dimension2.labels.includes(l))) {
      overlappingDimensionName = dimension.name;
      break;
    }
  }

  if (!overlap_resolver && overlappingDimensionName) {
    throw new Error(
      "Overlapping data cubes, but no overlap resolver has been specified."
    );
  }

  const levelToMerge = cube1.dimensions.findIndex(
    (d) => d.name === overlappingDimensionName
  );

  merge(cube1.data, cube2.data, 0, levelToMerge, overlap_resolver);

  if (levelToMerge === -1) {
    cube1.data.push(...cube2.data);
  }

  for (let dimension of cube1.dimensions) {
    cube1.getDimensionByName(dimension.name).labels = [
      ...new Set([
        ...cube1.getDimensionByName(dimension.name).labels,
        ...cube2.getDimensionByName(dimension.name).labels,
      ]),
    ];
  }

  return cube1;
}

function merge(data1, data2, level, levelToMerge, overlap_resolver) {
  if (level === levelToMerge) {
    for (let x = 0; x < data1.length; x++) {
      data1[x] = overlap_resolver({ x: data1[x], y: data2[x] });
    }
    return;
  }
  level++;
  for (let i = 0; i < data1.length; i++) {
    merge(data1[i], data2[i], level, levelToMerge, overlap_resolver);
  }
}
