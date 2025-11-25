#pragma once

#include <Arduino.h>

#include "iot_configs.h"

typedef struct DeviceConfig
{
  char wifi_ssid[64];
  char wifi_password[64];
  char iothub_host[128];
  char device_id[64];
  char device_key[128];
  char latitude[16];
  char longitude[16];
} DeviceConfig;

void device_config_load(DeviceConfig* config);
void device_config_save(const DeviceConfig* config);

void config_server_begin(DeviceConfig* config);
void config_server_handle();
bool config_server_should_reconnect();
void config_server_clear_reconnect_flag();
