function parse_rfc3339(dt, default_h = 0, default_m = 0, default_s = 0) {
  const regex =
    "^([0-9]{4})-([0-9]{2})-([0-9]{2})([Tt]([0-9]{2}):([0-9]{2}):([0-9]{2})(\\.[0-9]+)?)?(([Zz]|([+-])([0-9]{2}):([0-9]{2})))?";

  let result = null;

  try {
    const g = dt.match(regex);
    if (g) {
      let date = Date.UTC(
        parseInt(g[1]), //year
        parseInt(g[2]) - 1, // month
        parseInt(g[3]), //day
        parseInt(g[5] || default_h), //hour
        parseInt(g[6] || default_m), //minute
        parseInt(g[7] || default_s), // second
        parseFloat(g[8]) * 1000 || 0 // milisecond
      );

      //for date-time strings either time zone or Z should be provided
      if (g[5] !== undefined && g[9] === undefined) {
        return null;
      }

      //check if timezone is provided
      if (g[9] !== undefined && g[9] !== "Z") {
        const offset =
          (parseInt(g[12]) * 60 + parseInt(g[13])) * (g[11] === "+" ? -1 : +1);

        date = date + offset * 60000;
      }

      result = new Date(date).toISOString();
    }
  } catch (err) {
    //
  }

  return result;
}
