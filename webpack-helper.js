const glob = require('glob');

const apps = glob.sync('./src/frontend/js/apps/*.jsx');

function buildEntries(hotReload = false) {
  const entry = {};
  // Automatically create entry points for each top-level React app
  for (let i = 0; i < apps.length; i += 1) {
    const splitApp = apps[i].split('/');
    const appFilename = splitApp[splitApp.length - 1];
    const appName = appFilename.split('.')[0];
    entry[appName] = hotReload
      ? [
        'react-hot-loader/patch',
        'webpack-dev-server/client?http://localhost:3000',
        'webpack/hot/only-dev-server',
        apps[i],
      ]
      : [apps[i]];
  }
  return entry;
}

module.exports = {
  buildEntries,
};
