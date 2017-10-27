/**
 * The Urls object is a utility for constructing CSHC-specific urls.
 * 
 * Note: This module relies on the url patterns being set in the 'window.cshcUrls'
 * object. See the 'base.html' Django template. 
 * 
 * To add a new url pattern, first add it to the list in 'base.html' and then add a 
 * matching helper method to the Urls object in this file.
 */

import reduce from 'lodash/reduce';
import entries from 'lodash/entries';

const Urls = {
  buildUrl: (urlName, parameters) =>
    reduce(
      entries(parameters),
      (acc, parameter) => acc.replace(parameter[0], parameter[1]),
      window.cshcUrls[urlName],
    ),

  member_detail: modelId =>
    Urls.buildUrl('member_detail', { [window.cshcUrls.pkPlaceholder]: modelId }),

  match_detail: modelId =>
    Urls.buildUrl('match_detail', { [window.cshcUrls.pkPlaceholder]: modelId }),

  venue_detail: slug => Urls.buildUrl('venue_detail', { [window.cshcUrls.slugPlaceholder]: slug }),

  clubteam_detail: slug =>
    Urls.buildUrl('clubteam_detail', { [window.cshcUrls.slugPlaceholder]: slug }),

  opposition_club_detail: slug =>
    Urls.buildUrl('opposition_club_detail', {
      [window.cshcUrls.slugPlaceholder]: slug,
    }),
};

export default Urls;
