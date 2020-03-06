// Copyright 2012 The Obvious Corporation.

/*
 * This simply fetches the right version of phantom for the current platform.
 */

'use strict'

var requestProgress = require('request-progress')
var progress = require('progress')
var extractZip = require('extract-zip')
var cp = require('child_process')
var fs = require('fs-extra')
var helper = require('./lib/phantomjs')
var kew = require('kew')
var path = require('path')
var request = require('request')
var url = require('url')
var util = require('./lib/util')
var which = require('which')
var os = require('os')

var originalPath = process.env.PATH

var checkPhantomjsVersion = util.checkPhantomjsVersion
var getTargetPlatform = util.getTargetPlatform
var getTargetArch = util.getTargetArch
var getDownloadSpec = util.getDownloadSpec
var findValidPhantomJsBinary = util.findValidPhantomJsBinary
var verifyChecksum = util.verifyChecksum
var writeLocationFile = util.writeLocationFile

// If the process exits without going through exit(), then we did not complete.
var validExit = false

process.on('exit', function () {
  if (!validExit) {
    console.log('Install exited unexpectedly')
    exit(1)
  }
})

// NPM adds bin directories to the path, which will cause `which` to find the
// bin for this package not the actual phantomjs bin.  Also help out people who
// put ./bin on their path
process.env.PATH = helper.cleanPath(originalPath)

var libPath = path.join(__dirname, 'lib')
var pkgPath = path.join(libPath, 'phantom')
var phantomPath = null

// If the user manually installed PhantomJS, we want
// to use the existing version.
//
// Do not re-use a manually-installed PhantomJS with
// a different version.
//
// Do not re-use an npm-installed PhantomJS, because
// that can lead to weird circular dependencies between
// local versions and global versions.
// https://github.com/Obvious/phantomjs/issues/85
// https://github.com/Medium/phantomjs/pull/184
kew.resolve(true)
  .then(tryPhantomjsInLib)
  .then(checkFile)
  .then(extractDownload)
  .then(function (extractedPath) {
    return copyIntoPlace(extractedPath, pkgPath)
  })
  .then(function () {
    var location = getTargetPlatform() === 'win32' ?
        path.join(pkgPath, 'bin', 'phantomjs.exe') :
        path.join(pkgPath, 'bin' ,'phantomjs')

    try {
      // Ensure executable is executable by all users
      fs.chmodSync(location, '755')
    } catch (err) {
      if (err.code == 'ENOENT') {
        console.error('chmod failed: phantomjs was not successfully copied to', location)
        exit(1)
      }
      throw err
    }

    var relativeLocation = path.relative(libPath, location)
    writeLocationFile(relativeLocation)

    console.log('Done. Phantomjs binary available at', location)
    exit(0)
  })
  .fail(function (err) {
    console.error('Phantom installation failed', err, err.stack)
    exit(1)
  })

function exit(code) {
  validExit = true
  process.env.PATH = originalPath
  process.exit(code || 0)
}


/**
 * @return {?string} Get the download URL for phantomjs.
 *     May return null if no download url exists.
 */
function getDownloadUrl() {
  var spec = getDownloadSpec()
  return spec && spec.url
}

function checkFile() {
  var downloadSpec = getDownloadSpec(),
    fileName = path.join(__dirname, 'binaries', downloadSpec.url.split('/').pop()),
    deferred = kew.defer();

  return kew.fcall(function () {
    if (fs.existsSync(fileName)) {
      writeLocationFile(fileName);
      console.log(fileName)
      deferred.resolve(fileName);
    }
    return deferred.promise;
  });
}

function handleRequestError(error) {
  if (error && error.stack && error.stack.indexOf('SELF_SIGNED_CERT_IN_CHAIN') != -1) {
      console.error('Error making request, SELF_SIGNED_CERT_IN_CHAIN. ' +
          'Please read https://github.com/Medium/phantomjs#i-am-behind-a-corporate-proxy-that-uses-self-signed-ssl-certificates-to-intercept-encrypted-traffic')
      exit(1)
  } else if (error) {
    console.error('Error making request.\n' + error.stack + '\n\n' +
        'Please report this full log at https://github.com/Medium/phantomjs')
    exit(1)
  } else {
    console.error('Something unexpected happened, please report this full ' +
        'log at https://github.com/Medium/phantomjs')
    exit(1)
  }
}

function extractDownload(filePath) {
  var deferred = kew.defer()
  // extract to a unique directory in case multiple processes are
  // installing and extracting at once
  var extractedPath = filePath + '-extract-' + Date.now()
  var options = {cwd: extractedPath}

  fs.mkdirsSync(extractedPath, '0777')
  // Make double sure we have 0777 permissions; some operating systems
  // default umask does not allow write by default.
  fs.chmodSync(extractedPath, '0777')

  if (filePath.substr(-4) === '.zip') {
    console.log('Extracting zip contents')
    extractZip(path.resolve(filePath), {dir: extractedPath}, function(err) {
      if (err) {
        console.error('Error extracting zip')
        deferred.reject(err)
      } else {
        deferred.resolve(extractedPath)
      }
    })

  } else {
    console.log('Extracting tar contents (via spawned process)')
    cp.execFile('tar', ['jxf', path.resolve(filePath)], options, function (err) {
      if (err) {
        console.error('Error extracting archive')
        deferred.reject(err)
      } else {
        deferred.resolve(extractedPath)
      }
    })
  }
  return deferred.promise
}


function copyIntoPlace(extractedPath, targetPath) {
  console.log('Removing', targetPath)
  return kew.nfcall(fs.remove, targetPath).then(function () {
    // Look for the extracted directory, so we can rename it.
    var files = fs.readdirSync(extractedPath)
    for (var i = 0; i < files.length; i++) {
      var file = path.join(extractedPath, files[i])
      if (fs.statSync(file).isDirectory() && file.indexOf(helper.version) != -1) {
        console.log('Copying extracted folder', file, '->', targetPath)
        return kew.nfcall(fs.move, file, targetPath)
      }
    }

    console.log('Could not find extracted file', files)
    throw new Error('Could not find extracted file')
  })
}

/**
 * Check to see if the binary in lib is OK to use. If successful, exit the process.
 */
function tryPhantomjsInLib() {
  return kew.fcall(function () {
    return findValidPhantomJsBinary(path.resolve(__dirname, './lib/location.js'))
  }).then(function (binaryLocation) {
    if (binaryLocation) {
      console.log('PhantomJS is previously installed at', binaryLocation)
      exit(0)
    }
  }).fail(function () {
    // silently swallow any errors
  })
}
