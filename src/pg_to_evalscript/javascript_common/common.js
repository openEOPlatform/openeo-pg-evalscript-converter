function parse_rfc3339(dt, default_h = 0, default_m = 0, default_s = 0) {
  const regexDateTime =
    "^([0-9]{4})-([0-9]{2})-([0-9]{2})([Tt]([0-9]{2}):([0-9]{2}):([0-9]{2})(\\.[0-9]+)?)?(([Zz]|([+-])([0-9]{2}):([0-9]{2})))?";
  const regexDate = "^([0-9]{4})-([0-9]{2})-([0-9]{2})$";

  let result = null;

  try {
    const g = dt.match(regexDateTime);
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
        //offset in minutes
        const offset =
          (parseInt(g[12] || 0) * 60 + parseInt(g[13] || 0)) *
          (g[11] === "+" ? -1 : 1);
        //add offset in miliseconds
        date = date + offset * 60 * 1000;
      }

      return {
        type: dt.match(regexDate) ? "date" : "date-time",
        value: new Date(date).toISOString(),
      };
    }
  } catch (err) {
    //
  }

  return result;
}

class ProcessError extends Error {
  constructor({name, message}) {
    super(message);
    this.name = name;
  }
}
