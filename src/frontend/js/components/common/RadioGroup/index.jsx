import React from 'react';
import PropTypes from 'prop-types';
import Radio from './Radio';

const RadioGroup = ({ name, onChange, selectedValue, options, className }) => (
  <div className={className}>
    {options.map(option => (
      <Radio
        key={option.value || 'All'}
        name={name}
        label={option.label}
        value={option.value}
        onChange={onChange}
        selectedValue={selectedValue}
      />
    ))}
  </div>
);

RadioGroup.propTypes = {
  name: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  selectedValue: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  options: PropTypes.arrayOf(
    PropTypes.shape({
      label: PropTypes.string,
      value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    }),
  ).isRequired,
  className: PropTypes.string,
};

RadioGroup.defaultProps = {
  selectedValue: undefined,
  className: undefined,
};

export default RadioGroup;
