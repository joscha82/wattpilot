# Wattpilot API Description

## WebSocket Message Types

| Key | Title | Description | Example |
|-----|-------|-------------|---------|
| `hello` | Hello Message | Received upon connection before authentication | `{"type": "hello", "serial": "<some_serial>", "hostname": "Wattpilot_<some_serial>", "friendly_name": "<some_name>", "manufacturer": "fronius", "devicetype": "wattpilot", "version": "36.3", "protocol": 2, "secured": true}` |
| `authRequired` | Auth Required | Received after hello to ask for authentication | `{"type": "authRequired", "token1": "<some_token>", "token2": "<some_token>"}` |
| `auth` | Auth Message | This message is sent from the client to Wattpilot to perform an authentication. | `{"type": "auth", "token3": "<some_token>", "hash": "<some_hash>"}` |
| `authSuccess` | Auth Success | Received after sending a correct authentication message | `{"type": "authSuccess", "token3": "<some_token>", "hash": "<some_hash>"}` |
| `authError` | Auth Error | Received after sending an incorrect authentication message (e.g. wrong password) | `{"type": "authError", "token3": "<some_token>", "hash": "<some_hash>", "message": "Wrong password"}` |
| `fullStatus` | Full Status | Set of messages received after successful connection. These messages contain all properties of Wattpilot. `partial:true` means that more `fullStatus` messages will be sent with additional properties. | `{"type": "fullStatus", "partial": true, "status": {"mod": 1, "rfb": 1698, "stao": null, "alw": true, "acu": 6, "acui": 6, "adi": true, "dwo": null, "tpa": 0}}` |
| `deltaStatus` | Delta Status | Whenever a property changes a Delta Status is sent | `{"type": "deltaStatus", "status": {"rfb": 1699, "utc": "2022-04-22T10:44:08.865.407", "loc": "2022-04-22T12:44:08.866.280 +02:00", "rbt": 1560937433, "nrg": [236, 235, 235, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "fhz": 49.937, "rcd": 5, "lps": 61, "tpcm": [4, 0, 3, 1, 0, 0, 0, 0, 45, 0, 3, 0, 0, 47, 44, 0, 0, 0, 0, 0, 12]}}` |
| `clearInverters` | Clear Inverters | Unknown | `{"type": "clearInverters", "partial": true}` |
| `updateInverter` | Update Inverter | Contains information of connected PV inverter / power meter | `{"type": "updateInverter", "partial": false, "id": "<some_id>", "paired": true, "deviceFamily": "DataManager", "label": "<some_name>", "model": "PILOT", "commonName": "pilot-0.5e-<some_id>", "ip": "<some_ip>", "connected": true, "reachableMdns": true, "reachableUdp": true, "reachableHttp": true, "status": 0, "message": "ok"}` |
| `securedMsg` | Secured Message | Is sent by the client to change a property value. | `{"type": "securedMsg", "data": "{\"type\": \"setValue\", \"requestId\": 1, \"key\": \"nmo\", \"value\": true}", "requestId": "1sm", "hmac": "<some_hmac>"}` |
| `response` | Update Response Message | Received after sending an update and contains the result of the update | `{"type": "response", "requestId": "1", "success": true, "status": {"nmo": true}}` |

## WebSocket API Properties

