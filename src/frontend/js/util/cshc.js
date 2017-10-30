const toTitleCase = str =>
  str.replace(/\w\S*/g, txt => txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase());

const toGraphQLId = (nodeType, id) => btoa(`${nodeType}:${id}`);

const toModelId = graphQLId => atob(graphQLId).split(':')[1];

module.exports = {
  toTitleCase,
  toGraphQLId,
  toModelId,
};
