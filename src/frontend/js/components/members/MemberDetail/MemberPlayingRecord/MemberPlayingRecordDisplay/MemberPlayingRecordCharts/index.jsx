import React from 'react';
import PropTypes from 'prop-types';
import { Bar } from 'react-chartjs-2';
import { rounded } from 'util/cshc';
import { getTeamColorScales, getTeamColor } from 'util/colors';
import { Panel } from 'components/Unify';
import { getAllTeams } from '../util';

const primaryAxis = 'y-axis-1';
const secondaryAxis = 'y-axis-2';

const baseOptions = {
  responsive: true,
  tooltips: {
    mode: 'label',
  },
  elements: {
    line: {
      fill: false,
    },
  },
};

const xAxis = {
  display: true,
  gridLines: {
    display: false,
  },
  labels: {
    show: true,
  },
};

const xAxisStacked = {
  ...xAxis,
  stacked: true,
};

const yAxis = {
  type: 'linear',
  display: true,
  gridLines: {
    display: false,
  },
  labels: {
    show: true,
  },
};

const yAxisPrimary = {
  ...yAxis,
  position: 'left',
  id: primaryAxis,
};

const yAxisSecondary = {
  ...yAxis,
  position: 'right',
  id: secondaryAxis,
};

const yAxisPrimaryStacked = {
  ...yAxisPrimary,
  stacked: true,
};

const yAxisSecondaryStacked = {
  ...yAxisSecondary,
  stacked: true,
};

/**
 * Chart representations of a member's Playing Record.
 * 
 * This component incorportates 3 charts:
 * 1) Matches, Goals and Awards
 * 2) Team Representations
 * 3) Success Record
 */
const MemberPlayingRecordChart = ({ clubTeams, data }) => {
  const panelProps = { outlineColor: 'teal', headerColor: 'teal' };

  const allTeams = getAllTeams(data);
  const teamColorScales = getTeamColorScales(
    clubTeams.filter(ct => allTeams.find(t => t.slug === ct.slug)),
  );

  const addLine = (fieldName, label, color, yAxisID, isAvg = false) => ({
    label,
    type: 'line',
    data: data.map(
      seasonStats =>
        (isAvg
          ? rounded(seasonStats.memberStats[fieldName] / seasonStats.memberStats.played)
          : seasonStats.memberStats[fieldName]),
    ),
    fill: false,
    borderColor: color,
    backgroundColor: color,
    pointBorderColor: color,
    pointBackgroundColor: color,
    pointHoverBackgroundColor: color,
    pointHoverBorderColor: color,
    yAxisID,
  });

  const addBar = (label, dataSeries, color, yAxisID) => ({
    type: 'bar',
    label,
    data: dataSeries,
    fill: false,
    backgroundColor: color,
    yAxisID,
  });

  const labels = data.map(seasonStats => seasonStats.season.slug);

  const matchesData = {
    labels,
    datasets: [
      addLine('played', 'Appearances', 'orange', primaryAxis),
      addLine('goals', 'Goals Scored', 'blue', primaryAxis),
      addLine('cleanSheets', 'Clean Sheets', 'green', primaryAxis),
      addBar(
        'Man of the Match',
        data.map(seasonStats => seasonStats.memberStats.mom),
        'purple',
        secondaryAxis,
      ),
      addBar(
        'Lemon of the Match',
        data.map(seasonStats => -seasonStats.memberStats.lom),
        '#e2e277',
        secondaryAxis,
      ),
    ],
  };

  const matchesOptions = {
    ...baseOptions,
    scales: {
      xAxes: [
        {
          ...xAxisStacked,
          barPercentage: 0.5,
        },
      ],
      yAxes: [yAxisPrimary, yAxisSecondaryStacked],
    },
  };

  const teamRepresentations = allTeams.map(t => ({
    type: 'bar',
    label: t.shortName,
    data: data.map((seasonStats) => {
      // Find matching team representations for the specified season
      const matching = seasonStats.memberStats.teamRepresentations.find(
        tr => tr.team.slug === t.slug,
      );
      return matching ? matching.appearanceCount : 0;
    }),
    fill: false,
    backgroundColor: getTeamColor(teamColorScales, clubTeams, t.slug),
    yAxisID: primaryAxis,
  }));

  const teamsData = {
    labels,
    datasets: teamRepresentations,
  };

  const teamsOptions = {
    ...baseOptions,
    scales: {
      xAxes: [xAxis],
      yAxes: [yAxisPrimary],
    },
  };

  const successData = {
    labels,
    datasets: [
      addLine('goalsFor', 'Avg Goals For', 'green', secondaryAxis, true),
      addLine('goalsAgainst', 'Avg Goals Against', 'red', secondaryAxis, true),
      addLine('totalPoints', 'Avg Points', 'black', secondaryAxis, true),
      addBar('Won', data.map(seasonStats => seasonStats.memberStats.won), 'green', primaryAxis),
      addBar(
        'Drawn',
        data.map(seasonStats => seasonStats.memberStats.drawn),
        'lightgrey',
        primaryAxis,
      ),
      addBar('Lost', data.map(seasonStats => seasonStats.memberStats.lost), 'red', primaryAxis),
    ],
  };

  const successOptions = {
    ...baseOptions,
    scales: {
      xAxes: [
        {
          ...xAxisStacked,
          barPercentage: 0.5,
        },
      ],
      yAxes: [yAxisPrimaryStacked, yAxisSecondary],
    },
  };

  return (
    <div>
      <Panel title="Matches, Goals and Awards" {...panelProps}>
        <div className="card-block">
          <Bar data={matchesData} options={matchesOptions} />
        </div>
      </Panel>
      <Panel title="Team Representations" {...panelProps}>
        <div className="card-block">
          <Bar data={teamsData} options={teamsOptions} />
        </div>
      </Panel>
      <Panel title="Success Record" {...panelProps}>
        <div className="card-block">
          <Bar data={successData} options={successOptions} />
        </div>
      </Panel>
    </div>
  );
};

MemberPlayingRecordChart.propTypes = {
  clubTeams: PropTypes.arrayOf(PropTypes.shape()).isRequired,
  data: PropTypes.arrayOf(PropTypes.shape()).isRequired,
};

export default MemberPlayingRecordChart;
