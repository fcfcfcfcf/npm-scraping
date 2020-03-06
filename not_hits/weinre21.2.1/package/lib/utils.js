// Generated by CoffeeScript 1.8.0
var Program, SequenceNumber, SequenceNumberMax, fs, log, path, utils,
  __hasProp = {}.hasOwnProperty;

fs = require('fs');

path = require('path');

utils = exports;

utils.Program = Program = path.basename(process.argv[1]);

SequenceNumberMax = 100 * 1024 * 1024;

SequenceNumber = 0;

utils.getNextSequenceNumber = function(g) {
  SequenceNumber++;
  if (SequenceNumber > SequenceNumberMax) {
    SequenceNumber = 0;
  }
  return SequenceNumber;
};

utils.trim = function(string) {
  return string.replace(/(^\s+)|(\s+$)/g, '');
};

utils.log = log = function(message) {};

utils.logVerbose = function(message) {};

utils.logDebug = function(message) {};

utils.exit = function(message) {};

utils.pitch = function(message) {
  log(message);
  throw message;
};

utils.setOptions = function(options) {
  return utils.options = options;
};

utils.ensureInteger = function(value, message) {
  var newValue;
  newValue = parseInt(value);
  if (isNaN(newValue)) {
    utils.exit("" + message + ": '" + value + "'");
  }
  return newValue;
};

utils.ensureString = function(value, message) {
  if (typeof value !== 'string') {
    utils.exit("" + message + ": '" + value + "'");
  }
  return value;
};

utils.ensureBoolean = function(value, message) {
  var newValue, uValue;
  uValue = value.toString().toUpperCase();
  newValue = null;
  switch (uValue) {
    case 'TRUE':
      newValue = true;
      break;
    case 'FALSE':
      newValue = false;
  }
  if (typeof newValue !== 'boolean') {
    utils.exit("" + message + ": '" + value + "'");
  }
  return newValue;
};

utils.setNamesForClass = function(aClass) {
  var key, val, _ref, _results;
  for (key in aClass) {
    if (!__hasProp.call(aClass, key)) continue;
    val = aClass[key];
    if (typeof val === "function") {
      val.signature = "" + aClass.name + "::" + key;
      val.displayName = val.signature;
      val.name = val.signature;
    }
  }
  _ref = aClass.prototype;
  _results = [];
  for (key in _ref) {
    if (!__hasProp.call(_ref, key)) continue;
    val = _ref[key];
    if (typeof val === "function") {
      val.signature = "" + aClass.name + "." + key;
      val.displayName = val.signature;
      _results.push(val.name = val.signature);
    } else {
      _results.push(void 0);
    }
  }
  return _results;
};

utils.registerClass = function(aClass) {
  utils.setNamesForClass(aClass);
  return aClass;
};

utils.alignLeft = function(string, length) {
  while (string.length < length) {
    string = "" + string + " ";
  }
  return string;
};

utils.alignRight = function(string, length) {
  while (string.length < length) {
    string = " " + string;
  }
  return string;
};

utils.fileExistsSync = function(name) {
  if (fs.existsSync) {
    return fs.existsSync(name);
  }
  return path.existsSync(name);
};