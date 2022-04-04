function merge_cubes(arguments) {
  const { cube1, cube2, overlap_resolver = null, context = null } = arguments;
  let overlappingDimensionName;

  if (cube1 === undefined) {
    throw new Error("Mandatory argument `cube1` is not defined.");
  }

  if (cube2 === undefined) {
    throw new Error("Mandatory argument `cube2` is not defined.");
  }

  if (overlap_resolver && context) {
    overlap_resolver.context = Object.assign(context, overlap_resolver.context);
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

  if (levelToMerge === -1) {
    cube1.data.push(...cube2.data);
  } else {
    const mask = cube2
      .getDimensionByName(overlappingDimensionName)
      .labels.map((el1, i) => ({
        first: i,
        second: cube1
          .getDimensionByName(overlappingDimensionName)
          .labels.findIndex((el2) => el1 === el2),
      }));

    merge(
      cube1.data,
      cube2.data,
      mask,
      0,
      levelToMerge === 0 ? levelToMerge : levelToMerge - 1,
      overlap_resolver
    );
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

function merge(data1, data2, mask, level, levelToMerge, overlap_resolver) {
  if (level === levelToMerge) {
    for (let x = 0; x < mask.length; x++) {
      if (mask[x].second >= 0) {
        for (let i = 0; i < data1[x].length; i++) {
          data1[mask[x].second][i] = overlap_resolver({
            x: data1[mask[x].second][i],
            y: data2[mask[x].first][i],
          });
        }
      } else {
        data1.push([...data2[x]]);
      }
    }
    return;
  }
  level++;
  for (let i = 0; i < data1.length; i++) {
    merge(data1[i], data2[i], mask, level, levelToMerge, overlap_resolver);
  }
}
