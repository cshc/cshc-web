import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';

const TabNavigation = ({ title, targetId, active, onClick }) => (
  <li className="nav-item">
    <a
      className={classnames('nav-link', { 'active show': active })}
      data-toggle="tab"
      href={`#${targetId}`}
      role="tab"
      onClick={onClick}
    >
      {title}
    </a>
  </li>
);

TabNavigation.propTypes = {
  title: PropTypes.string.isRequired,
  targetId: PropTypes.string.isRequired,
  active: PropTypes.bool.isRequired,
  onClick: PropTypes.func.isRequired,
};

export default TabNavigation;
