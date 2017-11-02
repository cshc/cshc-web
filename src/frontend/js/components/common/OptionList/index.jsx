import React from 'react';
import PropTypes from 'prop-types';
import Option from './Option';
import { FilterValuePropType } from '../PropTypes';

const OptionList = ({ name, onChange, selectedValue, options, className, multiselect }) => (
  <div className={className}>
    {options.map(option => (
      <Option
        key={option.value || 'All'}
        name={name}
        label={option.label}
        value={option.value}
        onChange={onChange}
        selectedValue={selectedValue}
        multiselect={multiselect}
      />
    ))}
  </div>
);

OptionList.propTypes = {
  name: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  selectedValue: FilterValuePropType,
  options: PropTypes.arrayOf(
    PropTypes.shape({
      label: PropTypes.string,
      value: FilterValuePropType,
    }),
  ).isRequired,
  className: PropTypes.string,
  multiselect: PropTypes.bool,
};

OptionList.defaultProps = {
  selectedValue: undefined,
  className: undefined,
  multiselect: false,
};

export default OptionList;
