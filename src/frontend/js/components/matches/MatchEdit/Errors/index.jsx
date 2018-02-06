import React from 'react';
import PropTypes from 'prop-types';

const Errors = ({ errors }) => {
  if (!errors.length) {
    return null;
  }
  return (
    <div className="g-pa-5 g-font-size-80x g-line-height-1_2 g-rounded-3 g-bg-red g-color-white d-flex align-items-center">
      <i className="fa fa-exclamation-circle g-mr-5" />
      <div>{errors.map(e => <div key={e}>{e}</div>)}</div>
    </div>
  );
};

Errors.propTypes = {
  errors: PropTypes.arrayOf(PropTypes.string).isRequired,
};

Errors.defaultProps = {};

export default Errors;
