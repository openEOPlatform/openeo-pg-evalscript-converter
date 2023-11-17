function merge_cubes(arguments) {
const startTime = Date.now();
  let { cube1, cube2, overlap_resolver = null, context = null } = arguments;

  if (cube1 === undefined) {
    throw new Error("Mandatory argument `cube1` is not defined.");
  }

  if (cube2 === undefined) {
    throw new Error("Mandatory argument `cube2` is not defined.");
  }

  if (overlap_resolver && context) {
    overlap_resolver.context = Object.assign({}, context, overlap_resolver.context);
  }


  cube1 = cube1.clone()
  cube1.merge(cube2, overlap_resolver)


const endTime = Date.now();
executionTimes.push({ fun: "merge_cubes.js", params: {}, success: true, time: endTime - startTime });
  return cube1;
}
