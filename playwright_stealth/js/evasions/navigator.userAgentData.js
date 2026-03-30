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

  const filteredBrands = filterBrandList(originalUserAgentData.brands);

  const fakeUserAgentData = Object.create(Object.getPrototypeOf(originalUserAgentData), {
    brands: { get: () => filteredBrands, enumerable: true, configurable: true },
    mobile: { get: () => originalUserAgentData.mobile, enumerable: true, configurable: true },
    platform: { get: () => originalUserAgentData.platform, enumerable: true, configurable: true },
  });

  fakeUserAgentData.getHighEntropyValues = function (hints) {
    return originalUserAgentData.getHighEntropyValues(hints).then((data) => {
      const newData = { ...data };
      if (newData.brands) newData.brands = filterBrandList(newData.brands);
      if (newData.fullVersionList) newData.fullVersionList = filterBrandList(newData.fullVersionList);
      return newData;
    });
  };

  fakeUserAgentData.toJSON = function () {
    return {
      brands: filteredBrands,
      mobile: originalUserAgentData.mobile,
      platform: originalUserAgentData.platform,
    };
  };

  // Since userAgentData is a complex object, it may not be specified by opts
  utils.replaceProperty(Object.getPrototypeOf(navigator), "userAgentData", {
    get: () => fakeUserAgentData,
  });
}
