// Copyright (c) Microsoft Corporation. All rights reserved.
// SPDX-License-Identifier: MIT

// Wifi
#define IOT_CONFIG_WIFI_SSID "<WIFI_SSID>"
#define IOT_CONFIG_WIFI_PASSWORD "<WIFI_PASSWORD>"

// Azure IoT
#define IOT_CONFIG_IOTHUB_FQDN "<IOT_HUB_NAME>.azure-devices.net"
#define IOT_CONFIG_DEVICE_ID "<DEVICE_ID>"
#define IOT_CONFIG_DEVICE_KEY "<DEVICE_KEY>"

// Device location (update with your device coordinates)
#define IOT_CONFIG_DEVICE_LATITUDE "-23.5505"
#define IOT_CONFIG_DEVICE_LONGITUDE "-46.6333"

// HTTP config portal toggle (1 = enable, 0 = disable)
#define ENABLE_HTTP_CONFIG_SERVER 1

// Increment when you want to force devices to reload defaults into EEPROM
#define IOT_CONFIG_STORAGE_VERSION 2

// Publish 1 message every 10 seconds
#define TELEMETRY_FREQUENCY_MILLISECS 30000
