function sort(arguments) {
  const { data, asc = true, nodata = null } = arguments;

  if (!Array.isArray(data)) {
    throw new Error("Argument `data` is not an array.");
  }

  if (typeof asc !== "boolean") {
    throw new Error("Argument `asc` is not a boolean.");
  }

  if (nodata !== null && typeof nodata !== "boolean") {
    throw new Error("Argument `nodata` is not a boolean or null.");
  }

  let newData = [];
  let arr_of_nulls = [];

  for (let i = 0; i < data.length; i++) {
    if (
      typeof data[i] !== "number" &&
      typeof data[i] !== "string" &&
      data[i] !== null
    ) {
      throw new Error("Element in `data` is not of correct type.");
    }

    if (data[i] === null) {
      arr_of_nulls.push(data[i]);
    } else {
      newData.push(data[i]);
    }
  }

  newData.sort(compareFn);

  if (asc === false) {
    newData.reverse();
  }

  if (nodata === true) {
    newData = [...newData, ...arr_of_nulls];
  }

  if (nodata === false) {
    newData = [...arr_of_nulls, ...newData];
  }

  return newData;
}

function compareFn(x, y) {
  const isValidDate = function (date) {
    return (
      new Date(date).toString() !== "Invalid Date" && !isNaN(new Date(date))
    );
  };

  if (
    typeof x === "string" &&
    isValidDate(x) &&
    typeof y === "string" &&
    isValidDate(y)
  ) {
    if (Date.parse(x) < Date.parse(y)) {
      return -1;
    } else if (Date.parse(x) > Date.parse(y)) {
      return 1;
    }
    return 0;
  }

  if (x < y) {
    return -1;
  } else if (x > y) {
    return 1;
  }
  return 0;
}
