import React from 'react';
import PropTypes from 'prop-types';
import styles from './style.scss';

/**
 * Represents a single timeline item. 
 * 
 * Note: this is currently styled for a small timeline like those found on the Member Details page 
 * (Club Involvement section). 
 */
const Timeline2Item = ({ dateSmall, dateLarge, articleClassName, children }) => (
  <li className="col-md-12 g-brd-bottom g-brd-0--md g-brd-gray-light-v4 g-py-10 g-py-0--md g-mb-0--md">
    <div className="row">
      <div className="col-md-4 text-md-right g-my-10 g-my-0--md g-pr-20--md">
        <div className="g-py-10--md">
          {dateLarge && <h4 className="h5 g-font-weight-300">{dateLarge}</h4>}
          {dateSmall && <h5 className="h6 g-font-weight-300 mb-0">{dateSmall}</h5>}
        </div>
      </div>
      <div
        className={`col-md-8 g-orientation-left g-brd-left--md g-brd-gray-light-v4 ${styles.rightcol}`}
      >
        <div className={`g-hidden-sm-down ${styles.dot}`}>
          <i className="d-block g-width-18 g-height-18 g-bg-primary g-brd-around g-brd-4 g-brd-gray-light-v4 rounded-circle" />
        </div>
        <article className={articleClassName}>{children}</article>
      </div>
    </div>
  </li>
);

Timeline2Item.propTypes = {
  dateLarge: PropTypes.node,
  dateSmall: PropTypes.node,
  articleClassName: PropTypes.string,
  children: PropTypes.node.isRequired,
};

Timeline2Item.defaultProps = {
  dateLarge: undefined,
  dateSmall: undefined,
  articleClassName: 'g-py-10--md',
};

export default Timeline2Item;
