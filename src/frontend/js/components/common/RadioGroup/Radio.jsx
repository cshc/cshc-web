import React from 'react';
import PropTypes from 'prop-types';
import slugify from 'slugify';

const Radio = ({ name, label, selectedValue, onChange, value }) => {
  const optional = {};
  optional.checked = value === selectedValue;
  if (typeof onChange === 'function') {
    optional.onChange = onChange.bind(null, value);
  }
  const id = slugify(label);
  return (
    <div className="form-group g-mb-10">
      <label htmlFor={id} className="u-check g-pl-25">
        <input
          id={id}
          className="g-hidden-xs-up g-pos-abs g-top-0 g-left-0"
          name={name}
          value={value}
          onChange={onChange}
          {...optional}
          type="radio"
        />
        <div className="u-check-icon-font g-absolute-centered--y g-left-0">
          <i className="fa" data-check-icon="" data-uncheck-icon="" />
        </div>
        {label}
      </label>
    </div>
  );
};

Radio.propTypes = {
  name: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  selectedValue: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  onChange: PropTypes.func.isRequired,
};

Radio.defaultProps = {
  selectedValue: undefined,
  value: undefined,
};

export default Radio;
