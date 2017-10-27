import React from 'react';
import PropTypes from 'prop-types';

const Subheading = ({ children }) => (
  <div className="u-heading-v1-6 g-bg-main g-brd-gray-light-v2 g-mb-20 g-mt-40">
    <h2 className="h3 u-heading-v1__title">{children}</h2>
  </div>
);

Subheading.propTypes = {
  children: PropTypes.node.isRequired,
};

export default Subheading;
