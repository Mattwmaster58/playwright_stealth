log("loading navigator.userAgentData.js");
// Override navigator.userAgentData to hide HeadlessChrome
// Similar to navigator.userAgent.js

const originalUserAgentData = navigator.userAgentData;

if (originalUserAgentData) {
  const filterBrandList = (list) =>
    list.map((b) =>
      b.brand === "HeadlessChrome"
        ? { brand: "Google Chrome", version: b.version }
        : b
    );

  // Store original prototype methods before patching
  const NavigatorUADataProto = Object.getPrototypeOf(originalUserAgentData);
  const originalGetHighEntropyValues = NavigatorUADataProto.getHighEntropyValues;
  const originalToJSON = NavigatorUADataProto.toJSON;

  // Patch getHighEntropyValues on the prototype
  NavigatorUADataProto.getHighEntropyValues = function (hints) {
    return originalGetHighEntropyValues.call(this, hints).then((data) => {
      const newData = { ...data };
      if (newData.brands) newData.brands = filterBrandList(newData.brands);
      if (newData.fullVersionList) newData.fullVersionList = filterBrandList(newData.fullVersionList);
      return newData;
    });
  };

  // Patch toJSON on the prototype
  NavigatorUADataProto.toJSON = function () {
    const data = originalToJSON.call(this);
    return {
      brands: filterBrandList(data.brands),
      mobile: data.mobile,
      platform: data.platform,
    };
  };

  // Override the brands getter on the prototype to filter HeadlessChrome
  const originalBrandsDescriptor = Object.getOwnPropertyDescriptor(NavigatorUADataProto, "brands");
  if (originalBrandsDescriptor) {
    Object.defineProperty(NavigatorUADataProto, "brands", {
      get() {
        return filterBrandList(originalBrandsDescriptor.get.call(this));
      },
      enumerable: originalBrandsDescriptor.enumerable,
      configurable: originalBrandsDescriptor.configurable,
    });
  }

  // Since userAgentData is a complex object, it may not be specified by opts
  utils.replaceProperty(Object.getPrototypeOf(navigator), "userAgentData", {
    get: () => originalUserAgentData,
  });
}
