const path = require('path');
const glob = require('glob');
const forIn = require('lodash/forIn');
const forEach = require('lodash/forEach');
const BundleTracker = require('webpack-bundle-tracker');

const apps = glob.sync('./src/frontend/js/apps/*.jsx');

// Ref: https://github.com/ezhome/webpack-bundle-tracker/issues/4#issuecomment-191074951
const RelativeBundleTracker = function RelativeBundleTracker(options) {
  BundleTracker.call(this, options);
};
RelativeBundleTracker.prototype = Object.create(BundleTracker.prototype);
RelativeBundleTracker.prototype.writeOutput = function writeOutput(compiler, contents) {
  const relativePathRoot = `${path.join(__dirname)}${path.sep}src${path.sep}`;
  forIn(contents.chunks, (bundle) => {
    forEach(bundle, (chunk) => {
      if (chunk.path.startsWith(relativePathRoot)) {
        chunk.path = chunk.path.substr(relativePathRoot.length);
      }
    });
  });
  // contents.relativePathRoot = relativePathRoot;
  BundleTracker.prototype.writeOutput.call(this, compiler, contents);
};

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
  RelativeBundleTracker,
};
