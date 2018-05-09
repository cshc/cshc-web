import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';
import styles from './style.scss';

/**
 * Represents a single timeline item. 
 * 
 */
const TimelineBigItem = ({ id, highlighted, dateSmall, dateLarge, children }) => (
  <li id={id} className="col-md-12">
    <div className={classnames('row', { [styles.highlighted]: highlighted })}>
      <div className="col-md-3 text-md-right g-pt-20--md g-pr-40--md g-mb-20">
        <h5 className="h6 mb-0">{dateSmall}</h5>
        <h4 className="h5">{dateLarge}</h4>
      </div>

      <div className="col-md-9 g-orientation-left g-pl-40--md g-brd-left--md g-brd-gray-light-v4 g-pb-40">
        <div className="g-hidden-sm-down u-timeline-v2__icon g-top-35">
          <i
            className={`${styles.timelineDot} d-block g-width-18 g-height-18 g-bg-white g-brd-around g-brd-3 rounded-circle`}
          />
        </div>

        <article
          className={`${styles.timelineArticle} timeline-article g-pos-rel g-pa-10 g-pa-20--md`}
        >
          <div className="g-hidden-sm-down u-triangle-inclusive-v1--right g-top-30 g-z-index-2">
            <div className={`${styles.timelineLeftArrow} u-triangle-inclusive-v1--right__back`} />
          </div>
          <div className="g-hidden-md-up u-triangle-inclusive-v1--top g-left-20 g-z-index-2">
            <div className={`${styles.timelineTopArrow} u-triangle-inclusive-v1--top__back`} />
          </div>
          {children}
        </article>
      </div>
    </div>
  </li>
);

TimelineBigItem.propTypes = {
  id: PropTypes.string,
  highlighted: PropTypes.bool,
  dateLarge: PropTypes.node,
  dateSmall: PropTypes.node,
  children: PropTypes.node.isRequired,
};

TimelineBigItem.defaultProps = {
  id: undefined,
  highlighted: false,
  dateLarge: undefined,
  dateSmall: undefined,
};

export default TimelineBigItem;
