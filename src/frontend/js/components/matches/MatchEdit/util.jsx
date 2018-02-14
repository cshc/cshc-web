const toSelectOption = (member) => {
  if (!member) {
    return undefined;
  }
  const split = member.split(':');
  return { value: member, label: split[1] };
};

module.exports = {
  toSelectOption,
};
