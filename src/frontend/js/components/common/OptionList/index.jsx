import React from 'react';
import PropTypes from 'prop-types';
import Option from './Option';
import { FilterValuePropType } from '../PropTypes';

const OptionList = ({ options, className, ...props }) => (
  <div className={className}>
    {options.map(option => (
      <Option key={option.value || 'All'} label={option.label} value={option.value} {...props} />
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
  inline: PropTypes.bool,
};

OptionList.defaultProps = {
  selectedValue: undefined,
  className: undefined,
  multiselect: false,
  inline: false,
};

export default OptionList;
