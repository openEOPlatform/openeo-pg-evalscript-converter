function sort(arguments) {
  const { data, asc = true, nodata = null } = arguments;

  validateParameter({
    processName: "sort",
    parameterName: "data",
    value: data,
    required: true,
    nullable: false,
    array: true,
  });

  validateParameter({
    processName: "sort",
    parameterName: "asc",
    value: asc,
    nullable: false,
    allowedTypes: ["boolean"],
  });

  validateParameter({
    processName: "sort",
    parameterName: "nodata",
    value: nodata,
    allowedTypes: ["boolean"],
  });

  let newData = [];
  let arr_of_nulls = [];

  for (let i = 0; i < data.length; i++) {
    validateParameter({
      processName: "sort",
      parameterName: "element of data",
      value: data[i],
      allowedTypes: ["number", "string"],
    });

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
