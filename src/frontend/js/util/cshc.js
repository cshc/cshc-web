const toTitleCase = str =>
  str.replace(/\w\S*/g, txt => txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase());

const toGraphQLId = (nodeType, id) => btoa(`${nodeType}:${id}`);

const toModelId = graphQLId => atob(graphQLId).split(':')[1];

const getPosition = (position) => {
  if (!position) return undefined;
  const pos = position.split(',');
  return {
    lat: parseFloat(pos[0]),
    lng: parseFloat(pos[1]),
  };
};

module.exports = {
  toTitleCase,
  toGraphQLId,
  toModelId,
  getPosition,
};
