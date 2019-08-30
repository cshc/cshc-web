import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';

const TabBlock = ({ id, active, children }) => (
  <div className={classnames('tab-pane fade', { 'active show': active })} id={id} role="tabpanel">
    {children}
  </div>
);

TabBlock.propTypes = {
  id: PropTypes.string.isRequired,
  children: PropTypes.node,
  active: PropTypes.bool.isRequired,
};

TabBlock.defaultProps = {
  children: null,
};

export default TabBlock;
