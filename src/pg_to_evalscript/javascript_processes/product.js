function product(arguments) {
  const { data, ignore_nodata = true } = arguments;

  if (data === undefined) {
    throw new Error("Mandatory argument `data` is not defined.");
  }

  if (!Array.isArray(data)) {
    throw new Error("Argument `data` is not an array.");
  }

  if (typeof ignore_nodata !== "boolean") {
    throw new Error("Argument `ignore_nodata` is not a boolean.");
  }

  let product = 1;
  for (let x of data) {
    if (typeof x !== "number" && x !== null) {
      throw new Error("Value in argument `data` is not a number or null.");
    }

    if (x === null) {
      if (ignore_nodata) {
        continue;
      } else {
        product = null;
        break;
      }
    }

    product = product * x;
  }

  if (data.length === 0) {
    product = null;
  }

  return product;
}
