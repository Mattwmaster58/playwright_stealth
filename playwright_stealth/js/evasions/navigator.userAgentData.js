log("loading navigator.userAgentData.js");

const originalUserAgentData = navigator.userAgentData;

if (originalUserAgentData) {
  /**
   * Helper to replace HeadlessChrome with Google Chrome in brand lists
   * @param {Array<{brand: string, version: string}>} list - Array of UADataBrand objects
   */
  const filterBrandList = (list) =>
    list.map((b) => (b.brand === "HeadlessChrome" ? { brand: "Google Chrome", version: b.version } : b));

  // Get the NavigatorUAData prototype
  const NavigatorUADataProto = Object.getPrototypeOf(originalUserAgentData);

  // Cache original methods before patching
  const originalGetHighEntropyValues = NavigatorUADataProto.getHighEntropyValues;
  const originalToJSON = NavigatorUADataProto.toJSON;
  const originalBrandsDescriptor = Object.getOwnPropertyDescriptor(NavigatorUADataProto, "brands");

  let cachedFilteredBrands = null;
  // Helper to get filtered brands (cached for identity checks)
  const getFilteredBrands = () => {
    if (cachedFilteredBrands === null) {
      const originalBrands = originalBrandsDescriptor.get.call(originalUserAgentData);
      cachedFilteredBrands = filterBrandList(originalBrands);
    }
    return cachedFilteredBrands;
  };

  // Patch getHighEntropyValues to filter HeadlessChrome from results
  utils.replaceProperty(NavigatorUADataProto, "getHighEntropyValues", {
    value: function (hints) {
      return originalGetHighEntropyValues.call(this, hints).then((data) => {
        const newData = { ...data };
        if (newData.brands) {
          newData.brands = filterBrandList(newData.brands);
        }
        if (newData.fullVersionList) {
          newData.fullVersionList = filterBrandList(newData.fullVersionList);
        }
        return newData;
      });
    },
  });

  // Patch toJSON to filter HeadlessChrome
  utils.replaceProperty(NavigatorUADataProto, "toJSON", {
    value: function () {
      const data = originalToJSON.call(this);
      return {
        brands: filterBrandList(data.brands),
        mobile: data.mobile,
        platform: data.platform,
      };
    },
  });

  // Patch brands getter to return filtered array (same instance each call, like real Chrome)
  utils.replaceProperty(NavigatorUADataProto, "brands", {
    get: function () {
      // Return cached filtered brands, computing and freezing on first access
      return getFilteredBrands();
    },
    enumerable: originalBrandsDescriptor.enumerable,
    configurable: originalBrandsDescriptor.configurable,
  });

  utils.replaceProperty(NavigatorUADataProto, "userAgentData", {
    get: () => originalUserAgentData,
  });
}
