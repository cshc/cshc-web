import React from 'react';
import PropTypes from 'prop-types';

const Accordion = ({ children, accordionId }) => (
  <div
    id={accordionId}
    className="u-accordion u-accordion-color-primary u-accordion-brd-primary"
    role="tablist"
    aria-multiselectable="true"
  >
    {children}
  </div>
);

Accordion.propTypes = {
  accordionId: PropTypes.string.isRequired,
  children: PropTypes.arrayOf(PropTypes.shape()).isRequired,
};

export default Accordion;
