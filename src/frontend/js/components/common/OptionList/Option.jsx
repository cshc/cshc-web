import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';
import slugify from 'slugify';
import { FilterValuePropType } from '../PropTypes';

const Option = ({ name, label, selectedValue, onChange, value, multiselect, inline }) => {
  const checked = multiselect
    ? (selectedValue && selectedValue.includes(value)) || false
    : value === selectedValue;
  const inputType = multiselect ? 'checkbox' : 'radio';
  const icon = multiselect ? 'checkbox-v4' : 'font';
  const labelClass = classnames('u-check g-pl-25', {
    'form-check-inline': inline,
  });
  const id = slugify(label);
  const inner = (
    <label htmlFor={id} className={labelClass}>
      <input
        id={id}
        className="g-hidden-xs-up g-pos-abs g-top-0 g-left-0"
        name={name}
        value={value}
        onChange={onChange}
        checked={checked}
        type={inputType}
      />
      <div className={`u-check-icon-${icon} g-absolute-centered--y g-left-0`}>
        {multiselect ? (
          <i className="fa" data-check-icon="" />
        ) : (
          <i className="fa" data-check-icon="" data-uncheck-icon="" />
        )}
      </div>
      {label}
    </label>
  );
  return inline ? inner : <div className="form-group g-mb-10 g-mb-0--md">{inner}</div>;
};

Option.propTypes = {
  name: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  value: FilterValuePropType,
  selectedValue: FilterValuePropType,
  onChange: PropTypes.func.isRequired,
  multiselect: PropTypes.bool,
  inline: PropTypes.bool,
};

Option.defaultProps = {
  selectedValue: undefined,
  value: undefined,
  multiselect: false,
  inline: false,
};

export default Option;
