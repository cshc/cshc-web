import React from 'react';
import PropTypes from 'prop-types';

const AccordionCard = ({ cardId, title, leftIcon, rightIcon, accordionId, ...props }) => (
  <div className="card rounded-0 g-brd-none">
    <div id={`${accordionId}-heading-${cardId}`} className="u-accordion__header g-pa-0" role="tab">
      <h5 className="mb-0 g-font-weight-600 g-font-size-default">
        <a
          className="d-block g-color-main g-text-underline--none--hover g-brd-bottom g-brd-gray-light-v4 g-pa-15-0"
          href={`#${accordionId}-body-${cardId}`}
          data-toggle="collapse"
          data-parent={`#${accordionId}`}
          aria-expanded="true"
          aria-controls={`${accordionId}-body-${cardId}`}
        >
          {leftIcon && <i className={`${leftIcon} g-valign-middle g-font-size-18 mr-3`} />}
          <span className="float-right">
            {rightIcon}
            <span className="u-accordion__control-icon g-ml-10">
              <i className="fa fa-angle-right" />
              <i className="fa fa-angle-down" />
            </span>
          </span>
          <span className="g-valign-middle">{title}</span>
        </a>
      </h5>
    </div>
    <div
      id={`${accordionId}-body-${cardId}`}
      className="collapse"
      role="tabpanel"
      aria-labelledby={`${accordionId}-heading-${cardId}`}
    >
      <div className="u-accordion__body g-color-gray-dark-v5 g-pa-15-0">{props.children}</div>
    </div>
  </div>
);

AccordionCard.propTypes = {
  accordionId: PropTypes.string.isRequired,
  cardId: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  leftIcon: PropTypes.string,
  rightIcon: PropTypes.node,
};

AccordionCard.defaultProps = {
  leftIcon: undefined,
  rightIcon: undefined,
};

export default AccordionCard;
