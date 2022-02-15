function lt(arguments) {
  const isValidDate = function (date) {
    return new Date(date) !== "Invalid Date" && !isNaN(new Date(date));
  };
  const { x, y } = arguments;
  if (x === null || y === null) {
    return null;
  }
  if (typeof x === "object" || typeof y === "object") {
    return false;
  }
  if (
    typeof x === "string" &&
    typeof y === "string" &&
    isValidDate(x) &&
    isValidDate(y)
  ) {
    return Date.parse(x) < Date.parse(y);
  }
  return x < y;
}
