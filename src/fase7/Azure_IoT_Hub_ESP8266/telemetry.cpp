#include "telemetry.h"

#include <ESP8266WiFi.h>
#include <az_core.h>
#include <time.h>
#include <cstdlib>

namespace
{
static uint8_t telemetry_payload[256];
static uint32_t telemetry_send_count = 0;
}

String getISOTimestamp()
{
  time_t now = time(nullptr);
  struct tm* utc_tm = gmtime(&now);

  char timestamp[25];
  strftime(timestamp, sizeof(timestamp), "%Y-%m-%dT%H:%M:%SZ", utc_tm);

  return String(timestamp);
}

const char* getTelemetryPayload(const DeviceConfig& config)
{
  float temperature = 20.0 + (rand() % 10);
  float humidity = 50.0 + (rand() % 20);
  char temperature_buf[10];
  char humidity_buf[10];

  dtostrf(temperature, 4, 2, temperature_buf);
  dtostrf(humidity, 4, 2, humidity_buf);

  String timestamp = getISOTimestamp();
  String ip_address = WiFi.localIP().toString();

  az_span temp_span = az_span_create(telemetry_payload, sizeof(telemetry_payload));
  temp_span = az_span_copy(temp_span, AZ_SPAN_FROM_STR("{ \"msgCount\": "));
  (void)az_span_u32toa(temp_span, telemetry_send_count++, &temp_span);
  temp_span = az_span_copy(temp_span, AZ_SPAN_FROM_STR(", \"deviceId\": \""));
  temp_span = az_span_copy(temp_span, az_span_create((uint8_t*)config.device_id, strlen(config.device_id)));
  temp_span = az_span_copy(temp_span, AZ_SPAN_FROM_STR("\""));
  temp_span = az_span_copy(temp_span, AZ_SPAN_FROM_STR(", \"timestamp\": \""));
  temp_span = az_span_copy(temp_span, az_span_create_from_str((char*)timestamp.c_str()));
  temp_span = az_span_copy(temp_span, AZ_SPAN_FROM_STR("\""));
  temp_span = az_span_copy(temp_span, AZ_SPAN_FROM_STR(", \"ipAddress\": \""));
  temp_span = az_span_copy(temp_span, az_span_create_from_str((char*)ip_address.c_str()));
  temp_span = az_span_copy(temp_span, AZ_SPAN_FROM_STR("\""));
  temp_span = az_span_copy(temp_span, AZ_SPAN_FROM_STR(", \"temperature\": "));
  temp_span = az_span_copy(temp_span, az_span_create_from_str(temperature_buf));
  temp_span = az_span_copy(temp_span, AZ_SPAN_FROM_STR(", \"humidity\": "));
  temp_span = az_span_copy(temp_span, az_span_create_from_str(humidity_buf));
  temp_span = az_span_copy(temp_span, AZ_SPAN_FROM_STR(", \"latitude\": "));
  temp_span = az_span_copy(temp_span, az_span_create((uint8_t*)config.latitude, strlen(config.latitude)));
  temp_span = az_span_copy(temp_span, AZ_SPAN_FROM_STR(", \"longitude\": "));
  temp_span = az_span_copy(temp_span, az_span_create((uint8_t*)config.longitude, strlen(config.longitude)));
  temp_span = az_span_copy(temp_span, AZ_SPAN_FROM_STR(" }"));
  temp_span = az_span_copy_u8(temp_span, '\0');

  return (char*)telemetry_payload;
}
