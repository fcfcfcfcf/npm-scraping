
'use strict'

if (process.env.NODE_ENV === 'production') {
  module.exports = require('./invariantx.cjs.production.min.js')
} else {
  module.exports = require('./invariantx.cjs.development.js')
}
