'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _preactCompat = require('preact-compat');

var React = _interopRequireWildcard(_preactCompat);

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

exports.default = function (decoratedHref, decoratedText, key) {
  return React.createElement(
    'a',
    { href: decoratedHref, key: key },
    decoratedText
  );
};