"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

var _preact = require("preact");

function _objectWithoutProperties(obj, keys) { var target = {}; for (var i in obj) { if (keys.indexOf(i) >= 0) continue; if (!Object.prototype.hasOwnProperty.call(obj, i)) continue; target[i] = obj[i]; } return target; }

var IconBase = function IconBase(_ref, _ref2) {
  var _ref2$preactIconBase = _ref2.preactIconBase,
      preactIconBase = _ref2$preactIconBase === undefined ? {} : _ref2$preactIconBase;

  var children = _ref.children,
      color = _ref.color,
      size = _ref.size,
      style = _ref.style,
      props = _objectWithoutProperties(_ref, ["children", "color", "size", "style"]);

  var computedSize = size || preactIconBase.size || "1em";
  return (0, _preact.h)("svg", _extends({
    children: children,
    fill: "currentColor",
    preserveAspectRatio: "xMidYMid meet",
    height: computedSize,
    width: computedSize
  }, preactIconBase, props, {
    style: _extends({
      verticalAlign: "middle",
      color: color || preactIconBase.color
    }, preactIconBase.style || {}, style)
  }));
};

exports.default = IconBase;
module.exports = exports['default'];