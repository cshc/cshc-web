import React from 'react';
import PropTypes from 'prop-types';
import Match from 'models/match';
import MemberLink from 'components/members/MemberLink';
import AwardWinner from 'components/awards/AwardWinner';
import Urls from 'util/urls';
import { MatchItem } from 'util/constants';
import MatchDate from '../../MatchDate';
import OppositionTeam from '../../OppositionTeam';
import MatchVenue from '../../MatchVenue';
import FixtureTypeIcon from '../../FixtureTypeIcon';
import styles from './style.scss';

/** 
 * Representation of a single match as an item on a timeline.
 * 
 * Ref: https://htmlstream.com/preview/unify-v2.2/unify-main/shortcodes/shortcode-blocks-timelines.html#shortcode2
 */
const MatchTimelineCard = ({ match, exclude, dateFormat }) => {
  const incl = item => !exclude.includes(item);
  const moms = Match.mom(match);
  const loms = Match.lom(match);
  const scorers = Match.scorers(match);
  return (
    <li className="col-md-12 g-mb-40">
      <div className="row">
        <div className="col-md-2 text-md-right g-pt-20--md g-pr-40--md g-mb-20">
          {incl(MatchItem.time) && <h5 className="h6 mb-0">{match.time}</h5>}
          {incl(MatchItem.date) && (
            <h4 className="h5">
              <MatchDate date={match.date} format={dateFormat} />
            </h4>
          )}
        </div>

        <div className="col-md-10 g-orientation-left g-pl-40--md">
          <div className="g-hidden-sm-down u-timeline-v2__icon g-top-35">
            <i className="d-block g-width-18 g-height-18 g-bg-white g-brd-around g-brd-3 g-brd-gray-light-v5 rounded-circle" />
          </div>

          <article className="g-pos-rel g-bg-gray-light-v5 g-pa-30">
            <div className="g-hidden-sm-down u-triangle-inclusive-v1--right g-top-30 g-z-index-2">
              <div className="u-triangle-inclusive-v1--right__back g-brd-gray-light-v5-right" />
            </div>
            <div className="g-hidden-md-up u-triangle-inclusive-v1--top g-left-20 g-z-index-2">
              <div className="u-triangle-inclusive-v1--top__back g-brd-gray-light-v5-bottom" />
            </div>

            <header className="g-brd-bottom g-brd-gray-light-v4 g-pb-10 g-mb-25">
              <h3 className={`g-font-weight-300 ${styles.heading}`}>
                {incl('result') && (
                  <span>
                    <span className={`${Match.resultClass(match)} g-py-5 g-px-8`}>
                      {Match.scoreDisplay(match)}
                    </span>
                    {incl('opposition') && <span>&nbsp;vs&nbsp;</span>}
                  </span>
                )}
                {incl('opposition') && (
                  <span className={styles.headingMain}>
                    <OppositionTeam team={match.oppTeam} />
                  </span>
                )}
                {incl('fixtureType') && (
                  <span className={styles.headingRight}>
                    <FixtureTypeIcon fixtureType={match.fixtureType} />
                  </span>
                )}
              </h3>
            </header>

            <div className={styles.cardContent}>
              {incl(MatchItem.venue) && (
                <div className="g-mb-20">
                  <i className="fa fa-map-o g-pr-10" />
                  <MatchVenue match={match} />
                </div>
              )}
              {(incl(MatchItem.awards) || incl(MatchItem.scorers)) && (
                <div className={`${styles.flexWrap} g-mb-10`}>
                  {incl(MatchItem.awards) &&
                    moms.length > 0 && (
                      <span className={styles.flexWrap}>
                        <i className="fa fa-lg fa-star-o g-mr-5 g-mt-7" title="Man of the Match" />
                        {moms.map((awardWinner, index) => (
                          <AwardWinner
                            key={index}
                            awardWinner={awardWinner}
                            className="g-mr-10 g-mb-15"
                          />
                        ))}
                      </span>
                    )}
                  {incl(MatchItem.awards) &&
                    loms.length > 0 && (
                      <span className={styles.flexWrap}>
                        <i
                          className="fa fa-lg fa-lemon-o g-mr-5 g-mt-7"
                          title="Lemon of the Match"
                        />
                        {loms.map((awardWinner, index) => (
                          <AwardWinner
                            key={index}
                            awardWinner={awardWinner}
                            className="g-mr-10 g-mb-15"
                          />
                        ))}
                      </span>
                    )}
                  {incl(MatchItem.scorers) &&
                    scorers.length > 0 && (
                      <span className={styles.flexWrap}>
                        <span className="g-mr-10 g-mt-4">Scorers:</span>
                        {scorers.map((scorer, index) => (
                          <span key={scorer.member.modelId}>
                            <MemberLink
                              member={scorer.member}
                              badgeCount={scorer.goals}
                              className="g-mr-10 g-mb-15"
                              useFullName
                            />
                            {index < scorers.length - 1 && <span>,&nbsp;</span>}
                          </span>
                        ))}
                      </span>
                    )}
                </div>
              )}
              {incl(MatchItem.report) && (
                <a
                  href={Urls.match_detail(match.modelId)}
                  title="Match details"
                  className={`btn btn-md u-btn-primary ${styles.details}`}
                >
                  Details...
                </a>
              )}
            </div>
          </article>
        </div>
      </div>
    </li>
  );
};

MatchTimelineCard.propTypes = {
  match: PropTypes.shape().isRequired,
  exclude: PropTypes.arrayOf(PropTypes.string),
  dateFormat: PropTypes.string,
};

MatchTimelineCard.defaultProps = {
  exclude: [],
  dateFormat: 'Do MMM',
};

export default MatchTimelineCard;
