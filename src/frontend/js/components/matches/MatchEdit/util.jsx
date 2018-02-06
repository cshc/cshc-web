const AccordionId = 'match-edit';

const toSelectOption = (member) => {
  if (!member) {
    return undefined;
  }
  const split = member.split(':');
  return { value: member, label: split[1] };
};

const fromSelectOption = option => `${option.value}:${option.label}`;

module.exports = {
  AccordionId,
  toSelectOption,
  fromSelectOption,
};
