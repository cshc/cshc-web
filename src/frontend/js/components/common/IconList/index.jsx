import React from 'react';
import PropTypes from 'prop-types';

const IconList = ({ className, iconClass, count }) => {
  const icons = [];
  for (let i = 0; i < count; i += 1) {
    icons.push(<i className={iconClass} />);
  }
  return <div className={className}>{icons}</div>;
};

IconList.propTypes = {
  className: PropTypes.string,
  iconClass: PropTypes.string.isRequired,
  count: PropTypes.number.isRequired,
};

IconList.defaultProps = {
  className: '',
};

export default IconList;
