#pragma once

#include <Arduino.h>

#include "config_server.h"

String getISOTimestamp();
const char* getTelemetryPayload(const DeviceConfig& config);
