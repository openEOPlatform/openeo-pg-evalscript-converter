function merge_cubes(arguments) {
  const { cube1, cube2, overlap_resolver = null, context = null } = arguments;
  let overlappingDimension;

  if (overlap_resolver && context) {
    overlap_resolver.context = context;
  }

  for (let dimension of cube1.dimensions) {
    const dimension2 = cube2.getDimensionByName(dimension.name);
    if (
      dimension.labels.length === dimension2.labels.length &&
      dimension.labels.every((l) => dimension2.labels.includes(l))
    ) {
      continue;
    }
    overlappingDimension = dimension.name;
    if (!overlap_resolver) {
      throw new Error(
        "Overlapping data cubes, but no overlap resolver has been specified."
      );
    }
    break;
  }
  const levelToMerge = cube1.dimensions.findIndex(
    (d) => d.name === overlappingDimension
  );
  merge(cube1.data, cube2.data, 0, levelToMerge, overlap_resolver);
  return cube1;
}

function merge(data1, data2, level, levelToMerge, overlap_resolver) {
  if (level === levelToMerge) {
    for (let i = 0; i < data1.length; i++) {
      data1[i] = overlap_resolver({ x: data1[i], y: data2[i] });
    }
    return;
  }
  level++;
  for (let i = 0; i < data1.length; i++) {
    merge(data1[i], data2[i], level, levelToMerge, overlap_resolver);
  }
}
