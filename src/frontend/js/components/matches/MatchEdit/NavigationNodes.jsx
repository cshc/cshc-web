import { connect } from 'react-redux';
import NavigationNode from 'components/common/MultiStepForm/Navigation/NavigationNode';
import Match from 'models/match';

/**
 * The four navigation nodes of the Match Editing form. 
 * 
 * Each node is a Redux container that provides a 'complete' prop to the wrapped
 * NavigationNode component.
 */
module.exports = {
  ResultNavigationNode: connect(state => ({
    label: 'Result',
    icon: 'fa fa-handshake-o',
    complete: Match.resultIsComplete(state.matchState),
  }))(NavigationNode),
  AppearancesNavigationNode: connect(state => ({
    label: 'Appearances',
    icon: 'fa fa-users',
    complete: Match.appearancesIsComplete(state.matchState),
  }))(NavigationNode),
  AwardsNavigationNode: connect(state => ({
    label: 'Awards',
    icon: 'fa fa-trophy',
    complete: Match.awardsIsComplete(state.matchState),
  }))(NavigationNode),
  ReportNavigationNode: connect(state => ({
    label: 'Report',
    icon: 'fa fa-file-text',
    complete: Match.reportIsComplete(state.matchState),
  }))(NavigationNode),
};
