const fs = require("fs");

const layoutFile = "/home/pi/smart-mirror/pi-client/mirror/current_layout.json";
const outputFile = "/home/pi/MagicMirror/config/config.js";

function getModuleDefaults(moduleName) {
  const defaults = {
    alert: {},

    clock: {
      classes: "Kiko",
    },

    calendar: {
      classes: "Kiko",
      header: "Slovenské sviatky",
      calendars: [
        {
          symbol: "calendar-check",
          url: "webcal://www.calendarlabs.com/ical-calendar/ics/509/Slovakia_Holidays.ics",
        },
      ],
    },

    compliments: {},

    weather: {
      classes: "Kiko",
      weatherProvider: "openweathermap",
      degreeLabel: true,
      type: "current",
      location: "Nové Zámky",
      locationID: "3058472",
      apiKey: "037c997bf494c31f075858acc643599f",
    },

    newsfeed: {
      classes: "Kiko",
      feeds: [
        {
          title: "Slovenské Aktuality",
          url: "https://www.aktuality.sk/rss/",
        },
      ],
      showSourceTitle: true,
      showPublishDate: true,
      broadcastNewsFeeds: true,
      broadcastNewsUpdates: true,
    },

    "MMM-WeatherDependentClothes": {
      location: "Nové Zámky",
      locationID: "3058472",
      appid: "SEM_DAJ_SVOJ_OPENWEATHER_API_KEY",
      preferences: [
        {
          name: "Winter jacket",
          icon: "jacket-cold",
          conditions: {
            temp_max: 2.0,
          },
        },
        {
          name: "Jacket",
          icon: "jacket",
          conditions: {
            temp_min: 2.0,
            temp_max: 9.0,
            rainfall_max: 3,
          },
        },
        {
          name: "Rain jacket",
          icon: "jacket-wet",
          conditions: {
            temp_min: 2.0,
            temp_max: 9.0,
            rainfall_min: 3,
          },
        },
      ],
    },

    "MMM-NowPlayingOnSpotify": {
      classes: "Kiko",
      clientID: "e2ba2c071db0407d9f71de5d5ea0c55e",
      clientSecret: "69853d878e36467089b5e717a67374e5",
      accessToken: "BQDuiIcjP-Okv5fTW99UoLygaN4K0f9DfVnYdjxEuIhsrBJRgfeMPv8kMhm7FpZ_Y19JhE1fSXWHGD-ehWHwMmwLlPs4bycM35TgzWeJuQfwou8JmwY8PcearZlWxmtslyxceZSw7bDIGK7IK-RCOeKDHSoGv14PlyucTDY_gwiRr5zYpJ-4V0IL",
      refreshToken: "AQAu77-12mJIQpNzmQDARdFDOcdc7DXf-tPAumB0rKNlhR8fLDbd48XPwIpmG5Kw1lQrZMaMhiL1FAk0tS7HeV1Mhtbpzq87cS6_lypnQ2WHeyukKPRf-0Dhk8_L74wGmes"
    },
  };

  return defaults[moduleName] || {};
}

function getModuleEntry(item) {
  const defaults = getModuleDefaults(item.module);

  return {
    module: item.module,
    position: item.position,
    classes: defaults.classes || undefined,
    header: defaults.header || undefined,
    config: {
      ...defaults,
      ...(item.config || {}),
    },
  };
}

try {
  const layout = JSON.parse(fs.readFileSync(layoutFile, "utf8"));

  const modules = layout.map(getModuleEntry).map((module) => {
    // odstráni undefined polia
    return Object.fromEntries(
      Object.entries(module).filter(([_, value]) => value !== undefined)
    );
  });

  const config = {
    address: "localhost",
    port: 8080,
    basePath: "/",
    ipWhitelist: [],
    useHttps: false,
    language: "en",
    locale: "en-SK",
    logLevel: ["INFO", "LOG", "WARN", "ERROR"],
    timeFormat: 24,
    units: "metric",
    modules,
  };

  const content = `
let config = ${JSON.stringify(config, null, 2)};

if (typeof module !== "undefined") {module.exports = config;}
`;

  fs.writeFileSync(outputFile, content);
  console.log("MagicMirror config.js generated successfully.");
} catch (error) {
  console.error("Error generating config:", error);
}
