// eslint-disable-next-line import/no-extraneous-dependencies
const webpack = require('webpack');
const config = require('../webpack.config');

delete config.chromeExtensionBoilerplate;

webpack(config, function(err) {
  if (err) throw err;
});