| Key/Alias | Title | R/W | JSON/API Type | Category | HA Enabled | Description | Example |
|-----------|-------|-----|---------------|----------|------------|-------------|---------|
| `abm`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `"<SOME_MAC>"` |
| `acs`<br>`accessState` | Access State | R/W | `integer`<br>`uint8` | Config | :heavy_check_mark: | access_control user setting (Open=0, Wait=1) | `0` |
| `acu`<br>`allowedCurrent` | Allowed Current | R | `integer`<br>`int` | Status | :white_large_square: | How many ampere is the car allowed to charge now? | `6` |
| `acui`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `6` |
| `adi`<br>`adapterLimit` | Adapter (16A) Limit | R | `boolean`<br>`bool` | Status | :white_large_square: | Is the 16A adapter used? Limits the current to 16A | `true` |
| `al1`<br>`adapterLimit1` | Adapter Limit 1 |  | `integer`<br>- |  | :white_large_square: |  | `6` |
| `al2`<br>`adapterLimit2` | Adapter Limit 2 |  | `integer`<br>- |  | :white_large_square: |  | `10` |
| `al3`<br>`adapterLimit3` | Adapter Limit 3 |  | `integer`<br>- |  | :white_large_square: |  | `12` |
| `al4`<br>`adapterLimit4` | Adapter Limit 4 |  | `integer`<br>- |  | :white_large_square: |  | `14` |
| `al5`<br>`adapterLimit5` | Adapter Limit 5 |  | `integer`<br>- |  | :white_large_square: |  | `16` |
| `alw`<br>`allowCharging` | Allow Charging | R | `boolean`<br>`bool` | Status | :heavy_check_mark: | Is the car allowed to charge at all now? | `true` |
| `ama`<br>`maxCurrentLimit` | Max Current Limit | R/W | `integer`<br>`uint8` | Config | :heavy_check_mark: | ampere_max limit | `16` |
| `amp`<br>`chargingCurrent` | Charging Current | R/W | `integer`<br>`uint8` | Config | :heavy_check_mark: | requestedCurrent in Ampere, used for display on LED ring and logic calculations | `6` |
| `amt`<br>`temperatureCurrentLimit` | Temperature Current Limit | R | `integer`<br>`int` | Status | :white_large_square: | temperatureCurrentLimit | `32` |
| `apd`<br>`firmwareDescription` | Firmware Description | R | `object`<br>`object` | Constant | :white_large_square: | firmware description | `{"project_name": "wattpilot_hw4+", "version": "36.3", "secure_version": 0, "timestamp": "Jan 31 2022 22:51:39", "idf_ver": "v5.0-dev-1103-ga9ef558d", "sha256": "<some_sha256>"}` |
| `arv`<br>`appRecommendedVersion` | App Recommended Version | R | `string`<br>`string` | Constant | :white_large_square: | app recommended version (used to show in the app that the app is outdated) | `"1.2.1"` |
| `asc`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `true` |
| `aup`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `6` |
| `awc`<br>`awattarCountry` | Awattar Country | R/W | `integer`<br>`uint8` | Config | :heavy_check_mark: | awattar country (Austria=0, Germany=1) | `0` |
| `awcp`<br>`awattarCurrentPrice` | Awattar Current Price | R | `object`<br>`optional<object>` | Status | :white_large_square: | awattar current price | `{"start": 1650567600, "end": 1650571200, "marketprice": 22.044}` |
| `awp`<br>`awattarMaxPrice` | Awattar Max Price | R/W | `float`<br>`float` | Config | :heavy_check_mark: | awattarMaxPrice in ct | `3` |
| `awpl`<br>`awattarPriceList` | Awattar Price List | R/W | `array`<br>`array` | Status | :white_large_square: | awattar price list, timestamps are measured in unix-time, seconds since 1970 | `[{"start": 1650567600, "end": 1650571200, "marketprice": 22.044}, {"start": 1650571200, "end": 1650574800, "marketprice": 19.971}]` |
| `bac`<br>`buttonAllowCurrentChange` | Button Allow Current Change | R/W | `boolean`<br>`bool` | Config | :heavy_check_mark: | Button allow Current change | `true` |
| `bam`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `true` |
| `cae`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `false` |
| `cak`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `""` |
| `car`<br>`carState` | Car State | R | `integer`<br>`optional<uint8>` | Status | :heavy_check_mark: | carState, null if internal error (Unknown/Error=0, Idle=1, Charging=2, WaitCar=3, Complete=4, Error=5) | `1` |
| `cards`<br>`registeredCards` | Registered Cards | R/W | `array`<br>`array` |  | :white_large_square: | Registered RFID cards for different users | `[{"name": "User 1", "energy": 0, "cardId": true}, {"name": "User 2", "energy": 0, "cardId": false}]` |
| `cbl`<br>`cableCurrentLimit` | Cable Current Limit | R | `integer`<br>`optional<int>` | Status | :heavy_check_mark: | cable_current_limit in A | `20` |
| `cbm`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `null` |
| `cca`<br>`cloudClientAuth` | Cloud Client Auth | R | `boolean`<br>`bool` | Config | :white_large_square: | cloud websocket use client auth (if key&cert are setup correctly) | `true` |
| `cch`<br>`colorCharging` | Color Charging | R/W | `string`<br>`string` | Config | :heavy_check_mark: | color_charging, format: #RRGGBB | `"#00FFF"` |
| `cci`<br>- |  |  | `object`<br>- |  | :white_large_square: |  | `{"id": "<some_numeric_id>", "paired": true, "deviceFamily": "DataManager", "label": "<some_name>", "model": "PILOT", "commonName": "pilot-0.5e-<some_id>", "ip": "<some_ip>", "connected": true, "reachableMdns": true, "reachableUdp": true, "reachableHttp": true, "status": 0, "message": "ok"}` |
| `cco`<br>`carConsumption` | Car Consumption | R/W | `float`<br>`double` | Config | :heavy_check_mark: | car consumption in kWh for 100km (only stored for app) | `24` |
| `ccrv`<br>`chargeControllerRecommendedVersion` | Charge Controller Recommended Version | R | `string`<br>`string` | Constant | :white_large_square: |  |  |
| `ccu`<br>`chargeControllerUpdateProgress` | Charge Controller Update Progress | R | `object`<br>`optional<object>` | Status | :white_large_square: | charge controller update progress (null if no update is in progress) | `null` |
| `ccw`<br>`currentlyConnectedWifi` | Currently Connected Wifi | R | `object`<br>`optional<object>` | Status | :white_large_square: | Currently connected WiFi | `{"ssid": "<SOME_SSID>", "encryptionType": 3, "pairwiseCipher": 4, "groupCipher": 4, "b": true, "g": true, "n": true, "lr": false, "wps": false, "ftmResponder": false, "ftmInitiator": false, "channel": 6, "bssid": "<SOME_BSSID>", "ip": "<some_ip4>", "netmask": "255.255.255.0", "gw": "<some_ip4>", "ipv6": ["<some_ip6>", "<some_ip6>"], "dns0": "<some_ip4>", "dns1": "0.0.0.0", "dns2": "0.0.0.0"}` |
| `cdi`<br>`chargingDurationInfo` | Charging Duration Info | R | `object`<br>`object` | Status | :heavy_check_mark: | charging duration info (null=no charging in progress, type=0 counter going up, type=1 duration in ms) | `{"type": 1, "value": 11554770}` |
| `cdv`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `null` |
| `cfi`<br>`colorFinished` | Color Finished | R/W | `string`<br>`string` | Config | :white_large_square: | color_finished, format: #RRGGBB | `"#00FF00"` |
| `chr`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `true` |
| `cid`<br>`colorIdle` | Color Idle | R/W | `string`<br>`string` | Config | :white_large_square: | color_idle, format: #RRGGBB | `"#0000FF"` |
| `clp`<br>`currentLimitPresets` | Current Limit Presets | R/W | `array`<br>`array` | Config | :white_large_square: | current limit presets, max. 5 entries | `[6, 10, 12, 14, 16]` |
| `cpe`<br>`cpEnable` | CP Enable | R | `boolean`<br>`bool` | Status | :white_large_square: | The charge ctrl requests the CP signal enabled or not immediately | `true` |
| `cpr`<br>`cpEnableRequest` | CP Enable Request | R | `boolean`<br>`bool` | Status | :white_large_square: | CP enable request. cpd=0 triggers the charge ctrl to set cpe=0 once processed | `true` |
| `csca`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `2` |
| `ct`<br>`carType` | Car Type | R/W | `string`<br>`string` | Config | :white_large_square: | car type, free text string (max. 64 characters, only stored for app) | `"vwID3_4"` |
| `cus`<br>`cableUnlockStatus` | Cable Unlock Status | R | `integer`<br>`uint8` | Status | :heavy_check_mark: | Cable unlock status (Unknown=0, Unlocked=1, UnlockFailed=2, Locked=3, LockFailed=4, LockUnlockPowerout=5) | `1` |
| `cwc`<br>`colorWaitCar` | Color Wait Car | R/W | `string`<br>`string` | Config | :white_large_square: | color_waitcar, format: #RRGGBB | `"#FFFF00"` |
| `cwe`<br>`cloudWsEnabled` | Cloud WS Enabled | R/W | `boolean`<br>`bool` | Config | :white_large_square: | cloud websocket enabled | `true` |
| `cws`<br>`cloudWsStarted` | Cloud WS Started | R | `boolean`<br>`bool` | Status | :white_large_square: | cloud websocket started | `true` |
| `cwsc`<br>`cloudWsConnected` | Cloud WS Connected | R | `boolean`<br>`bool` | Status | :white_large_square: | cloud websocket connected | `true` |
| `cwsca`<br>`cloudWsConnectedAge` | Cloud WS Connected Age | R | `integer`<br>`optional<milliseconds>` | Status | :white_large_square: | cloud websocket connected (age) | `46954034` |
| `data`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `"{\"i\":120,\"url\":\"https://data.wattpilot.io/data?e=<some_token>\"}"` |
| `dbm`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `"<SOME_MAC_ADDRESS>"` |
| `dccu`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `false` |
| `dco`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `true` |
| `deltaa`<br>`deltaCurrent` | deltaCurrent | R | `float`<br>`float` | Other | :white_large_square: |  |  |
| `deltap`<br>`deltaPower` | Delta Power | R | `float`<br>`float` | Status | :white_large_square: |  |  |
| `dll`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `"https://data.wattpilot.io/export?e=<some_token>"` |
| `dns`<br>`dnsServer` | DNS Server | R | `object`<br>`object` | Status | :white_large_square: | DNS server | `{"dns": "0.0.0.0"}` |
| `dwo`<br>`chargingEnergyLimit` | Charging Energy Limit | R/W | `float`<br>`optional<double>` | Config | :heavy_check_mark: | charging energy limit, measured in Wh, null means disabled, not the next trip energy | `null` |
| `ecf`<br>`espCpuFreq` | ESP CPU Frequency | R | `object`<br>`object` | Constant | :white_large_square: | ESP CPU freq (source: XTAL=0, PLL=1, 8M=2, APLL=3) | `{"source": 1, "source_freq_mhz": 320, "div": 2, "freq_mhz": 160}` |
| `eci`<br>`espChipInfo` | ESP Chip Info | R | `object`<br>`object` | Constant | :white_large_square: | ESP chip info (model: ESP32=1, ESP32S2=2, ESP32S3=4, ESP32C3=5; features: EMB_FLASH=bit0, WIFI_BGN=bit1, BLE=bit4, BT=bit5) | `{"model": 1, "features": 50, "cores": 2, "revision": 3}` |
| `efh`<br>`espFreeHeap` | ESP Free Heap | R | `integer`<br>`size_t` | Status | :white_large_square: | ESP free heap | `125920` |
| `efh32`<br>`espFreeHeap32` | ESP Free Heap 32 | R | `integer`<br>`size_t` | Status | :white_large_square: | ESP free heap 32bit aligned | `125920` |
| `efh8`<br>`espFreeHeap8` | ESP Free Heap 8 | R | `integer`<br>`size_t` | Status | :white_large_square: | ESP free heap 8bit aligned | `86848` |
| `efi`<br>`espFlashInfo` | ESP Flash Info | R | `object`<br>`object` | Constant | :white_large_square: | ESP Flash info (spi_mode: QIO=0, QOUT=1, DIO=2, DOUT=3, FAST_READ=4, SLOW_READ=5; spi_speed: 40M=0, 26M=1, 20M=2, 80M=15; spi_size: 1MB=0, 2MB=1, 4MB=2, 8MB=3, 16MB=4, MAX=5) | `null` |
| `ehs`<br>`espHeapSize` | ESP Heap Size | R | `integer`<br>`size_t` | Status | :white_large_square: | ESP heap size | `282800` |
| `emfh`<br>`espMinFreeHeap` | ESP Min Free Heap | R | `integer`<br>`size_t` | Status | :white_large_square: | ESP minimum free heap since boot | `78104` |
| `emhb`<br>`espMaxHeap` | ESP Max Heap | R | `integer`<br>`size_t` | Status | :white_large_square: | ESP max size of allocated heap block since boot | `67572` |
| `ens`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `""` |
| `err`<br>`errorState` | Error State | R | `integer`<br>`optional<uint8>` | Status | :heavy_check_mark: | error, null if internal error (None = 0, FiAc = 1, FiDc = 2, Phase = 3, Overvolt = 4, Overamp = 5, Diode = 6, PpInvalid = 7, GndInvalid = 8, ContactorStuck = 9, ContactorMiss = 10, FiUnknown = 11, Unknown = 12, Overtemp = 13, NoComm = 14, StatusLockStuckOpen = 15, StatusLockStuckLocked = 16, Reserved20 = 20, Reserved21 = 21, Reserved22 = 22, Reserved23 = 23, Reserved24 = 24) | `0` |
| `esk`<br>`energySetKwh` | Energy Set kWh | R/W | `boolean`<br>`bool` | Config | :white_large_square: | energy set kwh (only stored for app) | `true` |
| `esr`<br>`rtcResetReasons` | RTC Reset Reasons | R | `array`<br>`array` | Status | :white_large_square: | rtc_get_reset_reason for core 0 and 1 (NO_MEAN=0, POWERON_RESET=1, SW_RESET=3, OWDT_RESET=4, DEEPSLEEP_RESET=5, SDIO_RESET=6, TG0WDT_SYS_RESET=7, TG1WDT_SYS_RESET=8, RTCWDT_SYS_RESET=9, INTRUSION_RESET=10, TGWDT_CPU_RESET=11, SW_CPU_RESET=12, RTCWDT_CPU_RESET=13, EXT_CPU_RESET=14, RTCWDT_BROWN_OUT_RESET=15, RTCWDT_RTC_RESET=16) | `[12, 12]` |
| `eto`<br>`energyCounterTotal` | Energy Counter Total | R | `integer`<br>`uint64` | Status | :heavy_check_mark: | energy_total, measured in Wh | `1076098` |
| `etop`<br>`energyTotalPersisted` | Energy Total Persisted | R | `integer`<br>`uint64` | Status | :heavy_check_mark: | energy_total persisted, measured in Wh, without the extra magic to have live values | `1076098` |
| `facwak`<br>`factoryWifiApKey` | Factory Wifi AP Key | R | `string`<br>`string` | Constant | :white_large_square: | WiFi AccessPoint Key RESET VALUE (factory) | `true` |
| `fam`<br>`pvBatteryLimit` | PV Battery Limit |  | `integer`<br>- |  | :white_large_square: | Battery limit for PV surplus charging | `20` |
| `fap`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `false` |
| `fbuf_age`<br>`fbufAge` | Fronius Age |  | `integer`<br>- |  | :white_large_square: |  | `93639347` |
| `fbuf_akkuMode`<br>`akkuMode` | Battery Mode |  | `integer`<br>- |  | :white_large_square: |  | `1` |
| `fbuf_akkuSOC`<br>`akkuSoc` | Battery SoC |  | `float`<br>- |  | :heavy_check_mark: | State of charge of the PV battery | `72.5` |
| `fbuf_ohmpilotState`<br>`ohmpilotState` | Ohmpilot State |  | `unknown`<br>- |  | :white_large_square: |  | `null` |
| `fbuf_ohmpilotTemperature`<br>`ohmpilotTemperature` | Ohmpilot Temperature |  | `unknown`<br>- |  | :white_large_square: |  | `null` |
| `fbuf_pAcTotal`<br>`powerAcTotal` | Power AC Total |  | `unknown`<br>- |  | :white_large_square: |  | `null` |
| `fbuf_pAkku`<br>`powerAkku` | Power Akku |  | `float`<br>- |  | :heavy_check_mark: | Power that is consumed from the PV battery (or delivered into the battery, if negative) | `-3985.899` |
| `fbuf_pGrid`<br>`powerGrid` | Power Grid |  | `integer`<br>- |  | :heavy_check_mark: | Power consumed from grid (or delivered to grid, if negative) | `11` |
| `fbuf_pPv`<br>`powerPv` | Power PV |  | `float`<br>- |  | :heavy_check_mark: | PV power that is produced | `4701.407` |
| `fcc`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `true` |
| `fck`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `true` |
| `fem`<br>`flashEncryptionMode` | Flash Encryption Mode | R | `integer`<br>`uint8` | Constant | :white_large_square: | Flash Encryption Mode (Disabled=0, Development=1, Release=2) | `2` |
| `ferm`<br>`effectiveRoundingMode` | Effective Rounding Mode | R | `integer`<br>`uint8` | Status | :white_large_square: | effectiveRoundingMode | `1` |
| `ffb`<br>`lockFeedback` | Lock Feedback | R | `integer`<br>`uint8` | Status | :heavy_check_mark: | lock feedback (NoProblem=0, ProblemLock=1, ProblemUnlock=2) | `0` |
| `ffba`<br>`lockFeedbackAge` | Lock Feedback Age | R | `integer`<br>`optional<milliseconds>` | Status | :white_large_square: | lock feedback (age) | `null` |
| `ffna`<br>`factoryFriendlyName` | Factory Friendly Name | R | `string`<br>`string` | Constant | :white_large_square: | factoryFriendlyName | `"Wattpilot_<some_serialnr>"` |
| `fhi`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `true` |
| `fhz`<br>`frequency` | Frequency | R | `float`<br>`optional<float>` | Status | :heavy_check_mark: | Power grid frequency (~50Hz) or 0 if unknown | `49.815` |
| `fi23`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `true` |
| `fio23`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `true` |
| `fit`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `1` |
| `fml`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `"grid"` |
| `fmmp`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `0` |
| `fmt`<br>`minChargeTime` | Min Charge Time | R/W | `integer`<br>`milliseconds` | Config | :white_large_square: | minChargeTime in milliseconds | `900000` |
| `fna`<br>`friendlyName` | Friendly Name | R/W | `string`<br>`string` | Config | :heavy_check_mark: | friendlyName | `"<some_name>"` |
| `fntp`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `null` |
| `fot`<br>`ohmpilotTemperatureLimit` | Ohmpilot Temperature Limit |  | `integer`<br>- |  | :heavy_check_mark: |  | `20` |
| `frc`<br>`forceState` | Force State | R/W | `integer`<br>`uint8` | Config | :heavy_check_mark: | forceState (Neutral=0, Off=1, On=2) | `0` |
| `frci`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `true` |
| `fre`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `false` |
| `frm`<br>`roundingMode` | Rounding Mode | R | `integer`<br>`uint8` | Config | :white_large_square: | roundingMode PreferPowerFromGrid=0, Default=1, PreferPowerToGrid=2 | `1` |
| `fsp`<br>`forceSinglePhase` | Force Single Phase | R/W | `boolean`<br>`bool` | Status | :white_large_square: | force_single_phase (shows if currently single phase charge is enforced) | `false` |
| `fsptws`<br>`forceSinglePhaseToggleWishedSince` | Force Single Phase Toggle Wished Since | R | `integer`<br>`optional<milliseconds>` | Status | :white_large_square: | force single phase toggle wished since | `28771782` |
| `fst`<br>`startingPower` | Starting Power | R/W | `float`<br>`float` | Config | :heavy_check_mark: | startingPower in watts. This is the minimum power at which charging can be started. | `1400` |
| `fte`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `50000` |
| `ftlf`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `false` |
| `ftls`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `null` |
| `ftt`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `25200` |
| `ful`<br>`useDynamicPricing` | useDynamicPricing |  | `boolean`<br>- |  | :white_large_square: | Uses dynamic electricity pricing (Lumina, aWattar) | `false` |
| `fup`<br>`usePvSurplus` | PV Surplus | R/W | `boolean`<br>`bool` | Config | :white_large_square: | Use PV surplus charging | `true` |
| `fwan`<br>`factoryWifiApName` | Factory WiFi AP Name | R | `string`<br>`string` | Constant | :white_large_square: | factoryWifiApName | `"Wattpilot_<some_serialnr>"` |
| `fwc`<br>`firmwareCarControl` | Firmware Car Control | R | `string`<br>`string` | Constant | :white_large_square: | firmware from CarControl | `10` |
| `fwv`<br>`firmwareVersion` | Firmware Version | R | `string`<br>`string` | Constant | :heavy_check_mark: | Version of the Wattpilot firmware | `36.3` |
| `fzf`<br>`zeroFeedin` | Zero Feedin | R/W | `boolean`<br>`bool` | Config | :white_large_square: | zeroFeedin | `false` |
| `gme`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `false` |
| `gmk`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `""` |
| `host`<br>`hostname` | Hostname | R | `string`<br>`optional<string>` | Status | :white_large_square: | hostname used on STA interface | `"Wattpilot_<some_serialnr>"` |
| `hsa`<br>`httpStaAuthentication` | HTTP STA Authentication | R/W | `boolean`<br>`bool` | Config | :white_large_square: | httpStaAuthentication | `true` |
| `hsta`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `"Wattpilot_<some_serialnr>"` |
| `hsts`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `"Wattpilot_<some_serialnr>"` |
| `hws`<br>`httpStaReachable` | HTTP STA Reachable | R/W | `boolean`<br>`bool` | Config | :white_large_square: | httpStaReachable, defines if the local webserver should be reachable from the customers WiFi | `true` |
| `ido`<br>`inverterDataOverride` | Inverter Data Override | R | `object`<br>`optional<object>` | Config | :white_large_square: | Inverter data override | `null` |
| `imd`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `false` |
| `imi`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `0` |
| `immr`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `20` |
| `imp`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `"_tcp"` |
| `ims`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `"_Fronius-SE-Inverter"` |
| `imse`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `true` |
| `inva`<br>`inverterDataAge` | Inverter Data Age | R | `integer`<br>`milliseconds` | Status | :white_large_square: | age of inverter data |  |
| `irs`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `false` |
| `isml`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `false` |
| `iuse`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `true` |
| `las`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `0` |
| `lbh`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `null` |
| `lbp`<br>`lastButtonPress` | Last Button Press | R | `integer`<br>`milliseconds` | Status | :white_large_square: | lastButtonPress in milliseconds | `null` |
| `lbr`<br>`ledBrightness` | LED Brightness | R/W | `integer`<br>`uint8` | Config | :white_large_square: | led_bright, 0-255 | `255` |
| `lbs`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `806` |
| `lccfc`<br>`lastCarStateChangedFromCharging` | Last Car State Changed From Charging | R | `integer`<br>`optional<milliseconds>` | Status | :white_large_square: | lastCarStateChangedFromCharging (in ms) | `7157569` |
| `lccfi`<br>`lastCarStateChangedFromIdle` | Last Car State Changed From Idle | R | `integer`<br>`optional<milliseconds>` | Status | :white_large_square: | lastCarStateChangedFromIdle (in ms) | `5369660` |
| `lcctc`<br>`lastCarStateChangedToCharging` | Last Car State Changed To Charging | R | `integer`<br>`optional<milliseconds>` | Status | :white_large_square: | lastCarStateChangedToCharging (in ms) | `5369660` |
| `lch`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `5369660` |
| `lck`<br>`effectiveLockSetting` | Effective Lock Setting | R | `integer`<br>`uint8` | Status | :heavy_check_mark: | Effective lock setting, as sent to Charge Ctrl (Normal=0, AutoUnlock=1, AlwaysLock=2, ForceUnlock=3) | `0` |
| `led`<br>`ledInfo` | LED Info | R | `object`<br>`object` | Status | :white_large_square: | internal infos about currently running led animation | `{"id": 5, "name": "Finished", "norwayOverlay": true, "modeOverlay": true, "subtype": "renderCmds", "ranges": [{"from": 0, "to": 31, "colors": ["#00FF00"]}]}` |
| `ledo`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `null` |
| `lfspt`<br>`lastForceSinglePhaseToggle` | Last Force Single Phase Toggle | R | `integer`<br>`optional<milliseconds>` | Status | :white_large_square: | last force single phase toggle | `null` |
| `llr`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `2` |
| `lmo`<br>`logicMode` | Logic Mode | R/W | `integer`<br>`uint8` | Config | :heavy_check_mark: | logic mode (Default=3, Awattar=4, AutomaticStop=5) | `3` |
| `lmsc`<br>`lastModelStatusChange` | Last Model Status Change | R | `integer`<br>`milliseconds` | Status | :white_large_square: | last model status change | `28822622` |
| `loa`<br>`loadBalancingAmpere` | Load Balancing Current | R | `integer`<br>`optional<uint8>` | Status | :white_large_square: | load balancing ampere | `null` |
| `loc`<br>`localTime` | Local Time | R | `string`<br>`string` | Status | :white_large_square: | local time | `"2022-03-06T11:59:38.182.123 +01:00"` |
| `loe`<br>`loadBalancingEnabled` | Load Balancing Enabled | R/W | `boolean`<br>`bool` | Config | :white_large_square: | Load balancing enabled | `false` |
| `lof`<br>`loadFallback` | Load Fallback | R/W | `integer`<br>`uint8` | Config | :white_large_square: | load_fallback | `0` |
| `log`<br>`loadGroupId` | Load Group ID | R/W | `string`<br>`string` | Config | :white_large_square: | load_group_id | `""` |
| `loi`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `false` |
| `lom`<br>`loadBalancingMembers` | Load Balancing Members | R | `array`<br>`array` | Status | :white_large_square: | load balancing members | `null` |
| `lop`<br>`loadPriority` | Load Priority | R/W | `integer`<br>`uint16` | Config | :white_large_square: | load_priority | `50` |
| `los`<br>`loadBalancingStatus` | Load Balancing Status | R | `string`<br>`optional<string>` | Status | :white_large_square: | load balancing status | `null` |
| `lot`<br>`loadBalancingTotalAmpere` | Load Balancing Current Total | R/W | `integer`<br>`uint32` | Config | :white_large_square: | load balancing total amp | `32` |
| `loty`<br>`loadBalancingType` | Load Balancing Type | R/W | `integer`<br>`uint8` | Config | :heavy_check_mark: | load balancing type (Static=0, Dynamic=1) | `0` |
| `lps`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `63` |
| `lpsc`<br>`lastPvSurplusCalculation` | Last PV Surplus Calculation | R | `integer`<br>`milliseconds` | Status | :white_large_square: | last pv surplus calculation | `28771782` |
| `lrc`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `null` |
| `lri`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `null` |
| `lrr`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `null` |
| `lse`<br>`ledSaveEnergy` | LED Save Energy | R/W | `boolean`<br>`bool` | Config | :white_large_square: | led_save_energy | `false` |
| `lssfc`<br>`lastStaSwitchedFromConnected` | Last STA Switched From Connected | R | `integer`<br>`optional<milliseconds>` | Status | :white_large_square: | lastStaSwitchedFromConnected (in milliseconds) | `null` |
| `lsstc`<br>`lastStaSwitchedToConnected` | Last STA Switched To Connected | R | `integer`<br>`optional<milliseconds>` | Status | :white_large_square: | lastStaSwitchedToConnected (in milliseconds) | `7970` |
| `maca`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `"<some_mac>"` |
| `macs`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `"<some_mac>"` |
| `map`<br>`loadMapping` | Load Mapping | R/W | `array`<br>`array` | Config | :white_large_square: | load_mapping (uint8_t[3]) | `[1, 2, 3]` |
| `mca`<br>`minChargingCurrent` | Min Charging Current | R/W | `integer`<br>`uint8` | Config | :white_large_square: | minChargingCurrent | `6` |
| `mci`<br>`minimumChargingInterval` | Minimum Charging Interval | R/W | `integer`<br>`milliseconds` | Config | :white_large_square: | minimumChargingInterval in milliseconds (0 means disabled) | `0` |
| `mcpd`<br>`minChargePauseDuration` | Min Charge Pause Duration | R/W | `integer`<br>`milliseconds` | Config | :white_large_square: | minChargePauseDuration in milliseconds (0 means disabled) | `0` |
| `mcpea`<br>`minChargePauseEndsAt` | Min Charge Pause End | R/W | `integer`<br>`optional<milliseconds>` | Status | :white_large_square: | minChargePauseEndsAt (set to null to abort current minChargePauseDuration) | `null` |
| `mod`<br>`moduleHwPcbVersion` | Module HW PCB Version | R | `integer`<br>`uint8` | Constant | :white_large_square: | Module hardware pcb version (0, 1, ...) | `1` |
| `modelStatus`<br>`modelStatus` | Model Status | R | `integer`<br>`uint8` | Status | :heavy_check_mark: | Reason why we allow charging or not right now (NotChargingBecauseNoChargeCtrlData=0, NotChargingBecauseOvertemperature=1, NotChargingBecauseAccessControlWait=2, ChargingBecauseForceStateOn=3, NotChargingBecauseForceStateOff=4, NotChargingBecauseScheduler=5, NotChargingBecauseEnergyLimit=6, ChargingBecauseAwattarPriceLow=7, ChargingBecauseAutomaticStopTestLadung=8, ChargingBecauseAutomaticStopNotEnoughTime=9, ChargingBecauseAutomaticStop=10, ChargingBecauseAutomaticStopNoClock=11, ChargingBecausePvSurplus=12, ChargingBecauseFallbackGoEDefault=13, ChargingBecauseFallbackGoEScheduler=14, ChargingBecauseFallbackDefault=15, NotChargingBecauseFallbackGoEAwattar=16, NotChargingBecauseFallbackAwattar=17, NotChargingBecauseFallbackAutomaticStop=18, ChargingBecauseCarCompatibilityKeepAlive=19, ChargingBecauseChargePauseNotAllowed=20, NotChargingBecauseSimulateUnplugging=22, NotChargingBecausePhaseSwitch=23, NotChargingBecauseMinPauseDuration=24) | `15` |
| `mptwt`<br>`minPhaseToggleWaitTime` | Min Phase Toggle Wait Time | R/W | `integer`<br>`milliseconds` | Config | :white_large_square: | min phase toggle wait time (in milliseconds) | `600000` |
| `mpwst`<br>`minPhaseWishSwitchTime` | Min Phase Wish Switch Time | R/W | `integer`<br>`milliseconds` | Config | :white_large_square: | min phase wish switch time (in milliseconds) | `120000` |
| `msca`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `0` |
| `mscs`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `188` |
| `msi`<br>`modelStatusInternal` | Model Status Internal | R | `integer`<br>`uint8` | Status | :white_large_square: | Reason why we allow charging or not right now INTERNAL without cpDisabledRequest | `15` |
| `mws`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `true` |
| `nif`<br>`defaultRoute` | Default Route | R | `string`<br>`string` | Status | :white_large_square: | Default route | `"st"` |
| `nmo`<br>`norwayMode` | Norway Mode | R/W | `boolean`<br>`bool` | Config | :white_large_square: | norway_mode / ground check enabled when norway mode is disabled (inverted) | `false` |
| `nrg`<br>`energy` | Charging Energy | R | `array`<br>`array` | Status | :heavy_check_mark: | energy array, U (L1, L2, L3, N), I (L1, L2, L3), P (L1, L2, L3, N, Total), pf (L1, L2, L3, N) | `[235, 234, 234, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]` |
| `nvs`<br>- |  |  | `object`<br>- |  | :white_large_square: |  | `{"used_entries": 120, "free_entries": 7944, "total_entries": 8064, "namespace_count": 2, "nvs_handle_user": 52}` |
| `obm`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `null` |
| `oca`<br>`otaCloudApp` | OTA Cloud App | R | `object`<br>`optional<object>` | Status | :white_large_square: | ota cloud app description | `null` |
| `occa`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `2` |
| `ocl`<br>`otaCloudLength` | OTA Cloud Length | R | `integer`<br>`optional<int>` | Status | :white_large_square: | ota from cloud length (total size) | `null` |
| `ocm`<br>`otaCloudMessage` | OTA Cloud Message | R | `string`<br>`string` | Status | :white_large_square: | ota from cloud message | `""` |
| `ocp`<br>`otaCloudProgress` | OTA Cloud Progress | R | `integer`<br>`int` | Status | :white_large_square: | ota from cloud progress | `0` |
| `ocppc`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `false` |
| `ocppca`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `null` |
| `ocppe`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `false` |
| `ocpph`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `3600` |
| `ocppi`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `0` |
| `ocppl`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `1` |
| `ocpps`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `false` |
| `ocppu`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `"ws://echo.websocket.org/"` |
| `ocs`<br>`otaCloudStatus` | OTA Cloud Status | R | `integer`<br>`uint8` | Status | :heavy_check_mark: | ota from cloud status (Idle=0, Updating=1, Failed=2, Succeeded=3) | `0` |
| `ocu`<br>`otaCloudBranches` | OTA Cloud Branches | R | `array`<br>`array` | Status | :white_large_square: | list of available firmware branches | `["__default"]` |
| `ocuca`<br>`otaCloudUseClientAuth` | OTA Cloud Use Client Auth | R | `boolean`<br>`bool` | Config | :white_large_square: | ota cloud use client auth (if keys were setup correctly) | `true` |
| `oem`<br>`oemManufacturer` | OEM Manufacturer | R | `string`<br>`string` | Constant | :white_large_square: | OEM manufacturer | `"fronius"` |
| `onv`<br>`otaNewestVersion` | OTA Newest Version | R | `string`<br>`string` | Status | :white_large_square: | OverTheAirUpdate newest version | `36.3` |
| `otap`<br>`otaPartition` | OTA Partition | R | `object`<br>`optional<object>` | Constant | :white_large_square: | currently used OTA partition | `{"type": 0, "subtype": 16, "address": 1441792, "size": 4194304, "label": "app_0", "encrypted": true}` |
| `pakku`<br>`pAkku` | Power Akku | R | `float`<br>`optional<float>` | Status | :white_large_square: | pAkku in W |  |
| `part`<br>`partitionTable` | Partition Table | R | `array`<br>`array` | Constant | :white_large_square: | partition table | `[{"type": 1, "subtype": 2, "address": 65536, "size": 262144, "label": "nvs", "encrypted": false}, {"type": 1, "subtype": 1, "address": 327680, "size": 4096, "label": "phy_init", "encrypted": false}]` |
| `pgrid`<br>`pGrid` | Power Grid | R | `float`<br>`optional<float>` | Status | :white_large_square: | pGrid in W |  |
| `pha`<br>`phases` | Phases | R | `array`<br>`optional<array>` | Status | :white_large_square: | phases | `"[false, false, false, true, true, true]"` |
| `pnp`<br>`numberOfPhases` | Number of Phases | R | `integer`<br>`uint8` | Status | :white_large_square: | numberOfPhases | `0` |
| `po`<br>`prioOffset` | Prio Offset | R/W | `float`<br>`float` | Config | :white_large_square: | prioOffset in W | `-300` |
| `ppv`<br>`pPv` | Power PV | R | `float`<br>`optional<float>` | Status | :white_large_square: | pPv in W |  |
| `psh`<br>`phaseSwitchHysteresis` | Phase Switch Hysteresis | R/W | `float`<br>`float` | Config | :white_large_square: | phaseSwitchHysteresis in W | `500` |
| `psm`<br>`phaseSwitchMode` | Phase Switch Mode | R/W | `integer`<br>`uint8` | Config | :white_large_square: | phaseSwitchMode (Auto=0, Force_1=1, Force_3=2) | `0` |
| `psmd`<br>`forceSinglePhaseDuration` | Force Single Phase Duration | R/W | `integer`<br>`milliseconds` | Config | :white_large_square: | forceSinglePhaseDuration (in milliseconds) | `10000` |
| `pto`<br>`partitionTableOffset` | Partition Table Offset | R | `integer`<br>`uint32` | Constant | :white_large_square: | partition table offset in flash | `61440` |
| `pvopt_averagePAkku`<br>`averagePAkku` | Average Power Akku | R | `float`<br>`float` | Status | :heavy_check_mark: | averagePAkku | `-5213.455` |
| `pvopt_averagePGrid`<br>`averagePGrid` | Average Power Grid | R | `float`<br>`float` | Status | :heavy_check_mark: | averagePGrid | `1.923335` |
| `pvopt_averagePOhmpilot`<br>`avgPowerOhmpilot` | Average Power Ohmpilot | R | `integer`<br>- |  | :heavy_check_mark: |  | `0` |
| `pvopt_averagePPv`<br>`averagePPv` | Average Power PV | R | `float`<br>`float` | Status | :heavy_check_mark: | averagePPv | `6008.117` |
| `pvopt_deltaA`<br>`deltaCurrent` | Delta Current | R | `integer`<br>- |  | :heavy_check_mark: |  | `0` |
| `pvopt_deltaP`<br>`deltaPower` | Delta Power | R | `float`<br>- |  | :heavy_check_mark: |  | `-1256.149` |
| `pvopt_specialCase`<br>`pvOptSpecialCase` | PVOpt Special Case | R | `integer`<br>- |  | :white_large_square: |  | `0` |
| `pwm`<br>`phaseWishMode` | Phase Wish Mode | R | `integer`<br>`uint8` | Status | :heavy_check_mark: | phase wish mode for debugging / only for pv optimizing / used for timers later (Force_3=0, Wish_1=1, Wish_3=2) | `0` |
| `qsc`<br>`queueSizeCloud` | Queue Size Cloud | R | `integer`<br>`size_t` | Status | :white_large_square: | queue size cloud | `0` |
| `qsw`<br>`queueSizeWs` | Queue Size WS | R | `integer`<br>`size_t` | Status | :white_large_square: | queue size webserver/websocket | `5` |
| `rbc`<br>`rebootCounter` | Reboot Counter | R | `integer`<br>`uint32` | Status | :white_large_square: | Number of device reboots | `32` |
| `rbt`<br>`timeSinceBoot` | Time Since Boot | R | `integer`<br>`milliseconds` | Status | :white_large_square: | time since boot in milliseconds | `93641458` |
| `rcd`<br>`residualCurrentDetection` | Residual Current Detection | R | `integer`<br>`optional<microseconds>` | Status | :white_large_square: | residual current detection (in microseconds) WILL CHANGE IN FUTURE | `null` |
| `rcsl`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `false` |
| `rfb`<br>`relayFeedback` | Relay Feedback | R | `integer`<br>`int` | Status | :white_large_square: | Relay Feedback | `1699` |
| `rfide`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `true` |
| `rial`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `false` |
| `riml`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `false` |
| `risl`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `false` |
| `riul`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `false` |
| `rmdns`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `false` |
| `rr`<br>`espResetReason` | ESP Reset Reason | R | `integer`<br>`uint8` | Status | :white_large_square: | esp_reset_reason (UNKNOWN=0, POWERON=1, EXT=2, SW=3, PANIC=4, INT_WDT=5, TASK_WDT=6, WDT=7, DEEPSLEEP=8, BROWNOUT=9, SDIO=10) | `4` |
| `rrca`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `2` |
| `rssi`<br>`wifiRssi` | WIFI Signal Strength | R | `integer`<br>`optional<int8>` | Status | :heavy_check_mark: | RSSI signal strength | `-66` |
| `rst`<br>`rebootCharger` | Reboot Charger | W | `any`<br>`any` | Other | :white_large_square: | Reboot charger |  |
| `sau`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `false` |
| `sbe`<br>`secureBootEnabled` | Secure Boot Enabled | R | `boolean`<br>`bool` | Constant | :white_large_square: | Secure boot enabled | `true` |
| `scaa`<br>`wifiScanAge` | WiFi Scan Age | R | `integer`<br>`milliseconds` | Status | :white_large_square: | wifi scan age | `6429` |
| `scan`<br>`wifiScanResult` | Scanned WIFI Hotspots | R | `array`<br>`array` | Status | :white_large_square: | wifi scan result (encryptionType: OPEN=0, WEP=1, WPA_PSK=2, WPA2_PSK=3, WPA_WPA2_PSK=4, WPA2_ENTERPRISE=5, WPA3_PSK=6, WPA2_WPA3_PSK=7) | `[{"ssid": "<SOME_SSID>", "encryptionType": 3, "rssi": -65, "channel": 6, "bssid": "<SOME_BSSID>", "f": [4, 4, true, true, true, false, false, false, false, "DE"]}, {"ssid": "<SOME_SSID>", "encryptionType": 3, "rssi": -65, "channel": 6, "bssid": "<SOME_BSSID>", "f": [4, 4, true, true, true, false, false, false, false, "DE"]}]` |
| `scas`<br>`wifiScanStatus` | WIFI Scan Status | R | `integer`<br>`uint8` | Status | :heavy_check_mark: | wifi scan status (None=0, Scanning=1, Finished=2, Failed=3) | `2` |
| `sch_satur`<br>`schedulerSaturday` | Charging Schedule Saturday | R/W | `object`<br>`object` | Config | :white_large_square: | scheduler_saturday, control enum values: Disabled=0, Inside=1, Outside=2 | `{"control": 0, "ranges": [{"begin": {"hour": 0, "minute": 0}, "end": {"hour": 0, "minute": 0}}, {"begin": {"hour": 0, "minute": 0}, "end": {"hour": 0, "minute": 0}}]}` |
| `sch_sund`<br>`schedulerSunday` | Charging Schedule Sunday | R/W | `object`<br>`object` | Config | :white_large_square: | scheduler_sunday, control enum values: Disabled=0, Inside=1, Outside=2 | `{"control": 0, "ranges": [{"begin": {"hour": 0, "minute": 0}, "end": {"hour": 0, "minute": 0}}, {"begin": {"hour": 0, "minute": 0}, "end": {"hour": 0, "minute": 0}}]}` |
| `sch_week`<br>`schedulerWeekday` | Charging Schedule Weekday | R/W | `object`<br>`object` | Config | :white_large_square: | scheduler_weekday, control enum values: Disabled=0, Inside=1, Outside=2 | `{"control": 0, "ranges": [{"begin": {"hour": 0, "minute": 0}, "end": {"hour": 0, "minute": 0}}, {"begin": {"hour": 0, "minute": 0}, "end": {"hour": 0, "minute": 0}}]}` |
| `sdca`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `2` |
| `sh`<br>`stopHysteresis` | Stop Hysteresis | R/W | `float`<br>`float` | Config | :white_large_square: | stopHysteresis in W | `200` |
| `smca`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `2` |
| `smd`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `null` |
| `spl3`<br>`threePhaseSwitchLevel` | Three Phase Switch Level | R/W | `float`<br>`float` | Config | :white_large_square: | threePhaseSwitchLevel | `4200` |
| `sse`<br>`serialNumber` | Serial Number | R | `string`<br>`string` | Constant | :heavy_check_mark: | serial number | `"<some_serialnr>"` |
| `stao`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `null` |
| `su`<br>`simulateUnplugging` | Simulate Unplugging | R/W | `boolean`<br>`bool` | Config | :white_large_square: | simulateUnplugging or simulateUnpluggingShort? (see v2) | `false` |
| `sua`<br>`simulateUnpluggingAlways` | Simulate Unplugging Always | R/W | `boolean`<br>`bool` | Config | :white_large_square: | simulateUnpluggingAlways | `false` |
| `sumd`<br>`simulateUnpluggingDuration` | Simulate Unplugging Duration | R/W | `integer`<br>`milliseconds` | Config | :white_large_square: | simulate unpluging duration (in milliseconds) | `5000` |
| `swc`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `false` |
| `tds`<br>`timezoneDaylightSavingMode` | Timezone Daylight Saving Mode | R/W | `integer`<br>`uint8` | Config | :heavy_check_mark: | timezone daylight saving mode, None=0, EuropeanSummerTime=1, UsDaylightTime=2 | `1` |
| `tma`<br>`temperatureSensors` | Temperature Sensors | R | `array`<br>`array` | Status | :heavy_check_mark: | temperature sensors | `[11, 16.75]` |
| `tof`<br>`timezoneOffset` | Timezone Offset | R/W | `integer`<br>`minutes` | Config | :white_large_square: | timezone offset in minutes | `60` |
| `tou`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `0` |
| `tpa`<br>`totalPowerAverage` | Total Power Average | R | `float`<br>`float` | Status | :white_large_square: | 30 seconds total power average (used to get better next-trip predictions) | `0` |
| `tpck`<br>- |  |  | `array`<br>- |  | :white_large_square: |  | `["chargectrl", "i2c", "led", "wifi", "webserver", "mdns", "time", "cloud", "rfid", "temperature", "status", "froniusinverter", "button", "delta_http", "delta_cloud", "ota_cloud", "cmdhandler", "loadbalancing", "ocpp", "remotereq", "cloud_send"]` |
| `tpcm`<br>- |  |  | `array`<br>- |  | :white_large_square: |  | `[4, 0, 3, 1, 0, 0, 0, 0, 43, 2, 53, 0, 0, 0, 50, 0, 0, 0, 0, 0, 10]` |
| `trx`<br>`transaction` | Transaction | R/W | `integer`<br>`optional<uint8>` | Status | :white_large_square: | transaction, null when no transaction, 0 when without card, otherwise
cardIndex + 1 (1: 0. card, 2: 1. card, ...)
 | `null` |
