const toTitleCase = str =>
  str.replace(/\w\S*/g, txt => txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase());

module.exports = {
  toTitleCase,
};
