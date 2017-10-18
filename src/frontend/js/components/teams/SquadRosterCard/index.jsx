import React from 'react';
import PropTypes from 'prop-types';
import { VictoryPie, VictoryTooltip } from 'victory';
import Member from 'models/member';
import ProgressBar from 'components/common/ProgressBar';
import IconList from 'components/common/IconList';
import styles from './style.scss';

const SquadRosterCard = ({ memberStats, teamTotals }) => {
  const imgSrc = memberStats.member.thumbUrl || '/static/img/avatar-placeholder.jpg';
  const playedPercentage = 100 * (memberStats.played / teamTotals.played);
  const goalsPercentage = 100 * (memberStats.goals / teamTotals.goals);
  const wldData = [];
  const wldColors = [];
  if (memberStats.won > 0) {
    wldData.push({ x: 'W', y: memberStats.won });
    wldColors.push('green');
  }
  if (memberStats.drawn > 0) {
    wldData.push({ x: 'D', y: memberStats.drawn });
    wldColors.push('lightgrey');
  }
  if (memberStats.lost > 0) {
    wldData.push({ x: 'L', y: memberStats.lost });
    wldColors.push('red');
  }

  return (
    <div className="col-md-6 col-lg-3 g-mb-30">
      <article className="g-bg-white">
        <div className={styles.imageFlipContainer}>
          <figure className={styles.imageContainer}>
            <div className={styles.front}>
              <div className={styles.frontContent}>
                <img className={styles.image} src={imgSrc} alt="Member profile pic" />
                <div className={styles.imageOverlayFront}>
                  <IconList
                    className={styles.awardRow}
                    iconClass="fa fa-star g-mr-5"
                    count={memberStats.mom}
                  />
                  <IconList
                    className={`${styles.awardRow} g-pb-10`}
                    iconClass="fa fa-lemon-o g-mr-5"
                    count={memberStats.lom}
                  />
                  {(memberStats.isCaptain || memberStats.isViceCaptain) && (
                    <div className={styles.captain}>
                      {memberStats.isCaptain ? 'Captain' : 'Vice Captain'}
                    </div>
                  )}
                </div>
              </div>
            </div>
            <div className={styles.back}>
              <div className={styles.backContent}>
                <span
                  className={`${styles.shirt} shirt-number shirt-number-2xl ${memberStats.member.gender.toLowerCase()}`}
                >
                  {memberStats.member.shirtNumber}
                </span>
              </div>
            </div>
          </figure>
        </div>
        <div className="u-shadow-v24 g-pa-25">
          <h3 className="h5 g-mb-5 text-center">{Member.fullName(memberStats.member)}</h3>
          <p className="text-center g-mb-5">
            &nbsp;{memberStats.member.prefPosition !== 'Not known' &&
              memberStats.member.prefPosition}&nbsp;
          </p>
          <ProgressBar label="Played" value={memberStats.played} progressValue={playedPercentage} />
          <ProgressBar
            label="Goals"
            value={memberStats.goals}
            progressValue={goalsPercentage}
            color="blue"
          />
          <div className={styles.flexRow}>
            <VictoryPie
              colorScale={wldColors}
              data={wldData}
              height={150}
              width={150}
              padding={10}
              labelRadius={40}
              labels={d => d.x}
            />
            <a
              className="btn btn-md u-btn-primary g-color-primary--hover g-bg-white--hover g-font-weight-600 g-font-size-11 text-uppercase"
              href="#"
            >
              Profile
            </a>
          </div>
        </div>
      </article>
    </div>
  );
};

SquadRosterCard.propTypes = {
  memberStats: PropTypes.shape().isRequired,
  teamTotals: PropTypes.shape().isRequired,
};

export default SquadRosterCard;
