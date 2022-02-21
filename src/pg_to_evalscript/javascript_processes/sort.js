function sort(arguments) {
  const { data, asc = true, nodata = null } = arguments;
  let newData = [...data];
  let arr_of_nulls = newData.filter((x) => x === null);

  newData = newData.filter((x) => x !== null);

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
    return new Date(date) !== "Invalid Date" && !isNaN(new Date(date));
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
