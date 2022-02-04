function divide(arguments) {
  const { x, y } = arguments;
  if (y === 0) {
    throw "Division by zero is not supported.";
  }
  if (x === null || y === null) {
    return null;
  }
  return x / y;
}