| `ts`<br>`timeServer` | Time Server | R | `string`<br>`string` | Config | :white_large_square: | time server | `"europe.pool.ntp.org"` |
| `tse`<br>`timeServerEnabled` | Time Server Enabled | R/W | `boolean`<br>`bool` | Config | :heavy_check_mark: | time server enabled (NTP) | `false` |
| `tsom`<br>`timeServerOperatingMode` | Time Server Operating Mode | R | `integer`<br>`uint8` | Status | :white_large_square: | time server operating mode (POLL=0, LISTENONLY=1) | `0` |
| `tssi`<br>`timeServerSyncInterval` | Time Server Sync Interval | R | `integer`<br>`milliseconds` | Config | :white_large_square: | time server sync interval (in ms, 15s minimum) | `3600000` |
| `tssm`<br>`timeServerSyncMode` | Time Server Sync Mode | R | `integer`<br>`uint8` | Config | :white_large_square: | time server sync mode (IMMED=0, SMOOTH=1) | `0` |
| `tsss`<br>`timeServerSyncStatus` | Time Server Sync Status | R | `integer`<br>`uint8` | Config | :white_large_square: | time server sync status (RESET=0, COMPLETED=1, IN_PROGRESS=2) | `0` |
| `typ`<br>`deviceType` | Device Type | R | `string`<br>`string` | Constant | :white_large_square: | Devicetype | `"wattpilot"` |
| `uaca`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `2` |
| `upd`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `false` |
| `upo`<br>`unlockPowerOutage` | Unlock Power Outage | R/W | `boolean`<br>`bool` | Config | :white_large_square: | unlock_power_outage | `false` |
| `ust`<br>`cableLock` | Unlock Setting | R/W | `integer`<br>`uint8` | Config | :heavy_check_mark: | unlock_setting (Normal=0, AutoUnlock=1, AlwaysLock=2) | `0` |
| `utc`<br>`utcTime` | UTC Time | R/W | `string`<br>`string` | Status | :white_large_square: | utc time | `"2022-03-06T10:59:38.181.250"` |
| `var`<br>`variant` | Variant | R | `integer`<br>`uint8` | Constant | :heavy_check_mark: | variant: max Ampere value of unit (11: 11kW/16A, 22: 22kW/32A) | `11` |
| `waap`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `3` |
| `wae`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `true` |
| `wak`<br>`wifiApKey` | WiFi AP Key | R/W | `string`<br>`string` | Config | :white_large_square: | WiFi AccessPoint Key (read/write from http) | `false` |
| `wan`<br>`wifiApName` | WiFi AP Name | R/W | `string`<br>`string` | Config | :white_large_square: | wifiApName | `"Wattpilot_<some_serialnr>"` |
| `wapc`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `1` |
| `wcb`<br>`wifiCurrentMac` | WiFi Current MAC Address | R | `string`<br>`string` | Status | :white_large_square: | WiFi current mac address | `"<some_mac>"` |
| `wcch`<br>`httpConnectedClients` | HTTP Connected Clients | R | `integer`<br>`uint8` | Status | :white_large_square: | webserver connected clients as HTTP | `0` |
| `wccw`<br>`wsConnectedClients` | WS Connected Clients | R | `integer`<br>`uint8` | Status | :white_large_square: | webserver connected clients as WEBSOCKET | `2` |
| `wda`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `false` |
| `wen`<br>`wifiEnabled` | WiFi Enabled | R/W | `boolean`<br>`bool` | Config | :white_large_square: | wifiEnabled (bool), turns off/on the WiFi (not the AccessPoint) | `true` |
| `wfb`<br>`wifiFailedMac` | WiFi Failed MAC Address | R | `array`<br>`array` | Status | :white_large_square: | WiFi failed mac addresses | `null` |
| `wh`<br>`energyCounterSinceStart` | Energy Counter Since Start | R | `float`<br>`double` | Status | :heavy_check_mark: | energy in Wh since car connected | `2133.804` |
| `wifis`<br>`wifiConfigs` | WiFi Configs | R/W | `array`<br>`array` | Config | :white_large_square: | wifi configurations with ssids and keys, if you only want to change the second entry, send an array with 1 empty and 1 filled wifi config object: `[{}, {"ssid":"","key":""}]` | `[{"ssid": "<SOME_SSID>", "key": true, "useStaticIp": false, "staticIp": "0.0.0.0", "staticSubnet": "0.0.0.0", "staticGateway": "0.0.0.0", "useStaticDns": false, "staticDns0": "0.0.0.0", "staticDns1": "0.0.0.0", "staticDns2": "0.0.0.0"}, {"ssid": "", "key": false, "useStaticIp": false, "staticIp": "0.0.0.0", "staticSubnet": "0.0.0.0", "staticGateway": "0.0.0.0", "useStaticDns": false, "staticDns0": "0.0.0.0", "staticDns1": "0.0.0.0", "staticDns2": "0.0.0.0"}]` |
| `wpb`<br>`wifiPlannedMac` | WiFi Planned MAC | R | `array`<br>`array` | Status | :white_large_square: | WiFi planned mac addresses | `"<SOME_BSSID>"` |
| `wsc`<br>`wifiStaErrorCount` | WiFi STA Error Count | R | `integer`<br>`uint8` | Status | :white_large_square: | WiFi STA error count | `0` |
| `wsm`<br>`wifiStaErrorMessage` | Wifi STA Error Message | R | `string`<br>`string` | Status | :white_large_square: | WiFi STA error message | `""` |
| `wsmr`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `-90` |
| `wsms`<br>`wifiStateMachineState` | WIFI State Machine State | R | `integer`<br>`uint8` | Status | :heavy_check_mark: | WiFi state machine state (None=0, Scanning=1, Connecting=2, Connected=3) | `3` |
| `wss`<br>`wifiSsid` | WIFI SSID |  | `unknown`<br>- |  | :white_large_square: |  |  |
| `wst`<br>`wifiStaStatus` | WIFI STA Status | R | `integer`<br>`uint8` | Status | :heavy_check_mark: | WiFi STA status (IDLE_STATUS=0, NO_SSID_AVAIL=1, SCAN_COMPLETED=2, CONNECTED=3, CONNECT_FAILED=4, CONNECTION_LOST=5, DISCONNECTED=6, CONNECTING=8, DISCONNECTING=9, NO_SHIELD=10 (for compatibility with WiFi Shield library)) | `3` |
| `zfo`<br>`zeroFeedinOffset` | Zero Feedin Offset | R/W | `float`<br>`float` | Config | :white_large_square: | zeroFeedinOffset in W | `200` |
