// this is close to the most accurate way to emulate this: https://stackoverflow.com/a/69533548
// no point "giving ourselves away" if we don't need to mock this values
// techniques exist to detect Object.defineProperty etc., so if we can avoid it we do
// if args include --disable-blink-features=AutomationControlled, we do not need to mock this
if (navigator.webdriver) {
  Object.defineProperty(Object.getPrototypeOf(navigator), "webdriver", {
    set: undefined,
    enumerable: true,
    configurable: true,
    get: new Proxy(
      Object.getOwnPropertyDescriptor(
        Object.getPrototypeOf(navigator),
        "webdriver"
      ).get,
      {
        apply: (target, thisArg, args) => {
          // emulate getter call validation
          Reflect.apply(target, thisArg, args);
          return false;
        },
      }
    ),
  });
}