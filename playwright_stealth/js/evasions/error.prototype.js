log("loading error.prototype.js");

Object.defineProperty(Error.prototype, "name", {configurable: false, enumerable: false})
