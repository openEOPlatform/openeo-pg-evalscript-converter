function round(arguments) {
  const { x, p = 0 } = arguments;

  validateParameter({
    processName: "round",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  validateParameter({
    processName: "round",
    parameterName: "p",
    value: p,
    integer: true,
  });

  if (x === null) {
    return null;
  }

  /**
   * implemented from https://stackoverflow.com/questions/3108986/gaussian-bankers-rounding-in-javascript/3109234#3109234
   */
  const m = Math.pow(10, p);
  const n = +(p ? x * m : x).toFixed(8); // Avoid rounding errors
  const i = Math.floor(n),
    f = n - i;
  const e = 1e-8; // Allow for rounding errors in f
  const r =
    f > 0.5 - e && f < 0.5 + e ? (i % 2 == 0 ? i : i + 1) : Math.round(n);
  return p ? r / m : r;
}
