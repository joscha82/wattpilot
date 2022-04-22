# Wattpilot API Description

## WebSocket Message Types

| Key | Title | Description | Example |
|-----|-------|-------------|---------|
| `hello` | Hello Message | Received upon connection before authentication |  |
| `authRequired` | Auth Required | Received after hello to ask for authentication |  |
| `response` | Update Response Message | Received after sending an update and contains the result of the update |  |
| `authSuccess` | Auth Success | Received after sending a correct authentication message |  |
| `authError` | Auth Error | Received after sending an incorrect authentication message (e.g. wrong password) |  |
| `fullStatus` | Full Status | Set of messages received after successful connection. These messages contain all properties of Wattpilot. |  |
| `deltaStatus` | Delta Status | Whenever a property changes a Delta Status is sent |  |
| `clearInverters` | Clear Inverters | Unknown |  |
| `updateInverter` | Update Inverter | Contains information of connected PV inverter / power meter |  |

## Wattpilot Properties

| Key/Alias | Title | R/W | JSON/API Type | Category | HA Enabled | Description | Example |
|-----------|-------|-----|---------------|----------|------------|-------------|---------|
| `abm`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `<SOME_MAC>` |
| `acs`<br>`accessState` | Access State | R/W | `integer`<br>`uint8` | Config | :heavy_check_mark: | access_control user setting (Open=0, Wait=1) | `0` |
| `acu`<br>- |  | R | `integer`<br>`int` | Status | :white_large_square: | How many ampere is the car allowed to charge now? | `6` |
| `acui`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `6` |
| `adi`<br>- |  | R | `boolean`<br>`bool` | Status | :white_large_square: | Is the 16A adapter used? Limits the current to 16A | `True` |
| `al1`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `6` |
| `al2`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `10` |
| `al3`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `12` |
| `al4`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `14` |
| `al5`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `16` |
| `alw`<br>`allowCharging` |  | R | `boolean`<br>`bool` | Status | :white_large_square: | Is the car allowed to charge at all now? | `True` |
| `ama`<br>`maxCurrentLimit` |  | R/W | `integer`<br>`uint8` | Config | :white_large_square: | ampere_max limit | `16` |
| `amp`<br>`chargingCurrent` | Charging Current | R/W | `integer`<br>`uint8` | Config | :heavy_check_mark: | requestedCurrent in Ampere, used for display on LED ring and logic calculations | `6` |
| `amt`<br>`temperatureCurrentLimit` |  | R | `integer`<br>`int` | Status | :white_large_square: | temperatureCurrentLimit | `32` |
| `apd`<br>- |  | R | `object`<br>`object` | Constant | :white_large_square: | firmware description | `{'project_name': 'wattpilot_hw4+', 'version': '36.3', 'secure_version': 0, 'timestamp': 'Jan 31 2022 22:51:39', 'idf_ver': 'v5.0-dev-1103-ga9ef558d', 'sha256': '<some_sha256>'}` |
| `arv`<br>`appRecommendedVersion` |  | R | `string`<br>`string` | Constant | :white_large_square: | app recommended version (used to show in the app that the app is outdated) | `1.2.1` |
| `asc`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `True` |
| `aup`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `6` |
| `awc`<br>`awattarCountry` | Awattar Country | R/W | `integer`<br>`uint8` | Config | :heavy_check_mark: | awattar country (Austria=0, Germany=1) | `0` |
| `awcp`<br>`awattarCurrentPrice` | Awattar Current Price? | R | `object`<br>`optional<object>` | Status | :white_large_square: | awattar current price | `{'start': 1650567600, 'end': 1650571200, 'marketprice': 22.044}` |
| `awp`<br>`awattarMaxPrice` |  | R/W | `integer`<br>`float` | Config | :heavy_check_mark: | awattarMaxPrice in ct | `3` |
| `awpl`<br>`awattarPriceList` | Awattar Price List | R/W | `array`<br>`array` | Status | :white_large_square: | awattar price list, timestamps are measured in unix-time, seconds since 1970 | `[{'start': 1650567600, 'end': 1650571200, 'marketprice': 22.044}, {'start': 1650571200, 'end': 1650574800, 'marketprice': 19.971}]` |
| `bac`<br>`buttonAllowCurrentChange` |  | R/W | `boolean`<br>`bool` | Config | :white_large_square: | Button allow Current change | `True` |
| `bam`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `True` |
| `cae`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `False` |
| `cak`<br>- |  |  | `string`<br>- |  | :white_large_square: |  |  |
| `car`<br>`carState` | Car State | R | `integer`<br>`optional<uint8>` | Status | :heavy_check_mark: | carState, null if internal error (Unknown/Error=0, Idle=1, Charging=2, WaitCar=3, Complete=4, Error=5) | `1` |
| `cards`<br>`registeredCards` | RFID Card List |  | `array`<br>- |  | :white_large_square: | Registered RFID cards for different users | `[{'name': 'User 1', 'energy': 0, 'cardId': True}, {'name': 'User 2', 'energy': 0, 'cardId': False}]` |
| `cbl`<br>`cableCurrentLimit` | Cable Current Limit | R | `integer`<br>`optional<int>` | Status | :heavy_check_mark: | cable_current_limit in A | `20` |
| `cbm`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `None` |
| `cca`<br>`cloudClientAuth` |  | R | `boolean`<br>`bool` | Config | :white_large_square: | cloud websocket use client auth (if key&cert are setup correctly) | `True` |
| `cch`<br>`colorCharging` |  | R/W | `string`<br>`string` | Config | :white_large_square: | color_charging, format: #RRGGBB | `#00FFF` |
| `cci`<br>- |  |  | `object`<br>- |  | :white_large_square: |  | `{'id': '<some_numeric_id>', 'paired': True, 'deviceFamily': 'DataManager', 'label': '<some_name>', 'model': 'PILOT', 'commonName': 'pilot-0.5e-1670626369628648631_1599713577', 'ip': '<some_ip>', 'connected': True, 'reachableMdns': True, 'reachableUdp': True, 'reachableHttp': True, 'status': 0, 'message': 'ok'}` |
| `cco`<br>`carConsumption` | Car Consumption | R/W | `float`<br>`double` | Config | :heavy_check_mark: | car consumption in kWh for 100km (only stored for app) | `24` |
| `ccu`<br>`chargeControllerUpdateProgress` |  | R | `unknown`<br>`optional<object>` | Status | :white_large_square: | charge controller update progress (null if no update is in progress) | `None` |
| `ccw`<br>`currentlyConnectedWifi` |  | R | `object`<br>`optional<object>` | Status | :white_large_square: | Currently connected WiFi | `{'ssid': '<SOME_SSID>', 'encryptionType': 3, 'pairwiseCipher': 4, 'groupCipher': 4, 'b': True, 'g': True, 'n': True, 'lr': False, 'wps': False, 'ftmResponder': False, 'ftmInitiator': False, 'channel': 6, 'bssid': '<SOME_BSSID>', 'ip': '<some_ip4>', 'netmask': '255.255.255.0', 'gw': '<some_ip4>', 'ipv6': ['<some_ip6>', '<some_ip6>'], 'dns0': '<some_ip4>', 'dns1': '0.0.0.0', 'dns2': '0.0.0.0'}` |
| `cdi`<br>`chargingDurationInfo` | Charging Duration Info | R | `object`<br>`object` | Status | :heavy_check_mark: | charging duration info (null=no charging in progress, type=0 counter going up, type=1 duration in ms) | `{'type': 1, 'value': 11554770}` |
| `cdv`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `None` |
| `cfi`<br>`colorFinished` |  | R/W | `string`<br>`string` | Config | :white_large_square: | color_finished, format: #RRGGBB | `#00FF00` |
| `chr`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `True` |
| `cid`<br>`colorIdle` |  | R/W | `string`<br>`string` | Config | :white_large_square: | color_idle, format: #RRGGBB | `#0000FF` |
| `clp`<br>`currentLimitPresets` | Charging Current Options | R/W | `array`<br>`array` | Config | :white_large_square: | current limit presets, max. 5 entries | `[6, 10, 12, 14, 16]` |
| `cpe`<br>- |  | R | `boolean`<br>`bool` | Status | :white_large_square: | The charge ctrl requests the CP signal enabled or not immediately | `True` |
| `cpr`<br>`cpEnableRequest` |  | R | `boolean`<br>`bool` | Status | :white_large_square: | CP enable request. cpd=0 triggers the charge ctrl to set cpe=0 once processed | `True` |
| `csca`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `2` |
| `ct`<br>`carType` |  | R/W | `string`<br>`string` | Config | :white_large_square: | car type, free text string (max. 64 characters, only stored for app) | `vwID3_4` |
| `cus`<br>`cableUnlockStatus` | Cable Unlock Status | R | `integer`<br>`uint8` | Status | :heavy_check_mark: | Cable unlock status (Unknown=0, Unlocked=1, UnlockFailed=2, Locked=3, LockFailed=4, LockUnlockPowerout=5) | `1` |
| `cwc`<br>`colorWaitCar` |  | R/W | `string`<br>`string` | Config | :white_large_square: | color_waitcar, format: #RRGGBB | `#FFFF00` |
| `cwe`<br>`cloudWsEnabled` |  | R/W | `boolean`<br>`bool` | Config | :white_large_square: | cloud websocket enabled | `True` |
| `cws`<br>`cloudWsStarted` |  | R | `boolean`<br>`bool` | Status | :white_large_square: | cloud websocket started | `True` |
| `cwsc`<br>`cloudWsConnected` |  | R | `boolean`<br>`bool` | Status | :white_large_square: | cloud websocket connected | `True` |
| `cwsca`<br>`cloudWsConnectedAge` |  | R | `integer`<br>`optional<milliseconds>` | Status | :white_large_square: | cloud websocket connected (age) | `46954034` |
| `data`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `{"i":120,"url":"https://data.wattpilot.io/data?e=<some_token>"}` |
| `dbm`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `<SOME_MAC_ADDRESS>` |
| `dccu`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `False` |
| `dco`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `True` |
| `dll`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `https://data.wattpilot.io/export?e=<some_token>` |
| `dns`<br>- |  |  | `object`<br>- |  | :white_large_square: |  | `{'dns': '0.0.0.0'}` |
| `dwo`<br>- |  | R/W | `unknown`<br>`optional<double>` | Config | :white_large_square: | charging energy limit, measured in Wh, null means disabled, not the next trip energy | `None` |
| `ecf`<br>`espCpuFreq` |  | R | `object`<br>`object` | Constant | :white_large_square: | ESP CPU freq (source: XTAL=0, PLL=1, 8M=2, APLL=3) | `{'source': 1, 'source_freq_mhz': 320, 'div': 2, 'freq_mhz': 160}` |
| `eci`<br>`espChipInfo` |  | R | `object`<br>`object` | Constant | :white_large_square: | ESP chip info (model: ESP32=1, ESP32S2=2, ESP32S3=4, ESP32C3=5; features: EMB_FLASH=bit0, WIFI_BGN=bit1, BLE=bit4, BT=bit5) | `{'model': 1, 'features': 50, 'cores': 2, 'revision': 3}` |
| `efh`<br>`espFreeHeap` |  | R | `integer`<br>`size_t` | Status | :white_large_square: | ESP free heap | `125920` |
| `efh32`<br>`espFreeHeap32` |  | R | `integer`<br>`size_t` | Status | :white_large_square: | ESP free heap 32bit aligned | `125920` |
| `efh8`<br>`espFreeHeap8` |  | R | `integer`<br>`size_t` | Status | :white_large_square: | ESP free heap 8bit aligned | `86848` |
| `efi`<br>`espFlashInfo` |  | R | `unknown`<br>`object` | Constant | :white_large_square: | ESP Flash info (spi_mode: QIO=0, QOUT=1, DIO=2, DOUT=3, FAST_READ=4, SLOW_READ=5; spi_speed: 40M=0, 26M=1, 20M=2, 80M=15; spi_size: 1MB=0, 2MB=1, 4MB=2, 8MB=3, 16MB=4, MAX=5) | `None` |
| `ehs`<br>`espHeapSize` |  | R | `integer`<br>`size_t` | Status | :white_large_square: | ESP heap size | `282800` |
| `emfh`<br>`espMinFreeHeap` |  | R | `integer`<br>`size_t` | Status | :white_large_square: | ESP minimum free heap since boot | `78104` |
| `emhb`<br>`espMaxHeap` |  | R | `integer`<br>`size_t` | Status | :white_large_square: | ESP max size of allocated heap block since boot | `67572` |
| `ens`<br>- |  |  | `string`<br>- |  | :white_large_square: |  |  |
| `err`<br>`errorState` | Error State | R | `integer`<br>`optional<uint8>` | Status | :heavy_check_mark: | error, null if internal error (Unknown/Error=0, Idle=1, Charging=2, WaitCar=3, Complete=4, Error=5) | `0` |
| `esk`<br>`energySetKwh` |  | R/W | `boolean`<br>`bool` | Config | :white_large_square: | energy set kwh (only stored for app) | `True` |
| `esr`<br>`rtcResetReasons` | RTC Reset Reasons | R | `array`<br>`array` | Status | :white_large_square: | rtc_get_reset_reason for core 0 and 1 (NO_MEAN=0, POWERON_RESET=1, SW_RESET=3, OWDT_RESET=4, DEEPSLEEP_RESET=5, SDIO_RESET=6, TG0WDT_SYS_RESET=7, TG1WDT_SYS_RESET=8, RTCWDT_SYS_RESET=9, INTRUSION_RESET=10, TGWDT_CPU_RESET=11, SW_CPU_RESET=12, RTCWDT_CPU_RESET=13, EXT_CPU_RESET=14, RTCWDT_BROWN_OUT_RESET=15, RTCWDT_RTC_RESET=16) | `[12, 12]` |
| `eto`<br>`energyCounterTotal` | Energy Counter Total | R | `integer`<br>`uint64` | Status | :heavy_check_mark: | energy_total, measured in Wh | `1076098` |
| `etop`<br>`energyTotalPersisted` | Energy Total Persisted | R | `integer`<br>`uint64` | Status | :heavy_check_mark: | energy_total persisted, measured in Wh, without the extra magic to have live values | `1076098` |
| `facwak`<br>`factoryWifiApKey` |  | R | `boolean`<br>`string` | Constant | :white_large_square: | WiFi AccessPoint Key RESET VALUE (factory) | `True` |
| `fam`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `20` |
| `fap`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `False` |
| `fbuf_age`<br>- | FBuf Age |  | `integer`<br>- |  | :white_large_square: |  | `93639347` |
| `fbuf_akkuMode`<br>- | Fronius Akku Mode |  | `integer`<br>- |  | :white_large_square: |  | `1` |
| `fbuf_akkuSOC`<br>- | Fronius Battery SoC |  | `float`<br>- |  | :heavy_check_mark: | State of charge of the PV battery | `72.5` |
| `fbuf_ohmpilotState`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `None` |
| `fbuf_ohmpilotTemperature`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `None` |
| `fbuf_pAcTotal`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `None` |
| `fbuf_pAkku`<br>- | Fronius Akku Power |  | `float`<br>- |  | :heavy_check_mark: | Power that is consumed from the PV battery (or delivered into the battery, if negative) | `-3985.899` |
| `fbuf_pGrid`<br>- | Fronius Grid Power |  | `integer`<br>- |  | :heavy_check_mark: | Power consumed from grid (or delivered to grid, if negative) | `11` |
| `fbuf_pPv`<br>- | Fronius PV Power |  | `float`<br>- |  | :heavy_check_mark: | PV power that is produced | `4701.407` |
| `fcc`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `True` |
| `fck`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `True` |
| `fem`<br>`flashEncryptionMode` | Flash Encryption Mode | R | `integer`<br>`uint8` | Constant | :white_large_square: | Flash Encryption Mode (Disabled=0, Development=1, Release=2) | `2` |
| `ferm`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `1` |
| `ffb`<br>`lockFeedback` | Lock Feedback | R | `integer`<br>`uint8` | Status | :heavy_check_mark: | lock feedback (NoProblem=0, ProblemLock=1, ProblemUnlock=2) | `0` |
| `ffba`<br>`lockFeedbackAge` |  | R | `unknown`<br>`optional<milliseconds>` | Status | :white_large_square: | lock feedback (age) | `None` |
| `ffna`<br>`factoryFriendlyName` |  | R | `string`<br>`string` | Constant | :white_large_square: | factoryFriendlyName | `Wattpilot_<some_serialnr>` |
| `fhi`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `True` |
| `fhz`<br>`frequency` | Frequency | R | `float`<br>`optional<float>` | Status | :heavy_check_mark: | Power grid frequency (~50Hz) or 0 if unknown | `49.815` |
| `fi23`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `True` |
| `fio23`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `True` |
| `fit`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `1` |
| `fml`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `grid` |
| `fmmp`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `0` |
| `fmt`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `900000` |
| `fna`<br>`friendlyName` |  | R/W | `string`<br>`string` | Config | :white_large_square: | friendlyName | `<some_name>` |
| `fntp`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `None` |
| `fot`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `20` |
| `frc`<br>`forceState` | Force State | R/W | `integer`<br>`uint8` | Config | :heavy_check_mark: | forceState (Neutral=0, Off=1, On=2) | `0` |
| `frci`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `True` |
| `fre`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `False` |
| `frm`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `1` |
| `fsp`<br>`forceSinglePhase` |  | R | `boolean`<br>`bool` | Status | :white_large_square: | force_single_phase (shows if currently single phase charge is enforced | `False` |
| `fsptws`<br>`forceSinglePhaseToggleWishedSince` |  | R | `integer`<br>`optional<milliseconds>` | Status | :white_large_square: | force single phase toggle wished since | `28771782` |
| `fst`<br>- | Start-up Power Level | R/W | `integer`<br>- |  | :heavy_check_mark: | This power level must be reached by the photovoltaic system before the Wattpilot starts charging the car with the minimum current. | `1400` |
| `fte`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `50000` |
| `ftlf`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `False` |
| `ftls`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `None` |
| `ftt`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `25200` |
| `ful`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `False` |
| `fup`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `True` |
| `fwan`<br>`factoryWifiApName` |  | R | `string`<br>`string` | Constant | :white_large_square: | factoryWifiApName | `Wattpilot_<some_serialnr>` |
| `fwc`<br>`firmwareCarControl` |  | R | `integer`<br>`string` | Constant | :white_large_square: | firmware from CarControl | `10` |
| `fwv`<br>`firmwareVersion` | Firmware Version | R | `string`<br>`string` | Constant | :heavy_check_mark: | Version of the Wattpilot firmware | `36.3` |
| `fzf`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `False` |
| `gme`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `False` |
| `gmk`<br>- |  |  | `string`<br>- |  | :white_large_square: |  |  |
| `host`<br>`hostname` |  | R | `string`<br>`optional<string>` | Status | :white_large_square: | hostname used on STA interface | `Wattpilot_<some_serialnr>` |
| `hsa`<br>`httpStaAuthentication` |  | R/W | `boolean`<br>`bool` | Config | :white_large_square: | httpStaAuthentication | `True` |
| `hsta`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `Wattpilot_<some_serialnr>` |
| `hsts`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `Wattpilot_<some_serialnr>` |
| `hws`<br>`httpStaReachable` |  | R/W | `boolean`<br>`bool` | Config | :white_large_square: | httpStaReachable, defines if the local webserver should be reachable from the customers WiFi | `True` |
| `ido`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `None` |
| `imd`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `False` |
| `imi`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `0` |
| `immr`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `20` |
| `imp`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `_tcp` |
| `ims`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `_Fronius-SE-Inverter` |
| `imse`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `True` |
| `irs`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `False` |
| `isml`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `False` |
| `iuse`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `True` |
| `las`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `0` |
| `lbh`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `None` |
| `lbp`<br>`lastButtonPress` |  | R | `unknown`<br>`milliseconds` | Status | :white_large_square: | lastButtonPress in milliseconds | `None` |
| `lbr`<br>`ledBrightness` |  | R | `integer`<br>`uint8` | Config | :white_large_square: | led_bright, 0-255 | `255` |
| `lbs`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `806` |
| `lccfc`<br>`lastCarStateChangedFromCharging` |  | R | `integer`<br>`optional<milliseconds>` | Status | :white_large_square: | lastCarStateChangedFromCharging (in ms) | `7157569` |
| `lccfi`<br>`lastCarStateChangedFromIdle` |  | R | `integer`<br>`optional<milliseconds>` | Status | :white_large_square: | lastCarStateChangedFromIdle (in ms) | `5369660` |
| `lcctc`<br>`lastCarStateChangedToCharging` |  | R | `integer`<br>`optional<milliseconds>` | Status | :white_large_square: | lastCarStateChangedToCharging (in ms) | `5369660` |
| `lch`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `5369660` |
| `lck`<br>`effectiveLockSetting` | Effective Lock Setting | R | `integer`<br>`uint8` | Status | :heavy_check_mark: | Effective lock setting, as sent to Charge Ctrl (Normal=0, AutoUnlock=1, AlwaysLock=2, ForceUnlock=3) | `0` |
| `led`<br>`ledInfo` |  | R | `object`<br>`object` | Status | :white_large_square: | internal infos about currently running led animation | `{'id': 5, 'name': 'Finished', 'norwayOverlay': True, 'modeOverlay': True, 'subtype': 'renderCmds', 'ranges': [{'from': 0, 'to': 31, 'colors': ['#00FF00']}]}` |
| `ledo`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `None` |
| `lfspt`<br>`lastForceSinglePhaseToggle` |  | R | `unknown`<br>`optional<milliseconds>` | Status | :white_large_square: | last force single phase toggle | `None` |
| `llr`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `2` |
| `lmo`<br>`logicMode` | Logic Mode | R/W | `integer`<br>`uint8` | Config | :heavy_check_mark: | logic mode (Default=3, Awattar=4, AutomaticStop=5) | `3` |
| `lmsc`<br>`lastModelStatusChange` |  | R | `integer`<br>`milliseconds` | Status | :white_large_square: | last model status change | `28822622` |
| `loa`<br>`loadBalancingAmpere` |  | R | `unknown`<br>`optional<uint8>` | Status | :white_large_square: | load balancing ampere | `None` |
| `loc`<br>`localTime` |  | R | `string`<br>`string` | Status | :white_large_square: | local time | `2022-03-06T11:59:38.182.123 +01:00` |
| `loe`<br>`loadBalancingEnabled` |  | R/W | `boolean`<br>`bool` | Config | :white_large_square: | Load balancing enabled | `False` |
| `lof`<br>`loadFallback` |  | R/W | `integer`<br>`uint8` | Config | :white_large_square: | load_fallback | `0` |
| `log`<br>`loadGroupId` |  | R/W | `string`<br>`string` | Config | :white_large_square: | load_group_id |  |
| `loi`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `False` |
| `lom`<br>`loadBalancingMembers` |  | R | `unknown`<br>`array` | Status | :white_large_square: | load balancing members | `None` |
| `lop`<br>`loadPriority` |  | R/W | `integer`<br>`uint16` | Config | :white_large_square: | load_priority | `50` |
| `los`<br>`loadBalancingStatus` |  | R | `unknown`<br>`optional<string>` | Status | :white_large_square: | load balancing status | `None` |
| `lot`<br>`loadBalancingTotalAmpere` |  | R/W | `integer`<br>`uint32` | Config | :white_large_square: | load balancing total amp | `32` |
| `loty`<br>`loadBalancingType` | Load Balancing Type | R/W | `integer`<br>`uint8` | Config | :heavy_check_mark: | load balancing type (Static=0, Dynamic=1) | `0` |
| `lps`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `63` |
| `lpsc`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `28771782` |
| `lrc`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `None` |
| `lri`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `None` |
| `lrr`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `None` |
| `lse`<br>`ledSaveEnergy` |  | R/W | `boolean`<br>`bool` | Config | :white_large_square: | led_save_energy | `False` |
| `lssfc`<br>`lastStaSwitchedFromConnected` |  | R | `unknown`<br>`optional<milliseconds>` | Status | :white_large_square: | lastStaSwitchedFromConnected (in milliseconds) | `None` |
| `lsstc`<br>`lastStaSwitchedToConnected` |  | R | `integer`<br>`optional<milliseconds>` | Status | :white_large_square: | lastStaSwitchedToConnected (in milliseconds) | `7970` |
| `maca`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `<some_mac>` |
| `macs`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `<some_mac>` |
| `map`<br>`loadMapping` |  | R/W | `array`<br>`array` | Config | :white_large_square: | load_mapping (uint8_t[3]) | `[1, 2, 3]` |
| `mca`<br>`minChargingCurrent` |  | R/W | `integer`<br>`uint8` | Config | :white_large_square: | minChargingCurrent | `6` |
| `mci`<br>`minimumChargingInterval` |  | R/W | `integer`<br>`milliseconds` | Config | :white_large_square: | minimumChargingInterval in milliseconds (0 means disabled) | `0` |
| `mcpd`<br>`minChargePauseDuration` |  | R/W | `integer`<br>`milliseconds` | Config | :white_large_square: | minChargePauseDuration in milliseconds (0 means disabled) | `0` |
| `mcpea`<br>`minChargePauseEndsAt` |  | R/W | `unknown`<br>`optional<milliseconds>` | Status | :white_large_square: | minChargePauseEndsAt (set to null to abort current minChargePauseDuration) | `None` |
| `mod`<br>`moduleHwPcbVersion` |  | R | `integer`<br>`uint8` | Constant | :white_large_square: | Module hardware pcb version (0, 1, ...) | `1` |
| `modelStatus`<br>`modelStatus` | Model Status | R | `integer`<br>`uint8` | Status | :heavy_check_mark: | Reason why we allow charging or not right now (NotChargingBecauseNoChargeCtrlData=0, NotChargingBecauseOvertemperature=1, NotChargingBecauseAccessControlWait=2, ChargingBecauseForceStateOn=3, NotChargingBecauseForceStateOff=4, NotChargingBecauseScheduler=5, NotChargingBecauseEnergyLimit=6, ChargingBecauseAwattarPriceLow=7, ChargingBecauseAutomaticStopTestLadung=8, ChargingBecauseAutomaticStopNotEnoughTime=9, ChargingBecauseAutomaticStop=10, ChargingBecauseAutomaticStopNoClock=11, ChargingBecausePvSurplus=12, ChargingBecauseFallbackGoEDefault=13, ChargingBecauseFallbackGoEScheduler=14, ChargingBecauseFallbackDefault=15, NotChargingBecauseFallbackGoEAwattar=16, NotChargingBecauseFallbackAwattar=17, NotChargingBecauseFallbackAutomaticStop=18, ChargingBecauseCarCompatibilityKeepAlive=19, ChargingBecauseChargePauseNotAllowed=20, NotChargingBecauseSimulateUnplugging=22, NotChargingBecausePhaseSwitch=23, NotChargingBecauseMinPauseDuration=24) | `15` |
| `mptwt`<br>`minPhaseToggleWaitTime` |  | R/W | `integer`<br>`milliseconds` | Config | :white_large_square: | min phase toggle wait time (in milliseconds) | `600000` |
| `mpwst`<br>`minPhaseWishSwitchTime` |  | R/W | `integer`<br>`milliseconds` | Config | :white_large_square: | min phase wish switch time (in milliseconds) | `120000` |
| `msca`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `0` |
| `mscs`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `188` |
| `msi`<br>- |  | R | `integer`<br>`uint8` | Status | :white_large_square: | Reason why we allow charging or not right now INTERNAL without cpDisabledRequest | `15` |
| `mws`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `True` |
| `nif`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `st` |
| `nmo`<br>`norwayMode` |  | R/W | `boolean`<br>`bool` | Config | :white_large_square: | norway_mode / ground check enabled when norway mode is disabled (inverted) | `False` |
| `nrg`<br>`energy` | Charging Energy | R | `array`<br>`array` | Status | :heavy_check_mark: | energy array, U (L1, L2, L3, N), I (L1, L2, L3), P (L1, L2, L3, N, Total), pf (L1, L2, L3, N) | `[235, 234, 234, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]` |
| `nvs`<br>- |  |  | `object`<br>- |  | :white_large_square: |  | `{'used_entries': 120, 'free_entries': 7944, 'total_entries': 8064, 'namespace_count': 2, 'nvs_handle_user': 52}` |
| `obm`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `None` |
| `oca`<br>`otaCloudApp` |  | R | `unknown`<br>`optional<object>` | Status | :white_large_square: | ota cloud app description | `None` |
| `occa`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `2` |
| `ocl`<br>`otaCloudLength` |  | R | `unknown`<br>`optional<int>` | Status | :white_large_square: | ota from cloud length (total size) | `None` |
| `ocm`<br>`otaCloudMessage` |  | R | `string`<br>`string` | Status | :white_large_square: | ota from cloud message |  |
| `ocp`<br>`otaCloudProgress` |  | R | `integer`<br>`int` | Status | :white_large_square: | ota from cloud progress | `0` |
| `ocppc`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `False` |
| `ocppca`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `None` |
| `ocppe`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `False` |
| `ocpph`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `3600` |
| `ocppi`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `0` |
| `ocppl`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `1` |
| `ocpps`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `False` |
| `ocppu`<br>- |  |  | `string`<br>- |  | :white_large_square: |  | `ws://echo.websocket.org/` |
| `ocs`<br>`otaCloudStatus` | OTA Cloud Status | R | `integer`<br>`uint8` | Status | :heavy_check_mark: | ota from cloud status (Idle=0, Updating=1, Failed=2, Succeeded=3) | `0` |
| `ocu`<br>`otaCloudBranches` |  | R | `array`<br>`array` | Status | :white_large_square: | list of available firmware branches | `['__default']` |
| `ocuca`<br>`otaCloudUseClientAuth` |  | R | `boolean`<br>`bool` | Config | :white_large_square: | ota cloud use client auth (if keys were setup correctly) | `True` |
| `oem`<br>`oemManufacturer` |  | R | `string`<br>`string` | Constant | :white_large_square: | OEM manufacturer | `fronius` |
| `onv`<br>`otaNewestVersion` |  | R | `string`<br>`string` | Status | :white_large_square: | OverTheAirUpdate newest version | `36.3` |
| `otap`<br>`otaPartition` |  | R | `object`<br>`optional<object>` | Constant | :white_large_square: | currently used OTA partition | `{'type': 0, 'subtype': 16, 'address': 1441792, 'size': 4194304, 'label': 'app_0', 'encrypted': True}` |
| `part`<br>`partitionTable` |  | R | `array`<br>`array` | Constant | :white_large_square: | partition table | `[{'type': 1, 'subtype': 2, 'address': 65536, 'size': 262144, 'label': 'nvs', 'encrypted': False}, {'type': 1, 'subtype': 1, 'address': 327680, 'size': 4096, 'label': 'phy_init', 'encrypted': False}]` |
| `pha`<br>`phases` |  | R | `array`<br>`optional<array>` | Status | :white_large_square: | phases | `[false, false, false, true, true, true]` |
| `pnp`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `0` |
| `po`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `-300` |
| `psh`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `500` |
| `psm`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `0` |
| `psmd`<br>`forceSinglePhaseDuration` |  | R/W | `integer`<br>`milliseconds` | Config | :white_large_square: | forceSinglePhaseDuration (in milliseconds) | `10000` |
| `pto`<br>`partitionTableOffset` |  | R | `integer`<br>`uint32` | Constant | :white_large_square: | partition table offset in flash | `61440` |
| `pvopt_averagePAkku`<br>- | Avg Akku Power | R | `float`<br>- |  | :heavy_check_mark: |  | `-5213.455` |
| `pvopt_averagePGrid`<br>- | Avg Grid Power | R | `float`<br>- |  | :heavy_check_mark: |  | `1.923335` |
| `pvopt_averagePOhmpilot`<br>- | Avg Ohmpilot Power | R | `integer`<br>- |  | :heavy_check_mark: |  | `0` |
| `pvopt_averagePPv`<br>- | Avg PV Power | R | `float`<br>- |  | :heavy_check_mark: |  | `6008.117` |
| `pvopt_deltaA`<br>- | Delta Current | R | `integer`<br>- |  | :heavy_check_mark: |  | `0` |
| `pvopt_deltaP`<br>- | Delta Power | R | `float`<br>- |  | :heavy_check_mark: |  | `-1256.149` |
| `pvopt_specialCase`<br>- |  | R | `integer`<br>- |  | :white_large_square: |  | `0` |
| `pwm`<br>`phaseWishMode` | Phase Wish Mode | R | `integer`<br>`uint8` | Status | :heavy_check_mark: | phase wish mode for debugging / only for pv optimizing / used for timers later (Force_3=0, Wish_1=1, Wish_3=2) | `0` |
| `qsc`<br>`queueSizeCloud` |  | R | `integer`<br>`size_t` | Status | :white_large_square: | queue size cloud | `0` |
| `qsw`<br>`queueSizeWs` |  | R | `integer`<br>`size_t` | Status | :white_large_square: | queue size webserver/websocket | `5` |
| `rbc`<br>`rebootCounter` | Reboot Counter | R | `integer`<br>`uint32` | Status | :white_large_square: | Number of device reboots | `32` |
| `rbt`<br>`timeSinceBoot` |  | R | `integer`<br>`milliseconds` | Status | :white_large_square: | time since boot in milliseconds | `93641458` |
| `rcd`<br>`residualCurrentDetection` |  | R | `unknown`<br>`optional<microseconds>` | Status | :white_large_square: | residual current detection (in microseconds) WILL CHANGE IN FUTURE | `None` |
| `rcsl`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `False` |
| `rfb`<br>`relayFeedback` |  | R | `integer`<br>`int` | Status | :white_large_square: | Relay Feedback | `1699` |
| `rfide`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `True` |
| `rial`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `False` |
| `riml`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `False` |
| `risl`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `False` |
| `riul`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `False` |
| `rmdns`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `False` |
| `rr`<br>`espResetReason` | ESP Reset Reason | R | `integer`<br>`uint8` | Status | :white_large_square: | esp_reset_reason (UNKNOWN=0, POWERON=1, EXT=2, SW=3, PANIC=4, INT_WDT=5, TASK_WDT=6, WDT=7, DEEPSLEEP=8, BROWNOUT=9, SDIO=10) | `4` |
| `rrca`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `2` |
| `rssi`<br>`wifiRssi` | WIFI Signal Strength | R | `integer`<br>`optional<int8>` | Status | :heavy_check_mark: | RSSI signal strength | `-66` |
| `sau`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `False` |
| `sbe`<br>`secureBootEnabled` |  | R | `boolean`<br>`bool` | Constant | :white_large_square: | Secure boot enabled | `True` |
| `scaa`<br>`wifiScanAge` |  | R | `integer`<br>`milliseconds` | Status | :white_large_square: | wifi scan age | `6429` |
| `scan`<br>`wifiScanResult` | Scanned WIFI Hotspots | R | `array`<br>`array` | Status | :white_large_square: | wifi scan result (encryptionType: OPEN=0, WEP=1, WPA_PSK=2, WPA2_PSK=3, WPA_WPA2_PSK=4, WPA2_ENTERPRISE=5, WPA3_PSK=6, WPA2_WPA3_PSK=7) | `[{'ssid': '<SOME_SSID>', 'encryptionType': 3, 'rssi': -65, 'channel': 6, 'bssid': '<SOME_BSSID>', 'f': [4, 4, True, True, True, False, False, False, False, 'DE']}, {'ssid': '<SOME_SSID>', 'encryptionType': 3, 'rssi': -65, 'channel': 6, 'bssid': '<SOME_BSSID>', 'f': [4, 4, True, True, True, False, False, False, False, 'DE']}]` |
| `scas`<br>`wifiScanStatus` | WIFI Scan Status | R | `integer`<br>`uint8` | Status | :heavy_check_mark: | wifi scan status (None=0, Scanning=1, Finished=2, Failed=3) | `2` |
| `sch_satur`<br>`schedulerSaturday` | Charging Schedule Saturday | R/W | `object`<br>`object` | Config | :white_large_square: | scheduler_saturday, control enum values: Disabled=0, Inside=1, Outside=2 | `{'control': 0, 'ranges': [{'begin': {'hour': 0, 'minute': 0}, 'end': {'hour': 0, 'minute': 0}}, {'begin': {'hour': 0, 'minute': 0}, 'end': {'hour': 0, 'minute': 0}}]}` |
| `sch_sund`<br>`schedulerSunday` | Charging Schedule Sunday | R/W | `object`<br>`object` | Config | :white_large_square: | scheduler_sunday, control enum values: Disabled=0, Inside=1, Outside=2 | `{'control': 0, 'ranges': [{'begin': {'hour': 0, 'minute': 0}, 'end': {'hour': 0, 'minute': 0}}, {'begin': {'hour': 0, 'minute': 0}, 'end': {'hour': 0, 'minute': 0}}]}` |
| `sch_week`<br>`schedulerWeekday` | Charging Schedule Weekday | R/W | `object`<br>`object` | Config | :white_large_square: | scheduler_weekday, control enum values: Disabled=0, Inside=1, Outside=2 | `{'control': 0, 'ranges': [{'begin': {'hour': 0, 'minute': 0}, 'end': {'hour': 0, 'minute': 0}}, {'begin': {'hour': 0, 'minute': 0}, 'end': {'hour': 0, 'minute': 0}}]}` |
| `sdca`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `2` |
| `sh`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `200` |
| `smca`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `2` |
| `smd`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `None` |
| `spl3`<br>`threePhaseSwitchLevel` |  | R/W | `integer`<br>`float` | Config | :white_large_square: | threePhaseSwitchLevel | `4200` |
| `sse`<br>`serialNumber` | Serial Number | R | `integer`<br>`string` | Constant | :heavy_check_mark: | serial number | `<some_serialnr>` |
| `stao`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `None` |
| `su`<br>`simulateUnplugging` |  | R/W | `boolean`<br>`bool` | Config | :white_large_square: | simulateUnplugging | `False` |
| `sua`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `False` |
| `sumd`<br>`simulateUnpluggingDuration` |  | R/W | `integer`<br>`milliseconds` | Config | :white_large_square: | simulate unpluging duration (in milliseconds) | `5000` |
| `swc`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `False` |
| `tds`<br>`timezoneDaylightSavingMode` | Timezone Daylight Saving Mode | R/W | `integer`<br>`uint8` | Config | :heavy_check_mark: | timezone daylight saving mode, None=0, EuropeanSummerTime=1, UsDaylightTime=2 | `1` |
| `tma`<br>`temperatureSensors` | Temperature Sensors | R | `array`<br>`array` | Status | :heavy_check_mark: | temperature sensors | `[11, 16.75]` |
| `tof`<br>`timezoneOffset` |  | R/W | `integer`<br>`minutes` | Config | :white_large_square: | timezone offset in minutes | `60` |
| `tou`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `0` |
| `tpa`<br>`totalPowerAverage` |  | R | `integer`<br>`float` | Status | :white_large_square: | 30 seconds total power average (used to get better next-trip predictions) | `0` |
| `tpck`<br>- |  |  | `array`<br>- |  | :white_large_square: |  | `['chargectrl', 'i2c', 'led', 'wifi', 'webserver', 'mdns', 'time', 'cloud', 'rfid', 'temperature', 'status', 'froniusinverter', 'button', 'delta_http', 'delta_cloud', 'ota_cloud', 'cmdhandler', 'loadbalancing', 'ocpp', 'remotereq', 'cloud_send']` |
| `tpcm`<br>- |  |  | `array`<br>- |  | :white_large_square: |  | `[4, 0, 3, 1, 0, 0, 0, 0, 43, 2, 53, 0, 0, 0, 50, 0, 0, 0, 0, 0, 10]` |
| `trx`<br>`transaction` |  | R | `unknown`<br>`optional<uint8>` | Status | :white_large_square: | transaction, null when no transaction, 0 when without card, otherwise cardIndex + 1 (1: 0. card, 2: 1. card, ...) | `None` |
| `ts`<br>`timeServer` |  | R | `string`<br>`string` | Config | :white_large_square: | time server | `europe.pool.ntp.org` |
| `tse`<br>`timeServerEnabled` |  | R/W | `boolean`<br>`bool` | Config | :heavy_check_mark: | time server enabled (NTP) | `False` |
| `tsom`<br>`timeServerOperatingMode` | Time Server Operating Mode | R | `integer`<br>`uint8` | Status | :white_large_square: | time server operating mode (POLL=0, LISTENONLY=1) | `0` |
| `tssi`<br>`timeServerSyncInterval` |  | R | `integer`<br>`milliseconds` | Config | :white_large_square: | time server sync interval (in ms, 15s minimum) | `3600000` |
| `tssm`<br>`timeServerSyncMode` | Time Server Sync Mode | R | `integer`<br>`uint8` | Config | :white_large_square: | time server sync mode (IMMED=0, SMOOTH=1) | `0` |
| `tsss`<br>`timeServerSyncStatus` | Time Server Sync Status | R | `integer`<br>`uint8` | Config | :white_large_square: | time server sync status (RESET=0, COMPLETED=1, IN_PROGRESS=2) | `0` |
| `typ`<br>`deviceType` |  | R | `string`<br>`string` | Constant | :white_large_square: | Devicetype | `wattpilot` |
| `uaca`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `2` |
| `upd`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `False` |
| `upo`<br>`unlockPowerOutage` |  | R/W | `boolean`<br>`bool` | Config | :white_large_square: | unlock_power_outage | `False` |
| `ust`<br>`cableLock` | Unlock Setting | R/W | `integer`<br>`uint8` | Config | :heavy_check_mark: | unlock_setting (Normal=0, AutoUnlock=1, AlwaysLock=2) | `0` |
| `utc`<br>- |  | R/W | `string`<br>`string` | Status | :white_large_square: | utc time | `2022-03-06T10:59:38.181.250` |
| `var`<br>`variant` | Variant | R | `integer`<br>`uint8` | Constant | :heavy_check_mark: | variant: max Ampere value of unit (11: 11kW/16A, 22: 22kW/32A) | `11` |
| `waap`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `3` |
| `wae`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `True` |
| `wak`<br>`wifiApKey` |  | R/W | `boolean`<br>`string` | Config | :white_large_square: | WiFi AccessPoint Key (read/write from http) | `False` |
| `wan`<br>`wifiApName` |  | R/W | `string`<br>`string` | Config | :white_large_square: | wifiApName | `Wattpilot_<some_serialnr>` |
| `wapc`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `1` |
| `wcb`<br>- | Wifi Connected BSSID |  | `string`<br>- |  | :white_large_square: | The BSSID of the connected WIFI access point. | `<some_mac>` |
| `wcch`<br>`httpConnectedClients` |  | R | `integer`<br>`uint8` | Status | :white_large_square: | webserver connected clients as HTTP | `0` |
| `wccw`<br>`wsConnectedClients` |  | R | `integer`<br>`uint8` | Status | :white_large_square: | webserver connected clients as WEBSOCKET | `2` |
| `wda`<br>- |  |  | `boolean`<br>- |  | :white_large_square: |  | `False` |
| `wen`<br>`wifiEnabled` |  | R/W | `boolean`<br>`bool` | Config | :white_large_square: | wifiEnabled (bool), turns off/on the WiFi (not the AccessPoint) | `True` |
| `wfb`<br>- |  |  | `unknown`<br>- |  | :white_large_square: |  | `None` |
| `wh`<br>`energyCounterSinceStart` | Energy Counter Since Start | R | `float`<br>`double` | Status | :heavy_check_mark: | energy in Wh since car connected | `2133.804` |
| `wifis`<br>- | Configured WIFI Networks? | R/W | `array`<br>`array` | Config | :white_large_square: | wifi configurations with ssids and keys, if you only want to change the second entry, send an array with 1 empty and 1 filled wifi config object: `[{}, {"ssid":"","key":""}]` | `[{'ssid': '<SOME_SSID>', 'key': True, 'useStaticIp': False, 'staticIp': '0.0.0.0', 'staticSubnet': '0.0.0.0', 'staticGateway': '0.0.0.0', 'useStaticDns': False, 'staticDns0': '0.0.0.0', 'staticDns1': '0.0.0.0', 'staticDns2': '0.0.0.0'}, {'ssid': '', 'key': False, 'useStaticIp': False, 'staticIp': '0.0.0.0', 'staticSubnet': '0.0.0.0', 'staticGateway': '0.0.0.0', 'useStaticDns': False, 'staticDns0': '0.0.0.0', 'staticDns1': '0.0.0.0', 'staticDns2': '0.0.0.0'}]` |
| `wpb`<br>- |  |  | `array`<br>- |  | :white_large_square: |  | `<SOME_BSSID>` |
| `wsc`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `0` |
| `wsm`<br>- |  |  | `string`<br>- |  | :white_large_square: |  |  |
| `wsmr`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `-90` |
| `wsms`<br>`wifiStateMachineState` | WIFI State Machine State | R | `integer`<br>`uint8` | Status | :heavy_check_mark: | WiFi state machine state (None=0, Scanning=1, Connecting=2, Connected=3) | `3` |
| `wss`<br>`wifiSsid` |  |  | `unknown`<br>- |  | :white_large_square: |  |  |
| `wst`<br>`wifiStaStatus` | WIFI STA Status | R | `integer`<br>`uint8` | Status | :heavy_check_mark: | WiFi STA status (IDLE_STATUS=0, NO_SSID_AVAIL=1, SCAN_COMPLETED=2, CONNECTED=3, CONNECT_FAILED=4, CONNECTION_LOST=5, DISCONNECTED=6, CONNECTING=8, DISCONNECTING=9, NO_SHIELD=10 (for compatibility with WiFi Shield library)) | `3` |
| `zfo`<br>- |  |  | `integer`<br>- |  | :white_large_square: |  | `200` |
